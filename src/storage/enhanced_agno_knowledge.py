"""Enhanced Agno Knowledge with contextual semantic chunking."""
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.pgvector import PgVector, SearchType
from agno.knowledge.embedder.google import GeminiEmbedder
from chonkie.embeddings import OpenAIEmbeddings # for semantic chunking

from src.config import settings
from src.ingestion.contextual_semantic_chunking import ContextualSemanticChunking


class EnhancedAgnoKnowledge:
    """
    Knowledge base with context-enhanced semantic chunking.
    
    Combines:
    - Semantic chunking (natural boundaries)
    - LLM contextual enhancement (situating context)
    - Hybrid search (vector + FTS)
    """
    
    def __init__(self, table_name: str = "documents_enhanced"):
        self.embedder = GeminiEmbedder(
            id=settings.embedding_model,
            api_key=settings.google_api_key
        )
        
        self.knowledge = Knowledge(
            vector_db=PgVector(
                table_name=table_name,
                db_url=settings.db_url,
                search_type=SearchType.hybrid,
                embedder=self.embedder
            )
        )
        
        # Context-enhanced semantic chunking
        self.pdf_reader = PDFReader(
            chunking_strategy=ContextualSemanticChunking(
                embedder=OpenAIEmbeddings(model="text-embedding-3-small"),
                chunk_size=settings.chunk_size,
                similarity_threshold=0.5
            )
        )
    
    def ingest_pdf(self, path: str):
        """Ingest PDF with contextual semantic chunking."""
        print(f"📄 Ingesting with context-enhanced semantic chunking: {path}")
        self.knowledge.insert(path=path, reader=self.pdf_reader)
    
    def ingest_directory(self, path: str):
        """Ingest directory with contextual semantic chunking."""
        print(f"📚 Ingesting directory with context-enhanced semantic chunking: {path}")
        self.knowledge.insert(path=path, reader=self.pdf_reader)
    
    def search(self, query: str, limit: int = 5):
        """Hybrid search with contextually enhanced chunks."""
        return self.knowledge.search(query=query, num_documents=limit)
