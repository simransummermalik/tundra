# db/database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env or .env.local
load_dotenv()

# Get variables from environment
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "tundra")

# Connect to MongoDB Atlas
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Collections
agents_collection = db["agents"]
jobs_collection = db["jobs"]

print(f"yay connected to MongoDB database: {DB_NAME}")
