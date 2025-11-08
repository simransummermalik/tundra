from __future__ import annotations

from typing import Any, Dict, List
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

class Event(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EventQueue:
    def __init__(self) -> None:
        self.events: List[Event] = []

    def push(self, event: Event) -> None:
        self.events.append(event)

    def list_events(self) -> List[Event]:
        return self.events

    def clear(self) -> None:
        self.events.clear()