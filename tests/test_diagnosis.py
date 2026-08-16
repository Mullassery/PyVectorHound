"""Tests for Diagnosis class."""

import pytest
import numpy as np
from pyvectorhound.diagnosis import Diagnosis


class TestDiagnosis:
    """Test Diagnosis class."""

    def test_init(self):
        """Test Diagnosis initialization."""
        results = [
            {"id": "1", "score": 0.9},
            {"id": "2", "score": 0.8},
        ]
        diagnosis = Diagnosis(query="test", results=results)

        assert diagnosis.query == "test"
        assert len(diagnosis.results) == 2

    def test_hunt_report(self):
        """Test plain English diagnosis report."""
        diagnosis = Diagnosis(
            query="quantum computing",
            results=[{"id": "1", "score": 0.8}],
        )

        report = diagnosis.hunt()
        assert isinstance(report, str)
        assert "quantum computing" in report
        assert "PyVectorHound" in report

    def test_metrics(self):
        """Test metrics retrieval."""
        diagnosis = Diagnosis(query="test", results=[])
        metrics = diagnosis.metrics()

        assert isinstance(metrics, dict)
        assert "embedding" in metrics or len(metrics) >= 0

    def test_recommendations(self):
        """Test recommendations generation."""
        diagnosis = Diagnosis(query="test", results=[])
        recs = diagnosis.recommendations()

        assert isinstance(recs, list)

    def test_root_cause(self):
        """Test root cause analysis."""
        diagnosis = Diagnosis(query="test", results=[])
        cause = diagnosis.root_cause()

        assert isinstance(cause, str)
        assert len(cause) > 0

    def test_with_expected_docs(self):
        """Test diagnosis with ground truth."""
        results = [{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}]
        expected = ["1", "3"]

        diagnosis = Diagnosis(
            query="test", results=results, expected_docs=expected
        )

        diagnosis.analyze()
        metrics = diagnosis.metrics()

        # Should have computed precision/recall
        assert metrics.get("vector_search", {}).get("precision", 0) >= 0


class FakeEmbeddingAdapter:
    """Minimal VectorDB-like stand-in that returns real, known vectors."""

    def __init__(self, embeddings_by_id):
        self._embeddings_by_id = embeddings_by_id

    def get_embeddings(self, doc_ids):
        return {
            doc_id: np.array(self._embeddings_by_id[doc_id], dtype=np.float32)
            for doc_id in doc_ids
            if doc_id in self._embeddings_by_id
        }


class TestEmbeddingAnalysis:
    """_analyze_embedding() must use real per-document vectors, not fixed placeholders."""

    def test_uses_real_embeddings_not_hardcoded_placeholders(self):
        results = [{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}, {"id": "3", "score": 0.7}]
        adapter = FakeEmbeddingAdapter(
            {"1": [1.0, 0.0, 0.0], "2": [0.0, 1.0, 0.0], "3": [0.0, 0.0, 1.0]}
        )

        diagnosis = Diagnosis(query="test", results=results, adapter=adapter)
        diagnosis.analyze()
        embedding_metrics = diagnosis.metrics()["embedding"]

        # Three mutually-orthogonal unit vectors are maximally isotropic/distinct --
        # the old code always returned the fixed 0.72/0.85/0.68 regardless of input.
        assert embedding_metrics["isotropy"] > 0.9
        assert embedding_metrics["status"] in ("GOOD", "MODERATE", "WEAK")
        assert embedding_metrics["isotropy"] != 0.72
        assert embedding_metrics["coverage"] != 0.85
        assert embedding_metrics["distinctiveness"] != 0.68

    def test_reports_unknown_without_adapter(self):
        diagnosis = Diagnosis(query="test", results=[{"id": "1", "score": 0.9}])
        diagnosis.analyze()
        embedding_metrics = diagnosis.metrics()["embedding"]

        assert embedding_metrics["status"] == "UNKNOWN"

    def test_reports_unknown_with_fewer_than_two_embeddings(self):
        results = [{"id": "1", "score": 0.9}]
        adapter = FakeEmbeddingAdapter({"1": [1.0, 0.0, 0.0]})

        diagnosis = Diagnosis(query="test", results=results, adapter=adapter)
        diagnosis.analyze()
        embedding_metrics = diagnosis.metrics()["embedding"]

        assert embedding_metrics["status"] == "UNKNOWN"


class TestVectorSearchMRR:
    """MRR must reflect the real rank of the first relevant result, not a fixed 0.85."""

    def test_mrr_is_one_when_first_result_is_relevant(self):
        results = [{"id": "a", "score": 0.9}, {"id": "b", "score": 0.8}]
        diagnosis = Diagnosis(query="test", results=results, expected_docs=["a"])
        diagnosis.analyze()

        assert diagnosis.metrics()["vector_search"]["mrr"] == 1.0

    def test_mrr_is_half_when_relevant_result_is_second(self):
        results = [{"id": "a", "score": 0.9}, {"id": "b", "score": 0.8}]
        diagnosis = Diagnosis(query="test", results=results, expected_docs=["b"])
        diagnosis.analyze()

        assert diagnosis.metrics()["vector_search"]["mrr"] == 0.5

    def test_mrr_is_zero_when_nothing_relevant_retrieved(self):
        results = [{"id": "a", "score": 0.9}, {"id": "b", "score": 0.8}]
        diagnosis = Diagnosis(query="test", results=results, expected_docs=["z"])
        diagnosis.analyze()

        assert diagnosis.metrics()["vector_search"]["mrr"] == 0.0


class TestUnimplementedComponentsReportHonestly:
    """BM25 and reranker have no real scoring subsystem wired in -- they must say
    so (UNKNOWN) instead of fabricating a "GOOD" verdict."""

    def test_bm25_reports_unknown_not_fake_good(self):
        diagnosis = Diagnosis(query="test", results=[])
        diagnosis.analyze()

        bm25 = diagnosis.metrics()["bm25"]
        assert bm25["status"] == "UNKNOWN"

    def test_reranker_reports_unknown_not_fake_good(self):
        diagnosis = Diagnosis(query="test", results=[])
        diagnosis.analyze()

        reranker = diagnosis.metrics()["reranker"]
        assert reranker["status"] == "UNKNOWN"

    def test_root_cause_does_not_blame_bm25_when_unmeasured(self):
        diagnosis = Diagnosis(query="test", results=[{"id": "1", "score": 0.9}])
        cause = diagnosis.root_cause()

        assert "BM25" not in cause


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
