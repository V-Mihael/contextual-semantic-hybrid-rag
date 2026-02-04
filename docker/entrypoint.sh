#!/bin/sh
set -e

# Start FastAPI in background
poetry run uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8000} &

# Start Telegram bot in foreground
exec poetry run python scripts/telegram_bot.py
