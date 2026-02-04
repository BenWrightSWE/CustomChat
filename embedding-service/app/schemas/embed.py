from pydantic import BaseModel, Field
from typing import List


class TxtDocumentRequest(BaseModel):
    document: str = Field(..., min_length=1)


class EmbedObject(BaseModel):
    chunk: str
    embedding: List[float]


class EmbedResponse(BaseModel):
    embedding_objects: List[EmbedObject]
