from pydantic import BaseModel
from typing import List


class ChatMessage(BaseModel):
    role: str
    message: str


class LLMRequest(BaseModel):
    chat_history: List[ChatMessage]
    input_context: List[str]
    user_input: str


class LLMResponse(BaseModel):
    response: str