"""Run Telegram bot."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.logger import logger
from src.config import settings
from src.agents import create_rag_agent
from src.integrations.telegram import TelegramBot


def main():
    """Initialize and run Telegram bot."""
    logger.info("Starting Telegram bot initialization")
    
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
    main()
