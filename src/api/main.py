"""FastAPI application for RAG system."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from telegram import Update

from src.agents import create_rag_agent
from src.integrations.telegram import TelegramBot
from src.config import settings
from src.logger import logger

agent = None
telegram_bot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    global agent, telegram_bot
    agent = create_rag_agent()
    
    # Initialize Telegram bot with webhook only if RENDER_EXTERNAL_URL is set
    telegram_token = getattr(settings, 'telegram_bot_token', None)
    if telegram_token and settings.render_external_url:
        telegram_bot = TelegramBot(token=telegram_token, agent=agent)
        webhook_url = f"{settings.render_external_url}/telegram"
        await telegram_bot.set_webhook(webhook_url)
        logger.info(f"Telegram webhook mode enabled: {webhook_url}")
    
    yield


app = FastAPI(title="RAG API", lifespan=lifespan)


class Query(BaseModel):
    """Query request model."""

    question: str
    session_id: Optional[str] = None
    max_results: Optional[int] = 5


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "service": "RAG API"}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook updates."""
    if not telegram_bot:
        raise HTTPException(status_code=503, detail="Telegram bot not initialized")
    
    data = await request.json()
    update = Update.de_json(data, telegram_bot.app.bot)
    await telegram_bot.app.process_update(update)
    return {"ok": True}


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
