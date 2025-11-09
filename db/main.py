# db/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import without dots when running directly
try:
    from .routes import agents, jobs
except ImportError:
    from routes import agents, jobs

app = FastAPI(title="TUNDRA Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router)
app.include_router(jobs.router)


@app.get("/")
async def root():
    return {"message": "TUNDRA backend running", "status": "ok"}
