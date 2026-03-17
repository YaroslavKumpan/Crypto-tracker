from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://user:password@db:5432/crypto"
    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()