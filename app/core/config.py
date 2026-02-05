from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Seettings(BaseSettings):
    
    # Настройки Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # База данных PostgreSQL
    @property
    def async_database_url(self) -> PostgresDsn:
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path={self.POSTGRES_DB},
        ))

    # Настройки Redis/Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Настройки и загрузки .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True # переменные окружения будут чувствительны к регистру
    )

# Инициализация
settings = Seettings()

