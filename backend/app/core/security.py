import os
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv
from app.crud import bots as bot_crud

load_dotenv()

security = HTTPBearer()
jwks_client = PyJWKClient(
    os.getenv(
        "SUPABASE_JWKS_URL", "http://127.0.0.1:54321/auth/v1/.well-known/jwks.json"
    )
)


def get_current_user(
    auth_credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verifies the Supabase JWT token and returns the user ID and token on success."""
    token = auth_credentials.credentials
    try:
        # Gets the signing key from Supabase's JWKS endpoint
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        # Verifies the token
        payload = jwt.decode(
            token, signing_key, algorithms=["ES256"], audience="authenticated"
        )

        # Extracts and validates user ID
        user_id = payload.get("sub")
        if not user_id:
            raise jwt.PyJWTError("Missing user ID in token")

        return {"id": user_id}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


# AUTH


def verify_bot_ownership(
    bot_id: int = Path(...), current_user: dict = Depends(get_current_user)
):
    """
    Verifies the bot belongs to the current user

    Raises HTTPException if the bot does not belong to the user.
    """
    bot = bot_crud.get_bot_by_id(current_user["id"], bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found or does not belong to the current user",
        )
    return bot
