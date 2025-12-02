from openai import OpenAI
from src.config import settings

class Contextualizer:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def contextualize_chunk(self, chunk: str, document_context: str) -> str:
        prompt = f"""<document>
{document_context}
</document>

Provide a concise context (2-3 sentences) for the following chunk to improve retrieval. Include key entities, topics, and relationships.

<chunk>
{chunk}
</chunk>

Context:"""
        
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=150
        )
        
        context = response.choices[0].message.content.strip()
        return f"{context}\n\n{chunk}"
