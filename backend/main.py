from fastapi import FastAPI
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue
from agent_executor.executor import AgentExecutor, WebScraperExecutor
from fastapi.middleware.cors import CORSMiddleware
from models import Job, JobResponse
from db import jobs_collection
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import uuid
import os

load_dotenv()

job_queue = asyncio.Queue()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)

def tundra_agent(prompt: str):
    """LLM reasoning for interpreting and routing tasks."""
    system_prompt = (
        "You are TundraAgent, a requester agent on the Tundra A2A marketplace. "
        "You interpret human or system jobs, decide which specialist agent should handle the task, "
        "and summarize your reasoning clearly and concisely."
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


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

        reasoning = tundra_agent(
            f"Task: {job['task']}. Decide which agent should handle it and describe reasoning."
        )
        print(f"TundraAgent reasoning: {reasoning}")

        if "scrape" in job["task"].lower():
            queue = EventQueue()
            scraper = WebScraperExecutor(name="WebScraperAgent")
            req = RequestContext(task_type="web_scrape", payload={"url": job.get("url", "unknown")})
            result = scraper.execute(req, queue)
            events = [e.model_dump() for e in queue.list_events()]
        else:
            result, events = {"message": "No scraping required."}, []

        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": "completed",
                "reasoning": reasoning,
                "output": result,
                "events": events,
                "finished_at": datetime.now(timezone.utc)
            }}
        )

        print(f"Job {job_id} finalized")
        job_queue.task_done()

@app.post("/execute")
def tundra_execute(request: RequestContext):

    reasoning = tundra_agent(
        f"Task type: {request.task_type}. Goal: {request.goal}. Payload: {request.payload}. "
        f"Decide the best next step or agent."
    )

    queue = EventQueue()

    if "scrape" in request.task_type.lower() or "scrape" in reasoning.lower():
        agent = WebScraperExecutor(name="WebScraperAgent")
        result = agent.execute(request, queue)
    else:
        agent = AgentExecutor(name="GenericAgent")
        result = {"message": "No specialized agent required for this task."}

    events = [event.model_dump() for event in queue.list_events()]

    return {
        "tundra_agent_reasoning": reasoning,
        "selected_agent": agent.name,
        "result": result,
        "events": events
    }
