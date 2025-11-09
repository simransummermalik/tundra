from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict

class Job(BaseModel):
    job_id: Optional[str] = None
    user_id: Optional[str] = None
    task: str
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    status: Optional[str] = None

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str
