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
        bm25_results: Optional[List[str]] = None,
        bm25_scores: Optional[Dict[str, float]] = None,
        reranker_scores: Optional[Dict[str, float]] = None,
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
            bm25_results: Optional ranked list of document ids from an
                external BM25/keyword search for the same query. Used to
                measure keyword-search precision/recall/MRR and its
                agreement with the vector results. PyVectorHound does not
                ship a BM25 index; this accepts the output of the keyword
                system you already run.
            bm25_scores: Optional document id -> BM25 score mapping. Used
                only when `bm25_results` is not supplied; ranking is derived
                by descending score.
            reranker_scores: Optional document id -> reranker score mapping
                for the retrieved results. Used to measure NDCG and score
                separation (a calibration proxy) against `expected_docs`.
        """
        self.query = query
        self.results = results
        self.expected_docs = expected_docs or []
        self.adapter = adapter
        self.query_embedding = query_embedding
        self.trend_analyzer = trend_analyzer
        self.document_texts = document_texts
        self.llm_judge_fn = llm_judge_fn
        self.bm25_results = list(bm25_results) if bm25_results is not None else None
        self.bm25_scores = dict(bm25_scores) if bm25_scores is not None else None
        self.reranker_scores = dict(reranker_scores) if reranker_scores is not None else None
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
        vectors = [v.tolist() if hasattr(v, "tolist") else list(v) for v in embeddings_by_id.values()]

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

    @staticmethod
    def _ranking_from_scores(scores: Dict[str, float]) -> List[str]:
        """Rank document ids by descending score, with a deterministic tie-break."""
        return [
            doc_id
            for doc_id, _score in sorted(
                scores.items(), key=lambda item: (-float(item[1]), str(item[0]))
            )
        ]

    @staticmethod
    def _ndcg_at_k(ranked_ids: List[str], relevant: set, k: int) -> float:
        """Binary-relevance NDCG@k against a ground-truth set."""
        if k <= 0 or not relevant:
            return 0.0

        def dcg(ids: List[str]) -> float:
            total = 0.0
            for index, doc_id in enumerate(ids[:k]):
                if doc_id in relevant:
                    total += 1.0 / np.log2(index + 2.0)
            return total

        ideal_hits = min(len(relevant), k)
        ideal = sum(1.0 / np.log2(index + 2.0) for index in range(ideal_hits))
        return dcg(ranked_ids) / ideal if ideal > 0 else 0.0

    @staticmethod
    def _calibration_separation(scores: Dict[str, float], relevant: set) -> float:
        """Score-separation calibration proxy in [0, 1].

        Reranker scores are min-max normalized across the retrieved documents,
        then the mean score of relevant documents is compared with the mean
        score of non-relevant documents. 0.5 means the scores do not separate
        relevant from non-relevant documents at all; 1.0 means perfect
        separation. This is a proxy, not a probability calibration curve --
        it answers "does a higher reranker score actually mean more relevant?"
        """
        values = list(scores.values())
        if not values or not relevant:
            return 0.0
        low, high = min(values), max(values)
        span = high - low
        if span <= 0:
            return 0.5

        def normalized(doc_id: str) -> float:
            return (float(scores[doc_id]) - low) / span

        relevant_scores = [normalized(d) for d in scores if d in relevant]
        non_relevant_scores = [normalized(d) for d in scores if d not in relevant]
        if not relevant_scores or not non_relevant_scores:
            return 0.5
        mean_rel = sum(relevant_scores) / len(relevant_scores)
        mean_non = sum(non_relevant_scores) / len(non_relevant_scores)
        return max(0.0, min(1.0, (mean_rel - mean_non + 1.0) / 2.0))

    def _analyze_bm25(self) -> Dict[str, Any]:
        """Analyze keyword-search quality from externally supplied BM25 results.

        PyVectorHound does not ship a BM25 index. Rather than fabricate a
        score, this accepts the ranked output (or scores) of the keyword
        system the caller already runs and measures its precision, recall,
        MRR and agreement with the vector results. Without BM25 input it
        still reports UNKNOWN.
        """
        ranking = self.bm25_results
        if ranking is None and self.bm25_scores is not None:
            ranking = self._ranking_from_scores(self.bm25_scores)

        if ranking is None:
            return {
                "status": "UNKNOWN",
                "precision": 0.0,
                "recall": 0.0,
                "mrr": 0.0,
                "agreement": 0.0,
                "k": len(self.results),
                "explanation": (
                    "BM25 was not measured. Pass bm25_results (ranked document ids) "
                    "or bm25_scores (doc id -> score) from your keyword search to "
                    "measure it; PyVectorHound does not ship a BM25 index."
                ),
            }

        ranking = [str(doc_id) for doc_id in ranking]
        k = len(self.results) or len(ranking)
        top = ranking[:k]
        retrieved_ids = [str(r["id"]) for r in self.results]
        agreement = 0.0
        if top and retrieved_ids:
            a, b = set(top), set(retrieved_ids)
            agreement = len(a & b) / len(a | b) if (a | b) else 0.0

        if not self.expected_docs:
            return {
                "status": "UNKNOWN",
                "precision": 0.0,
                "recall": 0.0,
                "mrr": 0.0,
                "agreement": agreement,
                "k": k,
                "explanation": (
                    f"BM25 ranking received, but no expected_docs were supplied, so "
                    f"precision/recall cannot be measured. Top-{k} agreement with "
                    f"the vector results: {agreement:.1%}."
                ),
            }

        relevant = {str(doc_id) for doc_id in self.expected_docs}
        hits = len(relevant & set(top))
        precision = hits / len(top) if top else 0.0
        recall = hits / len(relevant) if relevant else 0.0
        mrr = self._compute_mrr(ranking, relevant)
        status = self._classify(
            metric_name="bm25_precision",
            value=precision,
            fixed_good=0.8,
            fixed_moderate=0.5,
        )
        return {
            "status": status,
            "precision": precision,
            "recall": recall,
            "mrr": mrr,
            "agreement": agreement,
            "k": k,
            "measured": True,
            "explanation": (
                f"Measured from an external BM25 ranking over {len(ranking)} documents: "
                f"precision {precision:.1%}, recall {recall:.1%}, MRR {mrr:.2f}, "
                f"top-{k} agreement with vector results {agreement:.1%}."
            ),
        }

    def _analyze_reranker(self) -> Dict[str, Any]:
        """Analyze reranker quality from externally supplied scores.

        Measures NDCG@k and a score-separation calibration proxy against
        `expected_docs`. Without reranker scores (or ground truth) it reports
        UNKNOWN instead of inventing a verdict.
        """
        if self.reranker_scores is None:
            return {
                "status": "UNKNOWN",
                "calibration": 0.0,
                "ndcg": 0.0,
                "k": 0,
                "explanation": (
                    "Reranker quality was not measured. Pass reranker_scores "
                    "(doc id -> score) for the retrieved results to measure it."
                ),
            }

        scores = {str(doc_id): float(score) for doc_id, score in self.reranker_scores.items()}
        ranked = self._ranking_from_scores(scores)
        k = len(self.results) or len(ranked)

        if not self.expected_docs:
            return {
                "status": "UNKNOWN",
                "calibration": 0.0,
                "ndcg": 0.0,
                "k": k,
                "explanation": (
                    "Reranker scores received, but no expected_docs were supplied, "
                    "so NDCG/calibration cannot be measured."
                ),
            }

        relevant = {str(doc_id) for doc_id in self.expected_docs}
        ndcg = self._ndcg_at_k(ranked, relevant, k)
        calibration = self._calibration_separation(scores, relevant)
        status = self._classify(
            metric_name="reranker_ndcg",
            value=ndcg,
            fixed_good=0.8,
            fixed_moderate=0.5,
        )
        return {
            "status": status,
            "calibration": calibration,
            "ndcg": ndcg,
            "k": k,
            "measured": True,
            "explanation": (
                f"Measured from {len(scores)} reranker scores: NDCG@{k} {ndcg:.2f}, "
                f"score separation {calibration:.1%} (0.5 = no separation, 1.0 = perfect)."
            ),
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
  NDCG@{self._analysis.get("reranker", {}).get("k", 5)}: {self._analysis.get("reranker", {}).get("ndcg", 0.0):.2f}

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
