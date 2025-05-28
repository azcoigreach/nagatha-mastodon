from pydantic_settings import BaseSettings
from pydantic import Field
from datetime import datetime
from uuid import uuid4

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    INSTANCE_ID: str = Field(default_factory=lambda: str(uuid4()))
    START_TIME: datetime = Field(default_factory=datetime.utcnow)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    USE_LLM_ACTIVITY: bool = False
    MASTODON_ACCESS_TOKEN: str = ""
    MASTODON_API_BASE: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()