from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    EMBEDDING_API_KEY: str

    API_KEY_NAME: str = "X-API-KEY"
    MAX_DOCUMENT_SIZE_MB: int = 10

    @property
    def MAX_DOCUMENT_SIZE(self) -> int:
        return self.MAX_DOCUMENT_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ".env.test"


settings = Settings()