"""Agno Knowledge Base with PgVector and semantic chunking."""

from typing import Any

from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.pgvector import PgVector, SearchType
from chonkie.embeddings import OpenAIEmbeddings

from src.config import settings


class AgnoKnowledge:
    """Wrapper for Agno Knowledge with semantic chunking and hybrid search.

    This class provides a simplified interface for PDF ingestion and retrieval
    using semantic chunking and hybrid search (vector + full-text).

    Attributes:
        embedder: Gemini embedder for vector representations.
        knowledge: Agno Knowledge instance with PgVector backend.
        pdf_reader: PDF reader with semantic chunking strategy.
    """

    def __init__(self, table_name: str = "economics_docs_gemini") -> None:
        """Initialize Agno Knowledge Base.

        Args:
            table_name: PostgreSQL table name for document storage.
        """
        self.embedder = GeminiEmbedder(
            id=settings.embedding_model,
            api_key=settings.google_api_key,
            dimensions=768,
        )

        self.knowledge = Knowledge(
            vector_db=PgVector(
                table_name=table_name,
                db_url=settings.db_url,
                search_type=SearchType.hybrid,
                embedder=self.embedder,
            )
        )

        self.pdf_reader = PDFReader(
            chunking_strategy=SemanticChunking(
                embedder=OpenAIEmbeddings(model="text-embedding-3-small"),
                chunk_size=settings.chunk_size,
                similarity_threshold=0.5,
            )
        )

    def ingest_pdf(self, path: str) -> None:
        """Ingest a single PDF file with semantic chunking.

        Args:
            path: Path to the PDF file.
        """
        self.knowledge.insert(path=path, reader=self.pdf_reader)

    def ingest_directory(self, path: str) -> None:
        """Ingest all PDFs in a directory with semantic chunking.

        Args:
            path: Path to the directory containing PDF files.
        """
        self.knowledge.insert(path=path, reader=self.pdf_reader)

    def search(self, query: str, limit: int = 5) -> Any:
        """Perform hybrid search (vector + keyword).

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            Search results from the knowledge base.
        """
        return self.knowledge.search(query=query, max_results=limit)
