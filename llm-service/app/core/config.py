from pydantic_settings import BaseSettings


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_API_KEY: str = ""
    API_KEY_NAME: str = "X-API-KEY"

    class Config:
        env_file = ".env"  # <-- no @property

settings = Settings()
