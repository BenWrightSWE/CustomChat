from fastapi import APIRouter
from app.api.v1.endpoints import embedding

api_router = APIRouter()

api_router.include_router(embedding.router, prefix="/embedding", tags=["Embedding"])