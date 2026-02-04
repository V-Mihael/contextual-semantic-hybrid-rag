#!/bin/sh
set -e

# Start Telegram bot in foreground
exec poetry run python scripts/telegram_bot.py
