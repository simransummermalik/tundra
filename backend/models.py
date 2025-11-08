from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class Job(BaseModel):
    job_id: Optional[str] = None
    user_id: Optional[str] = None
    task: str
    budget: float
    workflow: List[str] = Field(default_factory=lambda: ["Scout", "Sentinel", "Custodian"])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

class Context(BaseModel):
    job_id: str
    current_step: str = "Scout"
    outputs: Dict[str, Dict] = Field(default_factory=dict)
    status: str = "pending"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None

class AgentOutput(BaseModel):
    agent_name: str
    success: bool = True
    output: Dict = Field(default_factory=dict)
    errors: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Provider(BaseModel):
    provider_id: Optional[str] = None
    name: str
    description: str
    pricing_per_job: float
    capabilities: List[str] = Field(default_factory=list)
    verified: bool = False
    metrics: Dict = Field(default_factory=lambda: {
        "success_rate": 0.0,
        "avg_latency_sec": 0.0,
        "jobs_completed": 0
    })

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str
