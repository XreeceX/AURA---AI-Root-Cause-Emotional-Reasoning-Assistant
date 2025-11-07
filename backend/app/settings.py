from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:///./aura.db"
    zero_shot_model: str = "facebook/bart-large-mnli"
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    topk: int = 3

    class Config:
        env_file = ".env"


settings = Settings()

