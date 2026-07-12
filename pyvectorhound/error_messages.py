"""User-friendly error messages for RAG diagnostics."""


class DiagnosticError:
    """Diagnostic error with troubleshooting steps."""
    
    def __init__(self, title: str, message: str, troubleshoot: list = None):
        self.title = title
        self.message = message
        self.troubleshoot = troubleshoot or []
    
    def format(self) -> str:
        """Format for display."""
        lines = [f"\n❌ {self.title}\n", f"   {self.message}\n"]
        if self.troubleshoot:
            lines.append("   🔍 Troubleshooting steps:")
            for i, step in enumerate(self.troubleshoot, 1):
                lines.append(f"      {i}. {step}")
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.format()


# Connection errors
VECTOR_DB_UNREACHABLE = DiagnosticError(
    title="Vector Database Unreachable",
    message="Cannot connect to vector database. Check connection and database status.",
    troubleshoot=[
        "Verify database URL/endpoint is correct",
        "Check that database server is running",
        "Test connection: telnet localhost 6333 (for Qdrant)",
        "Check firewall rules if using remote database",
        "Verify credentials are correct for authenticated databases",
    ]
)

EMBEDDING_MODEL_UNAVAILABLE = DiagnosticError(
    title="Embedding Model Unavailable",
    message="Cannot load embedding model. Check model name and dependencies.",
    troubleshoot=[
        "Verify model name: 'text-embedding-3-small', 'text-embedding-3-large'",
        "For local embeddings, ensure sentence-transformers is installed",
        "Check HuggingFace model cache: ~/.cache/huggingface/",
        "Try downloading model: model = SentenceTransformer('model-name')",
    ]
)

# Query errors
MALFORMED_QUERY = DiagnosticError(
    title="Malformed Query",
    message="Query format is invalid. Cannot process for diagnosis.",
    troubleshoot=[
        "Query must be non-empty text (1-5000 characters)",
        "Remove control characters and null bytes",
        "Ensure query is valid UTF-8 encoding",
        "Example valid query: 'What does this document say about pricing?'",
    ]
)

EMBEDDING_QUALITY_LOW = DiagnosticError(
    title="Embedding Quality is Poor",
    message="Embeddings appear to be low quality or misaligned with query.",
    troubleshoot=[
        "Check if embedding model is appropriate for your domain",
        "Try different model: 'text-embedding-3-large' vs 'small'",
        "Verify documents are properly formatted (not HTML, corrupted text)",
        "Check if using different embedding models for query vs documents",
    ]
)

# Retrieval errors
NO_RELEVANT_RESULTS = DiagnosticError(
    title="No Relevant Results Found",
    message="Vector search returned no results with sufficient relevance.",
    troubleshoot=[
        "Try lowering similarity threshold: threshold = 0.5 (instead of 0.8)",
        "Expand search limit: limit = 50 (instead of 10)",
        "Verify document collection is not empty",
        "Check if query is too different from documents",
        "Try rephrasing query in different words",
    ]

RERANKER_FAILURE = DiagnosticError(
    title="Reranker Failed",
    message="Could not rank retrieved results. Check reranker configuration.",
    troubleshoot=[
        "Verify reranker model is available and loaded",
        "Check that candidates are non-empty strings",
        "Try with fewer candidates if out of memory",
        "Ensure query and candidates are compatible encoding",
    ]
)

# Analysis errors
INSUFFICIENT_SAMPLES = DiagnosticError(
    title="Insufficient Data for Analysis",
    message="Not enough results to perform reliable diagnosis.",
    troubleshoot=[
        "Try broadening search parameters (lower threshold, higher limit)",
        "Add more documents to the vector database",
        "Check if database query is filtering out results",
        "Ensure at least 5-10 results for meaningful analysis",
    ]
)


def get_connection_error(endpoint: str, reason: str) -> DiagnosticError:
    """Error for specific connection failures."""
    return DiagnosticError(
        title=f"Cannot Connect to {endpoint}",
        message=f"Connection failed: {reason}",
        troubleshoot=[
            f"Test connectivity: curl http://{endpoint}/health",
            "Check endpoint is correct and accessible",
            "Verify credentials if authentication is required",
            "Check firewall and network settings",
        ]
    )


def get_similarity_error(actual: float, threshold: float) -> DiagnosticError:
    """Error for low similarity scores."""
    return DiagnosticError(
        title=f"Low Similarity Scores (avg: {actual:.3f})",
        message=f"Results are below threshold ({threshold:.3f}). Likely not relevant.",
        troubleshoot=[
            "Consider lowering threshold to {:.3f}".format(threshold * 0.8),
            "Review documents - may not contain relevant information",
            "Try rephrasing your query",
            "Check if using appropriate embedding model for domain",
        ]
    )
