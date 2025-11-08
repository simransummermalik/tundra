# database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<username>:<password>@cluster.mongodb.net/")
DB_NAME = "tundra"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
agents_collection = db["agents"]
