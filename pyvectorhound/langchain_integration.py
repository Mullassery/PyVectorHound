"""LangChain integration for PyVectorHound.

Enables automatic trace capture from LangChain RAG chains and provides
drop-in retriever replacements with built-in diagnostics.
"""

from typing import Any, List, Optional, Dict, Callable
from dataclasses import dataclass
import numpy as np
from datetime import datetime


@dataclass
class LangChainTracingConfig:
    """Configuration for LangChain tracing."""

    enabled: bool = True
    capture_embeddings: bool = False
    capture_reranker_scores: bool = True
    capture_metadata: bool = True
    trace_callbacks: bool = True
    auto_diagnose: bool = False


class PyVectorHoundCallbackHandler:
    """LangChain callback handler for PyVectorHound.

    Automatically captures traces from LangChain chain execution.
    """

    def __init__(self, hound: Optional[Any] = None, config: Optional[LangChainTracingConfig] = None):
        """Initialize callback handler.

        Args:
            hound: PyVectorHound Hound instance
            config: Tracing configuration
        """
        self.hound = hound
        self.config = config or LangChainTracingConfig()
        self._current_trace_id: Optional[str] = None
        self._phase_stack: List[str] = []

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        **kwargs: Any,
    ) -> None:
        """Called when retriever starts.

        Args:
            serialized: Serialized retriever info
            query: Query being executed
            **kwargs: Additional arguments
        """
        if not self.hound:
            return

        self._current_trace_id = kwargs.get("run_id", "trace_unknown")
        tracer = self.hound.tracer()

        # Get embedding model from retriever config if available
        embedding_model = self._extract_embedding_model(serialized)

        tracer.start_trace(self._current_trace_id, query, embedding_model)

    def on_retriever_end(
        self,
        documents: List[Any],
        **kwargs: Any,
    ) -> None:
        """Called when retriever ends.

        Args:
            documents: Retrieved documents
            **kwargs: Additional arguments
        """
        if not self.hound or not self._current_trace_id:
            return

        tracer = self.hound.tracer()

        # Convert LangChain documents to SearchResult
        from pyvectorhound.retrieval_tracing import SearchResult

        results = []
        for i, doc in enumerate(documents):
            # Handle both LangChain Document and dict formats
            if hasattr(doc, "page_content"):
                content = doc.page_content
                metadata = getattr(doc, "metadata", {})
            else:
                content = doc.get("page_content", "")
                metadata = doc.get("metadata", {})

            score = metadata.pop("score", 1.0 - (i * 0.1))  # Estimate score

            results.append(
                SearchResult(
                    doc_id=metadata.get("id", f"doc_{i}"),
                    content=content,
                    score=float(score),
                    metadata=metadata,
                    rank=i,
                )
            )

        tracer.record_vector_search_results(results)

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ) -> None:
        """Called when LLM starts.

        Args:
            serialized: Serialized LLM info
            prompts: Prompts being used
            **kwargs: Additional arguments
        """
        if not self.hound or not self._current_trace_id:
            return

        # Record context assembly (context is in the prompt)
        tracer = self.hound.tracer()
        if prompts:
            tracer.record_context_assembly(prompts[0])

    def on_llm_end(
        self,
        response: Any,
        **kwargs: Any,
    ) -> None:
        """Called when LLM ends.

        Args:
            response: LLM response
            **kwargs: Additional arguments
        """
        if not self.hound or not self._current_trace_id:
            return

        tracer = self.hound.tracer()

        # Extract response text
        response_text = ""
        if hasattr(response, "generations"):
            if response.generations and len(response.generations) > 0:
                gen = response.generations[0]
                if hasattr(gen, "text"):
                    response_text = gen.text
                elif isinstance(gen, list) and len(gen) > 0:
                    response_text = gen[0].text if hasattr(gen[0], "text") else str(gen[0])

        tracer.record_llm_response(response_text)
        trace = tracer.end_trace()

        # Auto-diagnose if enabled
        if self.config.auto_diagnose and trace:
            self._run_auto_diagnosis(trace)

    def _extract_embedding_model(self, serialized: Dict[str, Any]) -> str:
        """Extract embedding model name from retriever config.

        Args:
            serialized: Serialized retriever

        Returns:
            Embedding model name or default
        """
        # Try to extract from various LangChain retriever types
        if "kwargs" in serialized:
            kwargs = serialized["kwargs"]
            if "embeddings" in kwargs:
                embeddings = kwargs["embeddings"]
                if hasattr(embeddings, "model"):
                    return embeddings.model
                if isinstance(embeddings, dict) and "model" in embeddings:
                    return embeddings["model"]

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
            if analysis[slowest] > 100:  # >100ms
                print(f"⚠️  Slow phase detected: {slowest} ({analysis[slowest]:.0f}ms)")


class InstrumentedRetriever:
    """Instrumented retriever wrapper for LangChain.

    Wraps a LangChain retriever to capture diagnostics automatically.
    """

    def __init__(self, retriever: Any, hound: Optional[Any] = None):
        """Initialize instrumented retriever.

        Args:
            retriever: LangChain retriever to wrap
            hound: PyVectorHound Hound instance
        """
        self.retriever = retriever
        self.hound = hound
        self._callback_handler = PyVectorHoundCallbackHandler(hound) if hound else None

    def get_relevant_documents(self, query: str) -> List[Any]:
        """Get relevant documents with automatic tracing.

        Args:
            query: Query string

        Returns:
            List of relevant documents
        """
        if self._callback_handler:
            self._callback_handler.on_retriever_start({}, query)

        # Call underlying retriever
        documents = self.retriever.get_relevant_documents(query)

        if self._callback_handler:
            self._callback_handler.on_retriever_end(documents)

        return documents

    async def aget_relevant_documents(self, query: str) -> List[Any]:
        """Async version of get_relevant_documents.

        Args:
            query: Query string

        Returns:
            List of relevant documents
        """
        if self._callback_handler:
            self._callback_handler.on_retriever_start({}, query)

        # Call underlying retriever
        if hasattr(self.retriever, "aget_relevant_documents"):
            documents = await self.retriever.aget_relevant_documents(query)
        else:
            documents = self.retriever.get_relevant_documents(query)

        if self._callback_handler:
            self._callback_handler.on_retriever_end(documents)

        return documents

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to wrapped retriever.

        Args:
            name: Attribute name

        Returns:
            Attribute value
        """
        return getattr(self.retriever, name)


class DiagnosticRetrievalQA:
    """LangChain RetrievalQA with built-in diagnostics.

    Drop-in replacement for langchain.chains.RetrievalQA that captures
    diagnostics automatically.
    """

    def __init__(
        self,
        retriever: Any,
        llm: Any,
        hound: Optional[Any] = None,
        prompt: Optional[Any] = None,
        **kwargs: Any,
    ):
        """Initialize diagnostic retrieval QA.

        Args:
            retriever: LangChain retriever
            llm: Language model
            hound: PyVectorHound Hound instance
            prompt: Optional custom prompt
            **kwargs: Additional RetrievalQA arguments
        """
        self.hound = hound
        self.instrumented_retriever = InstrumentedRetriever(retriever, hound)

        # Import here to avoid hard dependency
        try:
            from langchain.chains import RetrievalQA

            self.chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.instrumented_retriever,
                **kwargs,
            )
        except ImportError:
            raise ImportError(
                "LangChain not installed. Install with: pip install langchain"
            )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the chain.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Chain result
        """
        return self.chain(*args, **kwargs)

    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        """Invoke the chain (newer LangChain API).

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Chain result
        """
        if hasattr(self.chain, "invoke"):
            return self.chain.invoke(*args, **kwargs)
        else:
            return self.chain(*args, **kwargs)


def instrument_langchain_chain(
    chain: Any, hound: Optional[Any] = None
) -> Any:
    """Instrument a LangChain chain for diagnostics.

    Args:
        chain: LangChain chain to instrument
        hound: PyVectorHound Hound instance

    Returns:
        Instrumented chain with callback handlers
    """
    if not hound:
        return chain

    # Add callback handler
    callback = PyVectorHoundCallbackHandler(hound)

    # Add to chain callbacks if supported
    if hasattr(chain, "callbacks"):
        if chain.callbacks is None:
            chain.callbacks = []
        chain.callbacks.append(callback)

    return chain


def create_diagnostic_qa_chain(
    retriever: Any,
    llm: Any,
    hound: Optional[Any] = None,
    **kwargs: Any,
) -> DiagnosticRetrievalQA:
    """Create a diagnostic retrieval QA chain.

    Args:
        retriever: LangChain retriever
        llm: Language model
        hound: PyVectorHound Hound instance
        **kwargs: Additional chain arguments

    Returns:
        DiagnosticRetrievalQA chain
    """
    return DiagnosticRetrievalQA(retriever, llm, hound, **kwargs)
