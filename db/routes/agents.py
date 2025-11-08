# routes/agents.py
from fastapi import APIRouter, HTTPException
from models import Agent
from database import agents_collection
from bson import ObjectId

router = APIRouter(prefix="/agents", tags=["Agents"])

# GET all agents
@router.get("/")
async def get_agents():
    agents = []
    async for agent in agents_collection.find():
        agent["_id"] = str(agent["_id"])
        agents.append(agent)
    return agents

# POST a new agent
@router.post("/")
async def create_agent(agent: Agent):
    agent_dict = agent.dict(by_alias=True)
    result = await agents_collection.insert_one(agent_dict)
    return {"_id": str(result.inserted_id)}

# GET a single agent by ID
@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    agent = await agents_collection.find_one({"_id": ObjectId(agent_id)})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent["_id"] = str(agent["_id"])
    return agent
