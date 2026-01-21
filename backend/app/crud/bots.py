from backend.app.schemas.bots import BotCreate, BotUpdate
from backend.app.core.supabase import supabase_admin


def create_bot(user_id: str, bot_data: BotCreate):
    bot_dict = bot_data.model_dump()
    bot_dict["user_id"] = user_id

    response = supabase_admin.table("bots").insert(bot_dict).execute()
    return response.data[0]


def get_all_bots(user_id: str):
    response = supabase_admin.table("bots").select("*").eq("user_id", user_id).execute()
    return response.data


def get_bot_by_id(user_id: str, bot_id: int):
    response = (
        supabase_admin.table("bots")
        .select("*")
        .eq("user_id", user_id)
        .eq("bot_id", bot_id)
        .single()
        .execute()
    )
    return response.data


def update_bot_by_id(user_id: str, bot_id: int, update_data: BotUpdate):

    update_dict = update_data.model_dump(exclude_unset=True)

    response = (
        supabase_admin.table("bots")
        .update(update_dict)
        .eq("user_id", user_id)
        .eq("bot_id", bot_id)
        .execute()
    )
    return response.data


def delete_bot_by_id(user_id: str, bot_id: int):
    response = (
        supabase_admin.table("bots")
        .delete()
        .eq("user_id", user_id)
        .eq("bot_id", bot_id)
        .execute()
    )
    return response.data
