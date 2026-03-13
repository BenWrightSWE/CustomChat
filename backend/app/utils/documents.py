from app.crud import documents as crud
from fastapi import HTTPException, status
from app.schemas.documents import DocumentResponse
import requests
import os


EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")


# Not put in CRUD due to it not directly accessing the database.
def get_document_and_storage_path_by_id(
    bot_id: int, doc_id: int
) -> tuple[DocumentResponse, str]:
    """
    Returns the document and its storage path for a document in the database by its id.
    Used in the case for you have the db data but need to access the storage version of the document.

    Returns a tuple where the first value is the DocumentResponse from the db and the second is the storage path.
    """
    document = crud.get_document_by_id(bot_id, doc_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    storage_path = f"documents/{bot_id}/{document['file_name']}"
    return document, storage_path


# Interacting with an API needed for create document endpoint
def get_document_embed_data_from_api(file_content: str):
    response = requests.post(
        f"{EMBEDDING_API_URL}/embed/txt",
        json={"document": file_content},
        headers={"X-API-KEY": os.getenv("EMBEDDING_API_KEY")}
    )

    print(response.json())

    return response.json()
