from openai import OpenAI
from src.config import settings

class Reranker:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def rerank(self, query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
        if not chunks:
            return []
        
        prompt = f"""Query: {query}

Rank the following passages by relevance (1=most relevant). Return only numbers separated by commas.

"""
        for i, chunk in enumerate(chunks, 1):
            content = chunk.get("contextualized_content") or chunk.get("content", "")
            prompt += f"{i}. {content[:300]}...\n\n"
        
        prompt += "Rankings (comma-separated):"
        
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=50
        )
        
        rankings_text = response.choices[0].message.content.strip()
        try:
            rankings = [int(x.strip()) - 1 for x in rankings_text.split(",")]
            reranked = [chunks[i] for i in rankings if i < len(chunks)]
            return reranked[:top_k]
        except:
            return chunks[:top_k]
