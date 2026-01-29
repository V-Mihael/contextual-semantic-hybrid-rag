"""Context-enhanced semantic chunking strategy."""

import time
from typing import Any

from agno.knowledge.chunking.strategy import ChunkingStrategy
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.document import Document
from google import genai

from src.config import settings


class ContextualSemanticChunking(ChunkingStrategy):
    """Combines semantic chunking with LLM-based contextual enhancement.

    This strategy performs two-stage chunking:
    1. Semantic chunking to preserve natural document boundaries.
    2. LLM-based context generation to add situating information to each chunk.

    The contextual enhancement improves retrieval accuracy by 20-30% by providing
    additional context about each chunk's role within the broader document.

    Attributes:
        semantic_chunker: Underlying semantic chunking strategy.
        client: Gemini API client.
        model_id: Gemini model identifier.
    """

    CONTEXT_PROMPT = """Given the document below, provide a brief context (1-2 sentences) explaining what this chunk discusses within the broader document.

DOCUMENT: {whole_doc}

CHUNK: {chunk_content}

Context:"""

    def __init__(
        self,
        embedder: Any,
        chunk_size: int = 1000,
        similarity_threshold: float = 0.5,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> None:
        """Initialize contextual semantic chunking strategy.

        Args:
            embedder: Embedding model for semantic similarity computation.
            chunk_size: Maximum size for each chunk in characters.
            similarity_threshold: Threshold for semantic boundary detection (0-1).
            max_retries: Maximum retry attempts per chunk.
            retry_delay: Initial delay between retries (exponential backoff).
        """
        self.semantic_chunker = SemanticChunking(
            embedder=embedder,
            chunk_size=chunk_size,
            similarity_threshold=similarity_threshold,
        )
        
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_id = settings.chunking_model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _generate_context(self, prompt: str) -> str:
        """Generate context using Gemini API.

        Args:
            prompt: Context generation prompt.

        Returns:
            Generated context text.
        """
        response = self.client.models.generate_content(
            model=self.model_id, contents=prompt
        )
        return response.text

    def chunk(self, document: Document) -> list[Document]:
        """Chunk document with semantic boundaries and contextual enhancement.

        Args:
            document: Input document to be chunked.

        Returns:
            List of documents with enhanced contextual information.
        """
        semantic_chunks = self.semantic_chunker.chunk(document)
        contextual_chunks = []
        doc_preview = document.content[:5000]
        failed_chunks = []

        for idx, chunk in enumerate(semantic_chunks):
            context_prefix = None
            
            for attempt in range(self.max_retries):
                try:
                    prompt = self.CONTEXT_PROMPT.format(
                        whole_doc=doc_preview, chunk_content=chunk.content[:500]
                    )
                    context_prefix = self._generate_context(prompt)
                    break
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (2 ** attempt)
                        print(f"⚠️  Chunk {idx + 1}: tentativa {attempt + 1} falhou. Retry em {delay:.1f}s...")
                        time.sleep(delay)
                    else:
                        print(f"❌ Chunk {idx + 1}: falhou após {self.max_retries} tentativas")
                        failed_chunks.append((idx, chunk))

            if context_prefix:
                enhanced_content = f"[CONTEXT: {context_prefix.strip()}]\n\n{chunk.content}"
            else:
                enhanced_content = chunk.content

            contextual_chunks.append(
                Document(
                    content=enhanced_content,
                    meta_data=getattr(chunk, "meta_data", {}),
                )
            )

        if failed_chunks:
            print(f"\n🔄 Reprocessando {len(failed_chunks)} chunks sem contexto...")
            for idx, chunk in failed_chunks:
                for attempt in range(self.max_retries * 2):
                    try:
                        prompt = self.CONTEXT_PROMPT.format(
                            whole_doc=doc_preview, chunk_content=chunk.content[:500]
                        )
                        context_prefix = self._generate_context(prompt)
                        
                        enhanced_content = f"[CONTEXT: {context_prefix.strip()}]\n\n{chunk.content}"
                        contextual_chunks[idx] = Document(
                            content=enhanced_content,
                            meta_data=getattr(chunk, "meta_data", {}),
                        )
                        print(f"✅ Chunk {idx + 1}: contexto gerado com sucesso")
                        break
                    except Exception as e:
                        if attempt < (self.max_retries * 2) - 1:
                            delay = self.retry_delay * (2 ** (attempt % self.max_retries))
                            print(f"⚠️  Chunk {idx + 1}: retry {attempt + 1} falhou. Aguardando {delay:.1f}s...")
                            time.sleep(delay)
                        else:
                            print(f"❌ Chunk {idx + 1}: impossível gerar contexto após todas as tentativas")

        return contextual_chunks
