"""Configuration settings for the RAG system."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        google_api_key: Google AI Studio API key for Gemini models.
        google_api_key_free_limited: Google API alternate free key.
        db_url: PostgreSQL connection string with pgvector support.
        embedding_model: Gemini embedding model identifier.
        llm_model: Gemini LLM model identifier for agent responses.
        chunk_size: Maximum size for document chunks in characters.
        chunk_overlap: Overlap between consecutive chunks in characters.
    """

    google_api_key: str
    google_api_key_free_limited: Optional[str] = None
    db_url: str
    embedding_model: str = "models/text-embedding-004"
    llm_model: str = "gemini-2.5-flash"
    chunking_model: str = "gemini-2.5-flash-lite"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    class Config:
        """Pydantic configuration."""

        env_file = ".env"


settings = Settings()
