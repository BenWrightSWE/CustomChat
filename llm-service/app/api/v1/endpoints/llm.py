from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.llm import (
    LLMRequest,
    LLMResponse
)
from app.core.llm_client import LLMClient, get_llm

MAX_INPUT_CONTEXT = 5


router = APIRouter()

@router.post("/response", response_model=LLMResponse)
def llm_response_with_context(input_data: LLMRequest, llm_client: LLMClient = Depends(get_llm)):
    if not input_data.user_input.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_input cannot be empty",
        )

    if len(input_data.input_context) > MAX_INPUT_CONTEXT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Too many context documents (max 5)",
        )

    try:
        response_text = llm_client.get_llm_response(
            input_data.chat_history,
            input_data.input_context,
            input_data.user_input,
        )

        return {"response": response_text}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while generating response",
        )