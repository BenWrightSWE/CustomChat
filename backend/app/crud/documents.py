from backend.app.schemas.documents import DocumentCreate
from backend.app.core.supabase import supabase_admin


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
        .single()
        .execute()
    )
    return response.data


def get_document_by_filename(bot_id: int, file_name: str):
    """
    returns a document based on the file name
    file_name is the name and the type (eg, name.txt)
    """
    file_name_split = file_name.split(".")
    doc_name = file_name_split[0]
    doc_type = "." + file_name_split[1]

    response = (
        supabase_admin.table("documents")
        .select("*")
        .eq("bot_id", bot_id)
        .eq("doc_name", doc_name)
        .eq("doc_type", doc_type)
        .maybe_single()
        .execute()
    )
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
