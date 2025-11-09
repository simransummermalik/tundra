# db/routes/jobs.py
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import jobs_collection
from models import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/")
async def list_jobs():
    jobs = []
    async for doc in jobs_collection.find():
        doc["_id"] = str(doc["_id"])
        jobs.append(doc)
    return jobs


@router.post("/")
async def create_job(job: Job):
    job_dict = job.dict(by_alias=True)
    result = await jobs_collection.insert_one(job_dict)
    return {"_id": str(result.inserted_id)}


@router.get("/{job_id}")
async def get_job(job_id: str):
    try:
        oid = ObjectId(job_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid job id")
    doc = await jobs_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")
    doc["_id"] = str(doc["_id"])
    return doc
