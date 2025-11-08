# db/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<user>:<pass>@cluster.mongodb.net/")
DB_NAME = os.getenv("DB_NAME", "tundra")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# collections you define here
agents_collection = db["agents"]
jobs_collection = db["jobs"]
