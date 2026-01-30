from backend.app.schemas.users import UserUpdate
from backend.app.core.supabase import supabase_admin


def get_user_by_user_id(user_id: str):
    response = (
        supabase_admin.table("users")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    return response.data


def update_user_by_user_id(user_id: str, update_data: UserUpdate):
    update_dict = update_data.model_dump(exclude_unset=True)

    response = (
        supabase_admin.table("users")
        .update(update_dict)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data
