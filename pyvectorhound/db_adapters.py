"""Unified database adapter interface for multi-database support.

Provides consistent API across different vector databases and enables
seamless swapping in replay mode.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import numpy as np
from datetime import datetime


class DatabaseType(Enum):
    """Supported vector database types."""

    QDRANT = "qdrant"
    CHROMA = "chroma"
    MILVUS = "milvus"
    WEAVIATE = "weaviate"
    PGVECTOR = "pgvector"
    PINECONE = "pinecone"


@dataclass
class DatabaseConfig:
    """Database connection configuration."""

    db_type: DatabaseType
    endpoint: str
    api_key: Optional[str] = None
    index_name: str = "documents"
    similarity_metric: str = "cosine"  # cosine, euclidean, dot_product
    timeout_seconds: int = 30
    max_retries: int = 3
    batch_size: int = 100
    additional_params: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "db_type": self.db_type.value,
            "endpoint": self.endpoint,
            "index_name": self.index_name,
            "similarity_metric": self.similarity_metric,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "batch_size": self.batch_size,
        }


@dataclass
class SearchResult:
    """Single search result."""

    doc_id: str
    content: str
    score: float
    metadata: Dict[str, Any]
    rank: int = 0


@dataclass
class DatabaseMetrics:
    """Database performance metrics."""

    total_documents: int
    total_size_mb: float
    avg_query_latency_ms: float
    p95_query_latency_ms: float
    p99_query_latency_ms: float
    index_size_mb: float
    memory_usage_mb: float
    timestamp: datetime = None

    def __post_init__(self):
        """Set default timestamp."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_documents": self.total_documents,
            "total_size_mb": self.total_size_mb,
            "avg_query_latency_ms": self.avg_query_latency_ms,
            "p95_query_latency_ms": self.p95_query_latency_ms,
            "p99_query_latency_ms": self.p99_query_latency_ms,
            "index_size_mb": self.index_size_mb,
            "memory_usage_mb": self.memory_usage_mb,
            "timestamp": self.timestamp.isoformat(),
        }


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters.

    All adapters must implement this interface to enable seamless swapping
    in replay mode and ensure consistent behavior.
    """

    def __init__(self, config: DatabaseConfig):
        """Initialize adapter with configuration.

        Args:
            config: DatabaseConfig with connection details
        """
        self.config = config
        self.db_type = config.db_type
        self._connected = False
        self._metrics_cache: Optional[DatabaseMetrics] = None

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to database.

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to database."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if database is healthy and accessible.

        Returns:
            True if database is accessible, False otherwise
        """
        pass

    @abstractmethod
    def index_exists(self, index_name: Optional[str] = None) -> bool:
        """Check if index/collection exists.

        Args:
            index_name: Index name (uses config default if None)

        Returns:
            True if index exists, False otherwise
        """
        pass

    @abstractmethod
    def create_index(
        self,
        index_name: Optional[str] = None,
        dimension: int = 768,
        metric: str = "cosine",
    ) -> bool:
        """Create new index/collection.

        Args:
            index_name: Index name (uses config default if None)
            dimension: Vector dimension
            metric: Similarity metric

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_index(self, index_name: Optional[str] = None) -> bool:
        """Delete index/collection.

        Args:
            index_name: Index name (uses config default if None)

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        index_name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Search for nearest neighbors.

        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            index_name: Index name (uses config default if None)
            filters: Optional metadata filters

        Returns:
            List of SearchResult objects
        """
        pass

    @abstractmethod
    def hybrid_search(
        self,
        query_vector: np.ndarray,
        keyword_query: str,
        top_k: int = 10,
        index_name: Optional[str] = None,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[SearchResult]:
        """Hybrid search combining vector and keyword search.

        Args:
            query_vector: Query embedding vector
            keyword_query: Keyword search query
            top_k: Number of results to return
            index_name: Index name (uses config default if None)
            vector_weight: Weight for vector search (0-1)
            keyword_weight: Weight for keyword search (0-1)

        Returns:
            List of SearchResult objects
        """
        pass

    @abstractmethod
    def upsert(
        self,
        vectors: List[np.ndarray],
        ids: List[str],
        metadata: List[Dict[str, Any]],
        index_name: Optional[str] = None,
    ) -> bool:
        """Insert or update vectors.

        Args:
            vectors: List of embedding vectors
            ids: List of document IDs
            metadata: List of metadata dictionaries
            index_name: Index name (uses config default if None)

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete(
        self, ids: List[str], index_name: Optional[str] = None
    ) -> bool:
        """Delete vectors by ID.

        Args:
            ids: List of document IDs to delete
            index_name: Index name (uses config default if None)

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_document(
        self, doc_id: str, index_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get document by ID.

        Args:
            doc_id: Document ID
            index_name: Index name (uses config default if None)

        Returns:
            Document dictionary or None if not found
        """
        pass

    @abstractmethod
    def get_metrics(self, index_name: Optional[str] = None) -> Optional[DatabaseMetrics]:
        """Get database/index metrics.

        Args:
            index_name: Index name (uses config default if None)

        Returns:
            DatabaseMetrics object or None if unavailable
        """
        pass

    @abstractmethod
    def count_documents(self, index_name: Optional[str] = None) -> int:
        """Count total documents in index.

        Args:
            index_name: Index name (uses config default if None)

        Returns:
            Number of documents
        """
        pass

    @abstractmethod
    def update_index_config(
        self,
        config_updates: Dict[str, Any],
        index_name: Optional[str] = None,
    ) -> bool:
        """Update index configuration parameters.

        Args:
            config_updates: Dictionary of parameter updates
            index_name: Index name (uses config default if None)

        Returns:
            True if successful, False otherwise
        """
        pass

    def _get_index_name(self, index_name: Optional[str] = None) -> str:
        """Get index name, defaulting to config value.

        Args:
            index_name: Optional override index name

        Returns:
            Index name to use
        """
        return index_name or self.config.index_name

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


class AdapterFactory:
    """Factory for creating database adapters."""

    _adapters: Dict[DatabaseType, type] = {}

    @classmethod
    def register(cls, db_type: DatabaseType, adapter_class: type) -> None:
        """Register an adapter class.

        Args:
            db_type: Database type
            adapter_class: Adapter class
        """
        cls._adapters[db_type] = adapter_class

    @classmethod
    def create(cls, config: DatabaseConfig) -> DatabaseAdapter:
        """Create an adapter instance.

        Args:
            config: Database configuration

        Returns:
            Adapter instance

        Raises:
            ValueError: If database type not supported
        """
        adapter_class = cls._adapters.get(config.db_type)
        if adapter_class is None:
            raise ValueError(f"Unsupported database type: {config.db_type.value}")

        return adapter_class(config)

    @classmethod
    def get_supported_databases(cls) -> List[DatabaseType]:
        """Get list of supported database types.

        Returns:
            List of DatabaseType enums
        """
        return list(cls._adapters.keys())


class MockDatabaseAdapter(DatabaseAdapter):
    """Mock database adapter for testing and development."""

    def __init__(self, config: DatabaseConfig):
        """Initialize mock adapter."""
        super().__init__(config)
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._vectors: Dict[str, np.ndarray] = {}
        self._index_created = False

    def connect(self) -> bool:
        """Mock connection."""
        self._connected = True
        return True

    def disconnect(self) -> None:
        """Mock disconnection."""
        self._connected = False

    def health_check(self) -> bool:
        """Mock health check."""
        return self._connected

    def index_exists(self, index_name: Optional[str] = None) -> bool:
        """Check if index exists."""
        return self._index_created

    def create_index(
        self,
        index_name: Optional[str] = None,
        dimension: int = 768,
        metric: str = "cosine",
    ) -> bool:
        """Create mock index."""
        self._index_created = True
        return True

    def delete_index(self, index_name: Optional[str] = None) -> bool:
        """Delete mock index."""
        self._documents.clear()
        self._vectors.clear()
        return True

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        index_name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Mock vector search."""
        results = []

        for doc_id, vector in self._vectors.items():
            # Cosine similarity
            similarity = np.dot(query_vector, vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(vector) + 1e-10
            )

            doc = self._documents.get(doc_id, {})

            # Apply filters if specified
            if filters:
                if not self._matches_filters(doc.get("metadata", {}), filters):
                    continue

            results.append(
                SearchResult(
                    doc_id=doc_id,
                    content=doc.get("content", ""),
                    score=float(similarity),
                    metadata=doc.get("metadata", {}),
                )
            )

        # Sort by score and return top_k
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def hybrid_search(
        self,
        query_vector: np.ndarray,
        keyword_query: str,
        top_k: int = 10,
        index_name: Optional[str] = None,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[SearchResult]:
        """Mock hybrid search."""
        # For now, just use vector search
        return self.search(query_vector, top_k, index_name)

    def upsert(
        self,
        vectors: List[np.ndarray],
        ids: List[str],
        metadata: List[Dict[str, Any]],
        index_name: Optional[str] = None,
    ) -> bool:
        """Mock upsert."""
        for vector, doc_id, meta in zip(vectors, ids, metadata):
            self._vectors[doc_id] = vector
            self._documents[doc_id] = {
                "content": meta.get("content", ""),
                "metadata": meta,
            }
        return True

    def delete(
        self, ids: List[str], index_name: Optional[str] = None
    ) -> bool:
        """Mock delete."""
        for doc_id in ids:
            self._vectors.pop(doc_id, None)
            self._documents.pop(doc_id, None)
        return True

    def get_document(
        self, doc_id: str, index_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Mock get document."""
        return self._documents.get(doc_id)

    def get_metrics(self, index_name: Optional[str] = None) -> Optional[DatabaseMetrics]:
        """Mock get metrics."""
        return DatabaseMetrics(
            total_documents=len(self._documents),
            total_size_mb=len(self._documents) * 0.5,
            avg_query_latency_ms=5.0,
            p95_query_latency_ms=8.0,
            p99_query_latency_ms=12.0,
            index_size_mb=len(self._documents) * 0.3,
            memory_usage_mb=len(self._documents) * 0.2,
        )

    def count_documents(self, index_name: Optional[str] = None) -> int:
        """Mock document count."""
        return len(self._documents)

    def update_index_config(
        self,
        config_updates: Dict[str, Any],
        index_name: Optional[str] = None,
    ) -> bool:
        """Mock update config."""
        return True

    def _matches_filters(
        self, metadata: Dict[str, Any], filters: Dict[str, Any]
    ) -> bool:
        """Check if metadata matches filters.

        Args:
            metadata: Document metadata
            filters: Filter dictionary

        Returns:
            True if metadata matches all filters
        """
        for key, value in filters.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True


# Register mock adapter by default
AdapterFactory.register(DatabaseType.QDRANT, MockDatabaseAdapter)  # Placeholder
