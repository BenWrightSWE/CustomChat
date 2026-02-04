from app.crud import documents as crud
from fastapi import HTTPException, status
from app.schemas.documents import DocumentResponse


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

    doc_name_type = f"{document['doc_name']}{document['doc_type']}"
    storage_path = f"documents/{bot_id}/{doc_name_type}"
    return document, storage_path
