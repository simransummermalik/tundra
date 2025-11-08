from fastapi import FastAPI
from agent_executor.context import RequestContext
from agent_executor.event_queue import EventQueue
from agent_executor.executor import AgentExecutor
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Job, Context, AgentOutput, JobResponse
from db import jobs_collection
import asyncio
import uuid
from datetime import datetime

app = FastAPI(title="Tundra Agent Runner")

app = FastAPI(title="TUNDRA Requester Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

job_queue = asyncio.Queue()

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

        # Step 1: Scout Agent
        scout_output = {"summary": f"Processed task: {job['task']}"}
        print(f"Scout output: {scout_output}")

        # Step 2: Sentinel Agent
        sentinel_pass = True
        print(f"Sentinel validation: {sentinel_pass}")

        # Step 3: Custodian Agent
        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": "completed",
                "output": scout_output,
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
    queue = EventQueue()
    agent = AgentExecutor(name="WebScraperAgent")

    result = agent.execute(request, queue)
    events = [event.dict() for event in queue.list_events()]

    return {
        "agent": agent.name,
        "result": result,
        "events": events
    }
