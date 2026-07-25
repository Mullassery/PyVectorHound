"""Tests for v0.5 Enterprise Integration features."""

import pytest
import numpy as np
from datetime import datetime

# Database adapters
from pyvectorhound.db_adapters import (
    DatabaseType,
    DatabaseConfig,
    MockDatabaseAdapter,
    SearchResult,
    AdapterFactory,
)

# LangChain integration
from pyvectorhound.langchain_integration import (
    PyVectorHoundCallbackHandler,
    InstrumentedRetriever,
)

# LlamaIndex integration
from pyvectorhound.llamaindex_integration import (
    PyVectorHoundInstrumentationCallback,
    DiagnosticVectorIndexRetriever,
)

# OpenTelemetry
from pyvectorhound.otel_integration import (
    OTelConfig,
    OTelBackend,
    OTelInstrument,
    TraceSpan,
    Metric,
)

# Advanced Analytics
from pyvectorhound.advanced_analytics import (
    AdvancedAnalytics,
    CostModel,
    OptimizationRecommendation,
)


class TestDatabaseAdapters:
    """Test database adapter interface."""

    def test_database_config(self):
        """Test database configuration."""
        config = DatabaseConfig(
            db_type=DatabaseType.QDRANT,
            endpoint="localhost:6333",
            index_name="documents",
        )
        assert config.db_type == DatabaseType.QDRANT
        assert config.endpoint == "localhost:6333"

    def test_mock_adapter_creation(self):
        """Test creating mock adapter."""
        config = DatabaseConfig(
            db_type=DatabaseType.QDRANT,
            endpoint="localhost:6333",
        )
        adapter = MockDatabaseAdapter(config)
        assert adapter.db_type == DatabaseType.QDRANT

    def test_mock_adapter_operations(self):
        """Test mock adapter basic operations."""
        config = DatabaseConfig(
            db_type=DatabaseType.QDRANT,
            endpoint="localhost:6333",
        )
        adapter = MockDatabaseAdapter(config)

        # Connect
        assert adapter.connect()
        assert adapter.health_check()

        # Create index
        assert adapter.create_index()
        assert adapter.index_exists()

        # Upsert
        vectors = [np.random.randn(768) for _ in range(3)]
        ids = ["doc_1", "doc_2", "doc_3"]
        metadata = [{"content": f"content_{i}"} for i in range(3)]
        assert adapter.upsert(vectors, ids, metadata)

        # Search
        query_vector = np.random.randn(768)
        results = adapter.search(query_vector, top_k=2)
        assert len(results) <= 2
        assert all(isinstance(r, SearchResult) for r in results)

        # Count
        assert adapter.count_documents() == 3

        # Delete
        assert adapter.delete(["doc_1"])
        assert adapter.count_documents() == 2

        # Disconnect
        adapter.disconnect()
        assert not adapter.health_check()

    def test_adapter_factory(self):
        """Test adapter factory."""
        config = DatabaseConfig(
            db_type=DatabaseType.QDRANT,
            endpoint="localhost:6333",
        )
        adapter = AdapterFactory.create(config)
        assert adapter is not None


class TestOpenTelemetry:
    """Test OpenTelemetry integration."""

    def test_otel_config(self):
        """Test OTel configuration."""
        config = OTelConfig(
            service_name="test_service",
            backend=OTelBackend.LOGGING,
        )
        assert config.service_name == "test_service"
        assert config.backend == OTelBackend.LOGGING

    def test_trace_span(self):
        """Test trace span."""
        span = TraceSpan("test_span")
        assert span.name == "test_span"
        assert span.status == "OK"

        span.set_attribute("key", "value")
        assert span.attributes["key"] == "value"

        span.end()
        assert span.end_time is not None
        assert span.duration_ms() > 0

    def test_metric(self):
        """Test metric."""
        metric = Metric("test_metric", 42.5, "ms")
        assert metric.name == "test_metric"
        assert metric.value == 42.5
        assert metric.unit == "ms"

    def test_otel_instrument(self):
        """Test OTel instrumentation."""
        config = OTelConfig(backend=OTelBackend.LOGGING)
        instrument = OTelInstrument(config)

        # Record metric
        instrument.record_metric("test_metric", 100.0, "ms")

        # Start and record span
        span = instrument.start_span("test_operation")
        span.set_attribute("test", "value")
        instrument.record_span(span)

        # Get stats
        stats = instrument.get_stats()
        assert stats["total_spans"] >= 0
        assert stats["total_metrics"] >= 0


class TestAdvancedAnalytics:
    """Test advanced analytics."""

    def test_analytics_initialization(self):
        """Test analytics engine initialization."""
        analytics = AdvancedAnalytics()
        assert len(analytics._cost_models) > 0

    def test_register_performance_data(self):
        """Test registering performance data."""
        analytics = AdvancedAnalytics()
        analytics.register_performance_data(
            "Qdrant",
            avg_latency_ms=50.0,
            p95_latency_ms=85.0,
            p99_latency_ms=120.0,
            throughput_qps=1000,
            recall_avg=0.85,
        )
        assert "Qdrant" in analytics._performance_data

    def test_cost_estimation(self):
        """Test cost estimation."""
        analytics = AdvancedAnalytics()
        costs = analytics.estimate_monthly_cost("Qdrant Cloud", num_documents=1_000_000)
        assert "total_monthly" in costs
        assert costs["total_monthly"] >= 0

    def test_database_comparison(self):
        """Test database comparison."""
        analytics = AdvancedAnalytics()

        # Register test data
        analytics.register_performance_data(
            "Qdrant", 50.0, 85.0, 120.0, 1000, 0.85
        )
        analytics.register_performance_data(
            "Pinecone", 45.0, 80.0, 115.0, 1200, 0.88
        )

        # Compare
        comparison = analytics.compare_databases(
            ["Qdrant", "Pinecone"],
            optimization_goal="balanced",
        )

        assert len(comparison["databases"]) == 2
        assert comparison["best_by_latency"] is not None


class TestLangChainIntegration:
    """Test LangChain integration."""

    def test_callback_handler_creation(self):
        """Test creating callback handler."""
        handler = PyVectorHoundCallbackHandler()
        assert handler.config.enabled

    def test_instrumented_retriever_creation(self):
        """Test creating instrumented retriever."""
        # Mock retriever
        class MockRetriever:
            def get_relevant_documents(self, query: str):
                return []

        retriever = MockRetriever()
        instrumented = InstrumentedRetriever(retriever)
        assert instrumented.retriever == retriever


class TestLlamaIndexIntegration:
    """Test LlamaIndex integration."""

    def test_callback_creation(self):
        """Test creating instrumentation callback."""
        callback = PyVectorHoundInstrumentationCallback()
        assert callback.config.enabled

    def test_diagnostic_retriever_creation(self):
        """Test creating diagnostic retriever."""
        # Mock retriever
        class MockRetriever:
            def retrieve(self, query_str: str):
                return []

        retriever = MockRetriever()
        diagnostic = DiagnosticVectorIndexRetriever(retriever)
        assert diagnostic.retriever == retriever


class TestIntegration:
    """End-to-end integration tests."""

    def test_full_workflow_mock_adapter(self):
        """Test full workflow with mock adapter."""
        # Create adapter
        config = DatabaseConfig(
            db_type=DatabaseType.QDRANT,
            endpoint="localhost:6333",
        )
        adapter = MockDatabaseAdapter(config)

        # Connect and prepare
        adapter.connect()
        adapter.create_index()

        # Add some data
        vectors = [np.random.randn(768) for _ in range(10)]
        ids = [f"doc_{i}" for i in range(10)]
        metadata = [{"content": f"content_{i}"} for i in range(10)]
        adapter.upsert(vectors, ids, metadata)

        # Search
        query = np.random.randn(768)
        results = adapter.search(query, top_k=5)

        assert len(results) <= 5
        for result in results:
            assert result.doc_id in ids

        adapter.disconnect()

    def test_analytics_workflow(self):
        """Test analytics workflow."""
        analytics = AdvancedAnalytics()

        # Register performance data for multiple databases
        analytics.register_performance_data(
            "Qdrant", 50.0, 85.0, 120.0, 1000, 0.85
        )
        analytics.register_performance_data(
            "Pinecone", 45.0, 80.0, 115.0, 1200, 0.88
        )
        analytics.register_performance_data(
            "Weaviate", 60.0, 95.0, 130.0, 800, 0.82
        )

        # Compare databases
        comparison = analytics.compare_databases(
            ["Qdrant", "Pinecone", "Weaviate"],
            optimization_goal="latency",
        )

        assert len(comparison["databases"]) == 3
        assert comparison["best_by_latency"] is not None

        # Estimate costs
        qdrant_costs = analytics.estimate_monthly_cost("Qdrant")
        assert qdrant_costs["total_monthly"] >= 0

        # Get optimization recommendations
        from pyvectorhound.advanced_analytics import PerformanceCharacteristics

        current_perf = PerformanceCharacteristics(
            database_name="Qdrant",
            avg_query_latency_ms=50.0,
            p95_query_latency_ms=85.0,
            p99_query_latency_ms=120.0,
            throughput_qps=1000,
            recall_avg=0.85,
            scalability_score=75.0,
        )

        recommendations = analytics.get_optimization_recommendations(
            "Qdrant",
            current_perf,
            constraints={"max_latency_ms": 40},
        )

        assert isinstance(recommendations, list)
