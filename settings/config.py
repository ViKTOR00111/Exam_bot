from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
import os


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(..., env="BOT_TOKEN")

    class Config:
        env_file = os.path.join(os.getcwd(), "venv", ".env")
        env_file_encoding = "utf-8"


config = Settings()
