from fastapi import APIRouter
from backend.app.api.v1.endpoints import users, bots, feedback

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(bots.router, prefix="/bots", tags=["Bots"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])