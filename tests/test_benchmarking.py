"""Tests for performance benchmarking module."""

import pytest
import time
import numpy as np
from datetime import datetime, timedelta
from pyvectorhound.benchmarking import (
    PerformanceBenchmark,
    LatencyMetrics,
    PerformanceSnapshot,
    StorageMetrics,
    EmbeddingComparison,
)


class TestLatencyMetrics:
    """Test LatencyMetrics data class."""

    def test_latency_metrics_creation(self):
        """Test creating latency metrics."""
        metrics = LatencyMetrics(
            mean=50.0,
            median=48.0,
            p95=85.0,
            p99=95.0,
            min=10.0,
            max=100.0,
            stddev=15.0,
            samples=100,
        )
        assert metrics.mean == 50.0
        assert metrics.p95 == 85.0
        assert metrics.samples == 100

    def test_latency_metrics_to_dict(self):
        """Test converting metrics to dict."""
        metrics = LatencyMetrics(
            mean=50.0,
            median=48.0,
            p95=85.0,
            p99=95.0,
            min=10.0,
            max=100.0,
            stddev=15.0,
            samples=100,
        )
        d = metrics.to_dict()
        assert d["mean"] == 50.0
        assert d["p95"] == 85.0


class TestPerformanceSnapshot:
    """Test PerformanceSnapshot data class."""

    def test_snapshot_creation(self):
        """Test creating performance snapshot."""
        query_latency = LatencyMetrics(50, 48, 85, 95, 10, 100, 15, 100)
        embedding_latency = LatencyMetrics(10, 9, 15, 18, 5, 20, 3, 100)
        db_query = LatencyMetrics(30, 28, 60, 70, 5, 80, 12, 100)
        total = LatencyMetrics(90, 85, 160, 180, 20, 200, 30, 100)

        snapshot = PerformanceSnapshot(
            timestamp=datetime.utcnow(),
            query_latency=query_latency,
            embedding_latency=embedding_latency,
            db_query_time=db_query,
            total_latency=total,
            recall_at_k={5: 0.8, 10: 0.85},
            precision_at_k={5: 0.9, 10: 0.85},
            mrr=0.75,
            ndcg=0.82,
        )

        assert snapshot.mrr == 0.75
        assert snapshot.recall_at_k[5] == 0.8

    def test_snapshot_to_dict(self):
        """Test converting snapshot to dict."""
        query_latency = LatencyMetrics(50, 48, 85, 95, 10, 100, 15, 100)
        embedding_latency = LatencyMetrics(10, 9, 15, 18, 5, 20, 3, 100)
        db_query = LatencyMetrics(30, 28, 60, 70, 5, 80, 12, 100)
        total = LatencyMetrics(90, 85, 160, 180, 20, 200, 30, 100)

        snapshot = PerformanceSnapshot(
            timestamp=datetime.utcnow(),
            query_latency=query_latency,
            embedding_latency=embedding_latency,
            db_query_time=db_query,
            total_latency=total,
            recall_at_k={},
            precision_at_k={},
            mrr=0.0,
            ndcg=0.0,
        )

        d = snapshot.to_dict()
        assert "timestamp" in d
        assert d["mrr"] == 0.0
        assert d["ndcg"] == 0.0


class TestStorageMetrics:
    """Test StorageMetrics data class."""

    def test_storage_metrics_creation(self):
        """Test creating storage metrics."""
        metrics = StorageMetrics(
            total_vectors=1000000,
            total_size_mb=512.5,
            avg_vector_size_bytes=512,
            index_overhead_mb=50.0,
            compression_ratio=0.95,
        )
        assert metrics.total_vectors == 1000000
        assert metrics.total_size_mb == 512.5


class TestEmbeddingComparison:
    """Test EmbeddingComparison data class."""

    def test_embedding_comparison_creation(self):
        """Test creating embedding comparison."""
        comparison = EmbeddingComparison(
            model_a="openai-3-small",
            model_b="cohere-v3",
            quality_a={"isotropy": 0.92, "coverage": 0.88},
            quality_b={"isotropy": 0.89, "coverage": 0.90},
            latency_a_ms=15.2,
            latency_b_ms=22.5,
            recall_diff=0.05,
            cost_per_1m_tokens_a=0.02,
            cost_per_1m_tokens_b=0.03,
        )
        assert comparison.model_a == "openai-3-small"
        assert comparison.recall_diff == 0.05


class TestPerformanceBenchmark:
    """Test PerformanceBenchmark class."""

    def test_benchmark_initialization(self):
        """Test initializing benchmarker."""
        benchmark = PerformanceBenchmark()
        assert benchmark.adapter is None
        assert len(benchmark._snapshots) == 0

    def test_measure_query_latency(self):
        """Test measuring query latency."""
        benchmark = PerformanceBenchmark()

        def mock_query():
            time.sleep(0.001)  # 1ms

        metrics = benchmark.measure_query_latency(mock_query, num_iterations=5)
        assert metrics.mean > 0
        assert metrics.p95 > 0
        assert metrics.p99 > 0
        assert metrics.samples == 5

    def test_measure_embedding_latency(self):
        """Test measuring embedding latency."""
        benchmark = PerformanceBenchmark()

        def mock_embedding_fn(embedding):
            time.sleep(0.0005)  # 0.5ms

        embeddings = [np.random.randn(768) for _ in range(5)]
        metrics = benchmark.measure_embedding_latency(mock_embedding_fn, embeddings)

        assert metrics.mean > 0
        assert metrics.samples == 5

    def test_measure_end_to_end_latency(self):
        """Test measuring end-to-end latency."""
        benchmark = PerformanceBenchmark()

        def mock_e2e():
            time.sleep(0.002)  # 2ms

        metrics = benchmark.measure_end_to_end_latency(mock_e2e, num_iterations=5)
        assert metrics.mean > 0
        assert metrics.samples == 5

    def test_compare_databases(self):
        """Test comparing multiple databases."""
        benchmark = PerformanceBenchmark()

        def query_qdrant():
            time.sleep(0.001)

        def query_chroma():
            time.sleep(0.0015)

        results = benchmark.compare_databases(
            {"qdrant": query_qdrant, "chroma": query_chroma}, num_iterations=5
        )

        assert "qdrant" in results
        assert "chroma" in results
        assert results["qdrant"]["mean_ms"] > 0

    def test_compare_embedding_models(self):
        """Test comparing embedding models."""
        benchmark = PerformanceBenchmark()

        model_configs = {
            "openai": {
                "quality_metrics": {"isotropy": 0.92, "coverage": 0.88},
                "latency_ms": 15.2,
                "recall": 0.85,
                "cost_per_1m": 0.02,
            },
            "cohere": {
                "quality_metrics": {"isotropy": 0.89, "coverage": 0.90},
                "latency_ms": 22.5,
                "recall": 0.80,
                "cost_per_1m": 0.03,
            },
        }

        comparisons = benchmark.compare_embedding_models(model_configs, [])
        assert len(comparisons) == 1
        assert comparisons[0].model_a == "openai"
        assert comparisons[0].model_b == "cohere"

    def test_capture_snapshot(self):
        """Test capturing performance snapshot."""
        benchmark = PerformanceBenchmark()

        query_latency = LatencyMetrics(50, 48, 85, 95, 10, 100, 15, 100)
        embedding_latency = LatencyMetrics(10, 9, 15, 18, 5, 20, 3, 100)
        db_query = LatencyMetrics(30, 28, 60, 70, 5, 80, 12, 100)
        total = LatencyMetrics(90, 85, 160, 180, 20, 200, 30, 100)

        snapshot = benchmark.capture_snapshot(
            query_latency=query_latency,
            embedding_latency=embedding_latency,
            db_query_time=db_query,
            total_latency=total,
            recall_at_k={5: 0.8, 10: 0.85},
        )

        assert snapshot is not None
        assert benchmark._baseline == snapshot
        assert len(benchmark._snapshots) == 1

    def test_detect_regression(self):
        """Test detecting performance regression."""
        benchmark = PerformanceBenchmark()

        # Set baseline
        query_latency = LatencyMetrics(50, 48, 85, 95, 10, 100, 15, 100)
        embedding_latency = LatencyMetrics(10, 9, 15, 18, 5, 20, 3, 100)
        db_query = LatencyMetrics(30, 28, 60, 70, 5, 80, 12, 100)
        total = LatencyMetrics(90, 85, 160, 180, 20, 200, 30, 100)

        benchmark.capture_snapshot(
            query_latency, embedding_latency, db_query, total
        )

        # Add degraded snapshot (10% worse)
        degraded_total = LatencyMetrics(99, 93, 176, 198, 22, 220, 33, 100)
        benchmark.capture_snapshot(
            query_latency, embedding_latency, db_query, degraded_total
        )

        regression = benchmark.detect_regression()
        assert regression is not None
        assert "total_latency_increase_pct" in regression

    def test_get_performance_report(self):
        """Test getting performance report."""
        benchmark = PerformanceBenchmark()

        query_latency = LatencyMetrics(50, 48, 85, 95, 10, 100, 15, 100)
        embedding_latency = LatencyMetrics(10, 9, 15, 18, 5, 20, 3, 100)
        db_query = LatencyMetrics(30, 28, 60, 70, 5, 80, 12, 100)
        total = LatencyMetrics(90, 85, 160, 180, 20, 200, 30, 100)

        benchmark.capture_snapshot(
            query_latency, embedding_latency, db_query, total
        )

        report = benchmark.get_performance_report()
        assert "latest_snapshot" in report
        assert report["num_snapshots"] == 1

    def test_compute_latency_metrics(self):
        """Test computing latency statistics."""
        benchmark = PerformanceBenchmark()

        latencies = [10.0, 15.0, 20.0, 25.0, 30.0]
        metrics = benchmark._compute_latency_metrics(latencies)

        assert metrics.mean == 20.0
        assert metrics.median == 20.0
        assert metrics.min == 10.0
        assert metrics.max == 30.0
        assert metrics.samples == 5

    def test_empty_latencies(self):
        """Test handling empty latency list."""
        benchmark = PerformanceBenchmark()

        metrics = benchmark._compute_latency_metrics([])
        assert metrics.mean == 0
        assert metrics.samples == 0
