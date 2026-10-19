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
    __license__ (str): License type (Apache-2.0)
"""

from importlib.metadata import PackageNotFoundError, version
from typing import Final

from pyvectorhound.logging_config import get_logger

# Module logger
logger = get_logger(__name__)
logger.info("Initializing Pyvectorhound")

try:
    __version__: Final[str] = version("pyvectorhound")
except PackageNotFoundError:
    __version__: Final[str] = "0.0.0+unknown"
__author__: Final[str] = "Georgi Mammen Mullassery"
__email__: Final[str] = "mullassery@gmail.com"
__license__: Final[str] = "Apache-2.0"

try:
    from pyvectorhound._mcp_connector import VectorRetrieval
    from pyvectorhound.benchmarking import (
        EmbeddingComparison,
        LatencyMetrics,
        PerformanceBenchmark,
        PerformanceSnapshot,
        StorageMetrics,
    )
    from pyvectorhound.comparison import ModelComparison
    from pyvectorhound.diagnosis import Diagnosis
    from pyvectorhound.hound import Hound
    from pyvectorhound.ranking import compute_reranker_metrics, rank_and_diversify
    from pyvectorhound.recommendations import (
        DiagnosticReport,
        FailureCategory,
        FixRecommendation,
        RecommendationEngine,
    )
    from pyvectorhound.retrieval_replay import (
        ComponentType,
        ReplayComparison,
        ReplayConfiguration,
        ReplayResult,
        RetrievalReplayer,
    )
    from pyvectorhound.retrieval_tracing import (
        PhaseMetrics,
        RetrievalTrace,
        RetrievalTracer,
        SearchResult,
        TracePhase,
    )
    from pyvectorhound.scorer import QualityScorer
    from pyvectorhound.synthetic import (
        EvalCase,
        RagasUnavailable,
        from_ragas_rows,
        generate_testset,
        to_hound_batch,
    )
    from pyvectorhound.trend_analysis import (
        AnomalyDetection,
        DriftAnalysis,
        RegressionAnalysis,
        TimeSeries,
        TrendAnalyzer,
    )

    logger.debug("Successfully imported core modules")
except ImportError as e:
    logger.error(f"Failed to import core modules: {e}")
    raise

__all__: Final[list[str]] = [
    "AnomalyDetection",
    "ComponentType",
    "Diagnosis",
    "DiagnosticReport",
    "DriftAnalysis",
    "EmbeddingComparison",
    "EvalCase",
    "FailureCategory",
    "FixRecommendation",
    "Hound",
    "LatencyMetrics",
    "ModelComparison",
    "PerformanceBenchmark",
    "PerformanceSnapshot",
    "PhaseMetrics",
    "QualityScorer",
    "RagasUnavailable",
    "RecommendationEngine",
    "RegressionAnalysis",
    "ReplayComparison",
    "ReplayConfiguration",
    "ReplayResult",
    "RetrievalReplayer",
    "RetrievalTrace",
    "RetrievalTracer",
    "SearchResult",
    "StorageMetrics",
    "TimeSeries",
    "TracePhase",
    "TrendAnalyzer",
    "VectorRetrieval",
    "compute_reranker_metrics",
    "from_ragas_rows",
    "generate_testset",
    "rank_and_diversify",
    "to_hound_batch",
]

logger.info(f"Pyvectorhound {__version__} initialized successfully")
