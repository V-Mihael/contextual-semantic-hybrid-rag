"""Enhanced Agno Knowledge with contextual semantic chunking."""

from typing import Any

from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.pgvector import PgVector, SearchType
from chonkie.embeddings import OpenAIEmbeddings

from src.config import settings
from src.ingestion.contextual_semantic_chunking import ContextualSemanticChunking


class EnhancedAgnoKnowledge:
    """Knowledge base with context-enhanced semantic chunking.

    This class combines three advanced techniques for improved retrieval:
    - Semantic chunking: Preserves natural document boundaries.
    - LLM contextual enhancement: Adds situating context to each chunk.
    - Hybrid search: Combines vector similarity and full-text search.

    Attributes:
        embedder: Gemini embedder for vector representations.
        knowledge: Agno Knowledge instance with PgVector backend.
        pdf_reader: PDF reader with contextual semantic chunking strategy.
    """

    def __init__(self, table_name: str = "documents_enhanced") -> None:
        """Initialize Enhanced Knowledge Base.

        Args:
            table_name: PostgreSQL table name for document storage.
        """
        self.embedder = GeminiEmbedder(
            id=settings.embedding_model, api_key=settings.google_api_key
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
            chunking_strategy=ContextualSemanticChunking(
                embedder=OpenAIEmbeddings(model="text-embedding-3-small"),
                chunk_size=settings.chunk_size,
                similarity_threshold=0.5,
            )
        )

    def ingest_pdf(self, path: str) -> None:
        """Ingest PDF with contextual semantic chunking.

        Args:
            path: Path to the PDF file.
        """
        print(f"📄 Ingesting with context-enhanced semantic chunking: {path}")
        self.knowledge.insert(path=path, reader=self.pdf_reader)

    def ingest_directory(self, path: str) -> None:
        """Ingest directory with contextual semantic chunking.

        Args:
            path: Path to the directory containing PDF files.
        """
        print(
            f"📚 Ingesting directory with context-enhanced semantic chunking: {path}"
        )
        self.knowledge.insert(path=path, reader=self.pdf_reader)

    def search(self, query: str, limit: int = 5) -> Any:
        """Perform hybrid search with contextually enhanced chunks.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            Search results from the knowledge base.
        """
        return self.knowledge.search(query=query, num_documents=limit)
