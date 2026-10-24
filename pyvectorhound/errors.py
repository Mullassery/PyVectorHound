"""Secure error handling to prevent information disclosure."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class VectorDiagnosticError(Exception):
    """Base exception for PyVectorhound."""

    def __init__(self, user_message: str, internal_message: Optional[str] = None):
        """
        Initialize with user-facing and internal messages.

        Args:
            user_message: What to show to users (safe, non-technical)
            internal_message: What to log internally (can include stack traces, details)
        """
        self.user_message = user_message
        self.internal_message = internal_message or user_message
        super().__init__(self.user_message)

    def get_user_message(self) -> str:
        """Get safe message for users."""
        return self.user_message

    def get_internal_message(self) -> str:
        """Get detailed message for logs."""
        return self.internal_message


class VectorDatabaseError(VectorDiagnosticError):
    """Vector database connection or query error."""

    pass


class EmbeddingError(VectorDiagnosticError):
    """Embedding model error."""

    pass


def safe_database_error(exception: Exception) -> VectorDatabaseError:
    """
    Convert database exceptions to safe error messages.

    Args:
        exception: Original exception from vector DB

    Returns:
        VectorDatabaseError with safe user message
    """
    exception_type = type(exception).__name__

    # Map exceptions to safe messages
    error_messages = {
        "ConnectionError": "Unable to connect to vector database",
        "TimeoutError": "Vector database request timed out",
        "PermissionError": "Access denied to vector database",
        "ValueError": "Invalid database configuration",
        "KeyError": "Database resource not found",
    }

    user_message = error_messages.get(exception_type, "Vector database error occurred")

    return VectorDatabaseError(
        user_message=user_message, internal_message=f"{exception_type}: {exception!s}"
    )


def safe_embedding_error(exception: Exception) -> EmbeddingError:
    """Convert embedding errors to safe messages."""
    return EmbeddingError(
        user_message="Unable to process embedding model",
        internal_message=f"Embedding error: {exception!s}",
    )
