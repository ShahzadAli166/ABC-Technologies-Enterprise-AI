import os
import secrets
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="ABC Technologies Enterprise AI",
    version="2.0"
)

API_KEY = os.environ.get("ABC_API_KEY", "")

@app.get("/")
def home():
    return {
        "application": "ABC Technologies Enterprise AI",
        "status": "running",
        "deployment": "Render"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/assistant")
async def assistant(
    payload: dict,
    x_api_key: str = Header(default="")
):
    if not API_KEY or not secrets.compare_digest(
        x_api_key, API_KEY
    ):
        raise HTTPException(401, "Unauthorized")

    # Agent runtime will be connected in the next stage.
    raise HTTPException(
        503,
        "AI runtime integration is not configured yet."
    )
