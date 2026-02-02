from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    API_KEY: str = os.getenv("EMBEDDING_API_KEY")
    API_KEY_NAME: str = "EMBEDDING_API_Key"

    class Config:
        env_file = ".env"


settings = Settings()