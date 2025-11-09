from fastapi import FastAPI
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue
from agent_executor.executor import AgentExecutor, WebScraperExecutor, SummarizerExecutor, SentimentExecutor
from fastapi.middleware.cors import CORSMiddleware
from models import Job, JobResponse
from db import jobs_collection
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import sys
import uuid
import json
import os

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
async def root():
    return {"message": "TUNDRA Requester Agent running"}

@app.get("/health")
async def health_check():
async def health_check():
    return {"status": "ok"}

@app.post("/submit_job")
async def submit_job(job: Job, user_id: str = "test_user"):
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
