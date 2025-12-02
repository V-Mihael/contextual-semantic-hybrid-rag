from src.storage.supabase_knowledge import SupabaseKnowledge

class HybridSearchRetriever:
    def __init__(self, vector_weight: float = 0.5):
        self.kb = SupabaseKnowledge()
        self.vector_weight = vector_weight
    
    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        results = self.kb.hybrid_search(
            query=query,
            limit=top_k,
            vector_weight=self.vector_weight
        )
        return results
