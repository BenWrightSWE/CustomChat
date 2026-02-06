from fastapi import APIRouter, status, HTTPException
from app import main
from app.schemas.llm import (
    LLMRequest,
    LLMResponse
)

MAX_INPUT_CONTEXT = 5


router = APIRouter()

@router.post("/response", model_response=LLMResponse)
def llm_response_with_context(input_data: LLMRequest):
    try:
        if not input_data.user_input.strip():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_input cannot be empty")

        if len(input_data.input_context) > MAX_INPUT_CONTEXT:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too many context documents (max 5)")

        return main.llm_client.get_llm_response(
            input_data["chat_history"], input_data["input_context"], input_data["user_input"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while embedding document"
        )