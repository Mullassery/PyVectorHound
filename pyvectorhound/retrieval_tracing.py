"""Retrieval pipeline trace capture for diagnostics and replay.

Captures complete pipeline state for every retrieval query, enabling
interactive debugging through replay mode.
"""

import time
import json
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import numpy as np
from enum import Enum


class TracePhase(Enum):
    """Retrieval pipeline phases."""

    QUERY_EMBEDDING = "query_embedding"
    VECTOR_SEARCH = "vector_search"
    BM25_SEARCH = "bm25_search"
    METADATA_FILTERING = "metadata_filtering"
    RERANKING = "reranking"
    CONTEXT_ASSEMBLY = "context_assembly"
    LLM_GENERATION = "llm_generation"


@dataclass
class SearchResult:
    """Single search result document."""

    doc_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    rank: int = 0
    is_relevant: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class PhaseMetrics:
    """Metrics for a single pipeline phase."""

    phase: str
    start_time: float
    end_time: float
    duration_ms: float
    input_size: int
    output_size: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class RetrievalTrace:
    """Complete trace of a retrieval query."""

    query_id: str
    query_text: str
    timestamp: datetime
    query_embedding: Optional[np.ndarray]
    embedding_model: str
    embedding_latency_ms: float
    vector_search_results: List[SearchResult]
    bm25_results: Optional[List[SearchResult]] = None
    filtered_results: Optional[List[SearchResult]] = None
    reranked_results: Optional[List[SearchResult]] = None
    final_context: Optional[str] = None
    llm_response: Optional[str] = None
    phase_metrics: Dict[str, PhaseMetrics] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self, include_embeddings: bool = False) -> Dict[str, Any]:
        """Convert to dictionary for storage.

        Args:
            include_embeddings: Whether to include embedding vectors (large)

        Returns:
            Dictionary representation
        """
        return {
            "query_id": self.query_id,
            "query_text": self.query_text,
            "timestamp": self.timestamp.isoformat(),
            "embedding_model": self.embedding_model,
            "embedding_latency_ms": self.embedding_latency_ms,
            "embedding": self.query_embedding.tolist() if include_embeddings and self.query_embedding is not None else None,
            "vector_search_results": [r.to_dict() for r in self.vector_search_results],
            "bm25_results": [r.to_dict() for r in (self.bm25_results or [])],
            "filtered_results": [r.to_dict() for r in (self.filtered_results or [])],
            "reranked_results": [r.to_dict() for r in (self.reranked_results or [])],
            "final_context": self.final_context,
            "llm_response": self.llm_response,
            "phase_metrics": {k: v.to_dict() for k, v in self.phase_metrics.items()},
            "metadata": self.metadata,
        }


class RetrievalTracer:
    """Trace and capture retrieval pipeline execution.

    Records every step of the retrieval pipeline for later analysis and replay.
    """

    def __init__(self):
        """Initialize tracer."""
        self.traces: Dict[str, RetrievalTrace] = {}
        self._current_trace: Optional[RetrievalTrace] = None
        self._phase_start_time: Optional[float] = None

    def start_trace(
        self,
        query_id: str,
        query_text: str,
        embedding_model: str = "openai-3-small",
    ) -> None:
        """Start tracing a new query.

        Args:
            query_id: Unique query identifier
            query_text: The search query
            embedding_model: Embedding model used
        """
        self._current_trace = RetrievalTrace(
            query_id=query_id,
            query_text=query_text,
            timestamp=datetime.utcnow(),
            query_embedding=None,
            embedding_model=embedding_model,
            embedding_latency_ms=0.0,
            vector_search_results=[],
        )

    def record_embedding(
        self, embedding: np.ndarray, latency_ms: float
    ) -> None:
        """Record query embedding.

        Args:
            embedding: Query embedding vector
            latency_ms: Embedding generation latency in milliseconds
        """
        if self._current_trace is None:
            return

        self._current_trace.query_embedding = embedding
        self._current_trace.embedding_latency_ms = latency_ms

    def start_phase(self, phase: TracePhase) -> None:
        """Mark start of a pipeline phase.

        Args:
            phase: Phase type
        """
        self._phase_start_time = time.perf_counter()

    def end_phase(
        self,
        phase: TracePhase,
        input_size: int,
        output_size: int,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Mark end of a pipeline phase.

        Args:
            phase: Phase type
            input_size: Number of items entering phase
            output_size: Number of items leaving phase
            metadata: Optional phase metadata
        """
        if self._current_trace is None or self._phase_start_time is None:
            return

        duration_ms = (time.perf_counter() - self._phase_start_time) * 1000

        metrics = PhaseMetrics(
            phase=phase.value,
            start_time=self._phase_start_time,
            end_time=time.perf_counter(),
            duration_ms=duration_ms,
            input_size=input_size,
            output_size=output_size,
            metadata=metadata or {},
        )

        self._current_trace.phase_metrics[phase.value] = metrics
        self._phase_start_time = None

    def record_vector_search_results(
        self, results: List[SearchResult]
    ) -> None:
        """Record vector search results.

        Args:
            results: List of retrieved documents
        """
        if self._current_trace is None:
            return

        self._current_trace.vector_search_results = results

    def record_bm25_results(self, results: List[SearchResult]) -> None:
        """Record BM25 search results.

        Args:
            results: List of keyword search results
        """
        if self._current_trace is None:
            return

        self._current_trace.bm25_results = results

    def record_filtered_results(self, results: List[SearchResult]) -> None:
        """Record results after metadata filtering.

        Args:
            results: Filtered results
        """
        if self._current_trace is None:
            return

        self._current_trace.filtered_results = results

    def record_reranked_results(self, results: List[SearchResult]) -> None:
        """Record results after reranking.

        Args:
            results: Reranked results
        """
        if self._current_trace is None:
            return

        self._current_trace.reranked_results = results

    def record_context_assembly(self, context: str) -> None:
        """Record assembled context for LLM.

        Args:
            context: Final context passed to LLM
        """
        if self._current_trace is None:
            return

        self._current_trace.final_context = context

    def record_llm_response(self, response: str) -> None:
        """Record LLM response.

        Args:
            response: LLM-generated response
        """
        if self._current_trace is None:
            return

        self._current_trace.llm_response = response

    def record_metadata(self, key: str, value: Any) -> None:
        """Record custom metadata.

        Args:
            key: Metadata key
            value: Metadata value
        """
        if self._current_trace is None:
            return

        self._current_trace.metadata[key] = value

    def end_trace(self) -> Optional[RetrievalTrace]:
        """Complete current trace and store it.

        Returns:
            Completed RetrievalTrace
        """
        if self._current_trace is None:
            return None

        trace = self._current_trace
        self.traces[trace.query_id] = trace
        self._current_trace = None

        return trace

    def get_trace(self, query_id: str) -> Optional[RetrievalTrace]:
        """Retrieve a stored trace.

        Args:
            query_id: Query identifier

        Returns:
            RetrievalTrace or None
        """
        return self.traces.get(query_id)

    def get_all_traces(self) -> List[RetrievalTrace]:
        """Get all stored traces.

        Returns:
            List of all traces
        """
        return list(self.traces.values())

    def get_trace_analysis(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Analyze a trace for bottlenecks and issues.

        Args:
            query_id: Query identifier

        Returns:
            Analysis dictionary
        """
        trace = self.get_trace(query_id)
        if trace is None:
            return None

        # Find slowest phase
        slowest_phase = max(
            trace.phase_metrics.items(),
            key=lambda x: x[1].duration_ms,
            default=(None, None),
        )

        # Calculate phase percentages
        total_time = sum(m.duration_ms for m in trace.phase_metrics.values())
        phase_percentages = {
            name: (metrics.duration_ms / total_time * 100) if total_time > 0 else 0
            for name, metrics in trace.phase_metrics.items()
        }

        # Analyze result quality
        recall_at_k = {}
        for k in [1, 5, 10]:
            if len(trace.vector_search_results) >= k:
                relevant = sum(
                    1
                    for r in trace.vector_search_results[:k]
                    if r.is_relevant
                )
                recall_at_k[k] = relevant / k

        return {
            "query_id": query_id,
            "total_time_ms": total_time,
            "slowest_phase": slowest_phase[0],
            "slowest_phase_duration_ms": slowest_phase[1].duration_ms if slowest_phase[1] else 0,
            "phase_breakdown": phase_percentages,
            "num_vector_results": len(trace.vector_search_results),
            "num_final_results": (
                len(trace.reranked_results)
                if trace.reranked_results
                else len(trace.vector_search_results)
            ),
            "recall_at_k": recall_at_k,
            "embedding_latency_ms": trace.embedding_latency_ms,
            "has_llm_response": trace.llm_response is not None,
        }

    def export_trace(
        self, query_id: str, include_embeddings: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Export trace as JSON-serializable dictionary.

        Args:
            query_id: Query identifier
            include_embeddings: Whether to include embedding vectors

        Returns:
            Dictionary representation
        """
        trace = self.get_trace(query_id)
        if trace is None:
            return None

        return trace.to_dict(include_embeddings=include_embeddings)

    def export_all_traces(
        self, include_embeddings: bool = False
    ) -> List[Dict[str, Any]]:
        """Export all traces.

        Args:
            include_embeddings: Whether to include embedding vectors

        Returns:
            List of trace dictionaries
        """
        return [t.to_dict(include_embeddings=include_embeddings) for t in self.get_all_traces()]

    def clear_traces(self) -> None:
        """Clear all stored traces."""
        self.traces.clear()
        self._current_trace = None

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics across all traces.

        Returns:
            Statistics dictionary
        """
        if not self.traces:
            return {}

        latencies = [t.embedding_latency_ms for t in self.traces.values()]
        result_counts = [len(t.vector_search_results) for t in self.traces.values()]

        return {
            "num_traces": len(self.traces),
            "avg_embedding_latency_ms": np.mean(latencies),
            "max_embedding_latency_ms": np.max(latencies),
            "min_embedding_latency_ms": np.min(latencies),
            "avg_results_retrieved": np.mean(result_counts),
            "max_results_retrieved": np.max(result_counts),
            "min_results_retrieved": np.min(result_counts),
        }
