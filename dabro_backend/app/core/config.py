from typing import Set

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'dabro_db'
    POSTGRES_USER: str = 'dabro_user'
    POSTGRES_PASSWORD: str

    SESSION_TTL_HOURS: int = 12
    SESSION_COOKIE_NAME: str = "session_id"
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_DOMAIN: str | None = None

    SHEET_NAME: str = "Товарные остатки Косметика"
    REQUIRED_COLUMNS: Set[str] = {"id", "стоимость", "остаток"}

    LOG_LEVEL_DEFAULT: str = "INFO"

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )
    #
    # @field_validator("CORS_ORIGINS", mode="before")
    # @classmethod
    # def parse_cors_origins(cls, v):
    #     if v is None:
    #         return []
    #     if isinstance(v, list):
    #         return v
    #     if isinstance(v, str):
    #         return [s.strip() for s in v.split(",") if s.strip()]
    #     return []


settings = Settings()
