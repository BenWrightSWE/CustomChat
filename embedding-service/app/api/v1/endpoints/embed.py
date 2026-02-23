from fastapi import APIRouter, status, HTTPException
from app import main
from app.core.config import settings
from app.schemas.embed import (
    UserInputRequest,
    TxtDocumentRequest,
    DocumentEmbedResponse,
    UserInputEmbedResponse,
    EmbedObject
)

router = APIRouter()


@router.post("/user_input", response_model=UserInputEmbedResponse)
def embed_user_input(request: UserInputRequest):
    try:
        embedding = main.embed_client.embed_input(request.user_input)
        return UserInputEmbedResponse(chunk=request.user_input, embedding=embedding.tolist())
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while embedding user input"
        )


@router.post("/txt", response_model=DocumentEmbedResponse)
def embed_txt_document(request: TxtDocumentRequest):
    try:
        doc_size = len(request.document.encode('utf-8'))
        if doc_size > settings.MAX_DOCUMENT_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail=f"Document exceeds {settings.MAX_DOCUMENT_SIZE_MB}MB limit"
            )

        chunks = main.chunk_client.chunk_document(request.document)
        embeddings = main.embed_client.embed_document(chunks)

        embed_objects = [
            EmbedObject(chunk=k, embedding=v.tolist())  # Convert numpy array to list
            for k, v in zip(chunks, embeddings)
        ]

        return DocumentEmbedResponse(embedding_objects=embed_objects)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while embedding document"
        )

# implement for pdf

# implement for docx