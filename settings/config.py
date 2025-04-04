from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field
import os


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(..., env="BOT_TOKEN")

    LOG_FILEPATH: str = Field(default="logs/app_log.log", env="LOG_FILEPATH")
    LOG_ROTATION: int = Field(default=1, env="LOG_ROTATION")
    LOG_RETENTION: int = Field(default=30, env="LOG_RETENTION")

    FILE_BOOK_MAPINGS: str = Field("book_mappings.json", env="FILE_BOOK_MAPINGS")
    TASKS_FOLDER: str = Field("task_images", env="TASKS_FOLDER")

    class Config:
        env_file = os.path.join(os.getcwd(), "venv", ".env")
        env_file_encoding = "utf-8"


config = Settings()
