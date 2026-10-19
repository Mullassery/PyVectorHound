"""Main PyVectorHound class for retrieval diagnostics."""

import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

import numpy as np

from pyvectorhound._retry import call_with_backoff
from pyvectorhound.benchmarking import LatencyMetrics, PerformanceBenchmark
from pyvectorhound.comparison import ModelComparison
from pyvectorhound.database import VectorDB, get_adapter
from pyvectorhound.diagnosis import Diagnosis
from pyvectorhound.quantization import QuantizedVectorStore
from pyvectorhound.recommendations import RecommendationEngine
from pyvectorhound.retrieval_replay import RetrievalReplayer
from pyvectorhound.retrieval_tracing import RetrievalTracer
from pyvectorhound.scorer import QualityScorer
from pyvectorhound.trend_analysis import TrendAnalyzer


def _parse_hound_timestamp(value: Any, argument_name: str) -> datetime:
    """Parse a date/datetime argument into naive UTC for trend comparisons."""
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        parsed = None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                parsed = datetime.strptime(text, fmt)
                break
            except ValueError:
                continue
        if parsed is None:
            raise ValueError(
                f"{argument_name} must be 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS', got {value!r}"
            )

    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _series_stats(values: List[float]) -> Dict[str, float]:
    """Mean/stddev for a non-empty list (stddev is 0.0 for a single sample)."""
    return {
        "mean": statistics.mean(values),
        "stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
    }


class Hound:
    """
    Main PyVectorHound class for diagnosing retrieval pipeline issues.

    Hunts down which component of your retrieval system is failing
    and provides actionable recommendations.

    Attributes:
        db: Vector database type (qdrant, chroma, milvus, weaviate, postgres)
        endpoint: Database endpoint URL
        index_name: Index/collection name in the database
        adapter: Connected database adapter

    Examples:
        >>> from pyvectorhound import Hound
        >>> # PyVectorHound doesn't ship an embedding model -- either pass a
        >>> # precomputed embedding per call, or give it a function that can
        >>> # produce one (wrapping OpenAI, Cohere, sentence-transformers, etc.)
        >>> hound = Hound(
        ...     db="qdrant",
        ...     endpoint="localhost:6333",
        ...     embed_fn=lambda text: my_embedding_model.embed(text),
        ... )
        >>> diagnosis = hound.diagnose(query="your query", top_k=5)
        >>> print(diagnosis.hunt())
    """

    def __init__(
        self,
        db: str,
        endpoint: str = "localhost:6333",
        index_name: str = "documents",
        api_key: Optional[str] = None,
        embed_fn: Optional[Callable[[str], np.ndarray]] = None,
        llm_judge_fn: Optional[Callable[[str, List[str]], Dict[str, Any]]] = None,
        quantized: bool = False,
        **kwargs: Any,
    ):
        """
        Initialize PyVectorHound.

        Args:
            db: Vector database type. Supported: 'qdrant', 'chroma',
                'milvus', 'weaviate', 'postgres'
            endpoint: Database endpoint URL
            index_name: Index/collection name in the database
            api_key: Optional API key (if needed)
            embed_fn: Optional callable that embeds a query string into a
                vector (e.g. wrapping an OpenAI, Cohere, or
                sentence-transformers client). PyVectorHound does not bundle
                an embedding model itself. If not provided, `diagnose()`
                requires a precomputed `query_embedding` on every call.
            llm_judge_fn: Optional callable `(query, doc_texts) -> dict` that
                runs an LLM-as-judge faithfulness/contradiction check (see
                `Diagnosis.__init__`). Set once here and every `diagnose()`
                call that's given `document_texts` will use it automatically.
            quantized: Opt in to an additional in-process int8-quantized vector
                store. When enabled, populate it with `add_vectors()`; while it
                is non-empty, `diagnose()`/`search_vectors()` read from it
                instead of the database adapter. The default `False` preserves
                the existing float path unchanged.
            **kwargs: Additional database-specific parameters

        Raises:
            ValueError: If database type is not supported
        """
        self.db = db.lower()
        self.endpoint = endpoint
        self.index_name = index_name
        self.api_key = api_key
        self.embed_fn = embed_fn
        self.llm_judge_fn = llm_judge_fn
        self.kwargs = kwargs
        self.quantized = bool(quantized)
        self._quantized_store: Optional[QuantizedVectorStore] = (
            QuantizedVectorStore() if self.quantized else None
        )

        # Initialize database adapter. Connection is intentionally lazy: every
        # adapter method (search/get_embeddings/corpus_size) already connects
        # on first use if needed, so Hound() doesn't require the optional
        # client library (e.g. qdrant-client) or a live server to be
        # constructed -- only to actually query the database.
        self.adapter = get_adapter(
            db=self.db,
            endpoint=self.endpoint,
            index_name=self.index_name,
            api_key=self.api_key,
            **self.kwargs,
        )

        # Initialize performance benchmarking and trend analysis
        self._benchmarker = PerformanceBenchmark(adapter=self.adapter)
        self._trend_analyzer = TrendAnalyzer()

        # Initialize retrieval tracing, replay, and recommendations
        self._tracer = RetrievalTracer()
        self._replayer = RetrievalReplayer()
        self._recommendation_engine = RecommendationEngine()

    def _active_adapter(self) -> VectorDB:
        """Return the quantized store when it has data, else the DB adapter."""
        if self._quantized_store is not None and not self._quantized_store.is_empty:
            return self._quantized_store
        return self.adapter

    def enable_quantization(self) -> QuantizedVectorStore:
        """Enable the opt-in in-process int8-quantized vector store.

        This is equivalent to constructing ``Hound(..., quantized=True)``.
        The store starts empty; call `add_vectors()` to populate it. While it
        is non-empty, `diagnose()`/`search_vectors()` use it instead of the
        database adapter.

        Returns:
            The active `QuantizedVectorStore`.

        Raises:
            RuntimeError: If the compiled Rust extension (`_core`, which
                implements quantize/dequantize) is unavailable.
        """
        if self._quantized_store is None:
            from pyvectorhound.quantization import _require_core

            _require_core()
            self._quantized_store = QuantizedVectorStore()
            self.quantized = True
        return self._quantized_store

    def add_vectors(
        self,
        vectors: List[np.ndarray],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Quantize and store embeddings in the opt-in local store.

        Existing ids are overwritten. If ``ids`` is omitted, ids are generated
        as ``quantized_0``, ``quantized_1``, ... without overwriting existing
        entries.

        Args:
            vectors: Embedding vectors to store (all the same dimension).
            ids: Optional document ids, one per vector.

        Returns:
            The stored document ids.

        Raises:
            ValueError: If quantization is not enabled, lengths differ, or a
                vector is empty/non-1-D/non-finite/inconsistent in dimension.
        """
        if self._quantized_store is None:
            raise ValueError(
                "Quantization is not enabled on this Hound instance. Construct "
                "it with Hound(..., quantized=True) or call "
                "hound.enable_quantization() before add_vectors(). The default "
                "float path is unchanged."
            )

        if ids is None:
            start = len(self._quantized_store)
            ids = [f"quantized_{start + i}" for i in range(len(vectors))]
        return self._quantized_store.add(ids, vectors)

    def search_vectors(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Search the opt-in quantized store by cosine similarity.

        Stored int8 vectors are dequantized on retrieval, then scored.

        Args:
            query_embedding: Query vector.
            top_k: Number of results to return.

        Returns:
            ``{"id", "score", "embedding"}`` dicts ordered by descending
            cosine similarity.

        Raises:
            ValueError: If quantization is not enabled, the query has the
                wrong dimension/has zero magnitude, or contains NaN/Inf.
            RuntimeError: If the compiled Rust extension is unavailable.
        """
        if self._quantized_store is None:
            raise ValueError(
                "Quantization is not enabled on this Hound instance. Construct "
                "it with Hound(..., quantized=True) or call "
                "hound.enable_quantization() before search_vectors()."
            )
        return self._quantized_store.search(query_embedding, top_k=top_k)

    def get_stored_embeddings(
        self,
        doc_ids: Optional[List[str]] = None,
    ) -> Dict[str, np.ndarray]:
        """Read embeddings back from the opt-in quantized store.

        Args:
            doc_ids: Ids to retrieve. If omitted, every stored id is read.

        Returns:
            Dequantized ``float32`` embeddings keyed by document id. Missing
            ids are omitted.

        Raises:
            ValueError: If quantization is not enabled.
            RuntimeError: If the compiled Rust extension is unavailable.
        """
        if self._quantized_store is None:
            raise ValueError(
                "Quantization is not enabled on this Hound instance. Construct "
                "it with Hound(..., quantized=True) or call "
                "hound.enable_quantization() before get_stored_embeddings()."
            )
        ids = list(self._quantized_store.ids) if doc_ids is None else doc_ids
        return self._quantized_store.get_embeddings(ids)

    def clear_stored_vectors(self) -> None:
        """Remove every vector from the opt-in quantized store.

        Raises:
            ValueError: If quantization is not enabled.
        """
        if self._quantized_store is None:
            raise ValueError(
                "Quantization is not enabled on this Hound instance. Construct "
                "it with Hound(..., quantized=True) or call "
                "hound.enable_quantization() before clear_stored_vectors()."
            )
        self._quantized_store.clear()

    def diagnose(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        expected_docs: Optional[List[str]] = None,
        verbose: bool = False,
        document_texts: Optional[Dict[str, str]] = None,
        bm25_results: Optional[List[str]] = None,
        bm25_scores: Optional[Dict[str, float]] = None,
        reranker_scores: Optional[Dict[str, float]] = None,
    ) -> Diagnosis:
        """
        Diagnose why retrieval is failing for a specific query.

        Args:
            query: The search query to diagnose
            query_embedding: Pre-computed query embedding. Required unless an
                `embed_fn` was passed to `Hound()`.
            top_k: Number of results to retrieve and analyze
            expected_docs: Optional list of document IDs that should be retrieved (ground truth)
            verbose: If True, show detailed diagnostic information
            document_texts: Optional doc_id -> text mapping for the results
                this query will retrieve. Combined with the `llm_judge_fn`
                passed to `Hound()`, enables the faithfulness/contradiction
                check (see `Diagnosis.__init__`). Adapters don't expose
                document text, so this has to come from the caller.
            bm25_results: Optional ranked document ids from an external
                BM25/keyword search for this query. Enables keyword-search
                precision/recall/MRR and vector-agreement diagnostics.
            bm25_scores: Optional doc id -> BM25 score mapping, used when
                `bm25_results` is not supplied.
            reranker_scores: Optional doc id -> reranker score mapping for
                the retrieved results. Enables NDCG and score-separation
                calibration diagnostics.

        Returns:
            Diagnosis object with findings and recommendations

        Raises:
            ValueError: If no query_embedding is given and no embed_fn was
                configured on this Hound instance. PyVectorHound does not
                fabricate a random embedding -- a diagnosis run against a
                meaningless vector would itself be meaningless.

        Examples:
            >>> diagnosis = hound.diagnose(query="quantum computing", top_k=5)
            >>> print(diagnosis.hunt())  # Plain English report
            >>> print(diagnosis.metrics())  # Raw metrics
            >>> print(diagnosis.recommendations())  # Ranked fixes
        """
        if query_embedding is None:
            if self.embed_fn is not None:
                query_embedding = np.asarray(
                    call_with_backoff(self.embed_fn, query), dtype=np.float32
                )
            else:
                raise ValueError(
                    "diagnose() requires a query_embedding. PyVectorHound does not "
                    "bundle an embedding model, so it cannot silently invent one -- "
                    "that would make every diagnosis meaningless. Either pass "
                    "query_embedding=<your embedding of `query`> to diagnose(), or "
                    "pass embed_fn=<callable str -> vector> to Hound() so it can "
                    "embed queries for you (e.g. wrapping OpenAI, Cohere, or "
                    "sentence-transformers)."
                )
        else:
            query_embedding = np.asarray(query_embedding, dtype=np.float32)

        # Search for results. When the opt-in quantized store has vectors,
        # it is the retrieval source; otherwise the configured DB adapter is.
        adapter = self._active_adapter()
        results = adapter.search(query_embedding, top_k=top_k)

        # Create diagnosis
        diagnosis = Diagnosis(
            query=query,
            results=results,
            expected_docs=expected_docs,
            adapter=adapter,
            query_embedding=query_embedding,
            trend_analyzer=self._trend_analyzer,
            document_texts=document_texts,
            llm_judge_fn=self.llm_judge_fn,
            bm25_results=bm25_results,
            bm25_scores=bm25_scores,
            reranker_scores=reranker_scores,
        )

        # Analyze
        diagnosis.analyze()

        return diagnosis

    def diagnose_batch(
        self,
        queries: List[str],
        query_embeddings: Optional[List[Optional[np.ndarray]]] = None,
        top_k: int = 5,
        expected_docs: Optional[List[Optional[List[str]]]] = None,
        document_texts: Optional[List[Optional[Dict[str, str]]]] = None,
        bm25_results: Optional[List[Optional[List[str]]]] = None,
        bm25_scores: Optional[List[Optional[Dict[str, float]]]] = None,
        reranker_scores: Optional[List[Optional[Dict[str, float]]]] = None,
        max_workers: int = 8,
    ) -> List[Diagnosis]:
        """
        Diagnose many queries concurrently.

        A single `diagnose()` call is dominated by I/O: the adapter's vector
        search is a network round trip, and (when `embed_fn`/`llm_judge_fn`
        are configured) so are the embedding and LLM-judge calls. Running a
        batch through `diagnose()` in a loop makes every one of those round
        trips serial, which is what stalls large-scale evaluation runs
        across thousands of queries. This runs each query's `diagnose()` on
        a thread pool instead -- real concurrency for I/O-bound calls
        without requiring every database adapter and caller-supplied
        `embed_fn`/`llm_judge_fn` to be rewritten as `async`. Each
        `embed_fn`/`llm_judge_fn` call already retries with exponential
        backoff (see `diagnose()`), which matters more once many queries
        are in flight at once against the same rate-limited API.

        Args:
            queries: Search queries to diagnose.
            query_embeddings: Optional precomputed embedding per query
                (same length as `queries`, entries may be None to fall back
                to `embed_fn`). If omitted entirely, `embed_fn` is used for
                every query.
            top_k: Number of results to retrieve and analyze per query.
            expected_docs: Optional ground-truth doc ids per query (same
                length as `queries`, entries may be None).
            document_texts: Optional doc_id -> text mapping per query (same
                length as `queries`, entries may be None) for the
                faithfulness check.
            bm25_results: Optional per-query BM25 rankings (same length as
                `queries`, entries may be None).
            bm25_scores: Optional per-query BM25 score maps (same length as
                `queries`, entries may be None).
            reranker_scores: Optional per-query reranker score maps (same
                length as `queries`, entries may be None).
            max_workers: Maximum number of queries diagnosed concurrently.

        Returns:
            List of Diagnosis objects, in the same order as `queries`. A
            query whose diagnosis raised (e.g. embed_fn/llm_judge_fn failed
            after retries) has its exception re-raised here, after every
            other query in the batch has finished -- so one bad query
            doesn't abandon partial work already done by the others.

        Examples:
            >>> diagnoses = hound.diagnose_batch(
            ...     queries=["quantum computing", "machine learning"],
            ...     max_workers=4,
            ... )
        """
        n = len(queries)
        query_embeddings = query_embeddings or [None] * n
        expected_docs = expected_docs or [None] * n
        document_texts = document_texts or [None] * n
        bm25_results = bm25_results or [None] * n
        bm25_scores = bm25_scores or [None] * n
        reranker_scores = reranker_scores or [None] * n
        if not (
            len(query_embeddings)
            == len(expected_docs)
            == len(document_texts)
            == len(bm25_results)
            == len(bm25_scores)
            == len(reranker_scores)
            == n
        ):
            raise ValueError(
                "queries, query_embeddings, expected_docs, document_texts, "
                "bm25_results, bm25_scores, and reranker_scores must all be the "
                "same length when provided."
            )

        results: List[Optional[Diagnosis]] = [None] * n
        errors: Dict[int, Exception] = {}

        with ThreadPoolExecutor(max_workers=max(1, max_workers)) as pool:
            future_to_index = {
                pool.submit(
                    self.diagnose,
                    query=queries[i],
                    query_embedding=query_embeddings[i],
                    top_k=top_k,
                    expected_docs=expected_docs[i],
                    document_texts=document_texts[i],
                    bm25_results=bm25_results[i],
                    bm25_scores=bm25_scores[i],
                    reranker_scores=reranker_scores[i],
                ): i
                for i in range(n)
            }
            for future in as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    results[i] = future.result()
                except Exception as exc:
                    errors[i] = exc

        if errors:
            first_index = min(errors)
            raise errors[first_index]

        return results  # type: ignore[return-value]

    def compare_models(
        self,
        model_type: str,
        candidates: List[str],
        sample_size: int = 100,
        **kwargs: Any,
    ) -> ModelComparison:
        """
        Compare different embedding or reranker models on your corpus.

        Args:
            model_type: Type of model to compare ('embedding' or 'reranker')
            candidates: List of model names to compare
            sample_size: Number of queries to test
            **kwargs: Additional comparison parameters

        Returns:
            ModelComparison object with quality/cost analysis

        Examples:
            >>> comparison = hound.compare_models(
            ...     model_type="embedding",
            ...     candidates=["3-small", "3-large", "cohere-v3"]
            ... )
            >>> print(comparison.report())
        """
        comparison = ModelComparison(
            model_type=model_type,
            candidates=candidates,
            adapter=self.adapter,
            sample_size=sample_size,
            **kwargs,
        )

        comparison.benchmark()

        return comparison

    def compare_metrics(
        self,
        before: str,
        after: str,
    ) -> Dict[str, Any]:
        """
        Compare metrics before and after applying a change.

        This compares real values that were recorded with `track_metric()`.
        Baseline values are points at or before ``before``; comparison values
        are points strictly after ``before`` and at or before ``after``. It
        does not reconstruct past diagnoses from the database, so call
        `track_metric()` as you run diagnostics to build the series.

        Args:
            before: Baseline boundary (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS).
                Points at or before this time form the baseline period.
            after: Comparison boundary (same format). Points after ``before``
                and at or before this time form the comparison period.

        Returns:
            Dictionary with per-metric baseline/current mean, stddev, sample
            counts, delta, percent change, and direction. Metrics that lack
            data in either period are listed under ``skipped_metrics`` with
            the reason rather than being assigned a fabricated value.

        Raises:
            ValueError: If a timestamp cannot be parsed, ``before`` is after
                ``after``, no metrics have been tracked, or no metric has
                samples in both periods.
        """
        before_dt = _parse_hound_timestamp(before, "before")
        after_dt = _parse_hound_timestamp(after, "after")
        if before_dt > after_dt:
            raise ValueError(f"before ({before!r}) must not be after after ({after!r})")

        series = self._trend_analyzer.series
        if not series:
            raise ValueError(
                "compare_metrics() has no tracked metrics to compare. Call "
                "hound.track_metric(name, value) as you run diagnoses (or at "
                "any cadence you want to compare), then retry."
            )

        metrics: Dict[str, Dict[str, Any]] = {}
        skipped: Dict[str, str] = {}
        for metric_name, time_series in series.items():
            baseline_values = [
                point.value for point in time_series.points if point.timestamp <= before_dt
            ]
            current_values = [
                point.value
                for point in time_series.points
                if before_dt < point.timestamp <= after_dt
            ]

            if not baseline_values:
                skipped[metric_name] = "no tracked points at or before the baseline boundary"
                continue
            if not current_values:
                skipped[metric_name] = (
                    "no tracked points after the baseline boundary and at or "
                    "before the comparison boundary"
                )
                continue

            baseline_stats = _series_stats(baseline_values)
            current_stats = _series_stats(current_values)
            delta = current_stats["mean"] - baseline_stats["mean"]
            change_pct = (
                delta / abs(baseline_stats["mean"]) * 100 if baseline_stats["mean"] != 0 else None
            )
            direction = "stable" if abs(delta) <= 1e-12 else "up" if delta > 0 else "down"

            metrics[metric_name] = {
                "baseline_samples": len(baseline_values),
                "current_samples": len(current_values),
                "baseline_mean": baseline_stats["mean"],
                "baseline_stddev": baseline_stats["stddev"],
                "current_mean": current_stats["mean"],
                "current_stddev": current_stats["stddev"],
                "delta": delta,
                "change_pct": change_pct,
                "direction": direction,
            }

        if not metrics:
            detail = "; ".join(f"{name}: {reason}" for name, reason in sorted(skipped.items()))
            raise ValueError(
                "compare_metrics() found no metric with samples in both "
                f"periods ({detail}). Track at least one value at or before "
                f"{before!r} and another after it up to {after!r}."
            )

        return {
            "before": before_dt.isoformat(),
            "after": after_dt.isoformat(),
            "metrics_compared": len(metrics),
            "metrics": metrics,
            "skipped_metrics": skipped,
            "explanation": (
                "Computed only from values recorded via track_metric(); no "
                "historical diagnoses are reconstructed or invented."
            ),
        }

    def quality_scorer(self) -> QualityScorer:
        """
        Get a quality scorer for monitoring embedding quality.

        Returns:
            QualityScorer instance

        Examples:
            >>> scorer = hound.quality_scorer()
            >>> quality = scorer.score(embedding_vector)
            >>> health = scorer.corpus_health()
        """
        return QualityScorer(
            hound=self,
            adapter=self._active_adapter(),
            trend_analyzer=self._trend_analyzer,
        )

    def detect_drift(
        self,
        baseline_date: str,
        current_date: str,
        metric_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Detect drift in tracked metrics between two time periods.

        Delegates the statistics to `TrendAnalyzer.detect_drift_between()`.
        Baseline values are points at or before ``baseline_date``; current
        values are points strictly after it and at or before ``current_date``.
        A metric is reported only when both windows have samples.

        Args:
            baseline_date: Inclusive baseline boundary (YYYY-MM-DD or
                YYYY-MM-DD HH:MM:SS).
            current_date: Inclusive current boundary (same format).
            metric_name: Optional single metric to analyze. When omitted,
                every tracked metric with data in both windows is analyzed.

        Returns:
            Dictionary with per-metric `DriftAnalysis` data (as dicts), the
            list of anomalous metrics, and a ``significant`` boolean. Metrics
            that lack data in either window are listed under
            ``skipped_metrics`` with the reason.

        Raises:
            ValueError: If a timestamp cannot be parsed, ``baseline_date`` is
                after ``current_date``, the named metric is not tracked, no
                metrics are tracked, or no analyzed metric has samples in
                both periods.
        """
        baseline_dt = _parse_hound_timestamp(baseline_date, "baseline_date")
        current_dt = _parse_hound_timestamp(current_date, "current_date")
        if baseline_dt > current_dt:
            raise ValueError(
                f"baseline_date ({baseline_date!r}) must not be after "
                f"current_date ({current_date!r})"
            )

        series = self._trend_analyzer.series
        if not series:
            raise ValueError(
                "detect_drift() has no tracked metrics. Call "
                "hound.track_metric(name, value) over time, then retry."
            )

        if metric_name is not None:
            if metric_name not in series:
                raise ValueError(
                    f"Metric {metric_name!r} is not tracked. Tracked metrics: {sorted(series)}"
                )
            metric_names = [metric_name]
        else:
            metric_names = list(series)

        drifts: Dict[str, Dict[str, Any]] = {}
        skipped: Dict[str, str] = {}
        for name in metric_names:
            drift = self._trend_analyzer.detect_drift_between(name, baseline_dt, current_dt)
            if drift is None:
                skipped[name] = (
                    "needs at least one tracked point at or before "
                    "baseline_date and one after it up to current_date"
                )
            else:
                drifts[name] = drift.to_dict()

        if not drifts:
            detail = "; ".join(f"{name}: {reason}" for name, reason in sorted(skipped.items()))
            raise ValueError(
                "detect_drift() found no metric with samples in both periods "
                f"({detail}). Track values on both sides of {baseline_date!r} "
                f"and up to {current_date!r}."
            )

        anomalous = [name for name, drift in drifts.items() if drift["is_anomaly"]]
        return {
            "baseline_date": baseline_dt.isoformat(),
            "current_date": current_dt.isoformat(),
            "metrics_analyzed": len(drifts),
            "metrics": drifts,
            "anomalous_metrics": anomalous,
            "significant": bool(anomalous),
            "skipped_metrics": skipped,
            "explanation": (
                "Computed only from values recorded via track_metric(); no "
                "historical diagnoses are reconstructed or invented."
            ),
        }

    def benchmark(self) -> PerformanceBenchmark:
        """
        Access performance benchmarking engine.

        Returns:
            PerformanceBenchmark instance for measuring latency and performance

        Examples:
            >>> benchmark = hound.benchmark()
            >>> latency = benchmark.measure_query_latency(query_fn, num_iterations=100)
            >>> report = benchmark.get_performance_report()
        """
        return self._benchmarker

    def analyze_trends(self) -> TrendAnalyzer:
        """
        Access trend analysis engine.

        Returns:
            TrendAnalyzer instance for detecting drift and anomalies over time

        Examples:
            >>> analyzer = hound.analyze_trends()
            >>> analyzer.track_metric("embedding_isotropy", 0.92)
            >>> drift = analyzer.detect_drift("embedding_isotropy")
            >>> report = analyzer.get_trend_report()
        """
        return self._trend_analyzer

    def measure_query_latency(
        self,
        query_fn,
        num_iterations: int = 100,
    ) -> LatencyMetrics:
        """
        Measure query latency with percentile analysis.

        Args:
            query_fn: Callable that performs a query
            num_iterations: Number of iterations to measure

        Returns:
            LatencyMetrics with p50, p95, p99 percentiles

        Examples:
            >>> metrics = hound.measure_query_latency(lambda: hound.diagnose("test"), 100)
            >>> print(f"P95 latency: {metrics.p95}ms")
        """
        return self._benchmarker.measure_query_latency(query_fn, num_iterations)

    def track_metric(
        self,
        metric_name: str,
        value: float,
        timestamp: Optional[datetime] = None,
        **tags,
    ) -> None:
        """
        Track a metric value for trend analysis.

        Args:
            metric_name: Name of metric (e.g., "embedding_isotropy")
            value: Metric value
            timestamp: Optional UTC datetime for the sample (defaults to now).
                Supply explicit timestamps when you want to compare or detect
                drift over named historical periods.
            **tags: Optional tags for filtering (e.g., db="qdrant")

        Examples:
            >>> hound.track_metric("embedding_isotropy", 0.92, model="openai")
            >>> hound.track_metric("query_latency_ms", 45.2, db="qdrant")
        """
        self._trend_analyzer.track_metric(metric_name, value, timestamp=timestamp, **tags)

    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get comprehensive performance benchmarking report.

        Returns:
            Dictionary with performance metrics and analysis

        Examples:
            >>> report = hound.get_performance_report()
            >>> print(report["latest_snapshot"])
        """
        return self._benchmarker.get_performance_report()

    def get_trend_report(self, metric_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get comprehensive trend analysis report.

        Args:
            metric_names: List of metrics to include (None = all)

        Returns:
            Dictionary with trend analysis for all tracked metrics

        Examples:
            >>> report = hound.get_trend_report()
            >>> print(report["metrics"])
        """
        return self._trend_analyzer.get_trend_report(metric_names)

    def tracer(self) -> RetrievalTracer:
        """
        Access retrieval trace capture engine.

        Returns:
            RetrievalTracer instance for capturing pipeline execution

        Examples:
            >>> tracer = hound.tracer()
            >>> tracer.start_trace("query_1", "search query")
            >>> tracer.record_embedding(embedding, 15.2)
            >>> tracer.record_vector_search_results(results)
            >>> trace = tracer.end_trace()
        """
        return self._tracer

    def replayer(self) -> RetrievalReplayer:
        """
        Access retrieval replay engine.

        Returns:
            RetrievalReplayer instance for interactive debugging

        Examples:
            >>> replayer = hound.replayer()
            >>> config = replayer.create_configuration("config_1", {...})
            >>> result = replayer.replay(trace, "config_1")
            >>> comparison = replayer.compare_configurations("config_1", "config_2")
        """
        return self._replayer

    def get_recommendations(
        self,
        query_id: str,
        query_text: str,
        diagnosis: Dict[str, Any],
        trace_analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get AI-powered recommendations for retrieval failure.

        Args:
            query_id: Unique query identifier
            query_text: The search query
            diagnosis: Diagnostic analysis results
            trace_analysis: Optional detailed trace analysis

        Returns:
            Dictionary with recommendations and ROI analysis

        Examples:
            >>> recommendations = hound.get_recommendations(
            ...     "query_1",
            ...     "search query",
            ...     diagnosis_results
            ... )
            >>> for rec in recommendations["recommendations"]:
            ...     print(f"{rec['title']}: +{rec['expected_improvement_pct']}%")
        """
        report = self._recommendation_engine.analyze_failure(
            query_id, query_text, diagnosis, trace_analysis
        )
        return report.to_dict()

    def get_recommendation_summary(self, query_id: str) -> Optional[Dict[str, Any]]:
        """
        Get summary of recommendations for a query.

        Args:
            query_id: Query identifier

        Returns:
            Summary dictionary or None if not found

        Examples:
            >>> summary = hound.get_recommendation_summary("query_1")
            >>> print(summary["executive_summary"])
        """
        return self._recommendation_engine.get_recommendation_summary(query_id)
