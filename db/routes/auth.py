# db/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
import secrets
import hashlib
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory storage for now (replace with database later)
api_keys = {}  # {api_key_hash: {user_id, email, created_at}}
user_keys = {}  # {user_id: api_key} - to track which users have keys


class SignupRequest(BaseModel):
    email: EmailStr
    user_id: str  # From Supabase


class APIKeyResponse(BaseModel):
    api_key: str
    message: str


def generate_api_key() -> str:
    """Generate a secure API key"""
    # Format: tundra_sk_<random_string>
    random_part = secrets.token_urlsafe(32)
    return f"tundra_sk_{random_part}"


def hash_api_key(api_key: str) -> str:
    """Hash API key for secure storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()


@router.post("/get-or-create-key", response_model=APIKeyResponse)
async def get_or_create_key(request: SignupRequest):
    """
    Get existing API key or create new one for user

    Call this from your frontend when user logs in:
    - User logs in with Supabase
    - Frontend calls this endpoint with user_id
    - If user has existing key, returns masked version
    - If new user, generates and returns full key
    """
    # Check if user already has a key
    existing_key = user_keys.get(request.user_id)

    if existing_key:
        # User already has a key, return masked version
        masked_key = existing_key[:13] + "•" * 20
        return APIKeyResponse(
            api_key=masked_key,
            message="You already have an API key. Check your Settings page."
        )

    # Generate new API key for new user
    api_key = generate_api_key()
    api_key_hash = hash_api_key(api_key)

    # Store in database (using in-memory for now)
    api_keys[api_key_hash] = {
        "user_id": request.user_id,
        "email": request.email,
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }

    # Track user's key
    user_keys[request.user_id] = api_key

    return APIKeyResponse(
        api_key=api_key,
        message="API key generated successfully. Save this key - it won't be shown again!"
    )


@router.post("/generate-key", response_model=APIKeyResponse)
async def generate_key(request: SignupRequest):
    """
    Generate NEW API key for user (even if they have one)

    This will invalidate the old key and create a new one.
    Use get-or-create-key for normal login flow.
    """
    # Revoke old key if exists
    old_key = user_keys.get(request.user_id)
    if old_key:
        old_hash = hash_api_key(old_key)
        if old_hash in api_keys:
            api_keys[old_hash]["active"] = False

    # Generate new API key
    api_key = generate_api_key()
    api_key_hash = hash_api_key(api_key)

    # Store in database (using in-memory for now)
    api_keys[api_key_hash] = {
        "user_id": request.user_id,
        "email": request.email,
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }

    # Update user's key
    user_keys[request.user_id] = api_key

    return APIKeyResponse(
        api_key=api_key,
        message="New API key generated. Your old key has been revoked. Save this key - it won't be shown again!"
    )


async def verify_api_key(x_api_key: str = Header(...)) -> dict:
    """
    Dependency to verify API key

    Use in routes like:
    @router.get("/agents")
    async def get_agents(user_data: dict = Depends(verify_api_key)):
        # user_data contains user info
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    # Hash the provided key
    api_key_hash = hash_api_key(x_api_key)

    # Check if exists
    user_data = api_keys.get(api_key_hash)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not user_data.get("active"):
        raise HTTPException(status_code=401, detail="API key has been revoked")

    return user_data


@router.delete("/revoke-key")
async def revoke_key(user_data: dict = Depends(verify_api_key)):
    """Revoke current API key"""
    # Find and deactivate the key
    for key_hash, data in api_keys.items():
        if data["user_id"] == user_data["user_id"]:
            data["active"] = False

    return {"message": "API key revoked successfully"}


@router.get("/verify")
async def verify_key(user_data: dict = Depends(verify_api_key)):
    """Test if API key is valid"""
    return {
        "valid": True,
        "email": user_data["email"],
        "created_at": user_data["created_at"]
    }
