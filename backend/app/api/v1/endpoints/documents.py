from fastapi import APIRouter, HTTPException, Depends, UploadFile, BackgroundTasks, Form, File, status
from fastapi.responses import FileResponse
from app.schemas.documents import DocumentCreate, DocumentResponse
from app.schemas.vectors import VectorCreate
from app.crud import documents as crud
from app.crud import vectors as vector_crud
from app.core.security import verify_bot_ownership
from app.utils.storage import (
    upload_file_to_storage,
    download_file_from_storage,
    delete_file_from_storage,
)
from app.utils.documents import get_document_and_storage_path_by_id
import requests
import tempfile
import os

"""
Should add rollback logic later for create_document and delete_document_by_id. I'm not doing it now because ordering of 
creating in storage then in db makes it sothat it won't show up to user if it fails and will overwrite if it's just in 
the storage.
"""


router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "text/plain",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")

@router.post(
    "/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
async def create_document(
    bot_id: int,
    doc_name: str = Form(...),
    doc_type: str = Form(...),
    doc_size: int = Form(...),
    file: UploadFile = File(...),
    _: dict = Depends(verify_bot_ownership),
):

    doc_data = DocumentCreate(doc_name=doc_name, doc_type=doc_type, doc_size=doc_size)

    try:
        # Validates content type
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="File type not allowed")

        # Validates file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        existing = crud.get_document_by_filename(bot_id, file.filename)

        if existing:
            raise HTTPException(status_code=409, detail="Document already exists")

        else:
            storage_path = f"documents/{bot_id}/{file.filename}"

            upload_file_to_storage(
                storage_path, file_content, file.content_type, upsert="true"
            )

            rdb_doc = crud.create_document(
                bot_id, doc_data
            )  # creates document in relational db

            response = requests.post(
                f"{EMBEDDING_API_URL}/embed/txt",
                json={"document": file_content.decode("utf-8")},
                headers={"X-API-KEY": os.getenv("EMBEDDING_API_KEY")}
            )

            embed_data = response.json()

            # Convert to VectorCreate objects
            vector_objects = [
                VectorCreate(context=obj["chunk"], embedding=obj["embedding"])
                for obj in embed_data["embedding_objects"]
            ]

            vector_crud.create_vectors(bot_id, rdb_doc["doc_id"], vector_objects)

            return rdb_doc
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating document: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error while creating document")


@router.get("/", response_model=list[DocumentResponse])
def get_all_documents(bot_id: int, _: dict = Depends(verify_bot_ownership)):
    try:
        return crud.get_all_documents(bot_id)
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error while getting all documents for bot")


@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document_by_id(
    bot_id: int, doc_id: int, _: dict = Depends(verify_bot_ownership)
):
    try:
        feedback = crud.get_document_by_id(bot_id, doc_id)
        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return feedback
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error while getting document by id")


@router.get("/{doc_id}/download", response_class=FileResponse)
def download_document_by_id(
    bot_id: int,
    doc_id: int,
    background_tasks: BackgroundTasks,
    _: dict = Depends(verify_bot_ownership),
):
    try:
        db_doc, storage_path = get_document_and_storage_path_by_id(bot_id, doc_id)

        if not db_doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        doc_bytes = download_file_from_storage(storage_path)

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=db_doc["doc_type"])

        temp.write(doc_bytes)
        temp.close()

        # Return file while cleaning up the temp file
        background_tasks.add_task(os.unlink, temp.name)

        return FileResponse(
            temp.name,
            media_type=db_doc["doc_type"],
            filename=f"{db_doc["doc_name"]}{db_doc["doc_type"]}",
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error while downloading document by id")


@router.delete(
    "/{doc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_by_id(
    bot_id: int, doc_id: int, _: dict = Depends(verify_bot_ownership)
):
    try:
        db_doc, storage_path = get_document_and_storage_path_by_id(bot_id, doc_id)

        if not db_doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        crud.delete_document_by_id(bot_id, doc_id)  # deletes from relational db

        delete_file_from_storage(storage_path)

        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error while deleting document by id")
