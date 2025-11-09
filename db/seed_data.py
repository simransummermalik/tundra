# db/seed_data.py
"""
Seed script to populate MongoDB with initial TUNDRA agents
"""

import asyncio
from datetime import datetime
from database import agents_collection, jobs_collection

# Initial agents to add to the marketplace
SEED_AGENTS = [
    {
        "agent_id": "A1",  # Custom readable ID
        "name": "WebScraperAgent",
        "capabilities": ["web_scraping", "data_extraction", "html_parsing"],
        "average_latency_ms": 2300,
        "success_rate": 94.0,
        "reliability_score": 0.94,
        "pricing": {
            "base_rate": 0.15,
            "unit": "per_task"
        },
        "region": "US-East",
        "status": "active",
        "total_jobs_completed": 1247,
        "last_updated": datetime.utcnow()
    },
    {
        "agent_id": "A2",
        "name": "SummarizeGPT",
        "capabilities": ["text_summarization", "nlp", "content_analysis"],
        "average_latency_ms": 1800,
        "success_rate": 91.0,
        "reliability_score": 0.91,
        "pricing": {
            "base_rate": 0.08,
            "unit": "per_task"
        },
        "region": "EU-West",
        "status": "active",
        "total_jobs_completed": 3421,
        "last_updated": datetime.utcnow()
    },
    {
        "agent_id": "A3",
        "name": "ValidatorPro",
        "capabilities": ["data_validation", "compliance_checking", "schema_verification"],
        "average_latency_ms": 3100,
        "success_rate": 89.0,
        "reliability_score": 0.89,
        "pricing": {
            "base_rate": 0.12,
            "unit": "per_task"
        },
        "region": "US-West",
        "status": "active",
        "total_jobs_completed": 892,
        "last_updated": datetime.utcnow()
    },
    {
        "agent_id": "A4",
        "name": "CodeReviewAI",
        "capabilities": ["code_review", "security_analysis", "best_practices"],
        "average_latency_ms": 4500,
        "success_rate": 85.0,
        "reliability_score": 0.85,
        "pricing": {
            "base_rate": 0.22,
            "unit": "per_task"
        },
        "region": "US-East",
        "status": "active",
        "total_jobs_completed": 567,
        "last_updated": datetime.utcnow()
    },
    {
        "agent_id": "A5",
        "name": "ImageAnalyzerPro",
        "capabilities": ["image_classification", "object_detection", "ocr"],
        "average_latency_ms": 2900,
        "success_rate": 92.0,
        "reliability_score": 0.92,
        "pricing": {
            "base_rate": 0.18,
            "unit": "per_task"
        },
        "region": "Asia-Pacific",
        "status": "idle",
        "total_jobs_completed": 2103,
        "last_updated": datetime.utcnow()
    }
]

# Sample job for demonstration
SEED_JOBS = [
    {
        "job_id": "JOB-DEMO-001",
        "task": "Extract competitor pricing data from e-commerce site",
        "task_type": "web_scrape",
        "budget": 0.15,
        "workflow": ["Scout", "Sentinel", "Custodian"],
        "created_at": datetime.utcnow(),
        "status": "completed",
        "assigned_agent_id": "A1",
        "assigned_agent_name": "WebScraperAgent",
        "payload": {
            "url": "https://example.com/",
            "target_data": "pricing_information"
        }
    }
]


async def seed_database():
    """Populate database with initial agents and jobs"""

    print("🌱 Starting database seed...")

    # Clear existing data (optional - remove if you want to keep existing data)
    print("Clearing existing agents and jobs...")
    await agents_collection.delete_many({})
    await jobs_collection.delete_many({})

    # Insert agents
    print(f"\n📦 Inserting {len(SEED_AGENTS)} agents...")
    result = await agents_collection.insert_many(SEED_AGENTS)
    print(f"✅ Inserted {len(result.inserted_ids)} agents")

    # Print agent IDs for reference
    print("\n🤖 Agent IDs:")
    async for agent in agents_collection.find({}):
        print(f"  - {agent['agent_id']}: {agent['name']} (MongoDB _id: {agent['_id']})")

    # Insert sample jobs
    print(f"\n📦 Inserting {len(SEED_JOBS)} sample jobs...")
    result = await jobs_collection.insert_many(SEED_JOBS)
    print(f"✅ Inserted {len(result.inserted_ids)} jobs")

    print("\n✨ Database seeding complete!")
    print(f"\nYou can now query agents by:")
    print(f"  - Custom ID: agents_collection.find_one({{'agent_id': 'A1'}})")
    print(f"  - MongoDB ID: agents_collection.find_one({{'_id': ObjectId('...')}})")


async def clear_database():
    """Clear all data from database"""
    print("🗑️  Clearing database...")
    await agents_collection.delete_many({})
    await jobs_collection.delete_many({})
    print("✅ Database cleared")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        asyncio.run(clear_database())
    else:
        asyncio.run(seed_database())
