from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.vectors import SearchableVector
from app.schemas.assistant import (
    AssistantResponse,
    AssistantRequest
)
from app.crud import vectors as vector_crud
import requests
import os

EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")
LLM_API_URL = os.getenv("EMBEDDING_API_URL")

router = APIRouter()

@router.post("/assistant", response_model=AssistantResponse)
def bot_contextual_response(bot_id: int, request_data: AssistantRequest):
    try:
        passed_values = request_data.model_dump()

        embed_response = requests.post(
            f"{EMBEDDING_API_URL}/embed/user_input",
            json={"user_input": passed_values.user_input},
            headers={"X-API-KEY": os.getenv("EMBEDDING_API_KEY")}
        )

        user_input_vector = SearchableVector(embedding=embed_response.json().embedding)

        neighbor_results = vector_crud.get_vector_neighbors(bot_id, user_input_vector)

        context_strings = []

        for result in neighbor_results:
            context_strings.append(result["context"])

        llm_request = {
            "chat_history": passed_values.chat_history,
            "input_context": context_strings,
            "user_input": passed_values.user_input
        }

        llm_response = requests.post(
            f"{LLM_API_URL}/{bot_id}/assistant",
            json=llm_request,
            headers={"X-API-KEY": os.getenv("LLM_API_KEY")}
        )

        return llm_response.model_dump().response

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching LLM response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while getting bot response"
        )

    # think about adding bot_id to an API_key
