from fastapi import FastAPI, Header, HTTPException, Depends
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue
from agent_executor.executor import AgentExecutor, WebScraperExecutor, SummarizerExecutor, SentimentExecutor
from fastapi.middleware.cors import CORSMiddleware
from models import Job, JobResponse, APIKey, APIKeyResponse, LoginRequest, RegisterRequest
from db import jobs_collection, api_keys_collection, users_collection
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import sys
import uuid
import json
import os
import secrets
import hashlib
import bcrypt

load_dotenv()

# On Windows, Playwright needs a Proactor event loop to spawn subprocesses.
# Uvicorn/Starlette may default to the Selector policy on Windows which breaks this.
# Set the Proactor policy early at import time to ensure Playwright works.
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

job_queue = asyncio.Queue()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)

def generate_api_key():
    """Generate a secure random API key"""
    return f"tundra_{secrets.token_urlsafe(32)}"

def hash_api_key(api_key: str):
    """Hash API key for secure storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

async def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key from request header"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    hashed_key = hash_api_key(x_api_key)
    api_key_doc = await api_keys_collection.find_one({"key": hashed_key, "is_active": True})

    if not api_key_doc:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")

    # Update last_used timestamp
    await api_keys_collection.update_one(
        {"key": hashed_key},
        {"$set": {"last_used": datetime.now(timezone.utc)}}
    )

    return api_key_doc["user_id"]

def tundra_agent(user_request: str):
    system_prompt = (
        "You are TundraAgent, a requester agent on the Tundra A2A marketplace. "
        "You interpret user requests and decide which specialist agent should handle the task. "
        "Available agents:\n"
        "- WebScraperAgent: For scraping any web data. Uses AI to intelligently extract data based on user goals.\n"
        "- SummarizerAgent: For summarizing data or text\n"
        "- SentimentAgent: For analyzing sentiment of text or news\n\n"
        "Respond with a JSON object containing:\n"
        "{\n"
        '  "agent": "agent_name",\n'
        '  "task_type": "web_scrape|summarize|sentiment_analysis",\n'
        '  "reasoning": "brief explanation",\n'
        '  "payload": {"url": "the exact URL to scrape"}\n'
        "}\n\n"
        "URL Selection Guidelines:\n"
        "- Stock queries: Use https://finance.yahoo.com/quote/SYMBOL (e.g., TSLA, AAPL, GOOGL)\n"
        "- Claude/Anthropic pricing: Use https://www.anthropic.com/api or https://www.anthropic.com/claude\n"
        "- News: Use specific news article URLs\n"
        "- Product info: Use direct product page URLs\n"
        "- General company info: Use official company websites\n\n"
        "The WebScraperAgent uses browser automation and AI to extract data from JavaScript-rendered pages."
    )

    response = client.chat.completions.create(
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(executor())
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

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/auth/register")
async def register_user(request: RegisterRequest):
    """Register a new user with username and password"""
    # Check if user already exists
    existing_user = await users_collection.find_one({"user_id": request.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password and create user
    password_hash = hash_password(request.password)
    user_doc = {
        "user_id": request.username,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc),
        "is_active": True
    }
    await users_collection.insert_one(user_doc)

    # Generate API key
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)

    api_key_doc = {
        "key": hashed_key,
        "user_id": request.username,
        "created_at": datetime.now(timezone.utc),
        "last_used": None,
        "is_active": True
    }
    await api_keys_collection.insert_one(api_key_doc)

    return APIKeyResponse(
        api_key=api_key,
        user_id=request.username,
        message="Registration successful! You are now logged in."
    )

@app.post("/auth/login")
async def login_user(request: LoginRequest):
    """Login with username and password"""
    # Find user
    user = await users_collection.find_one({"user_id": request.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Verify password
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Deactivate old API keys
    await api_keys_collection.update_many(
        {"user_id": request.username, "is_active": True},
        {"$set": {"is_active": False}}
    )

    # Generate new API key
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)

    api_key_doc = {
        "key": hashed_key,
        "user_id": request.username,
        "created_at": datetime.now(timezone.utc),
        "last_used": None,
        "is_active": True
    }
    await api_keys_collection.insert_one(api_key_doc)

    return APIKeyResponse(
        api_key=api_key,
        user_id=request.username,
        message="Login successful!"
    )

@app.delete("/auth/revoke")
async def revoke_api_key(user_id: str = Depends(verify_api_key)):
    """Revoke the current API key"""
    await api_keys_collection.update_many(
        {"user_id": user_id, "is_active": True},
        {"$set": {"is_active": False}}
    )
    return {"message": "API key revoked successfully"}

@app.get("/me")
async def get_user_info(user_id: str = Depends(verify_api_key)):
    """Get current user information and stats"""
    # Get user
    user = await users_collection.find_one({"user_id": user_id})

    # Get active API key
    api_key = await api_keys_collection.find_one({"user_id": user_id, "is_active": True})

    # Get job stats
    total_jobs = await jobs_collection.count_documents({"user_id": user_id})
    pending_jobs = await jobs_collection.count_documents({"user_id": user_id, "status": "pending"})
    completed_jobs = await jobs_collection.count_documents({"user_id": user_id, "status": "completed"})

    return {
        "user_id": user_id,
        "created_at": user["created_at"] if user else None,
        "api_key_created": api_key["created_at"] if api_key else None,
        "api_key_last_used": api_key["last_used"] if api_key else None,
        "stats": {
            "total_jobs": total_jobs,
            "pending_jobs": pending_jobs,
            "completed_jobs": completed_jobs
        }
    }

@app.get("/jobs")
async def get_user_jobs(user_id: str = Depends(verify_api_key), limit: int = 10):
    """Get user's recent jobs"""
    jobs = await jobs_collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1).limit(limit).to_list(limit)

    return {"jobs": jobs, "total": len(jobs)}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str, user_id: str = Depends(verify_api_key)):
    """Get specific job status and results"""
    job = await jobs_collection.find_one({"job_id": job_id, "user_id": user_id})

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@app.post("/submit_job")
async def submit_job(job: Job, user_id: str = Depends(verify_api_key)):
    job.job_id = str(uuid.uuid4())
    job.user_id = user_id
    job.created_at = datetime.now(timezone.utc)
    job.status = "pending"

    await jobs_collection.insert_one(job.model_dump())
    await job_queue.put(job.model_dump())

    return JobResponse(job_id=job.job_id, status="queued", message="Job added to queue")


async def executor():
    while True:
        job = await job_queue.get()
        job_id = job["job_id"]
        print(f"Processing job: {job_id}")

        decision = tundra_agent(job["task"])
        print(f"TundraAgent decision: {decision}")

        queue = EventQueue()
        agent_name = decision.get("agent", "WebScraperAgent")
        task_type = decision.get("task_type", "web_scrape")
        payload = decision.get("payload", {})

        if "url" in job and job["url"]:
            payload["url"] = job["url"]

        req = RequestContext(task_type=task_type, payload=payload)

        if agent_name == "WebScraperAgent" or task_type == "web_scrape":
            agent = WebScraperExecutor(name="WebScraperAgent")
            result = await agent.execute(req, queue)
        elif agent_name == "SummarizerAgent" or task_type == "summarize":
            agent = SummarizerExecutor(name="SummarizerAgent")
            result = agent.execute(req, queue)
        elif agent_name == "SentimentAgent" or task_type == "sentiment_analysis":
            agent = SentimentExecutor(name="SentimentAgent")
            result = agent.execute(req, queue)
        else:
            agent = AgentExecutor(name="GenericAgent")
            result = agent.execute(req, queue)

        events = [e.model_dump() for e in queue.list_events()]

        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": "completed",
                "agent_used": agent_name,
                "task_type": task_type,
                "reasoning": decision.get("reasoning", ""),
                "output": result,
                "events": events,
                "finished_at": datetime.now(timezone.utc)
            }}
        )

        print(f"Job {job_id} finalized")
        job_queue.task_done()

@app.post("/execute")
async def tundra_execute(request: RequestContext, user_id: str = Depends(verify_api_key)):

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
async def multi_agent_orchestration(user_query: str, user_id: str = Depends(verify_api_key)):
    decision = tundra_agent(user_query)

    orchestration_log = []
    final_result = {}

    queue = EventQueue()
    agent_name = decision.get("agent", "WebScraperAgent")
    task_type = decision.get("task_type", "web_scrape")
    payload = decision.get("payload", {})

    if agent_name == "WebScraperAgent" or task_type == "web_scrape":
        scraper = WebScraperExecutor(name="WebScraperAgent")
        scrape_request = RequestContext(task_type="web_scrape", payload=payload, goal=user_query)
        scrape_result = await scraper.execute(scrape_request, queue)

        orchestration_log.append({
            "step": 1,
            "agent": "WebScraperAgent",
            "action": "Scraped web data",
            "result": scrape_result
        })

        if "news" in scrape_result:
            news_text = " ".join([item["headline"] for item in scrape_result.get("news", [])])
            sentiment_queue = EventQueue()
            sentiment_agent = SentimentExecutor(name="SentimentAgent")
            sentiment_request = RequestContext(task_type="sentiment_analysis", payload={"text": news_text})
            sentiment_result = sentiment_agent.execute(sentiment_request, sentiment_queue)

            orchestration_log.append({
                "step": 2,
                "agent": "SentimentAgent",
                "action": "Analyzed sentiment of news",
                "result": sentiment_result
            })

            final_result["sentiment_analysis"] = sentiment_result

        final_result["scrape_data"] = scrape_result

    elif agent_name == "SentimentAgent" or task_type == "sentiment_analysis":
        sentiment_agent = SentimentExecutor(name="SentimentAgent")
        sentiment_request = RequestContext(task_type="sentiment_analysis", payload=payload)
        sentiment_result = sentiment_agent.execute(sentiment_request, queue)

        orchestration_log.append({
            "step": 1,
            "agent": "SentimentAgent",
            "action": "Analyzed sentiment",
            "result": sentiment_result
        })

        final_result["sentiment_analysis"] = sentiment_result

    return {
        "query": user_query,
        "tundra_decision": decision,
        "orchestration_log": orchestration_log,
        "final_result": final_result,
        "total_agents_used": len(orchestration_log)
    }
