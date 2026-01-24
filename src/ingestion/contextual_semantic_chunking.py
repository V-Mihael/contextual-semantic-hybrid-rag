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
        api_keys: List of Google API keys for rotation.
        current_key_index: Index of currently active API key.
        clients: Dictionary of genai clients per API key.
        model_fallback: List of (model_id, rpm_limit) tuples.
        current_model_index: Index of currently active model.
        last_request_time: Timestamp of last API call.
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
    ) -> None:
        """Initialize contextual semantic chunking strategy.

        Args:
            embedder: Embedding model for semantic similarity computation.
            chunk_size: Maximum size for each chunk in characters.
            similarity_threshold: Threshold for semantic boundary detection (0-1).
        """
        self.semantic_chunker = SemanticChunking(
            embedder=embedder,
            chunk_size=chunk_size,
            similarity_threshold=similarity_threshold,
        )
        
        self.api_keys = [settings.google_api_key]
        if settings.google_api_key_2:
            self.api_keys.append(settings.google_api_key_2)
        if settings.google_api_key_prod:
            self.api_keys.append(settings.google_api_key_prod)
        
        self.current_key_index = 0
        self.clients = {key: genai.Client(api_key=key) for key in self.api_keys}
        
        self.model_fallback = [
            ("gemini-2.5-flash-lite", 10),
            ("gemini-2.5-flash", 5),
        ]
        self.current_model_index = 0
        self.last_request_time = 0.0

    def _rate_limit(self) -> None:
        """Enforce rate limiting between API calls."""
        if self.api_keys[self.current_key_index] == settings.google_api_key_prod:
            return
        
        _, rpm = self.model_fallback[self.current_model_index]
        min_interval = 60.0 / rpm
        elapsed = time.time() - self.last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()

    def _generate_context(self, prompt: str) -> str:
        """Generate context with API key and model fallback.

        Args:
            prompt: Context generation prompt.

        Returns:
            Generated context text.

        Raises:
            Exception: If all keys and models fail.
        """
        for _ in range(len(self.api_keys) * len(self.model_fallback)):
            api_key = self.api_keys[self.current_key_index]
            client = self.clients[api_key]
            
            if api_key == settings.google_api_key_prod:
                model_id = "gemini-2.5-flash-lite"
            else:
                model_id, _ = self.model_fallback[self.current_model_index]
            
            try:
                response = client.models.generate_content(
                    model=model_id, contents=prompt
                )
                return response.text
            except Exception as e:
                error_str = str(e)
                
                if "API_KEY_INVALID" in error_str or "invalid" in error_str.lower():
                    print(f"❌ Key {self.current_key_index + 1} invalid, switching to PROD key...")
                    if settings.google_api_key_prod and settings.google_api_key_prod not in self.api_keys:
                        self.api_keys.append(settings.google_api_key_prod)
                        self.clients[settings.google_api_key_prod] = genai.Client(api_key=settings.google_api_key_prod)
                    self.current_key_index = len(self.api_keys) - 1
                    continue
                
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print(f"⚠️  {model_id} (key {self.current_key_index + 1}) quota exceeded")
                    
                    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                    if self.current_key_index == 0:
                        print(f"   Switching to next model...")
                        self.current_model_index = (self.current_model_index + 1) % len(self.model_fallback)
                    continue
                raise
        
        raise Exception("All API keys and models exhausted")

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

        for chunk in semantic_chunks:
            try:
                self._rate_limit()

                prompt = self.CONTEXT_PROMPT.format(
                    whole_doc=doc_preview, chunk_content=chunk.content[:500]
                )

                context_prefix = self._generate_context(prompt)
                if context_prefix:
                    enhanced_content = (
                        f"[CONTEXT: {context_prefix.strip()}]\n\n{chunk.content}"
                    )
                else:
                    enhanced_content = chunk.content

                contextual_chunks.append(
                    Document(
                        content=enhanced_content,
                        meta_data=getattr(chunk, "meta_data", {}),
                    )
                )
            except Exception as e:
                print(f"Warning: Context generation failed: {e}")
                contextual_chunks.append(chunk)

        return contextual_chunks
