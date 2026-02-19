from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "local"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    VECTOR_DB_DIR: str = "./chroma_store"

    LLM_PROVIDER: str = "openai"

    OPENAI_API_KEY: str | None = None
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBED_MODEL: str = "text-embedding-3-small"

    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_CHAT_DEPLOYMENT: str | None = None
    AZURE_OPENAI_EMBED_DEPLOYMENT: str | None = None

    VISION_PROVIDER: str = "openai"

@lru_cache()
def get_settings():
    return Settings()
