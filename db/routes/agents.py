# db/routes/agents.py
from fastapi import APIRouter, HTTPException
from database import agents_collection
from models import Agent
from bson import ObjectId

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/")
async def get_agents():
    agents = []
    async for agent in agents_collection.find():
        agent["_id"] = str(agent["_id"])
        agents.append(agent)
    return agents

@router.post("/")
async def create_agent(agent: Agent):
    agent_dict = agent.dict(by_alias=True)
    result = await agents_collection.insert_one(agent_dict)
    return {"_id": str(result.inserted_id)}

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    try:
      oid = ObjectId(agent_id)
    except Exception:
      raise HTTPException(status_code=400, detail="Invalid agent id")

    agent = await agents_collection.find_one({"_id": oid})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent["_id"] = str(agent["_id"])
    return agent
