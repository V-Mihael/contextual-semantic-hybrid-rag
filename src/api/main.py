"""FastAPI application for RAG system."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from agno.agent import Agent
from agno.models.google import Gemini
from src.rag.agno import ContextualAgnoKnowledgeBase
from agno.tools.yfinance import YFinanceTools
from agno.tools.tavily import TavilyTools
from src.integrations.whatsapp import WhatsAppClient
from src.config import settings

kb: Optional[ContextualAgnoKnowledgeBase] = None
agent: Optional[Agent] = None
whatsapp_client: Optional[WhatsAppClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    global kb, agent, whatsapp_client
    kb = ContextualAgnoKnowledgeBase()
    
    tools = [YFinanceTools()]
    if settings.tavily_api_key:
        tools.append(TavilyTools(api_key=settings.tavily_api_key))
    
    agent = Agent(
        model=Gemini(id="gemini-2.5-flash", api_key=settings.google_api_key),
        knowledge=kb.knowledge,
        search_knowledge=True,
        markdown=True,
        tools=tools,
    )
    whatsapp_client = WhatsAppClient()
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
    return {
        "response": response.content,
        "tools_used": [m.tool_name for m in response.messages if hasattr(m, 'tool_name')]
    }


@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verify WhatsApp webhook."""
    verify_token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if verify_token == whatsapp_client.verify_token:
        return int(challenge)
    return {"error": "Invalid token"}, 403


@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming WhatsApp messages."""
    data = await request.json()
    parsed = whatsapp_client.parse_webhook(data)
    
    if not parsed:
        return {"status": "ok"}
    
    phone = parsed["phone"]
    message = parsed["message"]
    
    response = agent.run(message)
    whatsapp_client.send_message(phone, response.content)
    
    return {"status": "ok"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
