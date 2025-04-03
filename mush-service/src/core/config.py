from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings loaded from environment variables or .env file."""

    project_name: str = "Mush Service"
    project_description: str = "Mush service for the mush store."

    # PostgreSQL
    sql_echo: bool = True
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432

    # Redis
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_db: int = 0

    # Logging settings
    log_level: str = "DEBUG"  # "INFO"

    @property
    def postgres_db_url(self) -> str:
        """Assemble the PostgreSQL database URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
logging_config.dictConfig(LOGGING)
