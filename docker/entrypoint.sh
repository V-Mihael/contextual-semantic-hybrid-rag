#!/bin/sh
set -e

# Start FastAPI server (includes Telegram webhook)
exec poetry run uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
