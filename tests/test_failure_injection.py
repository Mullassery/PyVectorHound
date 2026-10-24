"""Failure-injection tests for the vector-DB boundary (RECHECK-035).

The happy-path suite (`test_database_adapters.py`) proves adapters return real
vectors. These tests inject the failure modes that actually bite in production —
dimension mismatch, backend errors such as a payload filter on an unindexed
field, absent vectors, and embedding drift — and assert the code fails loudly or
flags the anomaly instead of fabricating data.
"""

import numpy as np
import pytest

from pyvectorhound.database import ChromaAdapter, MilvusAdapter, QdrantAdapter
from pyvectorhound.trend_analysis import TrendAnalyzer
from pyvectorhound.validation import VectorSearchQuery, validate_embedding_vector


class TestDimensionMismatch:
    def test_validate_embedding_vector_rejects_wrong_dimension(self):
        with pytest.raises(ValueError, match="dimension mismatch"):
            validate_embedding_vector([0.1, 0.2, 0.3], dimension=1536)

    def test_validate_embedding_vector_rejects_nan(self):
        with pytest.raises(ValueError, match="NaN or Inf"):
            validate_embedding_vector([0.1, float("nan")], dimension=2)

    def test_validate_embedding_vector_rejects_inf(self):
        with pytest.raises(ValueError, match="NaN or Inf"):
            validate_embedding_vector([0.1, float("inf")], dimension=2)

    def test_validate_embedding_vector_rejects_non_vector_type(self):
        with pytest.raises(ValueError, match="list or ndarray"):
            validate_embedding_vector("not-a-vector", dimension=1)  # type: ignore[arg-type]

    def test_search_query_rejects_zero_magnitude_vector(self):
        with pytest.raises(ValueError):
            VectorSearchQuery(vector=[0.0, 0.0, 0.0])

    def test_search_query_rejects_nan(self):
        with pytest.raises(ValueError):
            VectorSearchQuery(vector=[1.0, float("nan")])


class _RaisingClient:
    """A client whose every call raises, to prove errors are not swallowed."""

    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def search(self, *args, **kwargs):
        raise self._exc

    def retrieve(self, *args, **kwargs):
        raise self._exc

    def get(self, *args, **kwargs):
        raise self._exc


class TestBackendFailureInjection:
    def test_qdrant_search_error_propagates(self):
        """A backend error (e.g. filtering on an unindexed payload field) must
        surface, not be turned into a silent empty result."""
        adapter = QdrantAdapter(endpoint="http://localhost:6333", index_name="docs")
        adapter.client = _RaisingClient(RuntimeError("filter on unindexed payload field 'tenant'"))
        with pytest.raises(RuntimeError, match="unindexed payload"):
            adapter.search(np.ones(3, dtype=np.float32), top_k=5)

    def test_qdrant_get_embeddings_non_numeric_id_raises(self):
        adapter = QdrantAdapter(endpoint="http://localhost:6333", index_name="docs")
        adapter.client = _RaisingClient(ValueError("unreachable"))
        with pytest.raises(ValueError):
            adapter.get_embeddings(["not-an-int"])

    def test_milvus_get_embeddings_skips_records_without_vector(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")

        class Client:
            def get(self, collection_name, ids, output_fields=None):
                return [
                    {"id": "doc_1", "vector": [1.0, 2.0]},
                    {"id": "doc_2", "vector": None},
                ]

        adapter.client = Client()
        adapter.collection = "docs"

        embeddings = adapter.get_embeddings(["doc_1", "doc_2"])

        assert "doc_1" in embeddings
        assert "doc_2" not in embeddings

    def test_chroma_search_falls_back_when_backend_omits_embeddings(self):
        adapter = ChromaAdapter(endpoint="", index_name="docs")

        class Collection:
            def query(self, query_embeddings, n_results, include=None):
                return {"ids": [["doc_1"]], "distances": [[0.42]], "embeddings": None}

        adapter.collection = Collection()
        query = np.array([1.0, 2.0], dtype=np.float32)

        out = adapter.search(query, top_k=1)

        assert out[0]["id"] == "doc_1"
        np.testing.assert_array_equal(out[0]["embedding"], query)


class TestEmbeddingDriftInjection:
    def test_drift_detected_when_quality_degrades(self):
        analyzer = TrendAnalyzer()
        analyzer.set_baseline("embedding_isotropy", {"mean": 0.50, "stddev": 0.01})
        for _ in range(12):
            analyzer.track_metric("embedding_isotropy", 0.90)

        drift = analyzer.detect_drift("embedding_isotropy")

        assert drift is not None
        assert drift.is_anomaly
        assert drift.drift_direction == "up"

    def test_no_drift_when_metric_stable(self):
        analyzer = TrendAnalyzer()
        analyzer.set_baseline("embedding_isotropy", {"mean": 0.50, "stddev": 0.01})
        for _ in range(12):
            analyzer.track_metric("embedding_isotropy", 0.501)

        drift = analyzer.detect_drift("embedding_isotropy")

        assert drift is not None
        assert not drift.is_anomaly
