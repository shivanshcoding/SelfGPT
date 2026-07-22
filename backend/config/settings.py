"""
SelfGPT — Centralized Settings

Every configurable value is pulled from environment variables via Pydantic
BaseSettings.  Zero hardcoded secrets, model names, or identity content.
"""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = "SelfGPT"
    app_env: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    cors_origins: List[str] = Field(default=["http://localhost:3000"])

    # ── Auth / JWT ───────────────────────────────────────────────────────
    jwt_secret_key: str = "change-me-to-a-random-secret-at-least-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # ── Google OAuth ─────────────────────────────────────────────────────
    google_client_id: str = ""
    google_client_secret: str = ""

    # ── MongoDB ──────────────────────────────────────────────────────────
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "selfgpt"

    # ── Redis ────────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── ChromaDB ─────────────────────────────────────────────────────────
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_persist_dir: str = "./data/chroma"

    # ── Storage ──────────────────────────────────────────────────────────
    storage_backend: str = "local"
    storage_local_dir: str = "./data/uploads"
    s3_endpoint_url: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_bucket_name: str = "selfgpt-uploads"
    s3_region: str = "us-east-1"

    # ── LLM Provider ────────────────────────────────────────────────────
    llm_provider: str = "ollama"
    llm_base_url: str = "http://localhost:11434"
    llm_api_key: str = ""
    llm_default_model: str = "llama3.2"
    llm_default_vision_model: str = "llava"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # ── Embedding ────────────────────────────────────────────────────────
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "cpu"

    # ── Celery ───────────────────────────────────────────────────────────
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton — parsed once, reused everywhere."""
    return Settings()
