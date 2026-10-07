import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment or defaults."""
    app_name: str = "TaskBoard Cloud API"
    version: str = "1.0.0"
    environment: str = "production"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./taskboard.db"
    )
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
