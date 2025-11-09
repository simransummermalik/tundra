from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI, uuidRepresentation="standard")
db = client["tundra_db"]
jobs_collection = db["jobs"]
agents_collection = db["agents"]
credits_collection = db["credits"]
