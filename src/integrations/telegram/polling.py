"""Telegram bot polling runner for local development."""

from src.logger import logger
from src.config import settings
from src.agents import create_rag_agent
from src.integrations.telegram import TelegramBot


def run_polling():
    """Initialize and run Telegram bot in polling mode (for local development)."""
    logger.info("Starting Telegram bot initialization (polling mode)")
    
    agent = create_rag_agent()
    logger.info("Agent initialized with persistent database")
    
    telegram_token = getattr(settings, 'telegram_bot_token', None)
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env")
        return
    
    logger.info("Starting Telegram bot at https://t.me/VMihaelBot")
    logger.info("Logs saved to logs/telegram_bot_*.log")
    
    bot = TelegramBot(token=telegram_token, agent=agent)
    bot.run()


if __name__ == "__main__":
    run_polling()
