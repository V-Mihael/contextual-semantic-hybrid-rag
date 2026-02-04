"""Simple semantic chunking without contextual enhancement."""

from agno.knowledge.chunking.strategy import ChunkingStrategy
from agno.knowledge.document import Document
from chonkie import SemanticChunker

from src.config import settings


class SimpleSemanticChunking(ChunkingStrategy):
    """Semantic chunking using Chonkie without contextual enhancement."""

    def __init__(
        self,
        chunk_size: int = 1000,
        similarity_threshold: float = 0.5,
    ) -> None:
        """Initialize simple semantic chunking strategy.

        Args:
            chunk_size: Maximum size for each chunk in characters.
            similarity_threshold: Threshold for semantic boundary detection (0-1).
        """
        self.semantic_chunker = SemanticChunker(
            embedding_model=settings.semantic_chunking_model,
            chunk_size=chunk_size,
            threshold=similarity_threshold,
            api_key=settings.openai_api_key,
        )

    def chunk(self, document: Document) -> list[Document]:
        """Chunk document with semantic boundaries.

        Args:
            document: Input document to be chunked.

        Returns:
            List of semantically chunked documents.
        """
        chonkie_chunks = self.semantic_chunker.chunk(document.content)

        return [
            Document(
                content=chunk.text,
                meta_data=getattr(document, "meta_data", {}),
            )
            for chunk in chonkie_chunks
        ]
