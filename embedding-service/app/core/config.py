from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEYS: str = "key1,key2,key3"

    BOT_API_KEYS: dict = {}

    class Config:
        env_file = ".env"


settings = Settings()