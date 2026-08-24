"""Diagnosis class for retrieval pipeline analysis."""

from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
import numpy as np

from pyvectorhound.trend_analysis import TrendAnalyzer
from pyvectorhound._retry import call_with_backoff as _call_with_backoff

try:
    from pyvectorhound import _core
except ImportError:
    _core = None


def _status_from_threshold(value: float, good: float, moderate: float) -> str:
    """Fixed-cutoff status classification (the cold-start fallback)."""
    return "GOOD" if value > good else "MODERATE" if value > moderate else "WEAK"


def _status_from_baseline(value: float, baseline_mean: float, baseline_stddev: float) -> Optional[str]:
    """Classify `value` by how many standard deviations it sits from a tracked
    baseline, instead of a fixed numeric cutoff. Returns None if the baseline
    has no usable spread (e.g. a single sample), so callers can fall back to
    the fixed-cutoff classification.
    """
    if baseline_stddev <= 0:
        return None
    z = (value - baseline_mean) / baseline_stddev
    if z >= -0.5:
        return "GOOD"
    if z >= -1.5:
        return "MODERATE"
    return "WEAK"


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
        trend_analyzer: Optional[TrendAnalyzer] = None,
        document_texts: Optional[Dict[str, str]] = None,
        llm_judge_fn: Optional[Callable[[str, List[str]], Dict[str, Any]]] = None,
    ):
        """
        Initialize Diagnosis.

        Args:
            query: The search query being analyzed
            results: Retrieved results from the vector database
            expected_docs: Optional ground truth document IDs
            adapter: Database adapter for fetching additional data
            query_embedding: Query embedding vector
            trend_analyzer: Optional TrendAnalyzer with historical baselines
                (set via `track_metric()` on prior diagnoses). When a
                baseline exists for a metric, status (GOOD/MODERATE/WEAK) is
                computed from how many standard deviations the current value
                sits from that baseline instead of a fixed numeric cutoff --
                so thresholds stay meaningful across embedding-model
                migrations rather than drifting silently. Falls back to
                fixed cutoffs when no baseline is available yet (cold start).
            document_texts: Optional doc_id -> text mapping for the
                retrieved results. Required (together with llm_judge_fn) for
                faithfulness/contradiction analysis -- PyVectorHound's
                database adapters return ids/scores/embeddings, not document
                text, so this has to come from the caller.
            llm_judge_fn: Optional callable `(query, doc_texts) -> dict`
                that runs an LLM-as-judge faithfulness/contradiction check
                (e.g. wrapping an OpenAI/Anthropic call). Expected to return
                a dict with a "faithful" bool and/or a numeric
                "contradiction_score" (0.0 = fully consistent with the
                query, 1.0 = contradicts it) per call. PyVectorHound does
                not bundle an LLM client, matching how `embed_fn` works on
                `Hound`.
        """
        self.query = query
        self.results = results
        self.expected_docs = expected_docs or []
        self.adapter = adapter
        self.query_embedding = query_embedding
        self.trend_analyzer = trend_analyzer
        self.document_texts = document_texts
        self.llm_judge_fn = llm_judge_fn
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
        self._analysis["faithfulness"] = self._analyze_faithfulness()

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

        status = self._classify(
            metric_name="embedding_overall",
            value=overall,
            fixed_good=0.75,
            fixed_moderate=0.5,
        )

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

            status = self._classify(
                metric_name="vector_search_precision",
                value=precision,
                fixed_good=0.8,
                fixed_moderate=0.5,
            )

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

    def _classify(self, metric_name: str, value: float, fixed_good: float, fixed_moderate: float) -> str:
        """Classify `value` as GOOD/MODERATE/WEAK.

        Uses the tracked baseline for `metric_name` on `self.trend_analyzer`
        when one exists (relative, model-agnostic classification that
        doesn't drift when the embedding model changes), otherwise falls
        back to the fixed cutoff the caller supplies.
        """
        if self.trend_analyzer is not None:
            baseline = self.trend_analyzer._baseline_stats.get(metric_name)
            if not baseline:
                series = self.trend_analyzer.series.get(metric_name)
                if series is not None and len(series.get_values()) >= 5:
                    baseline = {"mean": series.mean(), "stddev": series.stddev()}
            if baseline:
                status = _status_from_baseline(value, baseline["mean"], baseline["stddev"])
                if status is not None:
                    return status
        return _status_from_threshold(value, fixed_good, fixed_moderate)

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

    def _analyze_faithfulness(self) -> Dict[str, Any]:
        """LLM-as-judge faithfulness / semantic contradiction check.

        Distance-based and lexical metrics (embedding isotropy, BM25
        precision) can't catch a retrieved document that's topically
        similar but actually contradicts or is irrelevant to the query --
        that needs a semantic judgment call. This runs one when the caller
        supplies both `document_texts` (adapters don't expose document
        text, only ids/scores/embeddings) and `llm_judge_fn` (PyVectorHound
        doesn't bundle an LLM client). Honestly reports UNKNOWN, like BM25
        and reranker above, when either input is missing rather than
        fabricating a score.
        """
        if self.llm_judge_fn is None or not self.document_texts or not self.results:
            missing = []
            if self.llm_judge_fn is None:
                missing.append("llm_judge_fn")
            if not self.document_texts:
                missing.append("document_texts")
            return {
                "status": "UNKNOWN",
                "contradiction_score": 0.0,
                "faithful_count": 0,
                "contradicted_count": 0,
                "explanation": (
                    f"Faithfulness not measured -- missing {' and '.join(missing) or 'results'}. "
                    "Pass document_texts and llm_judge_fn to check for semantic "
                    "contradictions an embedding-distance metric would miss."
                ),
            }

        doc_ids = [str(r["id"]) for r in self.results]
        doc_texts = [self.document_texts[d] for d in doc_ids if d in self.document_texts]

        if not doc_texts:
            return {
                "status": "UNKNOWN",
                "contradiction_score": 0.0,
                "faithful_count": 0,
                "contradicted_count": 0,
                "explanation": "None of the retrieved document ids had a matching entry in document_texts.",
            }

        judgment = _call_with_backoff(self.llm_judge_fn, self.query, doc_texts)

        faithful_count = int(judgment.get("faithful_count", 0))
        contradicted_count = int(judgment.get("contradicted_count", 0))
        contradiction_score = float(judgment.get("contradiction_score", 0.0))

        # A single aggregate judgment (no per-doc counts) still tells us
        # something -- treat "faithful": False as one contradicted doc.
        if "faithful_count" not in judgment and "contradicted_count" not in judgment:
            if judgment.get("faithful", contradiction_score < 0.5):
                faithful_count, contradicted_count = len(doc_texts), 0
            else:
                faithful_count, contradicted_count = 0, len(doc_texts)

        status = "GOOD" if contradiction_score < 0.2 else "MODERATE" if contradiction_score < 0.5 else "WEAK"

        return {
            "status": status,
            "contradiction_score": contradiction_score,
            "faithful_count": faithful_count,
            "contradicted_count": contradicted_count,
            "explanation": judgment.get(
                "reasoning",
                f"{contradicted_count} of {len(doc_texts)} retrieved documents flagged as "
                f"contradicting or irrelevant to the query by the LLM judge.",
            ),
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

FAITHFULNESS (LLM JUDGE): {self._analysis.get("faithfulness", {}).get("status", "UNKNOWN")}
  Contradiction score: {self._analysis.get("faithfulness", {}).get("contradiction_score", 0.0):.1%} (lower is better)
  Contradicted docs: {self._analysis.get("faithfulness", {}).get("contradicted_count", 0)}

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

        # Check faithfulness (LLM-judge contradiction check)
        faithfulness = self._analysis.get("faithfulness", {})
        if faithfulness.get("status") == "WEAK":
            recs.append(
                {
                    "priority": "HIGH",
                    "action": (
                        f"{faithfulness.get('contradicted_count', 0)} retrieved document(s) "
                        "contradict or are irrelevant to the query despite high embedding "
                        "similarity -- review chunking (over-broad chunks) or add a "
                        "reranker/filter stage before generation"
                    ),
                    "impact": "Reduces hallucination risk from unfaithful context",
                    "cost": "None (LLM judge already run)",
                }
            )
        elif faithfulness.get("status") == "MODERATE":
            recs.append(
                {
                    "priority": "MEDIUM",
                    "action": "Some retrieved documents were flagged as borderline by the LLM judge -- monitor contradiction_score over time",
                    "impact": "Preventive",
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
        faithfulness = self._analysis.get("faithfulness", {})

        # A high embedding/vector-search score with a contradiction flagged
        # by the LLM judge is exactly the "similar but wrong" failure mode
        # distance metrics can't see on their own -- surface it first.
        if faithfulness.get("status") == "WEAK" and embedding.get("status") in ("GOOD", "MODERATE"):
            return (
                f"{faithfulness.get('contradicted_count', 0)} retrieved document(s) score well "
                "on embedding similarity but were flagged by the LLM judge as contradicting or "
                "irrelevant to the query -- this is a semantic mismatch that distance metrics "
                "alone can't catch. Review chunk boundaries and consider a reranker/filter stage."
            )
        elif embedding.get("status") == "WEAK":
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
