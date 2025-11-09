# db/models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# agent side modeling

class Pricing(BaseModel):
    base_rate: float
    unit: str  # e.g. "per_task", "per_token"


class Agent(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Mongo _id
    name: str
    capabilities: List[str]
    average_latency_ms: Optional[int] = 0
    success_rate: Optional[float] = 0.0
    reliability_score: Optional[float] = 0.0
    pricing: Pricing
    region: str
    status: str = "active"
    total_jobs_completed: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True


# job side modeling

class Job(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Mongo _id
    job_id: Optional[str] = None  # optional human-readable id
    task: str
    budget: float
    workflow: List[str] = Field(
        default_factory=lambda: ["Scout", "Sentinel", "Custodian"]
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
    assigned_agent_id: Optional[str] = None  # optional link to Agent._id

    class Config:
        allow_population_by_field_name = True


# job response modeling (for API responses)

class JobResponse(BaseModel):
    """
    Response model when a job is created or updated
    Similar to what you showed:
    {
      "job_id": "A1",
      "agent": "WebScraperAgent",
      "event_type": "status_update",
      "message": "Extracting pricing information...",
      "timestamp": "2025-11-08T20:14:22Z"
    }
    """
    job_id: str
    agent: Optional[str] = None  # Agent name
    agent_id: Optional[str] = None  # Agent ID like "A1"
    event_type: str  # e.g. "status_update", "job_created", "job_completed"
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: Optional[str] = None  # current job status
    payload: Optional[dict] = None  # additional data
