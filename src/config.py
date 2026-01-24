from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str
    db_url: str  # PostgreSQL connection string for PgVector
    embedding_model: str = "models/text-embedding-004"
    llm_model: str = "gemini-2.0-flash-exp"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"

settings = Settings()
