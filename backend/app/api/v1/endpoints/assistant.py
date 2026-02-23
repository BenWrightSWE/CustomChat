from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.vectors import SearchableVector
from app.schemas.assistant import (
    AssistantResponse,
    AssistantRequest,
)
from app.utils.assistant import (
    get_api_embedding,
    get_llm_api_response
)
from app.crud.vectors import get_vector_neighbors
from app.crud.bots import does_bot_exist

router = APIRouter()


@router.post("/assistant", response_model=AssistantResponse)
def bot_contextual_response(bot_id: int, request_data: AssistantRequest):
    try:
        if not does_bot_exist(bot_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found")

        passed_values = request_data.model_dump()

        user_input_vector = SearchableVector(
            embedding=get_api_embedding(passed_values["user_input"])
        )

        neighbor_results = get_vector_neighbors(bot_id, user_input_vector)["neighbors"]

        context_strings = []

        for result in neighbor_results:
            context_strings.append(result["context"])

        return AssistantResponse(
            role="ASSISTANT",
            message=get_llm_api_response(
                passed_values["chat_history"],
                context_strings,
                passed_values["user_input"]
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching LLM response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while getting bot response"
        )

    # think about adding bot_id to an API_key
