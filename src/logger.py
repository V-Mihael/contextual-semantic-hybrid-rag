"""Centralized logging configuration."""

from loguru import logger
import sys

# Remove default handler
logger.remove()

# Console handler (stdout)
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO",
)

# File handler (rotating logs)
logger.add(
    "logs/app_{time}.log",
    rotation="1 day",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} - {message}",
    level="INFO",
)

__all__ = ["logger"]
