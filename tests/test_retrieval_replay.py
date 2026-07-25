"""Tests for retrieval replay module."""

import pytest
from datetime import datetime
import numpy as np
from pyvectorhound.retrieval_tracing import RetrievalTrace, SearchResult
from pyvectorhound.retrieval_replay import (
    RetrievalReplayer,
    ReplayConfiguration,
    ReplayResult,
    ComponentType,
)


class TestReplayConfiguration:
    """Test ReplayConfiguration."""

    def test_create_configuration(self):
        """Test creating configuration."""
        config = ReplayConfiguration(
            config_id="config_1",
            components={
                ComponentType.CHUNK_SIZE: 500,
                ComponentType.EMBEDDING_MODEL: "openai",
            },
            description="Test config",
        )
        assert config.config_id == "config_1"
        assert ComponentType.CHUNK_SIZE in config.components

    def test_configuration_to_dict(self):
        """Test converting configuration to dict."""
        config = ReplayConfiguration(
            config_id="config_1",
            components={ComponentType.CHUNK_SIZE: 500},
        )
        d = config.to_dict()
        assert d["config_id"] == "config_1"
        assert "chunk_size" in d["components"]


class TestReplayResult:
    """Test ReplayResult."""

    def test_result_creation(self):
        """Test creating replay result."""
        result = ReplayResult(
            config_id="config_1",
            latency_ms=45.2,
            results=[],
            recall_at_k={5: 0.8, 10: 0.85},
            precision_at_k={5: 0.9, 10: 0.85},
            ndcg=0.82,
            mrr=0.75,
            improvement_pct=15.0,
            metadata={},
        )
        assert result.config_id == "config_1"
        assert result.latency_ms == 45.2


class TestRetrievalReplayer:
    """Test RetrievalReplayer."""

    def test_replayer_initialization(self):
        """Test initializing replayer."""
        replayer = RetrievalReplayer()
        assert len(replayer.configurations) == 0
        assert len(replayer.results) == 0

    def test_create_configuration(self):
        """Test creating configuration."""
        replayer = RetrievalReplayer()
        config = replayer.create_configuration(
            "config_1", {ComponentType.CHUNK_SIZE: 500}
        )
        assert config.config_id == "config_1"
        assert "config_1" in replayer.configurations

    def test_replay(self):
        """Test replaying a trace."""
        replayer = RetrievalReplayer()

        # Create test trace
        trace = RetrievalTrace(
            query_id="query_1",
            query_text="test",
            timestamp=datetime.utcnow(),
            query_embedding=np.random.randn(768),
            embedding_model="openai",
            embedding_latency_ms=15.0,
            vector_search_results=[
                SearchResult(
                    doc_id="doc_1", content="content", score=0.9, is_relevant=True
                ),
                SearchResult(
                    doc_id="doc_2", content="content", score=0.8, is_relevant=False
                ),
            ],
        )

        # Create configuration
        replayer.create_configuration(
            "config_1", {ComponentType.CHUNK_SIZE: 500}
        )

        # Register a dummy handler
        def dummy_handler(trace, component, results):
            return results, {"applied": True}

        replayer.register_component_handler(ComponentType.CHUNK_SIZE, dummy_handler)

        # Replay
        result = replayer.replay(trace, "config_1")
        assert result.config_id == "config_1"
        assert len(result.results) > 0

    def test_compare_configurations(self):
        """Test comparing configurations."""
        replayer = RetrievalReplayer()

        # Create test trace
        trace = RetrievalTrace(
            query_id="query_1",
            query_text="test",
            timestamp=datetime.utcnow(),
            query_embedding=np.random.randn(768),
            embedding_model="openai",
            embedding_latency_ms=15.0,
            vector_search_results=[
                SearchResult(
                    doc_id="doc_1", content="content", score=0.9, is_relevant=True
                )
            ],
        )

        # Create configurations and dummy handler
        replayer.create_configuration("config_1", {ComponentType.CHUNK_SIZE: 500})
        replayer.create_configuration("config_2", {ComponentType.CHUNK_SIZE: 1000})

        def dummy_handler(trace, component, results):
            return results, {"applied": True}

        replayer.register_component_handler(ComponentType.CHUNK_SIZE, dummy_handler)

        # Replay both
        replayer.replay(trace, "config_1")
        replayer.replay(trace, "config_2")

        # Compare
        comparison = replayer.compare_configurations("config_1", "config_2")
        assert comparison is not None
        assert comparison.baseline_config_id == "config_1"

    def test_rank_configurations_by_recall(self):
        """Test ranking by recall."""
        replayer = RetrievalReplayer()

        # Create dummy results
        result1 = ReplayResult(
            config_id="config_1",
            latency_ms=50.0,
            results=[],
            recall_at_k={5: 0.8},
            precision_at_k={},
            ndcg=0.8,
            mrr=0.75,
            improvement_pct=0,
            metadata={},
        )

        result2 = ReplayResult(
            config_id="config_2",
            latency_ms=45.0,
            results=[],
            recall_at_k={5: 0.9},
            precision_at_k={},
            ndcg=0.85,
            mrr=0.8,
            improvement_pct=0,
            metadata={},
        )

        replayer.results["config_1"] = result1
        replayer.results["config_2"] = result2

        ranked = replayer.rank_configurations_by_recall()
        assert ranked[0].config_id == "config_2"
        assert ranked[0].recall_at_k[5] == 0.9

    def test_rank_configurations_by_latency(self):
        """Test ranking by latency."""
        replayer = RetrievalReplayer()

        result1 = ReplayResult(
            config_id="config_1",
            latency_ms=50.0,
            results=[],
            recall_at_k={5: 0.8},
            precision_at_k={},
            ndcg=0.8,
            mrr=0.75,
            improvement_pct=0,
            metadata={},
        )

        result2 = ReplayResult(
            config_id="config_2",
            latency_ms=30.0,
            results=[],
            recall_at_k={5: 0.8},
            precision_at_k={},
            ndcg=0.8,
            mrr=0.75,
            improvement_pct=0,
            metadata={},
        )

        replayer.results["config_1"] = result1
        replayer.results["config_2"] = result2

        ranked = replayer.rank_configurations_by_latency()
        assert ranked[0].config_id == "config_2"
        assert ranked[0].latency_ms == 30.0

    def test_rank_configurations_by_efficiency(self):
        """Test ranking by efficiency."""
        replayer = RetrievalReplayer()

        result1 = ReplayResult(
            config_id="config_1",
            latency_ms=50.0,
            results=[],
            recall_at_k={5: 0.5},
            precision_at_k={},
            ndcg=0.5,
            mrr=0.5,
            improvement_pct=0,
            metadata={},
        )

        result2 = ReplayResult(
            config_id="config_2",
            latency_ms=60.0,
            results=[],
            recall_at_k={5: 0.9},
            precision_at_k={},
            ndcg=0.9,
            mrr=0.9,
            improvement_pct=0,
            metadata={},
        )

        replayer.results["config_1"] = result1
        replayer.results["config_2"] = result2

        ranked = replayer.rank_configurations_by_efficiency()
        # Config 2 has better efficiency: 0.9/60 vs 0.5/50
        assert ranked[0].config_id == "config_2"

    def test_get_configuration_report(self):
        """Test getting configuration report."""
        replayer = RetrievalReplayer()

        result1 = ReplayResult(
            config_id="config_1",
            latency_ms=50.0,
            results=[],
            recall_at_k={5: 0.8, 10: 0.85},
            precision_at_k={},
            ndcg=0.8,
            mrr=0.75,
            improvement_pct=0,
            metadata={},
        )

        result2 = ReplayResult(
            config_id="config_2",
            latency_ms=45.0,
            results=[],
            recall_at_k={5: 0.9, 10: 0.92},
            precision_at_k={},
            ndcg=0.85,
            mrr=0.8,
            improvement_pct=0,
            metadata={},
        )

        replayer.results["config_1"] = result1
        replayer.results["config_2"] = result2

        report = replayer.get_configuration_report()
        assert report["num_configurations_tested"] == 2
        assert "best_by_recall" in report
        assert "best_by_latency" in report

    def test_compute_recall_at_k(self):
        """Test computing recall."""
        replayer = RetrievalReplayer()

        results = [
            SearchResult(
                doc_id="doc_1", content="content", score=0.9, is_relevant=True
            ),
            SearchResult(
                doc_id="doc_2", content="content", score=0.8, is_relevant=True
            ),
            SearchResult(
                doc_id="doc_3", content="content", score=0.7, is_relevant=False
            ),
        ]

        recall = replayer._compute_recall_at_k(results)
        assert 1 in recall
        assert 5 in recall
        assert recall[1] == 1.0  # First result is relevant

    def test_compute_ndcg(self):
        """Test computing NDCG."""
        replayer = RetrievalReplayer()

        results = [
            SearchResult(
                doc_id="doc_1", content="content", score=0.9, is_relevant=True
            ),
            SearchResult(
                doc_id="doc_2", content="content", score=0.8, is_relevant=True
            ),
        ]

        ndcg = replayer._compute_ndcg(results)
        assert ndcg > 0
        assert ndcg <= 1.0

    def test_compute_mrr(self):
        """Test computing MRR."""
        replayer = RetrievalReplayer()

        results = [
            SearchResult(
                doc_id="doc_1", content="content", score=0.9, is_relevant=False
            ),
            SearchResult(
                doc_id="doc_2", content="content", score=0.8, is_relevant=True
            ),
        ]

        mrr = replayer._compute_mrr(results)
        assert mrr == 0.5  # First relevant at position 2

    def test_generate_recommendation(self):
        """Test generating recommendation."""
        replayer = RetrievalReplayer()

        result1 = ReplayResult(
            config_id="config_1",
            latency_ms=50.0,
            results=[],
            recall_at_k={5: 0.8},
            precision_at_k={},
            ndcg=0.8,
            mrr=0.75,
            improvement_pct=0,
            metadata={},
        )

        result2 = ReplayResult(
            config_id="config_2",
            latency_ms=60.0,
            results=[],
            recall_at_k={5: 0.95},
            precision_at_k={},
            ndcg=0.9,
            mrr=0.85,
            improvement_pct=0,
            metadata={},
        )

        rec = replayer._generate_recommendation(result1, result2, 20.0, 15.0)
        assert isinstance(rec, str)
        assert len(rec) > 0
