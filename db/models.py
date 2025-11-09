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
