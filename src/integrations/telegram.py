"""Telegram bot integration."""

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


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
            "Hello! I'm a RAG assistant. Send me your questions and I'll answer using my base knowledge. I know some economics books and i can search on the internet."
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages."""
        user_message = update.message.text
        print(f"📩 Pergunta: {user_message}")

        # Show typing indicator
        await update.message.chat.send_action("typing")

        # Get response from agent
        response = self.agent.run(user_message)
        print(f"✅ Resposta gerada ({len(response.content)} chars)")

        # Send response
        await update.message.reply_text(response.content)

    def run(self):
        """Start the bot with polling."""
        print("🤖 Telegram bot iniciado!")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
