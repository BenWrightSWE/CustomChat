from app.schemas.bots import BotCreate, BotUpdate
from app.core.supabase import supabase_admin
from app.utils.vault import make_and_store_api_key


def create_bot(user_id: str, bot_data: BotCreate):
    bot_dict = bot_data.model_dump()
    bot_dict["user_id"] = user_id

    method_response = make_and_store_api_key()
    bot_dict["vault_uuid"] = method_response[1]

    db_response = supabase_admin.table("bots").insert(bot_dict).execute()
    return db_response.data[0], method_response[0]


def get_all_bots(user_id: str):
    response = supabase_admin.table("bots").select("*").eq("user_id", user_id).execute()
    return response.data


def get_bot_by_id(user_id: str, bot_id: int):
    response = (
        supabase_admin.table("bots")
        .select("*")
        .eq("user_id", user_id)
        .eq("bot_id", bot_id)
        .execute()
    )
    return response.data[0] if response.data else None


def update_bot_by_id(user_id: str, bot_id: int, update_data: BotUpdate):
    update_dict = update_data.model_dump(exclude_unset=True)

    response = (
        supabase_admin.table("bots")
        .update(update_dict)
        .eq("user_id", user_id)
        .eq("bot_id", bot_id)
        .execute()
    )
    return response.data[0] if response.data else None


def delete_bot_by_id(user_id: str, bot_id: int):
    response = (
        supabase_admin.table("bots")
        .delete()
        .eq("user_id", user_id)
        .eq("bot_id", bot_id)
        .execute()
    )
    return response.data


# used to check if a bot exists without the caller having access to the bots data
def does_bot_exist(bot_id: int) -> bool:
    response = (
        supabase_admin.table("bots")
        .select("*")
        .eq("bot_id", bot_id)
        .execute()
    )
    return True if response.data else False


# used for checking the bots API key against passed API key
def get_vault_uuid(bot_id: int) -> str:
    response = (
        supabase_admin.table("bots")
        .select("vault_uuid")
        .eq("bot_id", bot_id)
        .execute()
    )
    return response.data[0]["vault_uuid"]