from pydantic import BaseModel
from typing import List


# USED FOR VECTOR CREATION

class VectorBase(BaseModel):
    context: str
    embedding: List[float]


class VectorCreate(VectorBase):
    pass


class VectorCreateResponse(VectorBase):
    vec_id: int
    doc_id: int
    bot_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models


# USED FOR VECTOR RETRIEVAL

class SearchableVector(BaseModel):
    embedding: List[float]


class VectorSearchItem(BaseModel):
    vec_id: int
    context: str


class VectorSearchResponse(BaseModel):
    neighbors: List[VectorSearchItem]

    class Config:
        from_attributes = True
