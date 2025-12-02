from openai import OpenAI
from src.config import settings
from src.supabase_client import get_supabase_client

class SupabaseKnowledge:
    def __init__(self):
        self.client = get_supabase_client()
        self.openai = OpenAI(api_key=settings.openai_api_key)
    
    def create_embedding(self, text: str) -> list[float]:
        response = self.openai.embeddings.create(
            model=settings.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def add_document(self, title: str, source: str, metadata: dict = None) -> str:
        result = self.client.table("documents").insert({
            "title": title,
            "source": source,
            "metadata": metadata or {}
        }).execute()
        return result.data[0]["id"]
    
    def add_chunk(self, document_id: str, content: str, contextualized_content: str, 
                  chunk_index: int, metadata: dict = None):
        embedding = self.create_embedding(contextualized_content)
        self.client.table("chunks").insert({
            "document_id": document_id,
            "content": content,
            "contextualized_content": contextualized_content,
            "embedding": embedding,
            "chunk_index": chunk_index,
            "metadata": metadata or {}
        }).execute()
    
    def hybrid_search(self, query: str, limit: int = 10, vector_weight: float = 0.5) -> list[dict]:
        query_embedding = self.create_embedding(query)
        result = self.client.rpc("hybrid_search", {
            "query_embedding": query_embedding,
            "query_text": query,
            "match_count": limit,
            "vector_weight": vector_weight
        }).execute()
        return result.data
