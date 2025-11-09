from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["tundra_db"]
jobs_collection = db["jobs"]
api_keys_collection = db["api_keys"]
users_collection = db["users"]
