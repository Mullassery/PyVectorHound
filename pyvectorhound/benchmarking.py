"""Performance benchmarking and latency profiling for retrieval systems.

Provides latency metrics (p50, p95, p99), embedding quality comparison
across databases, and storage efficiency analysis.
"""

import time
import statistics
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from datetime import datetime


@dataclass
class LatencyMetrics:
    """Latency metrics for a retrieval operation."""

    mean: float
    median: float
    p95: float
    p99: float
    min: float
    max: float
    stddev: float
    samples: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class PerformanceSnapshot:
    """Performance metrics at a point in time."""

    timestamp: datetime
    query_latency: LatencyMetrics
    embedding_latency: LatencyMetrics
    db_query_time: LatencyMetrics
    total_latency: LatencyMetrics
    recall_at_k: Dict[int, float]
    precision_at_k: Dict[int, float]
    mrr: float
    ndcg: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "query_latency": self.query_latency.to_dict(),
            "embedding_latency": self.embedding_latency.to_dict(),
            "db_query_time": self.db_query_time.to_dict(),
            "total_latency": self.total_latency.to_dict(),
            "recall_at_k": self.recall_at_k,
            "precision_at_k": self.precision_at_k,
            "mrr": self.mrr,
            "ndcg": self.ndcg,
        }


@dataclass
class StorageMetrics:
    """Storage efficiency metrics."""

    total_vectors: int
    total_size_mb: float
    avg_vector_size_bytes: float
    index_overhead_mb: float
    compression_ratio: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class EmbeddingComparison:
    """Comparison of embedding models."""

    model_a: str
    model_b: str
    quality_a: Dict[str, float]
    quality_b: Dict[str, float]
    latency_a_ms: float
    latency_b_ms: float
    recall_diff: float
    cost_per_1m_tokens_a: float
    cost_per_1m_tokens_b: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class PerformanceBenchmark:
    """Benchmark retrieval system performance.

    Measures and compares latency, embedding quality, and storage efficiency
    across different configurations and databases.
    """

    def __init__(self, adapter: Optional[Any] = None):
        """Initialize benchmarking engine.

        Args:
            adapter: Optional database adapter for metrics collection
        """
        self.adapter = adapter
        self._latency_samples: Dict[str, List[float]] = {}
        self._snapshots: List[PerformanceSnapshot] = []
        self._baseline: Optional[PerformanceSnapshot] = None

    def measure_query_latency(
        self, query_fn, num_iterations: int = 100
    ) -> LatencyMetrics:
        """Measure latency of query operation.

        Args:
            query_fn: Callable that performs a query
            num_iterations: Number of times to run query

        Returns:
            LatencyMetrics with p50, p95, p99 percentiles
        """
        latencies = []

        for _ in range(num_iterations):
            start = time.perf_counter()
            query_fn()
            elapsed = (time.perf_counter() - start) * 1000  # Convert to ms

            latencies.append(elapsed)

        return self._compute_latency_metrics(latencies)

    def measure_embedding_latency(
        self, embedding_fn, embeddings: List[np.ndarray]
    ) -> LatencyMetrics:
        """Measure embedding model latency.

        Args:
            embedding_fn: Function that generates embeddings
            embeddings: List of embeddings to use for testing

        Returns:
            LatencyMetrics for embedding generation
        """
        latencies = []

        for embedding in embeddings:
            start = time.perf_counter()
            embedding_fn(embedding)
            elapsed = (time.perf_counter() - start) * 1000

            latencies.append(elapsed)

        return self._compute_latency_metrics(latencies)

    def measure_end_to_end_latency(
        self, e2e_fn, num_iterations: int = 50
    ) -> LatencyMetrics:
        """Measure end-to-end query latency.

        Args:
            e2e_fn: Function that performs complete retrieval pipeline
            num_iterations: Number of times to run

        Returns:
            LatencyMetrics for complete pipeline
        """
        latencies = []

        for _ in range(num_iterations):
            start = time.perf_counter()
            e2e_fn()
            elapsed = (time.perf_counter() - start) * 1000

            latencies.append(elapsed)

        return self._compute_latency_metrics(latencies)

    def compare_databases(
        self,
        query_fn_map: Dict[str, callable],
        num_iterations: int = 50,
    ) -> Dict[str, Dict[str, Any]]:
        """Compare performance across multiple databases.

        Args:
            query_fn_map: Mapping of db_name -> query_function
            num_iterations: Number of iterations per database

        Returns:
            Dictionary with performance metrics per database
        """
        results = {}

        for db_name, query_fn in query_fn_map.items():
            latency_metrics = self.measure_query_latency(query_fn, num_iterations)
            results[db_name] = {
                "latency": latency_metrics.to_dict(),
                "mean_ms": latency_metrics.mean,
                "p95_ms": latency_metrics.p95,
                "p99_ms": latency_metrics.p99,
            }

        return results

    def compare_embedding_models(
        self,
        model_configs: Dict[str, Dict[str, Any]],
        test_queries: List[str],
    ) -> List[EmbeddingComparison]:
        """Compare embedding model quality and performance.

        Args:
            model_configs: Dict mapping model_name -> {embedding_fn, quality_metrics, cost}
            test_queries: List of test queries

        Returns:
            List of EmbeddingComparison objects
        """
        comparisons = []
        model_names = list(model_configs.keys())

        for i in range(len(model_names)):
            for j in range(i + 1, len(model_names)):
                model_a = model_names[i]
                model_b = model_names[j]

                config_a = model_configs[model_a]
                config_b = model_configs[model_b]

                comparison = EmbeddingComparison(
                    model_a=model_a,
                    model_b=model_b,
                    quality_a=config_a.get("quality_metrics", {}),
                    quality_b=config_b.get("quality_metrics", {}),
                    latency_a_ms=config_a.get("latency_ms", 0.0),
                    latency_b_ms=config_b.get("latency_ms", 0.0),
                    recall_diff=config_a.get("recall", 0.0)
                    - config_b.get("recall", 0.0),
                    cost_per_1m_tokens_a=config_a.get("cost_per_1m", 0.0),
                    cost_per_1m_tokens_b=config_b.get("cost_per_1m", 0.0),
                )
                comparisons.append(comparison)

        return comparisons

    def analyze_storage_efficiency(self) -> Optional[StorageMetrics]:
        """Analyze storage efficiency of vector database.

        Returns:
            StorageMetrics if adapter supports storage queries, None otherwise
        """
        if not self.adapter or not hasattr(self.adapter, "get_storage_metrics"):
            return None

        try:
            metrics = self.adapter.get_storage_metrics()
            return StorageMetrics(
                total_vectors=metrics.get("total_vectors", 0),
                total_size_mb=metrics.get("total_size_mb", 0.0),
                avg_vector_size_bytes=metrics.get("avg_vector_size_bytes", 0.0),
                index_overhead_mb=metrics.get("index_overhead_mb", 0.0),
                compression_ratio=metrics.get("compression_ratio", 1.0),
            )
        except Exception:
            return None

    def capture_snapshot(
        self,
        query_latency: LatencyMetrics,
        embedding_latency: LatencyMetrics,
        db_query_time: LatencyMetrics,
        total_latency: LatencyMetrics,
        recall_at_k: Optional[Dict[int, float]] = None,
        precision_at_k: Optional[Dict[int, float]] = None,
        mrr: float = 0.0,
        ndcg: float = 0.0,
    ) -> PerformanceSnapshot:
        """Capture performance metrics snapshot.

        Args:
            query_latency: Query latency metrics
            embedding_latency: Embedding latency metrics
            db_query_time: Database query time
            total_latency: Total end-to-end latency
            recall_at_k: Recall at K metric
            precision_at_k: Precision at K metric
            mrr: Mean Reciprocal Rank
            ndcg: Normalized Discounted Cumulative Gain

        Returns:
            PerformanceSnapshot
        """
        snapshot = PerformanceSnapshot(
            timestamp=datetime.utcnow(),
            query_latency=query_latency,
            embedding_latency=embedding_latency,
            db_query_time=db_query_time,
            total_latency=total_latency,
            recall_at_k=recall_at_k or {},
            precision_at_k=precision_at_k or {},
            mrr=mrr,
            ndcg=ndcg,
        )

        self._snapshots.append(snapshot)

        if self._baseline is None:
            self._baseline = snapshot

        return snapshot

    def detect_regression(self) -> Optional[Dict[str, Any]]:
        """Detect performance regression compared to baseline.

        Returns:
            Dictionary with regression analysis or None if no baseline
        """
        if self._baseline is None or len(self._snapshots) < 2:
            return None

        current = self._snapshots[-1]
        baseline = self._baseline

        regression = {
            "query_latency_increase_pct": (
                (current.query_latency.mean - baseline.query_latency.mean)
                / baseline.query_latency.mean
                * 100
            ),
            "embedding_latency_increase_pct": (
                (current.embedding_latency.mean - baseline.embedding_latency.mean)
                / baseline.embedding_latency.mean
                * 100
            ),
            "total_latency_increase_pct": (
                (current.total_latency.mean - baseline.total_latency.mean)
                / baseline.total_latency.mean
                * 100
            ),
            "has_regression": False,
        }

        # Consider >5% increase as regression
        threshold = 5.0
        if any(
            abs(regression[key]) > threshold
            for key in regression
            if key.endswith("_increase_pct")
        ):
            regression["has_regression"] = True

        return regression

    def _compute_latency_metrics(self, latencies: List[float]) -> LatencyMetrics:
        """Compute latency statistics.

        Args:
            latencies: List of latency measurements in ms

        Returns:
            LatencyMetrics with computed percentiles
        """
        if not latencies:
            return LatencyMetrics(0, 0, 0, 0, 0, 0, 0, 0)

        sorted_latencies = sorted(latencies)

        return LatencyMetrics(
            mean=statistics.mean(latencies),
            median=statistics.median(latencies),
            p95=np.percentile(sorted_latencies, 95),
            p99=np.percentile(sorted_latencies, 99),
            min=min(latencies),
            max=max(latencies),
            stddev=statistics.stdev(latencies) if len(latencies) > 1 else 0,
            samples=len(latencies),
        )

    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report.

        Returns:
            Dictionary with all performance metrics and analysis
        """
        if not self._snapshots:
            return {}

        latest = self._snapshots[-1]
        regression = self.detect_regression()

        return {
            "latest_snapshot": latest.to_dict(),
            "num_snapshots": len(self._snapshots),
            "regression_analysis": regression,
            "baseline": self._baseline.to_dict() if self._baseline else None,
        }
