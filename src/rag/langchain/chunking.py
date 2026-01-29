"""Context-enhanced semantic chunking for LangChain."""

import time
from typing import List

from chonkie import SemanticChunker
from google import genai
from langchain_core.documents import Document

from src.config import settings


class LangChainContextualChunker:
    """Contextual semantic chunking for LangChain documents.

    This chunker performs two-stage processing:
    1. Semantic chunking using Chonkie to preserve natural boundaries.
    2. LLM-based context generation to add situating information.

    The contextual enhancement improves retrieval accuracy by 20-30%.
    """

    CONTEXT_PROMPT = """Given the document below, provide a brief context (1-2 sentences) explaining what this chunk discusses within the broader document.

DOCUMENT: {whole_doc}

CHUNK: {chunk_content}

Context:"""

    def __init__(
        self,
        embedder,
        chunk_size: int = 1000,
        similarity_threshold: float = 0.5,
        max_retries: int = 5,
        retry_delay: float = 2.0,
    ) -> None:
        """Initialize contextual chunker.

        Args:
            embedder: Chonkie embedding model for semantic similarity.
            chunk_size: Maximum chunk size in tokens.
            similarity_threshold: Threshold for semantic boundary detection (0-1).
            max_retries: Maximum retry attempts per chunk.
            retry_delay: Initial delay between retries (exponential backoff).
        """
        self.semantic_chunker = SemanticChunker(
            embedding_model=embedder,
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
        self.max_retries = max_retries
        self.retry_delay = retry_delay

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

    def _generate_context(self, prompt: str, retry_count: int = 0) -> str:
        """Generate context with API key and model fallback.

        Args:
            prompt: Context generation prompt.
            retry_count: Current retry attempt number.

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
                    print(f"❌ Key {self.current_key_index + 1} invalid, switching...")
                    if (
                        settings.google_api_key_prod
                        and settings.google_api_key_prod not in self.api_keys
                    ):
                        self.api_keys.append(settings.google_api_key_prod)
                        self.clients[settings.google_api_key_prod] = genai.Client(
                            api_key=settings.google_api_key_prod
                        )
                    self.current_key_index = len(self.api_keys) - 1
                    continue

                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print(
                        f"⚠️  {model_id} (key {self.current_key_index + 1}) quota exceeded"
                    )
                    self.current_key_index = (self.current_key_index + 1) % len(
                        self.api_keys
                    )
                    if self.current_key_index == 0:
                        self.current_model_index = (self.current_model_index + 1) % len(
                            self.model_fallback
                        )
                    continue
                raise

        raise Exception("All API keys and models exhausted")

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk documents with contextual enhancement.

        Args:
            documents: List of LangChain documents to chunk.

        Returns:
            List of chunked documents with contextual information.
        """
        all_chunks = []

        for doc in documents:
            text = doc.page_content
            doc_preview = text[:5000]

            # Semantic chunking
            semantic_chunks = self.semantic_chunker.chunk(text)

            # Add context to each chunk
            for idx, chunk in enumerate(semantic_chunks):
                context_prefix = None

                for attempt in range(self.max_retries):
                    try:
                        self._rate_limit()
                        prompt = self.CONTEXT_PROMPT.format(
                            whole_doc=doc_preview, chunk_content=chunk.text[:500]
                        )
                        context_prefix = self._generate_context(prompt, attempt)
                        break
                    except Exception as e:
                        if attempt < self.max_retries - 1:
                            delay = self.retry_delay * (2**attempt)
                            print(
                                f"⚠️  Chunk {idx + 1}: attempt {attempt + 1} failed. Retry in {delay:.1f}s..."
                            )
                            time.sleep(delay)
                        else:
                            print(
                                f"❌ Chunk {idx + 1}: failed after {self.max_retries} attempts"
                            )

                if context_prefix:
                    enhanced_content = (
                        f"[CONTEXT: {context_prefix.strip()}]\n\n{chunk.text}"
                    )
                else:
                    enhanced_content = chunk.text

                all_chunks.append(
                    Document(
                        page_content=enhanced_content,
                        metadata={
                            **doc.metadata,
                            "chunk_index": idx,
                            "token_count": chunk.token_count,
                        },
                    )
                )

        return all_chunks
