from pydantic import BaseModel
from typing import List


class ChatMessage(BaseModel):
    role: str
    message: str


class AssistantRequest(BaseModel):
    chat_history: List[ChatMessage]
    user_input: str


class AssistantResponse(ChatMessage):
    pass
