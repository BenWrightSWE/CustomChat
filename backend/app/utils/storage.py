from backend.app.core.supabase import supabase_admin


# gets storage path for document based storage functions
def get_document_storage_path(bot_id: int, file_name: str) -> str:
    return f"documents/{bot_id}/{file_name}"


# generalized upload to storage
def upload_file_to_storage(
    storage_path: str, file_content: bytes, content_type: str, upsert: str = "false"
):
    return supabase_admin.storage.from_("documents").upload(
        path=storage_path,
        file=file_content,
        file_options={"content-type": content_type, "upsert": upsert},
    )


# generalized download to storage
def download_file_from_storage(storage_path: str) -> bytes:
    return supabase_admin.storage.from_("documents").download(storage_path)


# generalized delete from storage
def delete_file_from_storage(storage_path: str):
    return supabase_admin.storage.from_("documents").remove([storage_path])
