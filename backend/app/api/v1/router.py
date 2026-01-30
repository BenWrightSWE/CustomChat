from fastapi import APIRouter
from backend.app.api.v1.endpoints import users, bots, documents, feedback

api_router = APIRouter()

api_router.include_router(users.router, prefix="/me", tags=["Users"])
api_router.include_router(documents.router, prefix="/bots/{bot_id}/documents", tags=["Documents"])
api_router.include_router(feedback.router, prefix="/bots/{bot_id}/feedback", tags=["Feedback"])
api_router.include_router(bots.router, prefix="/bots", tags=["Bots"])
