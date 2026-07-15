"""Pyvectorhound: Diagnose and optimize vector search in RAG/LLM systems.

A comprehensive toolkit for identifying and fixing vector database retrieval failures
by isolating problematic components: embedding quality, vector search performance,
keyword search effectiveness, and reranker calibration.

Features:
    - Component-level diagnostics for RAG retrieval failures
    - O(n) analysis (not O(n²) metric computation)
    - Multi-database support (Qdrant, Chroma, Milvus, Weaviate, pgvector)
    - Actionable recommendations with ROI estimates
    - Plain-English explanations of issues and fixes

Example:
    >>> from pyvectorhound import Hound
    >>> hound = Hound(vector_db_url="http://localhost:6333")
    >>> diagnosis = hound.diagnose(query_text, results)
    >>> print(diagnosis.recommendations)

Attributes:
    __version__ (str): Package version
    __author__ (str): Primary author
    __email__ (str): Author email
    __license__ (str): License type (MIT)
"""

import logging
from typing import Final

from pyvectorhound.logging_config import get_logger

# Module logger
logger = get_logger(__name__)
logger.info("Initializing Pyvectorhound")

__version__: Final[str] = "0.2.0"
__author__: Final[str] = "Georgi Mammen Mullassery"
__email__: Final[str] = "mullassery@gmail.com"
__license__: Final[str] = "MIT"

try:
    from pyvectorhound.hound import Hound
    from pyvectorhound.diagnosis import Diagnosis
    from pyvectorhound.comparison import ModelComparison
    from pyvectorhound.scorer import QualityScorer
    logger.debug("Successfully imported core modules")
except ImportError as e:
    logger.error(f"Failed to import core modules: {e}")
    raise

__all__: Final[list[str]] = [
    "Hound",
    "Diagnosis",
    "ModelComparison",
    "QualityScorer",
]

logger.info(f"Pyvectorhound {__version__} initialized successfully")
