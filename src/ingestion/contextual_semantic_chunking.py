"""Context-enhanced semantic chunking strategy."""
from agno.knowledge.chunking.strategy import ChunkingStrategy
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.document import Document
from google import genai

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
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_id = settings.llm_model
    
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
                
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                context_prefix = response.text
                enhanced_content = f"[CONTEXT: {context_prefix.strip()}]\n\n{chunk.content}"
                
                contextual_chunks.append(
                    Document(
                        content=enhanced_content,
                        meta_data=getattr(chunk, 'meta_data', {})
                    )
                )
            except Exception as e:
                print(f"Warning: Context generation failed: {e}")
                contextual_chunks.append(chunk)
        
        return contextual_chunks
