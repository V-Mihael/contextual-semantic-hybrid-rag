"""Telegram bot integration."""

import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from loguru import logger


class TelegramBot:
    """Telegram bot client."""

    def __init__(self, token: str, agent):
        """Initialize Telegram bot.

        Args:
            token: Telegram bot token from BotFather.
            agent: Agno agent instance.
        """
        self.token = token
        self.agent = agent
        self.app = Application.builder().token(token).build()

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "Hello! I'm *Spets*, a RAG assistant with economics knowledge and web search powers! Send me your questions and I'll answer using my base knowledge and the internet, if needed."
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages."""
        start_time = time.time()
        user_message = update.message.text
        user_name = update.message.from_user.first_name
        user_id = str(update.message.from_user.id)
        
        logger.info(f"Message received | user={user_name} user_id={user_id} message={user_message[:100]}")

        # Show typing indicator
        await update.message.chat.send_action("typing")

        # Get response from agent with user session
        try:
            # Add user info to message context
            user_context = f"[User_name: {user_name} (ID: {user_id})]"
            message_with_context = f"{user_context}\n{user_message}"
            
            response = self.agent.run(message_with_context, session_id=user_id)
            tools_used = [m.tool_name for m in response.messages if hasattr(m, 'tool_name')]
            duration = time.time() - start_time
            
            logger.info(
                f"Response generated | user={user_name} session={user_id} duration={duration:.2f}s "
                f"response_length={len(response.content)} tools={tools_used}"
            )
            
            # Send response
            await update.message.reply_text(
                response.content,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error processing message | user={user_name} error={str(e)}")
            await update.message.reply_text("Desculpe, ocorreu um erro. Tente novamente.")

    def run(self):
        """Start the bot with polling."""
        logger.info("Telegram bot started")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
