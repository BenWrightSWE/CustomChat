from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    """Compares presented API key to the LLM API's API key validating the use of the API."""
    if api_key != settings.LLM_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key