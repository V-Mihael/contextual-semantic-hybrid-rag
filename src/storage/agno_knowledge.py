"""Agno Knowledge Base with PgVector and semantic chunking."""
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.vectordb.pgvector import PgVector, SearchType
from agno.knowledge.embedder.google import GeminiEmbedder

from src.config import settings


class AgnoKnowledge:
    """Wrapper for Agno Knowledge with semantic chunking and hybrid search."""
    
    def __init__(self, table_name: str = "documents"):
        self.embedder = GeminiEmbedder(
            id=settings.embedding_model,
            api_key=settings.google_api_key
        )
        
        self.knowledge = Knowledge(
            vector_db=PgVector(
                table_name=table_name,
                db_url=settings.db_url,
                search_type=SearchType.hybrid,  # Vector + FTS
                embedder=self.embedder
            )
        )
        
        # Semantic chunking preserves context better than fixed-size
        self.pdf_reader = PDFReader(
            chunking_strategy=SemanticChunking(
                embedder=self.embedder,
                chunk_size=settings.chunk_size,
                similarity_threshold=0.5  # Keep related content together
            )
        )
    
    def ingest_pdf(self, path: str):
        """Ingest a single PDF file with semantic chunking."""
        self.knowledge.insert(path=path, reader=self.pdf_reader)
    
    def ingest_directory(self, path: str):
        """Ingest all PDFs in a directory with semantic chunking."""
        self.knowledge.insert(path=path, reader=self.pdf_reader)
    
    def search(self, query: str, limit: int = 5):
        """Hybrid search (vector + keyword)."""
        return self.knowledge.search(query=query, num_documents=limit)
