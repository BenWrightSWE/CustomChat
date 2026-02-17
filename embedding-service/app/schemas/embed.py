from pydantic import BaseModel, Field
from typing import List


class UserInputRequest(BaseModel):
    user_input: str


class TxtDocumentRequest(BaseModel):
    document: str = Field(..., min_length=1)


class EmbedObject(BaseModel):
    chunk: str
    embedding: List[float]


class UserInputEmbedResponse(EmbedObject):
    pass


class DocumentEmbedResponse(BaseModel):
    embedding_objects: List[EmbedObject]
