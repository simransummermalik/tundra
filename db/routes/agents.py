# routes/agents.py
from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId

try:
    from ..database import agents_collection
    from ..models import Agent
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from database import agents_collection
    from models import Agent

router = APIRouter(prefix="/agents", tags=["agents"])


def agent_helper(agent) -> dict:
    # convert Mongo's _id → string so frontend can use it
    return {
        "id": str(agent["_id"]),
        "name": agent["name"],
        "capabilities": agent.get("capabilities", []),
        "average_latency_ms": agent.get("average_latency_ms", 0),
        "success_rate": agent.get("success_rate", 0.0),
        "reliability_score": agent.get("reliability_score", 0.0),
        "pricing": agent.get("pricing"),
        "region": agent.get("region"),
        "status": agent.get("status", "active"),
        "total_jobs_completed": agent.get("total_jobs_completed", 0),
        "last_updated": agent.get("last_updated"),
    }


@router.get("/", response_model=List[Agent])
async def get_agents():
    agents = []
    cursor = agents_collection.find({})
    async for doc in cursor:
        # Agent(**doc) lets pydantic handle the alias "_id"
        agents.append(Agent(**doc))
    return agents


@router.post("/", response_model=Agent)
async def create_agent(agent: Agent):
    # pydantic model → dict; use by_alias=True so `_id` works if passed
    agent_dict = agent.model_dump(by_alias=True)
    result = await agents_collection.insert_one(agent_dict)
    created = await agents_collection.find_one({"_id": result.inserted_id})
    return Agent(**created)


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    doc = await agents_collection.find_one({"_id": ObjectId(agent_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Agent not found")
    return Agent(**doc)


@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, agent: Agent):
    agent_dict = agent.model_dump(by_alias=True)
    # don’t let user overwrite _id with a new value
    agent_dict.pop("_id", None)

    result = await agents_collection.update_one(
        {"_id": ObjectId(agent_id)},
        {"$set": agent_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found")

    updated = await agents_collection.find_one({"_id": ObjectId(agent_id)})
    return Agent(**updated)


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    result = await agents_collection.delete_one({"_id": ObjectId(agent_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"ok": True}
