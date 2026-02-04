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
from src.logger import logger
from src.integrations.telegram.transcriber import AudioTranscriber


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
        self.transcriber = AudioTranscriber()
        self.app = Application.builder().token(token).build()

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        self.app.add_handler(
            MessageHandler(filters.VOICE | filters.AUDIO, self.handle_audio)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "Hello! I'm *Spets*, a RAG assistant with economics knowledge and web search powers! Send me your questions and I'll answer using my base knowledge and the internet, if needed.\n\n🎤 You can also send voice messages!"
        )

    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice and audio messages."""
        start_time = time.time()
        user_name = update.message.from_user.first_name
        user_id = str(update.message.from_user.id)
        
        logger.info(f"Audio received | user={user_name} user_id={user_id}")
        
        try:
            # Show typing indicator
            await update.message.chat.send_action("typing")
            
            # Get audio file
            if update.message.voice:
                audio_file = await update.message.voice.get_file()
                format = "ogg"
            else:
                audio_file = await update.message.audio.get_file()
                format = "mp3"
            
            # Download audio
            audio_bytes = await audio_file.download_as_bytearray()
            
            # Transcribe
            transcription = self.transcriber.transcribe(bytes(audio_bytes), format=format)
            logger.info(f"Audio transcribed | user={user_name} text={transcription[:100]}")
            
            # Process as text message
            user_context = f"[User_name: {user_name} (ID: {user_id})]\n[Transcribed from audio]"
            message_with_context = f"{user_context}\n{transcription}"
            
            response = self.agent.run(message_with_context, session_id=user_id)
            duration = time.time() - start_time
            
            logger.info(
                f"Response generated | user={user_name} duration={duration:.2f}s "
                f"response_length={len(response.content)}"
            )
            
            # Send response with transcription
            await update.message.reply_text(
                f"🎤 *Transcription:* {transcription}\n\n{response.content}",
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error processing audio | user={user_name} error={str(e)}")
            await update.message.reply_text("Desculpe, ocorreu um erro ao processar o áudio. Tente novamente.")

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

    async def set_webhook(self, url: str):
        """Set webhook URL for the bot."""
        await self.app.bot.set_webhook(url)
        logger.info(f"Webhook set to {url}")

    def run(self):
        """Start the bot with polling."""
        logger.info("Telegram bot started")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
