from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict, List

class Job(BaseModel):
    job_id: Optional[str] = None
    requester_agent: Optional[str] = None
    provider_agent: Optional[str] = None
    task: Optional[str] = None
    task_type: Optional[str] = None
    goal: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    budget: Optional[int] = None
    created_at: Optional[datetime] = None
    claimed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Optional[str] = None
    status_history: List[Dict[str, Any]] = Field(default_factory=list)
    result: Optional[Dict[str, Any]] = None

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

class AgentInfo(BaseModel):
    name: str
    capabilities: List[str]
    rate: int
