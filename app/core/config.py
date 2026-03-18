from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()