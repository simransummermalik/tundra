from fastapi import FastAPI
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue
from agent_executor.executor import AgentExecutor, WebScraperExecutor, SummarizerExecutor, SentimentExecutor
from fastapi.middleware.cors import CORSMiddleware
from models import Job, JobResponse, AgentInfo
from db import jobs_collection, agents_collection, credits_collection, client as mongo_client
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import sys
import uuid
import json
import os
from pymongo import ReturnDocument
from bson import ObjectId

load_dotenv()

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

AGENTS = [
    {"name": "WebScraperAgent", "capabilities": ["web_scrape"], "rate": 15},
    {"name": "SummarizerAgent", "capabilities": ["summarize"], "rate": 5},
    {"name": "SentimentAgent", "capabilities": ["sentiment_analysis"], "rate": 5},
]
MARKETPLACE_ENABLED = os.getenv("MARKETPLACE_ENABLED", "1") == "1"
MARKETPLACE_ONLINE = False
MARKETPLACE_ERROR = ""

def eligible_agents_for(task_type: str, budget: int | None):
    result = []
    for a in AGENTS:
        if task_type in a["capabilities"] and (budget is None or a["rate"] <= budget):
            result.append(a["name"])
    return result

openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)

def tundra_agent(user_request: str):
    system_prompt = (
        "You are TundraAgent, a requester agent on the Tundra A2A marketplace. "
        "You interpret user requests and decide which specialist agent should handle the task. "
        "Available agents:\n"
        "- WebScraperAgent: For scraping any web data. Uses AI to intelligently extract data based on user goals.\n"
        "- SummarizerAgent: For summarizing data or text\n"
        "- SentimentAgent: For analyzing sentiment of text or news\n\n"
        "Routing rules:\n"
        "- If the user asks for price, quote, chart, or real-time data: choose WebScraperAgent and provide payload.url for an authoritative source (e.g., Yahoo Finance).\n"
        "- If the user asks buy/sell/hold, opinion, is it a good investment, bullish or bearish: choose SentimentAgent and provide payload.text equal to the user's request.\n"
        "- If the user asks to summarize provided content: choose SummarizerAgent and provide payload.data.\n\n"
        "Respond with a JSON object containing:\n"
        "{\n"
        '  "agent": "agent_name",\n'
        '  "task_type": "web_scrape|summarize|sentiment_analysis",\n'
        '  "reasoning": "brief explanation",\n'
        '  "payload": {"url": "the exact URL to scrape" | "text": "text to analyze" | "data": "text to summarize"}\n'
        "}\n\n"
        "URL Selection Guidelines:\n"
        "- Stock queries: Use https://finance.yahoo.com/quote/SYMBOL (e.g., TSLA, AAPL, GOOGL)\n"
        "- Claude/Anthropic pricing: Use https://www.anthropic.com/api or https://www.anthropic.com/claude\n"
        "- News: Use specific news article URLs\n"
        "- Product info: Use direct product page URLs\n"
        "- General company info: Use official company websites\n\n"
        "The WebScraperAgent uses browser automation and AI to extract data from JavaScript-rendered pages."
    )

    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_request}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    return json.loads(content)


async def init_marketplace():
    global MARKETPLACE_ONLINE, MARKETPLACE_ERROR
    try:
        await mongo_client.admin.command("ping")
        await jobs_collection.create_index("job_id", unique=True)
        await jobs_collection.create_index([("status", 1), ("task_type", 1)])
        for cfg in AGENTS:
            await agents_collection.update_one({"name": cfg["name"]}, {"$set": cfg}, upsert=True)
            await credits_collection.update_one({"agent": cfg["name"]}, {"$setOnInsert": {"balance": 0}}, upsert=True)
        await credits_collection.update_one({"agent": "OrchestratorAgent"}, {"$setOnInsert": {"balance": 1000}}, upsert=True)
        for cfg in AGENTS:
            asyncio.create_task(provider_loop(cfg))
        MARKETPLACE_ONLINE = True
        MARKETPLACE_ERROR = ""
        print("[Marketplace] online")
    except Exception as e:
        MARKETPLACE_ONLINE = False
        MARKETPLACE_ERROR = str(e)
        print(f"[Marketplace] offline: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if MARKETPLACE_ENABLED:
        await init_marketplace()
    yield

app = FastAPI(title="TUNDRA Requester Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TUNDRA Requester Agent running"}
async def root():
    return {"message": "TUNDRA Requester Agent running"}

@app.get("/health")
async def health_check():
async def health_check():
    return {"status": "ok"}

@app.post("/submit_job")
async def submit_job(job: Job):
    user_request = job.task or ""
    decision = tundra_agent(user_request)
    agent_name = decision.get("agent", "WebScraperAgent")
    task_type = decision.get("task_type", "web_scrape")
    payload = {**decision.get("payload", {}), **job.payload}
    if not MARKETPLACE_ONLINE:
        queue = EventQueue()
        req = RequestContext(task_type=task_type, payload=payload, goal=job.goal or user_request)
        if task_type == "web_scrape":
            result = await WebScraperExecutor(name=agent_name).execute(req, queue)
        elif task_type == "summarize":
            result = SummarizerExecutor(name=agent_name).execute(req, queue)
        elif task_type == "sentiment_analysis":
            result = SentimentExecutor(name=agent_name).execute(req, queue)
        else:
            result = AgentExecutor(name=agent_name).execute(req, queue)
        rid = str(uuid.uuid4())
        return JobResponse(job_id=rid, status="completed", message="Executed directly")
    agent_cfg = next((a for a in AGENTS if a["name"] == agent_name), None)
    budget = agent_cfg["rate"] if agent_cfg else 10
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    doc = {
        "job_id": job_id,
        "requester_agent": "OrchestratorAgent",
        "provider_agent": None,
        "task": user_request,
        "task_type": task_type,
        "goal": job.goal or user_request,
        "payload": payload,
        "budget": budget,
        "created_at": now,
        "status": "open",
        "status_history": [{"status": "open", "by": "OrchestratorAgent", "at": now.isoformat()}],
        "eligible_agents": eligible_agents_for(task_type, budget),
        "agent_scores": {name: {"eligible": True, "claimed": False, "completed": False} for name in eligible_agents_for(task_type, budget)}
    }
    await jobs_collection.insert_one(doc)
    print(f"[Orchestrator] posted job {job_id}")
    return JobResponse(job_id=job_id, status="open", message="Job posted")


async def provider_loop(cfg: dict):
    name = cfg["name"]
    caps = cfg["capabilities"]
    rate = cfg["rate"]
    while True:
        now = datetime.now(timezone.utc)
        doc = await jobs_collection.find_one_and_update(
            {"status": "open", "task_type": {"$in": caps}, "budget": {"$gte": rate}},
            {"$set": {"status": "claimed", "provider_agent": name, "claimed_at": now, f"agent_scores.{name}.eligible": True, f"agent_scores.{name}.claimed": True, f"agent_scores.{name}.claimed_at": now},
             "$push": {"status_history": {"status": "claimed", "by": name, "at": now.isoformat()}}},
            sort=[("created_at", 1)],
            return_document=ReturnDocument.AFTER,
        )
        if not doc:
            await asyncio.sleep(1.0)
            continue
        job_id = doc["job_id"]
        print(f"[{name}] claimed job {job_id}")
        now_exec = datetime.now(timezone.utc)
        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {"status": "in_progress", "started_at": now_exec},
             "$push": {"status_history": {"status": "in_progress", "by": name, "at": now_exec.isoformat()}}}
        )
        queue = EventQueue()
        req = RequestContext(task_type=doc.get("task_type"), payload=doc.get("payload", {}), goal=doc.get("goal"))
        try:
            if doc.get("task_type") == "web_scrape":
                agent = WebScraperExecutor(name=name)
                result = await agent.execute(req, queue)
            elif doc.get("task_type") == "summarize":
                agent = SummarizerExecutor(name=name)
                result = agent.execute(req, queue)
            elif doc.get("task_type") == "sentiment_analysis":
                agent = SentimentExecutor(name=name)
                result = await agent.execute(req, queue)
            else:
                agent = AgentExecutor(name=name)
                result = agent.execute(req, queue)
            now2 = datetime.now(timezone.utc)
            events = [e.model_dump(mode="json") for e in queue.list_events()]
            await jobs_collection.update_one(
                {"job_id": job_id},
                {"$set": {"status": "completed", "completed_at": now2, "result": result, "events": events, f"agent_scores.{name}.completed": True, f"agent_scores.{name}.completed_at": now2},
                 "$push": {"status_history": {"status": "completed", "by": name, "at": now2.isoformat()}}}
            )
            requester = doc.get("requester_agent", "OrchestratorAgent")
            budget = doc.get("budget", rate)
            await credits_collection.update_one({"agent": requester}, {"$inc": {"balance": -budget}}, upsert=True)
            await credits_collection.update_one({"agent": name}, {"$inc": {"balance": budget}}, upsert=True)
            print(f"[{name}] completed job {job_id}")
        except Exception as e:
            nowf = datetime.now(timezone.utc)
            events = [e2.model_dump(mode="json") for e2 in queue.list_events()]
            await jobs_collection.update_one(
                {"job_id": job_id},
                {"$set": {"status": "failed", "completed_at": nowf, "error": str(e), "events": events}},
            )
            print(f"[{name}] failed job {job_id}: {e}")

@app.post("/execute")
async def tundra_execute(request: RequestContext):

    user_request = f"Goal: {request.goal}. Task type: {request.task_type}. Payload: {request.payload}"
    decision = tundra_agent(user_request)

    queue = EventQueue()
    agent_name = decision.get("agent", "WebScraperAgent")
    task_type = decision.get("task_type", request.task_type)
    payload = {**request.payload, **decision.get("payload", {})}

    updated_request = RequestContext(task_type=task_type, payload=payload, goal=request.goal)

    if agent_name == "WebScraperAgent" or task_type == "web_scrape":
        agent = WebScraperExecutor(name="WebScraperAgent")
        result = await agent.execute(updated_request, queue)
    elif agent_name == "SummarizerAgent" or task_type == "summarize":
        agent = SummarizerExecutor(name="SummarizerAgent")
        result = agent.execute(updated_request, queue)
    elif agent_name == "SentimentAgent" or task_type == "sentiment_analysis":
        agent = SentimentExecutor(name="SentimentAgent")
        result = agent.execute(updated_request, queue)
    else:
        agent = AgentExecutor(name="GenericAgent")
        result = agent.execute(updated_request, queue)

    events = [event.model_dump() for event in queue.list_events()]

    return {
        "tundra_agent_decision": decision,
        "selected_agent": agent_name,
        "task_type": task_type,
        "result": result,
        "events": events
    }

@app.post("/orchestrate")
async def multi_agent_orchestration(user_query: str):
    decision = tundra_agent(user_query)
    agent_name = decision.get("agent", "WebScraperAgent")
    task_type = decision.get("task_type", "web_scrape")
    payload = decision.get("payload", {})
    if not MARKETPLACE_ONLINE:
        queue = EventQueue()
        req = RequestContext(task_type=task_type, payload=payload, goal=user_query)
        if task_type == "web_scrape":
            result = await WebScraperExecutor(name=agent_name).execute(req, queue)
        elif task_type == "summarize":
            result = SummarizerExecutor(name=agent_name).execute(req, queue)
        elif task_type == "sentiment_analysis":
            result = SentimentExecutor(name=agent_name).execute(req, queue)
        else:
            result = AgentExecutor(name=agent_name).execute(req, queue)
        return {"decision": decision, "executed": True, "result": result}
    cfg = next((a for a in AGENTS if a["name"] == agent_name), None)
    budget = cfg["rate"] if cfg else 10
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    doc = {
        "job_id": job_id,
        "requester_agent": "OrchestratorAgent",
        "provider_agent": None,
        "task": user_query,
        "task_type": task_type,
        "goal": user_query,
        "payload": payload,
        "budget": budget,
        "created_at": now,
        "status": "open",
        "status_history": [{"status": "open", "by": "OrchestratorAgent", "at": now.isoformat()}],
        "eligible_agents": eligible_agents_for(task_type, budget),
        "agent_scores": {name: {"eligible": True, "claimed": False, "completed": False} for name in eligible_agents_for(task_type, budget)}
    }
    await jobs_collection.insert_one(doc)
    print(f"[Orchestrator] posted job {job_id}")
    return {"job_id": job_id, "status": "open", "decision": decision}

@app.get("/agents")
async def list_agents():
    if not MARKETPLACE_ONLINE:
        return {"agents": [{"name": a["name"], "capabilities": a["capabilities"], "rate": a["rate"], "balance": 0} for a in AGENTS] + [{"name": "OrchestratorAgent", "capabilities": [], "rate": 0, "balance": 0}]}
    agents = await agents_collection.find({}).to_list(100)
    results = []
    for a in agents:
        bal = await credits_collection.find_one({"agent": a["name"]})
        results.append({"name": a["name"], "capabilities": a.get("capabilities", []), "rate": a.get("rate", 0), "balance": (bal or {}).get("balance", 0)})
    bal = await credits_collection.find_one({"agent": "OrchestratorAgent"})
    results.append({"name": "OrchestratorAgent", "capabilities": [], "rate": 0, "balance": (bal or {}).get("balance", 0)})
    return {"agents": results}

@app.get("/jobs")
async def list_jobs(status: str | None = None):
    if not MARKETPLACE_ONLINE:
        return {"jobs": []}
    query = {"status": status} if status else {}
    cursor = jobs_collection.find(query).sort("created_at", -1).limit(100)
    items = await cursor.to_list(100)
    for d in items:
        if isinstance(d.get("_id"), ObjectId):
            d["_id"] = str(d["_id"])
    return {"jobs": items}

@app.get("/jobs/{job_id}/score")
async def job_score(job_id: str):
    if not MARKETPLACE_ONLINE:
        return {"job_id": job_id, "online": False}
    doc = await jobs_collection.find_one({"job_id": job_id})
    if not doc:
        return {"job_id": job_id, "found": False}
    eligible = doc.get("eligible_agents", [])
    claimed_by = doc.get("provider_agent")
    didnt = [n for n in eligible if n != claimed_by]
    res = {
        "job_id": job_id,
        "task_type": doc.get("task_type"),
        "budget": doc.get("budget"),
        "status": doc.get("status"),
        "eligible_agents": eligible,
        "claimed_by": claimed_by,
        "didnt_claim_agents": didnt,
        "agent_scores": doc.get("agent_scores", {})
    }
    if isinstance(doc.get("_id"), ObjectId):
        res["_mongo_id"] = str(doc.get("_id"))
    return res

@app.get("/marketplace/status")
async def marketplace_status():
    uri_present = bool(os.getenv("MONGO_URI"))
    return {"enabled": MARKETPLACE_ENABLED, "online": MARKETPLACE_ONLINE, "uri_present": uri_present, "error": MARKETPLACE_ERROR}

@app.post("/marketplace/reload")
async def marketplace_reload():
    await init_marketplace()
    return {"enabled": MARKETPLACE_ENABLED, "online": MARKETPLACE_ONLINE, "error": MARKETPLACE_ERROR}

@app.get("/scoreboard")
async def scoreboard(limit: int = 200):
    names = [a["name"] for a in AGENTS]
    stats = {n: {"eligible": 0, "claimed": 0, "completed": 0} for n in names}
    if not MARKETPLACE_ONLINE:
        for n in names:
            stats[n]["missed"] = 0
            stats[n]["win_rate"] = 0.0
        return {"stats": stats}
    cursor = jobs_collection.find({}).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)
    for d in items:
        eligible = d.get("eligible_agents", [])
        for n in eligible:
            if n in stats:
                stats[n]["eligible"] += 1
        claimer = d.get("provider_agent")
        if claimer in stats:
            stats[claimer]["claimed"] += 1
            if d.get("status") == "completed":
                stats[claimer]["completed"] += 1
    for n in names:
        eligible = stats[n]["eligible"]
        claimed = stats[n]["claimed"]
        missed = max(0, eligible - claimed)
        stats[n]["missed"] = missed
        stats[n]["win_rate"] = (claimed / eligible) if eligible else 0.0
    return {"stats": stats}
