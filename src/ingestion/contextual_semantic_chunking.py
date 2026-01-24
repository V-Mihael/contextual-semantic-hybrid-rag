"""Context-enhanced semantic chunking strategy."""
from agno.knowledge.chunking.base import ChunkingStrategy
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.document import Document
from agno.models.google import Gemini

from src.config import settings


class ContextualSemanticChunking(ChunkingStrategy):
    """
    Combines semantic chunking with LLM-based contextual enhancement.
    
    1. Semantic chunking preserves natural boundaries
    2. LLM adds situating context to each chunk
    """
    
    CONTEXT_PROMPT = """Given the document below, provide a brief context (1-2 sentences) explaining what this chunk discusses within the broader document.

DOCUMENT: {whole_doc}

CHUNK: {chunk_content}

Context:"""
    
    def __init__(
        self, 
        embedder,
        chunk_size: int = 1000,
        similarity_threshold: float = 0.5
    ):
        self.semantic_chunker = SemanticChunking(
            embedder=embedder,
            chunk_size=chunk_size,
            similarity_threshold=similarity_threshold
        )
        self.llm = Gemini(id=settings.llm_model, api_key=settings.google_api_key)
    
    def chunk(self, document: Document) -> list[Document]:
        """Chunk document with semantic boundaries and contextual enhancement."""
        semantic_chunks = self.semantic_chunker.chunk(document)
        contextual_chunks = []
        doc_preview = document.content[:1000]
        
        for chunk in semantic_chunks:
            try:
                prompt = self.CONTEXT_PROMPT.format(
                    whole_doc=doc_preview,
                    chunk_content=chunk.content[:500]
                )
                
                response = self.llm.response(prompt)
                context_prefix = response.content.strip()
                enhanced_content = f"[CONTEXT: {context_prefix}]\n\n{chunk.content}"
                
                contextual_chunks.append(
                    Document(
                        content=enhanced_content,
                        metadata=chunk.metadata
                    )
                )
            except Exception as e:
                print(f"Warning: Context generation failed: {e}")
                contextual_chunks.append(chunk)
        
        return contextual_chunks
