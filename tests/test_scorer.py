"""Tests for QualityScorer.

score()/corpus_health()/trend_analysis() used to return fixed placeholder
numbers (e.g. isotropy always 0.72) regardless of the real embeddings passed
in. These tests verify the metrics actually respond to real input data.
"""

import numpy as np
import pytest

from pyvectorhound.scorer import QualityScorer


class FakeAdapter:
    """Minimal adapter stand-in: search() returns fixed neighbor ids,
    get_embeddings() returns real, known vectors for those ids."""

    def __init__(self, embeddings_by_id, corpus_size=0):
        self._embeddings_by_id = embeddings_by_id
        self._corpus_size = corpus_size

    def search(self, query_embedding, top_k=10):
        ids = list(self._embeddings_by_id.keys())[:top_k]
        return [{"id": doc_id, "score": 0.5} for doc_id in ids]

    def get_embeddings(self, doc_ids):
        return {
            doc_id: np.array(self._embeddings_by_id[doc_id], dtype=np.float32)
            for doc_id in doc_ids
            if doc_id in self._embeddings_by_id
        }

    def corpus_size(self):
        return self._corpus_size


class TestQualityScorerScore:
    def test_score_without_adapter_is_honestly_unknown_not_fake_good(self):
        scorer = QualityScorer()
        result = scorer.score(np.array([1.0, 2.0, 3.0]))

        # A single vector in isolation has no isotropy/coverage/distinctiveness --
        # the old code claimed fixed 0.72/0.85/0.68 regardless.
        assert result["status"] == "UNKNOWN"
        assert result["isotropy"] == 0.0
        assert result["coverage"] == 0.0
        assert result["distinctiveness"] == 0.0

    def test_score_with_adapter_uses_real_neighbor_embeddings(self):
        adapter = FakeAdapter(
            {"1": [1.0, 0.0, 0.0], "2": [0.0, 1.0, 0.0], "3": [0.0, 0.0, 1.0]}
        )
        scorer = QualityScorer(adapter=adapter)

        result = scorer.score(np.array([1.0, 0.0, 0.0], dtype=np.float32))

        assert result["sample_size"] == 4  # the query embedding + 3 real neighbors
        assert result["isotropy"] != 0.72
        assert result["coverage"] != 0.85
        assert result["distinctiveness"] != 0.68
        assert result["status"] in ("GOOD", "MODERATE", "WEAK")


class TestQualityScorerCorpusHealth:
    def test_corpus_health_without_adapter_is_honest(self):
        scorer = QualityScorer()
        health = scorer.corpus_health()

        assert health["corpus_size"] == 0
        assert health["status"] == "UNKNOWN"
        assert health["drift"] is None
        assert health["trend"] == "unknown"

    def test_corpus_health_uses_real_sampled_embeddings(self):
        adapter = FakeAdapter(
            {"1": [1.0, 0.0], "2": [0.0, 1.0], "3": [-1.0, 0.0]}, corpus_size=3
        )
        scorer = QualityScorer(adapter=adapter)

        health = scorer.corpus_health()

        assert health["corpus_size"] == 3
        assert health["sample_size"] == 3
        assert health["avg_isotropy"] != 0.73
        assert health["avg_coverage"] != 0.82


class TestQualityScorerTrendAnalysis:
    def test_trend_analysis_is_honest_about_not_tracking_history(self):
        scorer = QualityScorer()
        trend = scorer.trend_analysis(baseline_date="2026-01-01", current_date="2026-06-20")

        # The old code claimed a fixed "stable"/0.02 magnitude for any date range
        # without looking at any actual historical data.
        assert trend["direction"] == "unknown"
        assert trend["magnitude"] is None
        assert trend["components"] == {}


class TestQualityScorerDynamicCalibration:
    """GOOD/MODERATE/WEAK classification should use a tracked TrendAnalyzer
    baseline (relative, model-agnostic) instead of the fixed 0.75/0.5 cutoff
    once one exists, same pattern as Diagnosis._classify(). Exercises
    QualityScorer._classify() directly rather than going through score(),
    since score()'s real computation depends on the compiled _core
    extension being available in the test environment."""

    def test_falls_back_to_fixed_cutoff_without_trend_analyzer(self):
        scorer = QualityScorer()
        assert scorer._classify(0.6) == "MODERATE"
        assert scorer._classify(0.8) == "GOOD"
        assert scorer._classify(0.3) == "WEAK"

    def test_uses_baseline_when_trend_analyzer_has_one(self):
        from pyvectorhound.trend_analysis import TrendAnalyzer

        analyzer = TrendAnalyzer()
        # 0.55 would be MODERATE under the fixed cutoff, but this corpus's
        # own historical baseline is centered low with tight spread, so 0.55
        # is actually GOOD relative to its own history.
        analyzer.set_baseline("embedding_overall", {"mean": 0.4, "stddev": 0.05})

        scorer = QualityScorer(trend_analyzer=analyzer)
        assert scorer._classify(0.55) == "GOOD"


class TestQualityScorerAnomalyDetection:
    """detect_anomalies() already did real statistics -- a quick sanity check
    that it still does, since it wasn't touched by this fix."""

    def test_detects_outlier_by_magnitude(self):
        scorer = QualityScorer()
        normal = [np.array([1.0, 1.0], dtype=np.float32) for _ in range(5)]
        outlier = np.array([100.0, 100.0], dtype=np.float32)

        result = scorer.detect_anomalies(normal + [outlier])

        assert 5 in result["outliers"]
