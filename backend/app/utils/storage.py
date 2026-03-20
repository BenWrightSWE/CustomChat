from app.core.supabase import supabase_admin


def get_document_storage_path(bot_id: int, file_name: str) -> str:
    """gets storage path for document based storage functions"""
    return f"documents/{bot_id}/{file_name}"


def upload_file_to_storage(
    storage_path: str, file_content: bytes, content_type: str, upsert: str = "false"
):
    """generalized upload to storage"""
    return supabase_admin.storage.from_("documents").upload(
        path=storage_path,
        file=file_content,
        file_options={"content-type": content_type, "upsert": upsert},
    )


def download_file_from_storage(storage_path: str) -> bytes:
    """generalized download to storage"""
    return supabase_admin.storage.from_("documents").download(storage_path)


def delete_file_from_storage(storage_path: str):
    """generalized delete from storage"""
    return supabase_admin.storage.from_("documents").remove([storage_path])
