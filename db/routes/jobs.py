# routes/jobs.py
# db/routes/jobs.py
from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime

try:
    from ..database import jobs_collection
    from ..models import Job
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from database import jobs_collection
    from models import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[Job])
async def list_jobs():
    jobs = []
    cursor = jobs_collection.find({})
    async for doc in cursor:
      jobs.append(Job(**doc))
    return jobs


@router.post("/", response_model=Job)
async def create_job(job: Job):
    job_dict = job.model_dump(by_alias=True)
    result = await jobs_collection.insert_one(job_dict)
    created = await jobs_collection.find_one({"_id": result.inserted_id})
    return Job(**created)


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    doc = await jobs_collection.find_one({"_id": ObjectId(job_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")
    return Job(**doc)


@router.patch("/{job_id}/status", response_model=Job)
async def update_job_status(job_id: str, status: str):
    # you can add validation here for allowed statuses
    result = await jobs_collection.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {"status": status, "last_updated": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")

    updated = await jobs_collection.find_one({"_id": ObjectId(job_id)})
    return Job(**updated)
