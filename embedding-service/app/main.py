from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.chunk_client import ChunkClient
from app.core.embed_client import EmbedClient

chunk_client = None
embed_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chunk_client, embed_client

    print("Loading models...")
    chunk_client = ChunkClient()
    embed_client = EmbedClient()
    print("Models loaded")

    yield

    print("Shutting down Embedding API")


app = FastAPI(title="Embedding API", version="1.0.0", lifespan=lifespan)

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
    tags=["embeddings"],
    dependencies=[Depends(get_api_key)]
)
