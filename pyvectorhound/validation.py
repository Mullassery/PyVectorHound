"""Input validation for PyVectorhound queries and data."""

from typing import List, Optional

import numpy as np
from pydantic import BaseModel, Field, field_validator


class EmbeddingQuery(BaseModel):
    """Validated embedding query."""

    text: str = Field(min_length=1, max_length=10000)
    embedding_model: str = Field(pattern="^[a-zA-Z0-9_-]+$")

    @field_validator("text")
    def validate_text(cls, v):  # noqa: N805
        if not v or not v.strip():
            raise ValueError("Query text cannot be empty")
        return v.strip()


class VectorSearchQuery(BaseModel):
    """Validated vector search query."""

    vector: List[float] = Field(min_items=1, max_items=2000)
    limit: int = Field(ge=1, le=1000, default=10)
    threshold: Optional[float] = Field(ge=0.0, le=1.0, default=None)

    @field_validator("vector")
    def validate_vector(cls, v):  # noqa: N805
        # Check for NaN/Inf values
        arr = np.array(v)
        if not np.isfinite(arr).all():
            raise ValueError("Vector contains NaN or Inf values")

        # Check vector magnitude
        magnitude = np.linalg.norm(arr)
        if magnitude == 0:
            raise ValueError("Vector magnitude is zero")

        return v


class RerankerQuery(BaseModel):
    """Validated reranker query."""

    query: str = Field(min_length=1, max_length=5000)
    candidates: List[str] = Field(min_items=1, max_items=100)
    model: str = Field(pattern="^[a-zA-Z0-9_-]+$")

    @field_validator("candidates")
    def validate_candidates(cls, v):  # noqa: N805
        for i, candidate in enumerate(v):
            if not candidate or not str(candidate).strip():
                raise ValueError(f"Candidate {i} is empty")
        return v


class DiagnosisParams(BaseModel):
    """Validated diagnosis parameters."""

    query_text: str = Field(min_length=1, max_length=5000)
    results_count: int = Field(ge=1, le=1000, default=10)
    embedding_dimension: int = Field(ge=64, le=4096, default=1536)

    @field_validator("query_text")
    def validate_query(cls, v):  # noqa: N805
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


def validate_query_object(query_obj) -> bool:
    """
    Validate a query object to ensure it's safe.

    Args:
        query_obj: Query object to validate

    Returns:
        True if valid

    Raises:
        ValueError: If query is invalid
    """
    if query_obj is None:
        raise ValueError("Query object cannot be None")

    if not hasattr(query_obj, "__dict__"):
        raise ValueError("Query object must be a dict-like object")

    # Check for suspicious attributes
    suspicious = ["__import__", "eval", "exec", "__code__"]
    for attr in dir(query_obj):
        if any(s in attr.lower() for s in suspicious):
            raise ValueError(f"Suspicious attribute: {attr}")

    return True


def validate_embedding_vector(vector: List[float], dimension: int = 1536) -> bool:
    """
    Validate embedding vector.

    Args:
        vector: Embedding vector
        dimension: Expected dimension

    Returns:
        True if valid

    Raises:
        ValueError: If vector is invalid
    """
    if not isinstance(vector, (list, np.ndarray)):
        raise ValueError(f"Vector must be list or ndarray, got {type(vector)}")

    if len(vector) != dimension:
        raise ValueError(f"Vector dimension mismatch: {len(vector)} != {dimension}")

    # Check for NaN/Inf
    arr = np.array(vector, dtype=np.float32)
    if not np.isfinite(arr).all():
        raise ValueError("Vector contains NaN or Inf")

    return True
