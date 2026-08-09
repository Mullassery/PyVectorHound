"""Embedding quality scoring and monitoring."""

from typing import Dict, Any, List, Optional
import numpy as np

try:
    from pyvectorhound import _core
except ImportError:
    _core = None


class QualityScorer:
    """
    Score and monitor embedding quality in real-time.

    Provides metrics like isotropy, coverage, and distinctiveness
    for detecting embedding degradation.
    """

    def __init__(self, hound: Optional[Any] = None, adapter: Optional[Any] = None):
        """
        Initialize QualityScorer.

        Args:
            hound: Optional Hound instance for corpus access
            adapter: Database adapter for corpus operations
        """
        self.hound = hound
        self.adapter = adapter
        self._cache = {}
        self._baseline_metrics = None

    def score(self, embedding: np.ndarray) -> Dict[str, Any]:
        """
        Score a single embedding for quality, in the context of its nearest
        neighbors in the corpus (isotropy/coverage/distinctiveness are
        properties of a *set* of vectors, not a single one in isolation).

        Args:
            embedding: Embedding vector to score

        Returns:
            Dictionary with quality metrics

        Examples:
            >>> scorer = hound.quality_scorer()
            >>> quality = scorer.score(embedding_vector)
            >>> print(f"Isotropy: {quality['isotropy']:.2%}")
            >>> print(f"Status: {quality['status']}")
        """
        embedding = np.array(embedding, dtype=np.float32)

        sample_vectors = [embedding.tolist()]
        if self.adapter is not None:
            try:
                neighbors = self.adapter.search(embedding, top_k=20)
                neighbor_ids = [str(r["id"]) for r in neighbors]
                neighbor_embeddings = self.adapter.get_embeddings(neighbor_ids)
                sample_vectors.extend(v.tolist() for v in neighbor_embeddings.values())
            except Exception:
                pass  # Fall back to scoring the embedding in isolation below.

        can_compute = _core is not None and len(sample_vectors) >= 2
        if can_compute:
            isotropy = _core.py_compute_isotropy(sample_vectors)
            coverage = _core.py_compute_coverage(sample_vectors)
            distinctiveness = _core.py_compute_distinctiveness(sample_vectors)
            overall = _core.py_compute_quality_score(sample_vectors)

            status = "GOOD" if overall > 0.75 else "MODERATE" if overall > 0.5 else "WEAK"
        else:
            isotropy = coverage = distinctiveness = overall = 0.0
            status = "UNKNOWN"

        return {
            "isotropy": isotropy,
            "coverage": coverage,
            "distinctiveness": distinctiveness,
            "sample_size": len(sample_vectors),
            "status": status,  # GOOD, MODERATE, WEAK, or UNKNOWN if not enough data
            "overall": overall,
        }

    def corpus_health(self, sample_size: int = 100) -> Dict[str, Any]:
        """
        Get overall corpus embedding health, computed from a real sample of
        corpus vectors rather than fixed placeholder numbers.

        Note: drift/trend require a historical baseline snapshot to compare
        against, which this class doesn't yet store -- those fields honestly
        report as not-measured rather than a fabricated "stable" value.

        Args:
            sample_size: Number of corpus vectors to sample for the quality metrics

        Returns:
            Health metrics for the entire corpus

        Examples:
            >>> health = scorer.corpus_health()
            >>> print(f"Status: {health['status']}")
        """
        corpus_size = self.adapter.corpus_size() if self.adapter else 0

        sample_vectors: List[List[float]] = []
        if self.adapter is not None and corpus_size > 0:
            try:
                probe = np.random.randn(768).astype(np.float32)
                neighbors = self.adapter.search(probe, top_k=sample_size)
                neighbor_ids = [str(r["id"]) for r in neighbors]
                sample_embeddings = self.adapter.get_embeddings(neighbor_ids)
                sample_vectors = [v.tolist() for v in sample_embeddings.values()]
            except Exception:
                sample_vectors = []

        if _core is not None and len(sample_vectors) >= 2:
            avg_isotropy = _core.py_compute_isotropy(sample_vectors)
            avg_coverage = _core.py_compute_coverage(sample_vectors)
            avg_distinctiveness = _core.py_compute_distinctiveness(sample_vectors)
            overall = _core.py_compute_quality_score(sample_vectors)
            status = "GOOD" if overall > 0.75 else "MODERATE" if overall > 0.5 else "WEAK"
        else:
            avg_isotropy = avg_coverage = avg_distinctiveness = 0.0
            status = "UNKNOWN"

        return {
            "avg_isotropy": avg_isotropy,
            "avg_coverage": avg_coverage,
            "avg_distinctiveness": avg_distinctiveness,
            "sample_size": len(sample_vectors),
            "drift": None,  # Requires a stored historical baseline; not tracked yet.
            "corpus_size": corpus_size,
            "trend": "unknown",  # Requires historical tracking; not computed here.
            "status": status,
        }

    def detect_anomalies(
        self, embeddings: List[np.ndarray], threshold: float = 2.0
    ) -> Dict[str, List[int]]:
        """
        Detect anomalous embeddings in a batch.

        Args:
            embeddings: List of embedding vectors
            threshold: Standard deviations from mean to flag as anomaly

        Returns:
            Dictionary mapping anomaly types to indices

        Examples:
            >>> anomalies = scorer.detect_anomalies(embedding_list)
            >>> print(f"Low isotropy: {anomalies['low_isotropy']}")
        """
        if not embeddings:
            return {
                "low_isotropy": [],
                "high_clustering": [],
                "outliers": [],
            }

        embeddings_array = np.array([np.array(e) for e in embeddings], dtype=np.float32)

        # Compute norms (magnitude of vectors)
        norms = np.linalg.norm(embeddings_array, axis=1)
        norm_mean = np.mean(norms)
        norm_std = np.std(norms)

        # Find outliers (unusually small or large vectors)
        outliers = []
        for i, norm in enumerate(norms):
            if abs(norm - norm_mean) > threshold * norm_std:
                outliers.append(i)

        # Find low isotropy (check pairwise similarity)
        low_isotropy = []
        if len(embeddings_array) > 1:
            # Normalize
            normalized = embeddings_array / (norms[:, np.newaxis] + 1e-8)
            # Compute similarity matrix
            similarities = np.dot(normalized, normalized.T)
            # Average similarity per vector
            avg_similarities = np.mean(np.abs(similarities), axis=1)
            # Flag high similarity (low isotropy)
            sim_mean = np.mean(avg_similarities)
            sim_std = np.std(avg_similarities)
            for i, sim in enumerate(avg_similarities):
                if sim > sim_mean + threshold * sim_std:
                    low_isotropy.append(i)

        return {
            "low_isotropy": low_isotropy,
            "high_clustering": low_isotropy,  # Same as low isotropy
            "outliers": outliers,
        }

    def trend_analysis(
        self, baseline_date: str, current_date: str
    ) -> Dict[str, Any]:
        """
        Analyze quality trends over time.

        Args:
            baseline_date: Starting date (YYYY-MM-DD)
            current_date: Ending date (YYYY-MM-DD)

        Returns:
            Trend analysis with direction and magnitude

        Examples:
            >>> trend = scorer.trend_analysis(
            ...     baseline_date="2026-01-01",
            ...     current_date="2026-06-20"
            ... )
            >>> print(f"Trend: {trend['direction']}")

        Note:
            QualityScorer doesn't persist historical quality snapshots, so
            this can't compute a real trend between two dates yet -- use
            `pyvectorhound.trend_analysis.TrendAnalyzer` (wired up on `Hound`
            as `hound._trend_analyzer`) to track metrics over time and get a
            real trend report via `get_trend_report()`.
        """
        return {
            "direction": "unknown",
            "magnitude": None,
            "baseline_date": baseline_date,
            "current_date": current_date,
            "components": {},
            "explanation": (
                "QualityScorer does not store historical snapshots. "
                "Use TrendAnalyzer.track_metric() over time and TrendAnalyzer.get_trend_report() "
                "for a real trend analysis."
            ),
        }
