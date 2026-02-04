"""Configuration settings for the RAG system."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        google_api_key: Google AI Studio API key for Gemini models.
        openai_api_key: OpenAI API key for semantic chunking embeddings.
        tavily_api_key: Tavily API key for web search.
        groq_api_key: Groq API key for Whisper transcription (free tier).
        db_url: PostgreSQL connection string with pgvector support.
        embedding_model: Gemini embedding model identifier for final embeddings.
        llm_model: Gemini LLM model identifier for agent responses.
        semantic_chunking_model: OpenAI embedding model for semantic chunking.
        context_generation_model: Gemini model for contextual enhancement.
        chunk_size: Maximum size for document chunks in characters.
        chunk_overlap: Overlap between consecutive chunks in characters.
    """

    google_api_key: str
    openai_api_key: str
    google_api_key_free_limited: Optional[str] = None
    tavily_api_key: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    groq_api_key: Optional[str] = None
    render_external_url: Optional[str] = None
    db_url: str
    embedding_model: str = "models/text-embedding-004"
    llm_model: str = "gemini-2.5-flash"
    semantic_chunking_model: str = "text-embedding-3-small"
    context_generation_model: str = "gemini-2.5-flash-lite"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        extra = "ignore"


settings = Settings()
