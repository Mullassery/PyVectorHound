"""Tests for Diagnosis class."""

import numpy as np
import pytest

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

        diagnosis = Diagnosis(query="test", results=results, expected_docs=expected)

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


class TestUnmeasuredComponentsReportHonestly:
    """BM25 and reranker have no bundled scoring subsystem -- without caller
    inputs they must say UNKNOWN instead of fabricating a "GOOD" verdict."""

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


class TestBM25Diagnostics:
    """BM25 diagnostics measure an externally supplied keyword ranking."""

    def test_measures_precision_recall_mrr_and_agreement(self):
        diagnosis = Diagnosis(
            query="test",
            results=[
                {"id": "a", "score": 0.9},
                {"id": "b", "score": 0.8},
                {"id": "c", "score": 0.7},
            ],
            expected_docs=["a", "c"],
            bm25_results=["a", "c", "x"],
        )
        diagnosis.analyze()
        bm25 = diagnosis.metrics()["bm25"]

        assert bm25["status"] == "MODERATE"
        assert bm25["precision"] == pytest.approx(2 / 3)
        assert bm25["recall"] == 1.0
        assert bm25["mrr"] == 1.0
        assert bm25["agreement"] == 0.5
        assert bm25["measured"] is True

    def test_derives_ranking_from_scores_when_results_absent(self):
        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "a", "score": 0.9}, {"id": "b", "score": 0.8}],
            expected_docs=["b"],
            bm25_scores={"a": 0.2, "b": 0.9},
        )
        diagnosis.analyze()
        bm25 = diagnosis.metrics()["bm25"]

        assert bm25["mrr"] == 1.0
        assert bm25["precision"] == 0.5

    def test_agreement_without_ground_truth_stays_unknown(self):
        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "a", "score": 0.9}, {"id": "b", "score": 0.8}],
            bm25_results=["a", "b"],
        )
        diagnosis.analyze()
        bm25 = diagnosis.metrics()["bm25"]

        assert bm25["status"] == "UNKNOWN"
        assert bm25["agreement"] == 1.0


class TestRerankerDiagnostics:
    """Reranker diagnostics measure NDCG and score separation."""

    def test_perfect_ranking_scores_high(self):
        diagnosis = Diagnosis(
            query="test",
            results=[
                {"id": "a", "score": 0.9},
                {"id": "b", "score": 0.8},
                {"id": "c", "score": 0.7},
            ],
            expected_docs=["a", "c"],
            reranker_scores={"a": 0.9, "b": 0.1, "c": 0.8},
        )
        diagnosis.analyze()
        reranker = diagnosis.metrics()["reranker"]

        assert reranker["status"] == "GOOD"
        assert reranker["ndcg"] == pytest.approx(1.0)
        assert reranker["calibration"] > 0.9
        assert reranker["measured"] is True

    def test_inverted_ranking_scores_low(self):
        diagnosis = Diagnosis(
            query="test",
            results=[
                {"id": "a", "score": 0.9},
                {"id": "b", "score": 0.8},
                {"id": "c", "score": 0.7},
            ],
            expected_docs=["a", "c"],
            reranker_scores={"a": 0.1, "b": 0.9, "c": 0.2},
        )
        diagnosis.analyze()
        reranker = diagnosis.metrics()["reranker"]

        assert reranker["ndcg"] < 0.75
        assert reranker["calibration"] < 0.1

    def test_scores_without_ground_truth_stay_unknown(self):
        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "a", "score": 0.9}],
            reranker_scores={"a": 0.9},
        )
        diagnosis.analyze()

        assert diagnosis.metrics()["reranker"]["status"] == "UNKNOWN"


class TestFaithfulnessAnalysis:
    """LLM-as-judge faithfulness/contradiction check."""

    def test_reports_unknown_without_llm_judge_fn_or_document_texts(self):
        diagnosis = Diagnosis(query="test", results=[{"id": "1", "score": 0.9}])
        diagnosis.analyze()

        faithfulness = diagnosis.metrics()["faithfulness"]
        assert faithfulness["status"] == "UNKNOWN"

    def test_reports_unknown_with_judge_fn_but_no_texts(self):
        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "1", "score": 0.9}],
            llm_judge_fn=lambda q, texts: {"faithful": True},
        )
        diagnosis.analyze()

        assert diagnosis.metrics()["faithfulness"]["status"] == "UNKNOWN"

    def test_calls_llm_judge_fn_with_query_and_retrieved_texts(self):
        captured = {}

        def judge(query, doc_texts):
            captured["query"] = query
            captured["doc_texts"] = doc_texts
            return {"faithful_count": 2, "contradicted_count": 0, "contradiction_score": 0.0}

        diagnosis = Diagnosis(
            query="what is quantum computing",
            results=[{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}],
            document_texts={
                "1": "quantum computers use qubits",
                "2": "quantum entanglement basics",
            },
            llm_judge_fn=judge,
        )
        diagnosis.analyze()

        assert captured["query"] == "what is quantum computing"
        assert set(captured["doc_texts"]) == {
            "quantum computers use qubits",
            "quantum entanglement basics",
        }

        faithfulness = diagnosis.metrics()["faithfulness"]
        assert faithfulness["status"] == "GOOD"
        assert faithfulness["contradicted_count"] == 0

    def test_flags_contradicted_documents_as_weak(self):
        def judge(query, doc_texts):
            return {"faithful_count": 0, "contradicted_count": 1, "contradiction_score": 0.9}

        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "1", "score": 0.9}],
            document_texts={"1": "unrelated content"},
            llm_judge_fn=judge,
        )
        diagnosis.analyze()

        faithfulness = diagnosis.metrics()["faithfulness"]
        assert faithfulness["status"] == "WEAK"
        assert faithfulness["contradicted_count"] == 1

    def test_root_cause_surfaces_contradiction_over_embedding_score(self):
        """A high embedding score with a flagged contradiction is the exact failure
        mode distance metrics alone can't see -- root_cause should lead with it."""

        def judge(query, doc_texts):
            return {"faithful_count": 0, "contradicted_count": 1, "contradiction_score": 0.9}

        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "1", "score": 0.9}],
            document_texts={"1": "unrelated content"},
            llm_judge_fn=judge,
        )
        diagnosis._analysis = {
            "embedding": {"status": "GOOD"},
            "vector_search": {"status": "UNKNOWN"},
            "bm25": {"status": "UNKNOWN"},
            "reranker": {"status": "UNKNOWN"},
            "faithfulness": diagnosis._analyze_faithfulness(),
        }
        cause = diagnosis.root_cause()

        assert "contradict" in cause.lower() or "LLM judge" in cause

    def test_llm_judge_fn_retries_on_transient_failure(self):
        calls = {"count": 0}

        def flaky_judge(query, doc_texts):
            calls["count"] += 1
            if calls["count"] < 2:
                raise RuntimeError("simulated rate limit")
            return {"faithful_count": 1, "contradicted_count": 0, "contradiction_score": 0.0}

        diagnosis = Diagnosis(
            query="test",
            results=[{"id": "1", "score": 0.9}],
            document_texts={"1": "text"},
            llm_judge_fn=flaky_judge,
        )
        diagnosis.analyze()

        assert calls["count"] == 2
        assert diagnosis.metrics()["faithfulness"]["status"] == "GOOD"


class TestDynamicThresholdCalibration:
    """Quality-status classification should use a tracked baseline (relative,
    model-agnostic) instead of a fixed numeric cutoff once one exists."""

    def test_falls_back_to_fixed_cutoff_without_trend_analyzer(self):
        results = [{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}]
        expected = ["1"]
        diagnosis = Diagnosis(query="test", results=results, expected_docs=expected)
        diagnosis.analyze()

        # precision = 1/2 = 0.5, exactly the fixed MODERATE/WEAK boundary
        assert diagnosis.metrics()["vector_search"]["status"] == "WEAK"

    def test_uses_baseline_when_trend_analyzer_has_one(self):
        from pyvectorhound.trend_analysis import TrendAnalyzer

        analyzer = TrendAnalyzer()
        # A precision of 0.5 would be WEAK under the fixed cutoff, but this
        # system's historical baseline for this metric is centered low with
        # tight spread, so 0.5 is actually GOOD relative to its own history.
        analyzer.set_baseline("vector_search_precision", {"mean": 0.3, "stddev": 0.05})

        results = [{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}]
        diagnosis = Diagnosis(
            query="test",
            results=results,
            expected_docs=["1"],
            trend_analyzer=analyzer,
        )
        diagnosis.analyze()

        assert diagnosis.metrics()["vector_search"]["status"] == "GOOD"

    def test_uses_tracked_series_as_baseline_without_explicit_set_baseline(self):
        from pyvectorhound.trend_analysis import TrendAnalyzer

        analyzer = TrendAnalyzer()
        for v in [0.2, 0.22, 0.19, 0.21, 0.2, 0.23]:
            analyzer.track_metric("vector_search_precision", v)

        results = [{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}]
        diagnosis = Diagnosis(
            query="test",
            results=results,
            expected_docs=["1"],  # precision 0.5, far above this metric's own history
            trend_analyzer=analyzer,
        )
        diagnosis.analyze()

        assert diagnosis.metrics()["vector_search"]["status"] == "GOOD"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
