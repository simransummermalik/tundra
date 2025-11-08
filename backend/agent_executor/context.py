from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Optional, ClassVar
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel, Field

class TaskState(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class RequestContext(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    task_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    sender: str = "unknown"
    received_at: datetime = Field(default_factory=datetime.utcnow)
    state: TaskState = TaskState.pending

    agent_name: str = "TundraAgent"
    goal: str = "Process assigned task autonomously"

    parent_job_id: Optional[str] = None
    correlation_id: Optional[str] = None

    ALLOWED_TASK_TYPES: ClassVar[set[str]] = {"web_scrape"}

    def validate_task_type(self) -> None:
        if self.task_type not in self.ALLOWED_TASK_TYPES:
            raise ValueError(f"Unsupported task_type: {self.task_type}")

    def mark_in_progress(self) -> None:
        self.state = TaskState.in_progress

    def mark_completed(self) -> None:
        self.state = TaskState.completed

    def mark_failed(self) -> None:
        self.state = TaskState.failed
