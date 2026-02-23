import os

from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_db_url() -> str:
    # Vercel file system is ephemeral; /tmp is writable at runtime.
    if os.getenv("VERCEL"):
        return "sqlite:////tmp/aura.db"
    return "sqlite:///./aura.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_url: str = _default_db_url()
    zero_shot_model: str = "facebook/bart-large-mnli"
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    topk: int = 3


settings = Settings()

