"""Diagnosis class for retrieval pipeline analysis."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np

try:
    from pyvectorhound import _core
except ImportError:
    _core = None


@dataclass
class DiagnosisResult:
    """Result of a single diagnostic component."""

    component: str
    status: str  # "GOOD", "MODERATE", "WEAK"
    metrics: Dict[str, float]
    explanation: str
    recommendations: List[str]


class Diagnosis:
    """
    Diagnosis results for a retrieval query.

    Provides component-level analysis of why retrieval failed,
    in plain English with actionable recommendations.
    """

    def __init__(
        self,
        query: str,
        results: List[Dict[str, Any]],
        expected_docs: Optional[List[str]] = None,
        adapter: Optional[Any] = None,
        query_embedding: Optional[np.ndarray] = None,
    ):
        """
        Initialize Diagnosis.

        Args:
            query: The search query being analyzed
            results: Retrieved results from the vector database
            expected_docs: Optional ground truth document IDs
            adapter: Database adapter for fetching additional data
            query_embedding: Query embedding vector
        """
        self.query = query
        self.results = results
        self.expected_docs = expected_docs or []
        self.adapter = adapter
        self.query_embedding = query_embedding
        self._analysis = {}

    def analyze(self) -> None:
        """Run analysis on the retrieval results."""
        # Vector search precision/recall/MRR only need self.results and
        # expected_docs -- they don't depend on the compiled Rust extension,
        # so they run regardless of whether _core is available.
        self._analysis["embedding"] = self._analyze_embedding()
        self._analysis["vector_search"] = self._analyze_vector_search()
        self._analysis["bm25"] = self._analyze_bm25()
        self._analysis["reranker"] = self._analyze_reranker()

    def _analyze_embedding(self) -> Dict[str, Any]:
        """Analyze embedding quality using real per-document vectors.

        Fetches the actual stored embeddings for the retrieved documents via
        the adapter (not the query embedding echoed back by search()), then
        computes isotropy/coverage/distinctiveness with the compiled Rust
        engine. Reports UNKNOWN rather than a fabricated score whenever the
        real inputs needed for the computation aren't available.
        """
        if _core is None:
            return {
                "status": "UNKNOWN",
                "isotropy": 0.0,
                "coverage": 0.0,
                "distinctiveness": 0.0,
                "overall": 0.0,
                "explanation": (
                    "The compiled embedding-quality engine (pyvectorhound._core) "
                    "isn't available in this install, so embedding quality wasn't measured."
                ),
            }

        if self.adapter is None or not self.results:
            return {
                "status": "UNKNOWN",
                "isotropy": 0.0,
                "coverage": 0.0,
                "distinctiveness": 0.0,
                "overall": 0.0,
                "explanation": "No adapter or results available to fetch document embeddings from.",
            }

        doc_ids = [str(r["id"]) for r in self.results]
        embeddings_by_id = self.adapter.get_embeddings(doc_ids)
        vectors = [v.tolist() for v in embeddings_by_id.values()]

        if len(vectors) < 2:
            return {
                "status": "UNKNOWN",
                "isotropy": 0.0,
                "coverage": 0.0,
                "distinctiveness": 0.0,
                "overall": 0.0,
                "explanation": (
                    f"Only {len(vectors)} document embedding(s) could be fetched "
                    "(need at least 2) to compute embedding quality metrics."
                ),
            }

        isotropy = _core.py_compute_isotropy(vectors)
        coverage = _core.py_compute_coverage(vectors)
        distinctiveness = _core.py_compute_distinctiveness(vectors)
        overall = _core.py_compute_quality_score(vectors)

        status = "GOOD" if overall > 0.75 else "MODERATE" if overall > 0.5 else "WEAK"

        return {
            "status": status,
            "isotropy": isotropy,
            "coverage": coverage,
            "distinctiveness": distinctiveness,
            "overall": overall,
            "explanation": (
                f"Computed from {len(vectors)} real document embeddings. "
                f"Isotropy {isotropy:.1%}, coverage {coverage:.1%}, distinctiveness {distinctiveness:.1%}."
            ),
        }

    def _analyze_vector_search(self) -> Dict[str, Any]:
        """Analyze vector search quality."""
        # Calculate precision/recall/MRR if ground truth available
        if self.expected_docs:
            retrieved_ids = [str(r["id"]) for r in self.results]
            relevant = set(self.expected_docs)
            retrieved = set(retrieved_ids)

            tp = len(relevant & retrieved)
            precision = tp / len(retrieved) if retrieved else 0.0
            recall = tp / len(relevant) if relevant else 0.0
            mrr = self._compute_mrr(retrieved_ids, relevant)

            status = "GOOD" if precision > 0.8 else "MODERATE" if precision > 0.5 else "WEAK"

            return {
                "status": status,
                "precision": precision,
                "recall": recall,
                "mrr": mrr,
                "explanation": f"Vector search precision: {precision:.1%}",
            }

        return {
            "status": "UNKNOWN",
            "precision": 0.0,
            "recall": 0.0,
            "mrr": 0.0,
            "explanation": "Provide expected_docs for ground truth comparison.",
        }

    @staticmethod
    def _compute_mrr(retrieved_ids: List[str], relevant_ids: set) -> float:
        """Reciprocal rank of the first relevant result actually retrieved, in order."""
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_ids:
                return 1.0 / (i + 1)
        return 0.0

    def _analyze_bm25(self) -> Dict[str, Any]:
        """Analyze BM25 quality.

        There is no keyword-search index or BM25 scoring subsystem wired into
        this codebase, so this honestly reports UNKNOWN rather than a
        fabricated score. Pass real BM25 precision/recall in to replace this
        once that subsystem exists.
        """
        return {
            "status": "UNKNOWN",
            "precision": 0.0,
            "recall": 0.0,
            "explanation": "BM25 keyword search is not implemented in this version; not measured.",
        }

    def _analyze_reranker(self) -> Dict[str, Any]:
        """Analyze reranker quality.

        No reranker score input exists on this Diagnosis (see __init__), so
        this honestly reports UNKNOWN rather than a fabricated score.
        """
        return {
            "status": "UNKNOWN",
            "calibration": 0.0,
            "ndcg": 0.0,
            "explanation": "No reranker scores were provided; reranker quality not measured.",
        }

    def hunt(self) -> str:
        """
        Get plain English diagnosis report.

        Returns:
            Human-readable diagnosis with recommendations

        Examples:
            >>> diagnosis = hound.diagnose(query="quantum computing")
            >>> print(diagnosis.hunt())
        """
        if not self._analysis:
            self.analyze()

        report = f"""
═══════════════════════════════════════════════════════════════
                PyVectorHound Diagnosis Report
═══════════════════════════════════════════════════════════════

Query: "{self.query}"
Results Retrieved: {len(self.results)}

COMPONENT ANALYSIS
─────────────────────────────────────────────────────────────

EMBEDDING: {self._analysis.get("embedding", {}).get("status", "UNKNOWN")}
  Isotropy: {self._analysis.get("embedding", {}).get("isotropy", 0.0):.1%} (should be >70%)
  Coverage: {self._analysis.get("embedding", {}).get("coverage", 0.0):.1%} (should be >80%)
  Distinctiveness: {self._analysis.get("embedding", {}).get("distinctiveness", 0.0):.1%} (should be >60%)

VECTOR SEARCH: {self._analysis.get("vector_search", {}).get("status", "UNKNOWN")}
  Precision: {self._analysis.get("vector_search", {}).get("precision", 0.0):.1%}
  Recall: {self._analysis.get("vector_search", {}).get("recall", 0.0):.1%}

BM25 (KEYWORD): {self._analysis.get("bm25", {}).get("status", "UNKNOWN")}
  Precision: {self._analysis.get("bm25", {}).get("precision", 0.0):.1%}
  Recall: {self._analysis.get("bm25", {}).get("recall", 0.0):.1%}

RERANKER: {self._analysis.get("reranker", {}).get("status", "UNKNOWN")}
  Calibration: {self._analysis.get("reranker", {}).get("calibration", 0.0):.1%}
  NDCG@5: {self._analysis.get("reranker", {}).get("ndcg", 0.0):.2f}

ROOT CAUSE
─────────────────────────────────────────────────────────────
{self.root_cause()}

RECOMMENDATIONS
─────────────────────────────────────────────────────────────
"""
        for i, rec in enumerate(self.recommendations(), 1):
            report += f"\n{i}. [{rec.get('priority', 'MEDIUM')}] {rec.get('action', 'No action')}"

        report += "\n"
        return report

    def metrics(self) -> Dict[str, Any]:
        """
        Get detailed metrics for the diagnosis.

        Returns:
            Dictionary with component-level metrics

        Examples:
            >>> metrics = diagnosis.metrics()
            >>> print(metrics["embedding"]["isotropy"])
        """
        if not self._analysis:
            self.analyze()

        return self._analysis

    def recommendations(self) -> List[Dict[str, Any]]:
        """
        Get ranked recommendations for fixing retrieval issues.

        Returns:
            List of recommendations ranked by impact

        Examples:
            >>> recs = diagnosis.recommendations()
            >>> for rec in recs:
            ...     print(f"{rec['priority']}: {rec['action']}")
        """
        if not self._analysis:
            self.analyze()

        recs = []

        # Check embedding
        if self._analysis.get("embedding", {}).get("status") == "WEAK":
            recs.append(
                {
                    "priority": "HIGH",
                    "action": "Upgrade embedding model (e.g., to text-embedding-3-large)",
                    "impact": "8-12% quality improvement",
                    "cost": "+$8/month",
                }
            )

        # Check vector search
        vector_search = self._analysis.get("vector_search", {})
        if vector_search.get("status") not in (None, "UNKNOWN") and vector_search.get("precision", 0) < 0.7:
            recs.append(
                {
                    "priority": "MEDIUM",
                    "action": "Increase vector_weight in hybrid scoring",
                    "impact": "2-3% quality improvement",
                    "cost": "None",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "LOW",
                    "action": "Retrieval quality is good. Monitor for drift.",
                    "impact": "Preventive",
                    "cost": "None",
                }
            )

        return recs

    def root_cause(self) -> str:
        """
        Get root cause analysis.

        Returns:
            Explanation of the primary issue

        Examples:
            >>> cause = diagnosis.root_cause()
            >>> print(cause)
        """
        if not self._analysis:
            self.analyze()

        # Simple rule-based root cause
        embedding = self._analysis.get("embedding", {})
        vector = self._analysis.get("vector_search", {})
        bm25 = self._analysis.get("bm25", {})

        if embedding.get("status") == "WEAK":
            return (
                "Your embedding model doesn't understand domain-specific concepts. "
                "Consider upgrading to a larger or domain-specific model."
            )
        elif vector.get("status") not in (None, "UNKNOWN") and vector.get("precision", 0) < 0.7:
            return (
                "Vector search precision is low. Results are not well-ranked. "
                "This could be caused by poor embeddings or low similarity thresholds."
            )
        elif bm25.get("status") not in (None, "UNKNOWN") and bm25.get("precision", 0) < 0.7:
            return "Keyword search (BM25) is not finding relevant matches."
        elif embedding.get("status") == "UNKNOWN" and vector.get("status") == "UNKNOWN":
            return (
                "Not enough data was available to diagnose retrieval quality -- "
                "provide expected_docs and ensure the adapter can return document embeddings."
            )
        else:
            return "Retrieval quality is good. No obvious issues detected."

    def summary(self) -> str:
        """
        Get concise summary of diagnosis.

        Returns:
            One-paragraph summary

        Examples:
            >>> summary = diagnosis.summary()
        """
        return self.hunt()
