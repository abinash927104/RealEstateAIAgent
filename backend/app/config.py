"""
Application configuration loaded from environment variables.
Uses pydantic-settings for validation and type coercion.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ─────────────────────────────────────────────
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    # ── Database ────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://realestate:realestate@localhost:5432/realestate_db"

    # ── Redis ───────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Auth ────────────────────────────────────────────
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── AI / LLM ────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ── ChromaDB ────────────────────────────────────────
    CHROMA_PERSIST_DIR: str = "./data/chroma"

    # ── Real Estate API ─────────────────────────────────
    RAPIDAPI_KEY: str = ""
    RAPIDAPI_HOST: str = "realty-in-us.p.rapidapi.com"

    # ── Frontend ────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — reads .env once."""
    return Settings()
