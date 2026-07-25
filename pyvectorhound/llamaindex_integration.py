"""LlamaIndex integration for PyVectorHound.

Enables automatic trace capture from LlamaIndex query engines and provides
node postprocessors with built-in diagnostics.
"""

from typing import Any, List, Optional, Dict
from dataclasses import dataclass
import numpy as np
from datetime import datetime


@dataclass
class LlamaIndexTracingConfig:
    """Configuration for LlamaIndex tracing."""

    enabled: bool = True
    capture_embeddings: bool = False
    capture_node_scores: bool = True
    capture_metadata: bool = True
    capture_retrieval_events: bool = True
    auto_diagnose: bool = False


class PyVectorHoundInstrumentationCallback:
    """LlamaIndex instrumentation callback for PyVectorHound.

    Captures trace events from LlamaIndex query execution.
    """

    def __init__(self, hound: Optional[Any] = None, config: Optional[LlamaIndexTracingConfig] = None):
        """Initialize instrumentation callback.

        Args:
            hound: PyVectorHound Hound instance
            config: Tracing configuration
        """
        self.hound = hound
        self.config = config or LlamaIndexTracingConfig()
        self._current_query_id: Optional[str] = None
        self._retrieved_nodes: List[Any] = []

    def on_retrieve_start(
        self,
        event_id: str,
        retriever: Any,
        query_str: str,
        **kwargs: Any,
    ) -> None:
        """Called when retrieval starts.

        Args:
            event_id: Event ID
            retriever: Retriever instance
            query_str: Query string
            **kwargs: Additional arguments
        """
        if not self.hound:
            return

        self._current_query_id = event_id
        tracer = self.hound.tracer()

        # Extract embedding model from retriever if available
        embedding_model = self._extract_embedding_model(retriever)

        tracer.start_trace(event_id, query_str, embedding_model)

    def on_retrieve_end(
        self,
        nodes: List[Any],
        retriever: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        """Called when retrieval ends.

        Args:
            nodes: Retrieved nodes
            retriever: Retriever instance
            **kwargs: Additional arguments
        """
        if not self.hound or not self._current_query_id:
            return

        self._retrieved_nodes = nodes
        tracer = self.hound.tracer()

        # Convert LlamaIndex nodes to SearchResult
        from pyvectorhound.retrieval_tracing import SearchResult

        results = []
        for i, node in enumerate(nodes):
            # Handle both Node and TextNode
            if hasattr(node, "get_content"):
                content = node.get_content()
            elif hasattr(node, "text"):
                content = node.text
            else:
                content = str(node)

            # Get score if available
            score = getattr(node, "score", 1.0 - (i * 0.1))

            # Get metadata
            metadata = {}
            if hasattr(node, "metadata"):
                metadata = node.metadata or {}

            results.append(
                SearchResult(
                    doc_id=getattr(node, "node_id", f"node_{i}"),
                    content=content,
                    score=float(score),
                    metadata=metadata,
                    rank=i,
                )
            )

        tracer.record_vector_search_results(results)

    def on_synthesize_start(
        self,
        event_id: str,
        nodes: List[Any],
        query_str: str,
        **kwargs: Any,
    ) -> None:
        """Called when synthesis (LLM generation) starts.

        Args:
            event_id: Event ID
            nodes: Retrieved nodes being synthesized
            query_str: Query string
            **kwargs: Additional arguments
        """
        if not self.hound or not self._current_query_id:
            return

        tracer = self.hound.tracer()

        # Record context assembly from nodes
        context_parts = []
        for node in nodes:
            if hasattr(node, "get_content"):
                context_parts.append(node.get_content())
            elif hasattr(node, "text"):
                context_parts.append(node.text)

        context = "\n".join(context_parts[:5])  # First 5 nodes
        if len(context_parts) > 5:
            context += f"\n... and {len(context_parts) - 5} more nodes"

        tracer.record_context_assembly(context)

    def on_synthesize_end(
        self,
        response: Any,
        **kwargs: Any,
    ) -> None:
        """Called when synthesis ends.

        Args:
            response: Synthesized response
            **kwargs: Additional arguments
        """
        if not self.hound or not self._current_query_id:
            return

        tracer = self.hound.tracer()

        # Extract response text
        response_text = ""
        if hasattr(response, "response"):
            response_text = response.response
        elif isinstance(response, str):
            response_text = response
        elif hasattr(response, "get_response"):
            response_text = response.get_response()

        tracer.record_llm_response(response_text)
        trace = tracer.end_trace()

        # Auto-diagnose if enabled
        if self.config.auto_diagnose and trace:
            self._run_auto_diagnosis(trace)

    def _extract_embedding_model(self, retriever: Any) -> str:
        """Extract embedding model from retriever.

        Args:
            retriever: LlamaIndex retriever

        Returns:
            Embedding model name or default
        """
        # Try various LlamaIndex retriever types
        if hasattr(retriever, "_embed_model"):
            embed_model = retriever._embed_model
            if hasattr(embed_model, "model_name"):
                return embed_model.model_name
            if hasattr(embed_model, "model"):
                return embed_model.model

        if hasattr(retriever, "embed_model"):
            embed_model = retriever.embed_model
            if hasattr(embed_model, "model_name"):
                return embed_model.model_name

        return "unknown"

    def _run_auto_diagnosis(self, trace: Any) -> None:
        """Run automatic diagnosis on trace.

        Args:
            trace: RetrievalTrace to analyze
        """
        if not self.hound:
            return

        # Get analysis
        analysis = self.hound.tracer().get_trace_analysis(trace.query_id)
        if analysis and analysis.get("slowest_phase"):
            slowest = analysis["slowest_phase"]
            if analysis.get(slowest, 0) > 100:  # >100ms
                print(f"⚠️  Slow phase detected: {slowest} ({analysis[slowest]:.0f}ms)")


class DiagnosticNodePostprocessor:
    """Node postprocessor with built-in diagnostics.

    Base class for creating node postprocessors that capture diagnostics.
    """

    def __init__(self, hound: Optional[Any] = None):
        """Initialize diagnostic postprocessor.

        Args:
            hound: PyVectorHound Hound instance
        """
        self.hound = hound

    def _postprocess_nodes(
        self,
        nodes: List[Any],
        query_str: Optional[str] = None,
    ) -> List[Any]:
        """Post-process retrieved nodes.

        Override this method to implement custom post-processing.

        Args:
            nodes: Retrieved nodes
            query_str: Query string

        Returns:
            Post-processed nodes
        """
        return nodes

    def postprocess_nodes(
        self,
        nodes: List[Any],
        query_bundle: Optional[Any] = None,
    ) -> List[Any]:
        """Post-process nodes (LlamaIndex interface).

        Args:
            nodes: Retrieved nodes
            query_bundle: Query bundle

        Returns:
            Post-processed nodes
        """
        query_str = None
        if query_bundle is not None:
            if hasattr(query_bundle, "query_str"):
                query_str = query_bundle.query_str

        return self._postprocess_nodes(nodes, query_str)

    def __call__(self, nodes: List[Any]) -> List[Any]:
        """Call interface.

        Args:
            nodes: Retrieved nodes

        Returns:
            Post-processed nodes
        """
        return self.postprocess_nodes(nodes)


class DiagnosticVectorIndexRetriever:
    """Instrumented vector index retriever for LlamaIndex.

    Wraps a LlamaIndex vector retriever to capture diagnostics automatically.
    """

    def __init__(self, retriever: Any, hound: Optional[Any] = None):
        """Initialize diagnostic retriever.

        Args:
            retriever: LlamaIndex retriever to wrap
            hound: PyVectorHound Hound instance
        """
        self.retriever = retriever
        self.hound = hound
        self._callback = PyVectorHoundInstrumentationCallback(hound)

    def retrieve(self, query_str: str) -> List[Any]:
        """Retrieve with automatic tracing.

        Args:
            query_str: Query string

        Returns:
            Retrieved nodes
        """
        event_id = f"retrieve_{hash(query_str)}"
        self._callback.on_retrieve_start(event_id, self.retriever, query_str)

        # Call underlying retriever
        nodes = self.retriever.retrieve(query_str)

        self._callback.on_retrieve_end(nodes, self.retriever)

        return nodes

    async def aretrieve(self, query_str: str) -> List[Any]:
        """Async retrieve with automatic tracing.

        Args:
            query_str: Query string

        Returns:
            Retrieved nodes
        """
        event_id = f"retrieve_{hash(query_str)}"
        self._callback.on_retrieve_start(event_id, self.retriever, query_str)

        # Call underlying retriever
        if hasattr(self.retriever, "aretrieve"):
            nodes = await self.retriever.aretrieve(query_str)
        else:
            nodes = self.retriever.retrieve(query_str)

        self._callback.on_retrieve_end(nodes, self.retriever)

        return nodes

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to wrapped retriever.

        Args:
            name: Attribute name

        Returns:
            Attribute value
        """
        return getattr(self.retriever, name)


class DiagnosticQueryEngine:
    """LlamaIndex query engine with built-in diagnostics.

    Wraps a LlamaIndex query engine to capture diagnostics automatically.
    """

    def __init__(self, engine: Any, hound: Optional[Any] = None):
        """Initialize diagnostic query engine.

        Args:
            engine: LlamaIndex query engine to wrap
            hound: PyVectorHound Hound instance
        """
        self.engine = engine
        self.hound = hound
        self._callback = PyVectorHoundInstrumentationCallback(hound)

    def query(self, query_str: str, **kwargs: Any) -> Any:
        """Query with automatic tracing.

        Args:
            query_str: Query string
            **kwargs: Additional arguments

        Returns:
            Query response
        """
        event_id = f"query_{hash(query_str)}"
        self._callback.on_retrieve_start(event_id, self.engine, query_str)

        # Call underlying engine
        response = self.engine.query(query_str, **kwargs)

        # Record end events
        if hasattr(response, "source_nodes"):
            self._callback.on_retrieve_end(response.source_nodes)

        self._callback.on_synthesize_end(response)

        return response

    async def aquery(self, query_str: str, **kwargs: Any) -> Any:
        """Async query with automatic tracing.

        Args:
            query_str: Query string
            **kwargs: Additional arguments

        Returns:
            Query response
        """
        event_id = f"query_{hash(query_str)}"
        self._callback.on_retrieve_start(event_id, self.engine, query_str)

        # Call underlying engine
        if hasattr(self.engine, "aquery"):
            response = await self.engine.aquery(query_str, **kwargs)
        else:
            response = self.engine.query(query_str, **kwargs)

        # Record end events
        if hasattr(response, "source_nodes"):
            self._callback.on_retrieve_end(response.source_nodes)

        self._callback.on_synthesize_end(response)

        return response

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to wrapped engine.

        Args:
            name: Attribute name

        Returns:
            Attribute value
        """
        return getattr(self.engine, name)


def instrument_llamaindex_engine(
    engine: Any, hound: Optional[Any] = None
) -> DiagnosticQueryEngine:
    """Instrument a LlamaIndex query engine for diagnostics.

    Args:
        engine: LlamaIndex query engine to instrument
        hound: PyVectorHound Hound instance

    Returns:
        Instrumented query engine
    """
    return DiagnosticQueryEngine(engine, hound)


def instrument_llamaindex_retriever(
    retriever: Any, hound: Optional[Any] = None
) -> DiagnosticVectorIndexRetriever:
    """Instrument a LlamaIndex retriever for diagnostics.

    Args:
        retriever: LlamaIndex retriever to instrument
        hound: PyVectorHound Hound instance

    Returns:
        Instrumented retriever
    """
    return DiagnosticVectorIndexRetriever(retriever, hound)
