from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.assistant import (
    AssistantResponse,
    AssistantRequest
)

router = APIRouter()
