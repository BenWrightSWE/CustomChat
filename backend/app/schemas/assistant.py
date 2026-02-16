from pydantic import BaseModel
from typing import List


class ChatMessage(BaseModel):
    role: str
    message: str


class AssistantRequest:
    chat_history: List[ChatMessage]
    user_input: str


class AssistantResponse:
    response: ChatMessage
