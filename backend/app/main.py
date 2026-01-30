from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core import supabase
from backend.app.api.v1.router import api_router

app = FastAPI(title="CustomChat API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def ping():
    return {"message": "pong"}


@app.get("/health")
def health_check():
    try:
        user = supabase.auth.get_user()
        return {"status": "ok", "supabase_connected": user}
    except Exception as error:
        return {"status": "error", "supabase_connected": error}
