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
    
    logger.info("Starting FastAPI application initialization")
    
    try:
        agent = create_rag_agent()
        logger.info("Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise
    
    # Initialize Telegram bot with webhook only if RENDER_EXTERNAL_URL is set
    telegram_token = getattr(settings, 'telegram_bot_token', None)
    render_url = getattr(settings, 'render_external_url', None)
    
    if telegram_token and render_url:
        try:
            telegram_bot = TelegramBot(token=telegram_token, agent=agent)
            await telegram_bot.initialize()  # Initialize for webhook mode
            webhook_url = f"{render_url}/telegram"
            await telegram_bot.set_webhook(webhook_url)
            logger.info(f"Telegram webhook mode enabled: {webhook_url}")
        except Exception as e:
            logger.error(f"Failed to initialize Telegram webhook: {e}")
            # Don't raise - allow API to work without Telegram
    elif telegram_token:
        logger.warning("TELEGRAM_BOT_TOKEN set but RENDER_EXTERNAL_URL not set - webhook disabled")
    else:
        logger.info("Telegram bot not configured")
    
    yield
    
    logger.info("Shutting down FastAPI application")


app = FastAPI(title="RAG API", lifespan=lifespan)


class Query(BaseModel):
    """Query request model."""

    question: str
    session_id: Optional[str] = None
    max_results: Optional[int] = 5


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "ok", 
        "service": "RAG API",
        "telegram_enabled": telegram_bot is not None
    }


@app.post("/telegram")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook updates."""
    if not telegram_bot:
        logger.error("Telegram webhook called but bot not initialized")
        raise HTTPException(status_code=503, detail="Telegram bot not initialized")
    
    try:
        data = await request.json()
        logger.info(f"Telegram webhook received: {data.get('update_id', 'unknown')}")
        
        update = Update.de_json(data, telegram_bot.app.bot)
        await telegram_bot.app.process_update(update)
        
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    return {
        "status": "ok",
        "agent_ready": agent is not None,
        "telegram_ready": telegram_bot is not None
    }
