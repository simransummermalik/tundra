from fastapi import FastAPI
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue
from agent_executor.executor import AgentExecutor, WebScraperExecutor
from fastapi.middleware.cors import CORSMiddleware
from models import Job, JobResponse
from db import jobs_collection
from dotenv import load_dotenv
from openai import AzureOpenAI
import asyncio
import uuid
import os
from datetime import datetime

load_dotenv()
app = FastAPI(title="TUNDRA Requester Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

job_queue = asyncio.Queue()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)

def tundra_agent(prompt: str):
    system_prompt = (
        "You are TundraAgent, a requester agent on the Tundra A2A marketplace. "
        "You understand user jobs, decide which specialist agent to hire, "
        "and summarize reasoning clearly."
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

@app.get("/")
async def root():
    return {"message": "TUNDRA Requester Agent running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/submit_job")
async def submit_job(job: Job, user_id: str = "test_user"):
    """Queue a new job for execution."""
    job.job_id = str(uuid.uuid4())
    job.user_id = user_id
    job.created_at = datetime.utcnow()
    job.status = "pending"

    await jobs_collection.insert_one(job.dict())
    await job_queue.put(job.dict())

    return JobResponse(job_id=job.job_id, status="queued", message="Job added to queue")

async def executor():
    while True:
        job = await job_queue.get()
        job_id = job["job_id"]
        print(f"Processing job: {job_id}")

        analysis = tundra_agent(f"Task: {job['task']}. Determine the best next action or agent.")
        print(f"TundraAgent reasoning: {analysis}")

        if "scrape" in job["task"].lower():
            queue = EventQueue()
            scraper = WebScraperExecutor(name="WebScraperAgent")
            req = RequestContext(task_type="web_scrape", payload={"url": job.get("url", "unknown")})
            result = scraper.execute(req, queue)
            events = [e.dict() for e in queue.list_events()]
        else:
            result, events = {"message": "Task did not require scraping"}, []

        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": "completed",
                "reasoning": analysis,
                "output": result,
                "events": events,
                "finished_at": datetime.utcnow()
            }}
        )
        print(f"Job {job_id} finalized")
        job_queue.task_done()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(executor())

@app.post("/execute")
def run_agent(request: RequestContext):
    """
    Manual execution endpoint for testing an agent.
    """
    queue = EventQueue()
    agent = WebScraperExecutor(name="WebScraperAgent")

    result = agent.execute(request, queue)
    events = [event.dict() for event in queue.list_events()]

    return {
        "agent": agent.name,
        "result": result,
        "events": events
    }
