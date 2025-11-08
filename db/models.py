# db/models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Pricing(BaseModel):
    base_rate: float
    unit: str  # "per_task", "per_token", etc.

class Agent(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    owner: str
    capabilities: List[str]
    average_latency_ms: Optional[int] = 0
    success_rate: Optional[float] = 0.0
    reliability_score: Optional[float] = 0.0
    pricing: Pricing
    region: str
    status: str = "active"
    total_jobs_completed: int = 0
    last_updated: datetime = datetime.utcnow()
