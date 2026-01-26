"""FastAPI application for RAG system."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.storage.contextual_agno_knowledge import ContextualAgnoKnowledge

app = FastAPI(title="RAG API")

kb: Optional[ContextualAgnoKnowledge] = None


@app.on_event("startup")
async def startup():
    """Initialize knowledge base on startup."""
    global kb
    kb = ContextualAgnoKnowledge()


class Query(BaseModel):
    """Query request model."""
    question: str
    max_results: Optional[int] = 5


@app.post("/query")
async def query(req: Query):
    """Query the knowledge base."""
    if not kb:
        raise HTTPException(status_code=503, detail="Knowledge base loading...")
    
    results = kb.search(query=req.question, limit=req.max_results)
    return {"response": results}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
