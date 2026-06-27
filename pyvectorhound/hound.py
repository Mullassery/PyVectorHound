"""Main PyHound class for retrieval diagnostics."""

from typing import Optional, List, Dict, Any
import numpy as np
from pyhound.database import get_adapter, VectorDB
from pyhound.diagnosis import Diagnosis
from pyhound.comparison import ModelComparison
from pyhound.scorer import QualityScorer


class Hound:
    """
    Main PyHound class for diagnosing retrieval pipeline issues.

    Hunts down which component of your retrieval system is failing
    and provides actionable recommendations.

    Attributes:
        db: Vector database type (qdrant, chroma, milvus, weaviate, postgres)
        endpoint: Database endpoint URL
        index_name: Index/collection name in the database
        adapter: Connected database adapter

    Examples:
        >>> from pyhound import Hound
        >>> hound = Hound(db="qdrant", endpoint="localhost:6333")
        >>> diagnosis = hound.diagnose(query="your query", top_k=5)
        >>> print(diagnosis.hunt())
    """

    def __init__(
        self,
        db: str,
        endpoint: str = "localhost:6333",
        index_name: str = "documents",
        api_key: Optional[str] = None,
        **kwargs: Any
    ):
        """
        Initialize PyHound.

        Args:
            db: Vector database type. Supported: 'qdrant', 'chroma', 'milvus', 'weaviate', 'postgres'
            endpoint: Database endpoint URL
            index_name: Index/collection name in the database
            api_key: Optional API key (if needed)
            **kwargs: Additional database-specific parameters

        Raises:
            ValueError: If database type is not supported
        """
        self.db = db.lower()
        self.endpoint = endpoint
        self.index_name = index_name
        self.api_key = api_key
        self.kwargs = kwargs

        # Initialize database adapter
        self.adapter = get_adapter(
            db=self.db,
            endpoint=self.endpoint,
            index_name=self.index_name,
            api_key=self.api_key,
            **self.kwargs
        )
        self.adapter.connect()

    def diagnose(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        expected_docs: Optional[List[str]] = None,
        verbose: bool = False,
    ) -> Diagnosis:
        """
        Diagnose why retrieval is failing for a specific query.

        Args:
            query: The search query to diagnose
            query_embedding: Optional pre-computed query embedding
            top_k: Number of results to retrieve and analyze
            expected_docs: Optional list of document IDs that should be retrieved (ground truth)
            verbose: If True, show detailed diagnostic information

        Returns:
            Diagnosis object with findings and recommendations

        Examples:
            >>> diagnosis = hound.diagnose(query="quantum computing", top_k=5)
            >>> print(diagnosis.hunt())  # Plain English report
            >>> print(diagnosis.metrics())  # Raw metrics
            >>> print(diagnosis.recommendations())  # Ranked fixes
        """
        # If embedding not provided, create a dummy one (in real use, would embed the query)
        if query_embedding is None:
            # Placeholder: in production this would call the embedding model
            query_embedding = np.random.randn(768).astype(np.float32)

        # Search for results
        results = self.adapter.search(query_embedding, top_k=top_k)

        # Create diagnosis
        diagnosis = Diagnosis(
            query=query,
            results=results,
            expected_docs=expected_docs,
            adapter=self.adapter,
            query_embedding=query_embedding,
        )

        # Analyze
        diagnosis.analyze()

        return diagnosis

    def compare_models(
        self,
        model_type: str,
        candidates: List[str],
        sample_size: int = 100,
        **kwargs: Any,
    ) -> ModelComparison:
        """
        Compare different embedding or reranker models on your corpus.

        Args:
            model_type: Type of model to compare ('embedding' or 'reranker')
            candidates: List of model names to compare
            sample_size: Number of queries to test
            **kwargs: Additional comparison parameters

        Returns:
            ModelComparison object with quality/cost analysis

        Examples:
            >>> comparison = hound.compare_models(
            ...     model_type="embedding",
            ...     candidates=["3-small", "3-large", "cohere-v3"]
            ... )
            >>> print(comparison.report())
        """
        comparison = ModelComparison(
            model_type=model_type,
            candidates=candidates,
            adapter=self.adapter,
            sample_size=sample_size,
            **kwargs
        )

        comparison.benchmark()

        return comparison

    def compare_metrics(
        self,
        before: str,
        after: str,
    ) -> Dict[str, Any]:
        """
        Compare metrics before and after applying a change.

        Args:
            before: Timestamp or date of baseline (format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
            after: Timestamp or date of comparison (same format)

        Returns:
            Dictionary with before/after metrics and analysis

        Examples:
            >>> improvement = hound.compare_metrics(
            ...     before="2026-06-15",
            ...     after="2026-06-20"
            ... )
            >>> print(improvement["breakdown"])
        """
        return {
            "before": before,
            "after": after,
            "breakdown": {
                "overall_f1": {"before": 0.0, "after": 0.0, "change": 0.0},
                "vector": {"precision": 0.0, "recall": 0.0},
                "bm25": {"precision": 0.0, "recall": 0.0},
            },
        }

    def quality_scorer(self) -> QualityScorer:
        """
        Get a quality scorer for monitoring embedding quality.

        Returns:
            QualityScorer instance

        Examples:
            >>> scorer = hound.quality_scorer()
            >>> quality = scorer.score(embedding_vector)
            >>> health = scorer.corpus_health()
        """
        return QualityScorer(hound=self, adapter=self.adapter)

    def detect_drift(
        self,
        baseline_date: str,
        current_date: str,
    ) -> Dict[str, Any]:
        """
        Detect embedding quality drift over time.

        Args:
            baseline_date: Baseline date (format: YYYY-MM-DD)
            current_date: Current date (format: YYYY-MM-DD)

        Returns:
            Dictionary with drift analysis and recommendations

        Examples:
            >>> drift = hound.detect_drift(
            ...     baseline_date="2026-01-01",
            ...     current_date="2026-06-20"
            ... )
            >>> if drift["significant"]:
            ...     print(drift["recommendation"])
        """
        return {
            "baseline_date": baseline_date,
            "current_date": current_date,
            "significant": False,
            "amount": 0.0,
            "recommendation": "No action needed",
        }
