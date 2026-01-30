from pydantic import BaseModel


class DocumentBase(BaseModel):
    doc_name: str
    doc_type: str
    doc_size: int


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    doc_id: int
    bot_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models
