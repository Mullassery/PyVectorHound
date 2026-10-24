"""Logging configuration for Pyvectorhound.

Provides structured logging setup with support for multiple vector database backends
and diagnostic logging for search operations.
"""

import logging
import os
import sys
from typing import Optional

__all__ = ["configure_logging", "get_logger"]


def configure_logging(
    level: str = "INFO",
    format_style: str = "detailed",
    log_file: Optional[str] = None,
) -> None:
    """Configure logging for Pyvectorhound.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_style: Format style ("simple" or "detailed")
        log_file: Optional file path to write logs to

    Example:
        >>> configure_logging(level="DEBUG", log_file="/var/log/vectordb.log")
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    if format_style == "detailed":
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - " "%(filename)s:%(lineno)d - %(message)s"
        )
    else:
        log_format = "%(levelname)s - %(name)s - %(message)s"

    formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # File handler (if specified)
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Configure root logger
    root_logger = logging.getLogger("pyvectorhound")
    root_logger.setLevel(log_level)
    for handler in handlers:
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.debug(f"Searching {k} nearest neighbors")
    """
    return logging.getLogger(f"pyvectorhound.{name}")


# Auto-configure logging on import
_log_level = os.environ.get("PYVECTORHOUND_LOG_LEVEL", "INFO")
_log_file = os.environ.get("PYVECTORHOUND_LOG_FILE", None)
configure_logging(level=_log_level, log_file=_log_file)
