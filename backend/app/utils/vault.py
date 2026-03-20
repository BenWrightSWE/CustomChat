from app.core.supabase import supabase_admin
import hashlib
import base64
import hmac
import os


def generate_api_key(length: int) -> tuple[str, str]:
    """
    Used to generate API key and its hash for the bots
    Returns a tuple (raw_key, hashed_key)
    """
    raw_bytes = os.urandom(length)
    raw_key = f"bot_response_{base64.urlsafe_b64encode(raw_bytes).decode().rstrip('=')}"
    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, hashed_key


def make_and_store_api_key() -> tuple[str, str]:
    """
    Creates an API key for bot assistant usage
    Returns a tuple of the API key to present to the user and the UUID of the secret in the vault
    """
    api_key_and_hash = generate_api_key(32)
    response = supabase_admin.rpc(
        "insert_secret",
        {
            "secret": api_key_and_hash[1],
        },
    ).execute()
    vault_uuid = response.data

    return api_key_and_hash[0], vault_uuid


def make_and_update_api_key(vault_uuid: str) -> str:
    """
    Updates an API key for bot assistant usage
    Returns the updated API key to present to the user
    """
    api_key_and_hash = generate_api_key(32)
    response = supabase_admin.rpc(
        "update_secret",
        {
            "secret_id": vault_uuid,
            "secret": api_key_and_hash[1],
        },
    ).execute()
    return api_key_and_hash[0]


def get_secret(vault_uuid: str) -> str:
    """returns the API key pertaining to the passed vault_uuid"""
    response = supabase_admin.rpc(
        "get_secret",
        {
            "secret_id": vault_uuid,
        },
    ).execute()
    return response.data


def verify_api_key(incoming_key: str, vault_uuid: str) -> bool:
    """verifies the passed API key to use the bot assistant compared to its actual API key"""
    stored_hash = get_secret(vault_uuid)
    incoming_hash = hashlib.sha256(incoming_key.encode()).hexdigest()
    return hmac.compare_digest(incoming_hash, stored_hash)
    # hmac prevents timing attack, always same amount of time each comparison
