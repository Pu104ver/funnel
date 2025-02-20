from pydantic_settings import BaseSettings
from dotenv import load_dotenv

import os


load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    API_ID: int = int(os.getenv("API_ID"))
    API_HASH: str = os.getenv("API_HASH")
    POSTGRES_ASYNC_DATABASE_URL: str = os.getenv("POSTGRES_ASYNC_DATABASE_URL")
    POSTGRES_DATABASE_URL: str = os.getenv("POSTGRES_DATABASE_URL")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    DEBUG: bool = os.getenv("DEBUG", False)

    class Config:
        env_file = ".env"


settings = Settings()
