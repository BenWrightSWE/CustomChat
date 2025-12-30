from backend.app.schemas.users import UserCreate, UserUpdate
from backend.app.core.supabase import supabase_admin


def create_user(user_id: str, user_data: UserCreate):
    user_dict = user_data.model_dump()
    user_dict["user_id"] = user_id  # Add the required user_id
    response = supabase_admin.table("users").insert(user_dict).execute()
    return response


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
    # Excludes unset fields
    update_dict = update_data.model_dump(exclude_unset=True)

    response = (
        supabase_admin.table("users")
        .update(update_dict)
        .eq("user_id", user_id)
        .execute()
    )
    return response
