from agno import Agent
from src.retrieval.hybrid_search import HybridSearchRetriever
from src.retrieval.reranker import Reranker
from src.config import settings

class ResearchAgent:
    def __init__(self):
        self.retriever = HybridSearchRetriever()
        self.reranker = Reranker()
        self.agent = Agent(
            model=settings.llm_model,
            instructions="You are a research assistant. Answer questions based on the provided context.",
        )
    
    def query(self, question: str, top_k: int = 5) -> dict:
        # Hybrid search
        chunks = self.retriever.retrieve(question, top_k=10)
        
        # Rerank
        reranked_chunks = self.reranker.rerank(question, chunks, top_k=top_k)
        
        # Build context
        context = "\n\n".join([
            f"[{i+1}] {chunk.get('contextualized_content') or chunk.get('content', '')}"
            for i, chunk in enumerate(reranked_chunks)
        ])
        
        # Generate answer
        prompt = f"""Context:
{context}

Question: {question}

Answer based on the context above. If the answer is not in the context, say so."""
        
        response = self.agent.run(prompt)
        
        return {
            "answer": response.content,
            "sources": reranked_chunks,
            "num_sources": len(reranked_chunks)
        }
