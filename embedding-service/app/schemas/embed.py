from pydantic import BaseModel, Field
from typing import List


class TxtDocumentRequest(BaseModel):
    document: str = Field(..., min_length=1)


class EmbedResponse(BaseModel):
    chunks: List[str]
    embeddings: List[List[float]]