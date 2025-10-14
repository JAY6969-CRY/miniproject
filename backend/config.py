from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str = "demo"
    NEWS_API_KEY: str = ""  # Get from https://newsapi.org/
    GEMINI_API_KEY: str = ""  # Get from https://ai.google.dev/
    CACHE_DB_PATH: str = "cache.db"
    MODEL_DIR: str = "./models"
    
    class Config:
        env_file = ".env"

settings = Settings()
