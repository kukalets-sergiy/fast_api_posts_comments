from dotenv import load_dotenv
import os
from pydantic import BaseSettings

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
API_KEY = os.getenv("API_KEY")


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    api_key: str

    class Config:
        env_file = ".env"


settings = Settings()

