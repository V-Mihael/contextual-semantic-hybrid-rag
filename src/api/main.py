from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import tempfile
from src.ingestion.loaders import DocumentLoader
from src.ingestion.chunking import Chunker
from src.ingestion.contextualizer import Contextualizer
from src.storage.supabase_knowledge import SupabaseKnowledge
from src.agents.research_agent import ResearchAgent

app = FastAPI(title="Contextual RAG API")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        text = DocumentLoader.load(tmp_path)
        chunker = Chunker()
        chunks = chunker.chunk(text)
        
        contextualizer = Contextualizer()
        kb = SupabaseKnowledge()
        
        doc_id = kb.add_document(title=file.filename, source=tmp_path)
        
        for i, chunk in enumerate(chunks):
            contextualized = contextualizer.contextualize_chunk(chunk, text[:1000])
            kb.add_chunk(doc_id, chunk, contextualized, i)
        
        return {"status": "success", "document_id": doc_id, "chunks": len(chunks)}
    finally:
        Path(tmp_path).unlink()

@app.post("/query")
async def query(request: QueryRequest):
    agent = ResearchAgent()
    result = agent.query(request.question, top_k=request.top_k)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
