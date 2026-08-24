"""Main PyHound class for retrieval diagnostics."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Dict, Any, Callable
import numpy as np
from pyvectorhound.database import get_adapter, VectorDB
from pyvectorhound.diagnosis import Diagnosis
from pyvectorhound.comparison import ModelComparison
from pyvectorhound.scorer import QualityScorer
from pyvectorhound.benchmarking import PerformanceBenchmark, LatencyMetrics
from pyvectorhound.trend_analysis import TrendAnalyzer
from pyvectorhound.retrieval_tracing import RetrievalTracer
from pyvectorhound.retrieval_replay import RetrievalReplayer
from pyvectorhound.recommendations import RecommendationEngine
from pyvectorhound._retry import call_with_backoff


class Hound:
    """
    Main PyHound class for diagnosing retrieval pipeline issues.

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
        **kwargs: Any
    ):
        """
        Initialize PyHound.

        Args:
            db: Vector database type. Supported: 'qdrant', 'chroma', 'milvus', 'weaviate', 'postgres'
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
            **self.kwargs
        )

        # Initialize performance benchmarking and trend analysis
        self._benchmarker = PerformanceBenchmark(adapter=self.adapter)
        self._trend_analyzer = TrendAnalyzer()

        # Initialize retrieval tracing, replay, and recommendations
        self._tracer = RetrievalTracer()
        self._replayer = RetrievalReplayer()
        self._recommendation_engine = RecommendationEngine()

    def diagnose(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        expected_docs: Optional[List[str]] = None,
        verbose: bool = False,
        document_texts: Optional[Dict[str, str]] = None,
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

        # Search for results
        results = self.adapter.search(query_embedding, top_k=top_k)

        # Create diagnosis
        diagnosis = Diagnosis(
            query=query,
            results=results,
            expected_docs=expected_docs,
            adapter=self.adapter,
            query_embedding=query_embedding,
            trend_analyzer=self._trend_analyzer,
            document_texts=document_texts,
            llm_judge_fn=self.llm_judge_fn,
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
        if not (len(query_embeddings) == len(expected_docs) == len(document_texts) == n):
            raise ValueError(
                "queries, query_embeddings, expected_docs, and document_texts must "
                "all be the same length when provided."
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
                ): i
                for i in range(n)
            }
            for future in as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    results[i] = future.result()
                except Exception as exc:  # noqa: BLE001 - surfaced to the caller below
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
            **kwargs
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

        Hound keeps no historical record of past diagnoses by date, so it
        has nothing to honestly compare `before` against `after` with. Use
        `hound.track_metric()` after each `diagnose()` call to build a real
        time series, then `hound.get_trend_report()` to compare periods for
        real.

        Args:
            before: Timestamp or date of baseline (format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
            after: Timestamp or date of comparison (same format)

        Raises:
            NotImplementedError: Always -- this method has no backing data
                store to answer the question honestly.
        """
        raise NotImplementedError(
            f"compare_metrics() has no historical data to compare {before!r} "
            f"against {after!r} -- Hound does not store past diagnoses. Use "
            "track_metric() after each diagnose() call, then get_trend_report() "
            "to compare periods for real."
        )

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
        return QualityScorer(hound=self, adapter=self.adapter, trend_analyzer=self._trend_analyzer)

    def detect_drift(
        self,
        baseline_date: str,
        current_date: str,
    ) -> Dict[str, Any]:
        """
        Detect embedding quality drift over time.

        This convenience method has no historical record to compare
        `baseline_date` against `current_date` with. Use
        `hound.analyze_trends()` (a real `TrendAnalyzer`) instead:
        `track_metric()` after each `diagnose()` call to build a real time
        series, then `TrendAnalyzer.detect_drift(metric_name)` for a real
        statistical comparison.

        Args:
            baseline_date: Baseline date (format: YYYY-MM-DD)
            current_date: Current date (format: YYYY-MM-DD)

        Raises:
            NotImplementedError: Always -- this method has no backing data
                store to answer the question honestly.
        """
        raise NotImplementedError(
            f"detect_drift() has no historical data to compare {baseline_date!r} "
            f"against {current_date!r} -- Hound does not store past diagnoses. "
            "Use hound.analyze_trends() (TrendAnalyzer): track_metric() after "
            "each diagnose() call, then TrendAnalyzer.detect_drift(metric_name) "
            "for a real statistical comparison."
        )

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
        **tags,
    ) -> None:
        """
        Track a metric value for trend analysis.

        Args:
            metric_name: Name of metric (e.g., "embedding_isotropy")
            value: Metric value
            **tags: Optional tags for filtering (e.g., db="qdrant")

        Examples:
            >>> hound.track_metric("embedding_isotropy", 0.92, model="openai")
            >>> hound.track_metric("query_latency_ms", 45.2, db="qdrant")
        """
        self._trend_analyzer.track_metric(metric_name, value, **tags)

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
