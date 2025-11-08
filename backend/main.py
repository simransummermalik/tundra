from fastapi import FastAPI

app = FastAPI(title="Tundra Requester Agent")

@app.get("/")
def root():
    return {"message": "Requester Agent is running"}

# Simple check to see if it works
@app.get("/health")
def health_check():
    return {"status": "ok"}
