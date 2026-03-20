from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EMBEDDING_API_KEY: str

    API_KEY_NAME: str = "X-API-KEY"
    MAX_DOCUMENT_SIZE_MB: int = 10
    MAX_STRING_SIZE_CHAR: int = 2000  # keep at 2000

    @property
    def MAX_DOCUMENT_SIZE_BYTES(self) -> int:
        return self.MAX_DOCUMENT_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ".env"


settings = Settings()
