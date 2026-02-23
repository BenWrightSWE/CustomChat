import requests
import os

EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")
LLM_API_URL = os.getenv("LLM_API_URL")


def get_api_embedding(user_input: str) -> list:
    response = requests.post(
        f"{EMBEDDING_API_URL}/embed/user_input",
        json={"user_input": user_input},
        headers={"X-API-KEY": os.getenv("EMBEDDING_API_KEY")}
    )
    response.raise_for_status()
    return response.json()["embedding"]


def get_llm_api_response(chat_history, context_strings: list, user_input: str) -> str:
    response = requests.post(
        f"{LLM_API_URL}/llm/response",
        json={
            "chat_history": chat_history,
            "input_context": context_strings,
            "user_input": user_input
        },
        headers={"X-API-KEY": os.getenv("LLM_API_KEY")}
    )
    response.raise_for_status()
    return response.json()["response"]