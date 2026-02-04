from pydantic import BaseModel
from typing import List


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


class VectorSearchBase(BaseModel):
    embedding: List[float]


class VectorSearch(VectorSearchBase):
    pass


class VectorSearchResponse(VectorSearch):
    vec_id: int
    doc_id: int

    class Config:
        from_attributes = True
