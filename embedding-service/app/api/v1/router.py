from fastapi import APIRouter
from app.api.v1.endpoints import embed

api_router = APIRouter()

api_router.include_router(embed.router, prefix="/embed", tags=["Embed"])