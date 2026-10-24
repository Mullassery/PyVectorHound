"""Decorator for safe execution with error handling."""

import logging
from functools import wraps
from typing import Any, Callable

from .errors import VectorDiagnosticError, safe_database_error

logger = logging.getLogger(__name__)


def safe_execute(func: Callable) -> Callable:
    """
    Decorator to safely execute functions with error handling.

    Catches exceptions and converts them to safe error messages.
    Logs full error internally without exposing to users.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except VectorDiagnosticError:
            # Already safe error, re-raise
            raise
        except Exception as e:
            # Log full error internally
            logger.exception(f"Error in {func.__name__}: {e}")

            # Convert to safe error for user
            if "database" in func.__name__.lower():
                raise safe_database_error(e)
            else:
                raise VectorDiagnosticError(
                    user_message=f"Error in {func.__name__}", internal_message=str(e)
                )

    return wrapper
