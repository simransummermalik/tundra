# main.py
from fastapi import FastAPI
from routes import agents

app = FastAPI(title="TUNDRA Backend")

app.include_router(agents.router)

@app.get("/")
def root():
    return {"message": "TUNDRA backend running"}
