"""LangChain-based Knowledge with contextual semantic chunking."""

from typing import Any, List

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from src.config import settings
from src.rag.langchain.chunking import LangChainContextualChunker


class ContextualLangChainKnowledgeBase:
    """LangChain-based knowledge base with context-enhanced semantic chunking.

    This class combines three advanced techniques for improved retrieval:
    - Semantic chunking: Preserves natural document boundaries.
    - LLM contextual enhancement: Adds situating context to each chunk.
    - Hybrid search: Combines vector similarity and full-text search.

    Attributes:
        embeddings: Google Gemini embeddings for vector representations.
        vectorstore: PGVector vectorstore instance.
        chunker: Contextual semantic chunker.
    """

    def __init__(self, collection_name: str = "economics_enhanced_langchain") -> None:
        """Initialize LangChain Knowledge Base.

        Args:
            collection_name: PostgreSQL collection name for document storage.
        """
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )

        self.chunker = LangChainContextualChunker(
            embedder=self.embeddings,
            chunk_size=settings.chunk_size,
            similarity_threshold=0.5,
        )

        self.vectorstore = PGVector(
            collection_name=collection_name,
            connection_string=settings.db_url,
            embedding_function=self.embeddings,
        )

    def ingest_pdf(self, path: str) -> None:
        """Ingest PDF with contextual semantic chunking.

        Args:
            path: Path to the PDF file.
        """
        print(f"📄 Ingesting with context-enhanced semantic chunking: {path}")
        loader = PyPDFLoader(path)
        documents = loader.load()
        chunked_docs = self.chunker.chunk_documents(documents)
        self.vectorstore.add_documents(chunked_docs)
        print(f"✅ Ingested {len(chunked_docs)} chunks from {path}")

    def ingest_directory(self, path: str) -> None:
        """Ingest directory with contextual semantic chunking.

        Args:
            path: Path to the directory containing PDF files.
        """
        from pathlib import Path

        print(
            f"📚 Ingesting directory with context-enhanced semantic chunking: {path}"
        )
        pdf_files = list(Path(path).glob("*.pdf"))
        for pdf_file in pdf_files:
            self.ingest_pdf(str(pdf_file))

    def search(self, query: str, limit: int = 5) -> List[Document]:
        """Perform similarity search with contextually enhanced chunks.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            List of relevant documents.
        """
        return self.vectorstore.similarity_search(query, k=limit)

    def search_with_score(self, query: str, limit: int = 5) -> List[tuple[Document, float]]:
        """Perform similarity search with relevance scores.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            List of tuples containing documents and their relevance scores.
        """
        return self.vectorstore.similarity_search_with_score(query, k=limit)

    def as_retriever(self, **kwargs: Any):
        """Return a LangChain retriever interface.

        Args:
            **kwargs: Additional arguments for the retriever.

        Returns:
            LangChain retriever instance.
        """
        return self.vectorstore.as_retriever(**kwargs)
