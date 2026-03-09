from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env-dev', extra='ignore')

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

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str = "https://s3.ru-1.storage.selcloud.ru"
    S3_BUCKET_NAME: str = "test-dabro-bucket"
    S3_VERIFY: str = "/etc/ssl/certs/ca-certificates.crt"

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )


settings = Settings()
