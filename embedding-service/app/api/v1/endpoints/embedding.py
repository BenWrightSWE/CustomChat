from fastapi import APIRouter, status, HTTPException
from app import main
from app.schemas.embedding import (
    DocumentRequest,
    EmbeddingResponse
)

router = APIRouter()

@router.post("/embed", response_model=EmbeddingResponse)
def embed_document(request: DocumentRequest):
    try:
        chunks = main.chunk_client.chunk_document(request.document)
        embeddings = main.embed_client.embed_document(chunks)
        return {"embeddings": embeddings.tolist()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while embedding document"
        )



