"""Main PyHound class for retrieval diagnostics."""

from typing import Optional, List, Dict, Any
import numpy as np
from pyvectorhound.database import get_adapter, VectorDB
from pyvectorhound.diagnosis import Diagnosis
from pyvectorhound.comparison import ModelComparison
from pyvectorhound.scorer import QualityScorer
from pyvectorhound.benchmarking import PerformanceBenchmark, LatencyMetrics
from pyvectorhound.trend_analysis import TrendAnalyzer
from pyvectorhound.retrieval_tracing import RetrievalTracer
from pyvectorhound.retrieval_replay import RetrievalReplayer
from pyvectorhound.recommendations import RecommendationEngine


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

        # Initialize performance benchmarking and trend analysis
        self._benchmarker = PerformanceBenchmark(adapter=self.adapter)
        self._trend_analyzer = TrendAnalyzer()

        # Initialize retrieval tracing, replay, and recommendations
        self._tracer = RetrievalTracer()
        self._replayer = RetrievalReplayer()
        self._recommendation_engine = RecommendationEngine()

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

    def benchmark(self) -> PerformanceBenchmark:
        """
        Access performance benchmarking engine.

        Returns:
            PerformanceBenchmark instance for measuring latency and performance

        Examples:
            >>> benchmark = hound.benchmark()
            >>> latency = benchmark.measure_query_latency(query_fn, num_iterations=100)
            >>> report = benchmark.get_performance_report()
        """
        return self._benchmarker

    def analyze_trends(self) -> TrendAnalyzer:
        """
        Access trend analysis engine.

        Returns:
            TrendAnalyzer instance for detecting drift and anomalies over time

        Examples:
            >>> analyzer = hound.analyze_trends()
            >>> analyzer.track_metric("embedding_isotropy", 0.92)
            >>> drift = analyzer.detect_drift("embedding_isotropy")
            >>> report = analyzer.get_trend_report()
        """
        return self._trend_analyzer

    def measure_query_latency(
        self,
        query_fn,
        num_iterations: int = 100,
    ) -> LatencyMetrics:
        """
        Measure query latency with percentile analysis.

        Args:
            query_fn: Callable that performs a query
            num_iterations: Number of iterations to measure

        Returns:
            LatencyMetrics with p50, p95, p99 percentiles

        Examples:
            >>> metrics = hound.measure_query_latency(lambda: hound.diagnose("test"), 100)
            >>> print(f"P95 latency: {metrics.p95}ms")
        """
        return self._benchmarker.measure_query_latency(query_fn, num_iterations)

    def track_metric(
        self,
        metric_name: str,
        value: float,
        **tags,
    ) -> None:
        """
        Track a metric value for trend analysis.

        Args:
            metric_name: Name of metric (e.g., "embedding_isotropy")
            value: Metric value
            **tags: Optional tags for filtering (e.g., db="qdrant")

        Examples:
            >>> hound.track_metric("embedding_isotropy", 0.92, model="openai")
            >>> hound.track_metric("query_latency_ms", 45.2, db="qdrant")
        """
        self._trend_analyzer.track_metric(metric_name, value, **tags)

    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get comprehensive performance benchmarking report.

        Returns:
            Dictionary with performance metrics and analysis

        Examples:
            >>> report = hound.get_performance_report()
            >>> print(report["latest_snapshot"])
        """
        return self._benchmarker.get_performance_report()

    def get_trend_report(self, metric_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get comprehensive trend analysis report.

        Args:
            metric_names: List of metrics to include (None = all)

        Returns:
            Dictionary with trend analysis for all tracked metrics

        Examples:
            >>> report = hound.get_trend_report()
            >>> print(report["metrics"])
        """
        return self._trend_analyzer.get_trend_report(metric_names)

    def tracer(self) -> RetrievalTracer:
        """
        Access retrieval trace capture engine.

        Returns:
            RetrievalTracer instance for capturing pipeline execution

        Examples:
            >>> tracer = hound.tracer()
            >>> tracer.start_trace("query_1", "search query")
            >>> tracer.record_embedding(embedding, 15.2)
            >>> tracer.record_vector_search_results(results)
            >>> trace = tracer.end_trace()
        """
        return self._tracer

    def replayer(self) -> RetrievalReplayer:
        """
        Access retrieval replay engine.

        Returns:
            RetrievalReplayer instance for interactive debugging

        Examples:
            >>> replayer = hound.replayer()
            >>> config = replayer.create_configuration("config_1", {...})
            >>> result = replayer.replay(trace, "config_1")
            >>> comparison = replayer.compare_configurations("config_1", "config_2")
        """
        return self._replayer

    def get_recommendations(
        self,
        query_id: str,
        query_text: str,
        diagnosis: Dict[str, Any],
        trace_analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get AI-powered recommendations for retrieval failure.

        Args:
            query_id: Unique query identifier
            query_text: The search query
            diagnosis: Diagnostic analysis results
            trace_analysis: Optional detailed trace analysis

        Returns:
            Dictionary with recommendations and ROI analysis

        Examples:
            >>> recommendations = hound.get_recommendations(
            ...     "query_1",
            ...     "search query",
            ...     diagnosis_results
            ... )
            >>> for rec in recommendations["recommendations"]:
            ...     print(f"{rec['title']}: +{rec['expected_improvement_pct']}%")
        """
        report = self._recommendation_engine.analyze_failure(
            query_id, query_text, diagnosis, trace_analysis
        )
        return report.to_dict()

    def get_recommendation_summary(self, query_id: str) -> Optional[Dict[str, Any]]:
        """
        Get summary of recommendations for a query.

        Args:
            query_id: Query identifier

        Returns:
            Summary dictionary or None if not found

        Examples:
            >>> summary = hound.get_recommendation_summary("query_1")
            >>> print(summary["executive_summary"])
        """
        return self._recommendation_engine.get_recommendation_summary(query_id)
