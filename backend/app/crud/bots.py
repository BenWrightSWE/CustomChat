from app.schemas.bots import BotCreate, BotUpdate
from app.core.supabase import supabase_admin
import hashlib
import base64
import os


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


# used to generate API key and its hash for the bots
def generate_api_key(length: int) -> tuple[str, str]:
    raw_bytes = os.urandom(length)
    raw_key = f"bot_response_{base64.urlsafe_b64encode(raw_bytes).decode().rstrip('=')}"
    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, hashed_key


# returns the API key to present to the user and the UUID of the secret in the vault
def make_and_store_api_key() -> tuple[str, str]:
    api_key_and_hash = generate_api_key(32)
    response = supabase_admin.rpc(
        "insert_secret",
        {
            "secret": api_key_and_hash[1],
        }
    ).execute()
    vault_uuid = response.data

    return api_key_and_hash[0], vault_uuid
