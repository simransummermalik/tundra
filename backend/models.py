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

class User(BaseModel):
    user_id: str
    password_hash: str
    created_at: datetime
    is_active: bool = True

class APIKey(BaseModel):
    key: str
    user_id: str
    created_at: datetime
    last_used: Optional[datetime] = None
    is_active: bool = True

class APIKeyResponse(BaseModel):
    api_key: str
    user_id: str
    message: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
