from app.schemas.documents import DocumentCreate
from app.core.supabase import supabase_admin
from fastapi import HTTPException, status


def create_document(bot_id: int, doc_data: DocumentCreate):
    doc_dict = doc_data.model_dump()
    doc_dict["bot_id"] = bot_id

    response = supabase_admin.table("documents").insert(doc_dict).execute()
    return response.data[0]


def get_all_documents(bot_id: int):
    response = supabase_admin.table("documents").select("*").eq("bot_id", bot_id).execute()
    return response.data


def get_document_by_id(bot_id: int, doc_id: int):
    response = (
        supabase_admin.table("documents")
        .select("*")
        .eq("bot_id", bot_id)
        .eq("doc_id", doc_id)
        .maybe_single()
        .execute()
    )

    if response is None or response.data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return response.data


def get_document_by_filename(bot_id: int, file_name: str):
    """
    Returns a document based on the file name.
    file_name is the full name including extension (eg, name.txt)
    """
    if "." not in file_name:
        raise ValueError("File must have an extension")

    doc_name = ".".join(file_name.split(".")[:-1])
    doc_type = "." + file_name.split(".")[-1]

    response = (
        supabase_admin.table("documents")
        .select("*")
        .eq("bot_id", bot_id)
        .eq("doc_name", doc_name)
        .eq("doc_type", doc_type)
        .maybe_single()
        .execute()
    )

    # maybe_single returns None if no row is found
    if response is None or not hasattr(response, "data"):
        return None

    return response.data


def delete_document_by_id(bot_id: int, doc_id: int):
    response = (
        supabase_admin.table("documents")
        .delete()
        .eq("bot_id", bot_id)
        .eq("doc_id", doc_id)
        .execute()
    )
    return response.data
