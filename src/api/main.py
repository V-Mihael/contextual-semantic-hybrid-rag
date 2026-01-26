"""FastAPI application for RAG system."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agno.agent import Agent
from agno.models.google import Gemini
from src.storage.contextual_agno_knowledge import ContextualAgnoKnowledge
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

kb: Optional[ContextualAgnoKnowledge] = None
agent: Optional[Agent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    global kb, agent
    kb = ContextualAgnoKnowledge()
    agent = Agent(
        model=Gemini(id="gemini-2.5-flash"),
        knowledge=kb.knowledge,
        search_knowledge=True,
        markdown=True,
        tools=[
            YFinanceTools(stock_price=True, analyst_recommendations=True),
            DuckDuckGoTools(),
        ],
    )
    yield
    # Cleanup if needed


app = FastAPI(title="RAG API", lifespan=lifespan)


class Query(BaseModel):
    """Query request model."""

    question: str
    max_results: Optional[int] = 5


@app.post("/query")
async def query(req: Query):
    """Query the knowledge base with LLM-powered response."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent loading...")

    response = agent.run(req.question)
    return {"response": response.content}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
