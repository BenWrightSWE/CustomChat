import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv

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
    """Verify Supabase JWT token and return user ID and token on success."""
    token = auth_credentials.credentials
    try:
        # Get the signing key from Supabase's JWKS endpoint
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        # Verify the token
        payload = jwt.decode(
            token, signing_key, algorithms=["ES256"], audience="authenticated"
        )

        # Extract and validate user ID
        user_id = payload.get("sub")
        if not user_id:
            raise jwt.PyJWTError("Missing user ID in token")

        return {"id": user_id}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
