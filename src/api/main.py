"""FastAPI application for RAG system."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.agents import create_rag_agent

agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    global agent
    agent = create_rag_agent()
    yield


app = FastAPI(title="RAG API", lifespan=lifespan)


class Query(BaseModel):
    """Query request model."""

    question: str
    session_id: Optional[str] = None
    max_results: Optional[int] = 5


@app.post("/query")
async def query(req: Query):
    """Query the knowledge base with LLM-powered response."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent loading...")

    response = agent.run(req.question, session_id=req.session_id or "default")
    return {
        "response": response.content,
        "tools_used": [m.tool_name for m in response.messages if hasattr(m, 'tool_name')]
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
