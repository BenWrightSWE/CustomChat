from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

llm_client = None

from app.core.llm_client import get_llm
from app.api.v1.router import api_router
from app.api.deps import get_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm_client

    print("Loading model...")
    llm_client = get_llm()
    print("Model loaded")

    yield

    print("Shutting down LLM API")


app = FastAPI(title="LLM API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api/v1",
    tags=["llm"],
    dependencies=[Depends(get_api_key)]
)


@app.get("/")
async def ping():
    return {"message": "pong"}