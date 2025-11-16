from typing import Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # APP
    APP_PROJECT: str = "GreenUp backend"
    APP_API_V1_STR: str = "/api/v1"
    APP_ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"

    # Logger
    LOGGER_CHANNEL: Literal["file", "console"] = "file"  # ← в будущем: "sentry"

    # Cache
    CACHE_STORAGE: Literal["redis", "memory"] = "redis"

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Redis
    CACHE_REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "<GENERATED_SECRET_KEY>"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Background tasks
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
