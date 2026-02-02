from pydantic import BaseModel, Field
from typing import List


class DocumentRequest(BaseModel):
    document: str = Field(..., min_length=1)


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]