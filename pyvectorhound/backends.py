"""Vector database backend implementations for Pyvectorhound.

Supports multiple vector database platforms with a unified interface:
- Qdrant: Open-source vector search engine
- Chroma: Lightweight vector DB with embedding support
- Pinecone: Managed cloud vector database
- Memory: In-process memory backend (for testing)
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import numpy as np

from pyvectorhound.logging_config import get_logger

logger = get_logger(__name__)


class VectorDBBackend(ABC):
    """Abstract base class for vector database backends."""

    def __init__(self, name: str) -> None:
        """Initialize backend.

        Args:
            name: Backend identifier (qdrant, chroma, pinecone, memory)
        """
        self.name = name
        logger.debug(f"Initializing {name} backend")

    @abstractmethod
    def search(
        self,
        query: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for nearest neighbors.

        Args:
            query: Query vector
            top_k: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of {id, score, metadata} dicts
        """

    @abstractmethod
    def add(
        self,
        vectors: np.ndarray,
        ids: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add vectors to database.

        Args:
            vectors: [N, D] array of vectors
            ids: List of N vector IDs
            metadata: Optional list of N metadata dicts
        """

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        """Delete vectors by ID."""

    @abstractmethod
    def get_metadata(self, id: str) -> Optional[Dict[str, Any]]:
        """Get vector metadata by ID."""


class QdrantBackend(VectorDBBackend):
    """Qdrant vector database backend."""

    def __init__(self, url: str = "http://localhost:6333") -> None:
        """Initialize Qdrant backend.

        Args:
            url: Qdrant server URL
        """
        super().__init__("qdrant")
        self.url = url
        self.collection_name = "vectors"
        logger.info(f"Connecting to Qdrant at {url}")

    def search(
        self,
        query: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search Qdrant collection."""
        logger.debug(f"Searching Qdrant for {top_k} neighbors")
        try:
            from qdrant_client import QdrantClient

            client = QdrantClient(url=self.url)
            results = client.search(
                collection_name=self.collection_name,
                query_vector=query.tolist(),
                limit=top_k,
                query_filter=filters,
            )
            logger.debug(f"Found {len(results)} results")
            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "metadata": hit.payload or {},
                }
                for hit in results
            ]
        except ImportError:
            logger.error("qdrant-client not installed. Install: pip install qdrant-client")
            raise
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            raise

    def add(
        self,
        vectors: np.ndarray,
        ids: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add vectors to Qdrant."""
        logger.debug(f"Adding {len(ids)} vectors to Qdrant")
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import PointStruct

            client = QdrantClient(url=self.url)
            points = [
                PointStruct(
                    id=hash(id) % (10**8),
                    vector=vec.tolist(),
                    payload=metadata[i] if metadata else {},
                )
                for i, (id, vec) in enumerate(zip(ids, vectors))
            ]
            client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Added {len(ids)} vectors to Qdrant")
        except ImportError:
            logger.error("qdrant-client not installed")
            raise

    def delete(self, ids: List[str]) -> None:
        """Delete vectors from Qdrant."""
        logger.debug(f"Deleting {len(ids)} vectors from Qdrant")
        try:
            from qdrant_client import QdrantClient

            client = QdrantClient(url=self.url)
            client.delete(
                collection_name=self.collection_name,
                points_selector=[hash(id) % (10**8) for id in ids],
            )
        except ImportError:
            logger.error("qdrant-client not installed")
            raise

    def get_metadata(self, id: str) -> Optional[Dict[str, Any]]:
        """Get metadata from Qdrant."""
        try:
            from qdrant_client import QdrantClient

            client = QdrantClient(url=self.url)
            point = client.retrieve(
                collection_name=self.collection_name,
                ids=[hash(id) % (10**8)],
            )
            return point[0].payload if point else None
        except ImportError:
            logger.error("qdrant-client not installed")
            raise


class ChromaBackend(VectorDBBackend):
    """Chroma vector database backend."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        is_persistent: bool = False,
    ) -> None:
        """Initialize Chroma backend.

        Args:
            host: Chroma server hostname
            port: Chroma server port
            is_persistent: Use persistent storage
        """
        super().__init__("chroma")
        self.host = host
        self.port = port
        self.is_persistent = is_persistent
        logger.info(f"Connecting to Chroma at {host}:{port}")

    def search(
        self,
        query: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search Chroma collection."""
        logger.debug(f"Searching Chroma for {top_k} neighbors")
        try:
            import chromadb

            client = chromadb.HttpClient(host=self.host, port=self.port)
            collection = client.get_or_create_collection("vectors")

            results = collection.query(
                query_embeddings=[query.tolist()],
                n_results=top_k,
                where=filters,
            )

            logger.debug(f"Found {len(results['ids'][0])} results")
            return [
                {
                    "id": id_val,
                    "score": 1 - dist,
                    "metadata": metadata or {},
                }
                for id_val, dist, metadata in zip(
                    results["ids"][0],
                    results["distances"][0],
                    results["metadatas"][0] or [],
                )
            ]
        except ImportError:
            logger.error("chromadb not installed. Install: pip install chromadb")
            raise

    def add(
        self,
        vectors: np.ndarray,
        ids: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add vectors to Chroma."""
        logger.debug(f"Adding {len(ids)} vectors to Chroma")
        try:
            import chromadb

            client = chromadb.HttpClient(host=self.host, port=self.port)
            collection = client.get_or_create_collection("vectors")

            collection.add(
                ids=ids,
                embeddings=vectors.tolist(),
                metadatas=metadata or [],
            )
            logger.info(f"Added {len(ids)} vectors to Chroma")
        except ImportError:
            logger.error("chromadb not installed")
            raise

    def delete(self, ids: List[str]) -> None:
        """Delete vectors from Chroma."""
        logger.debug(f"Deleting {len(ids)} vectors from Chroma")
        try:
            import chromadb

            client = chromadb.HttpClient(host=self.host, port=self.port)
            collection = client.get_or_create_collection("vectors")
            collection.delete(ids=ids)
        except ImportError:
            logger.error("chromadb not installed")
            raise

    def get_metadata(self, id: str) -> Optional[Dict[str, Any]]:
        """Get metadata from Chroma."""
        try:
            import chromadb

            client = chromadb.HttpClient(host=self.host, port=self.port)
            collection = client.get_or_create_collection("vectors")
            result = collection.get(ids=[id])
            return result["metadatas"][0] if result["metadatas"] else None
        except ImportError:
            logger.error("chromadb not installed")
            raise


class PineconeBackend(VectorDBBackend):
    """Pinecone cloud vector database backend."""

    def __init__(self, api_key: str, environment: str, index_name: str = "vectors") -> None:
        """Initialize Pinecone backend.

        Args:
            api_key: Pinecone API key
            environment: Pinecone environment (us-west1, etc)
            index_name: Index name
        """
        super().__init__("pinecone")
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        logger.info(f"Connecting to Pinecone index '{index_name}'")

    def search(
        self,
        query: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search Pinecone index."""
        logger.debug(f"Searching Pinecone for {top_k} neighbors")
        try:
            import pinecone

            pinecone.init(api_key=self.api_key, environment=self.environment)
            index = pinecone.Index(self.index_name)

            results = index.query(
                vector=query.tolist(),
                top_k=top_k,
                filter=filters,
                include_metadata=True,
            )

            logger.debug(f"Found {len(results['matches'])} results")
            return [
                {
                    "id": match["id"],
                    "score": match["score"],
                    "metadata": match.get("metadata", {}),
                }
                for match in results["matches"]
            ]
        except ImportError:
            logger.error("pinecone-client not installed. Install: pip install pinecone-client")
            raise

    def add(
        self,
        vectors: np.ndarray,
        ids: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add vectors to Pinecone."""
        logger.debug(f"Adding {len(ids)} vectors to Pinecone")
        try:
            import pinecone

            pinecone.init(api_key=self.api_key, environment=self.environment)
            index = pinecone.Index(self.index_name)

            vectors_to_upsert = [
                (id_val, vec.tolist(), metadata[i] if metadata else {})
                for i, (id_val, vec) in enumerate(zip(ids, vectors))
            ]

            index.upsert(vectors=vectors_to_upsert)
            logger.info(f"Added {len(ids)} vectors to Pinecone")
        except ImportError:
            logger.error("pinecone-client not installed")
            raise

    def delete(self, ids: List[str]) -> None:
        """Delete vectors from Pinecone."""
        logger.debug(f"Deleting {len(ids)} vectors from Pinecone")
        try:
            import pinecone

            pinecone.init(api_key=self.api_key, environment=self.environment)
            index = pinecone.Index(self.index_name)
            index.delete(ids=ids)
        except ImportError:
            logger.error("pinecone-client not installed")
            raise

    def get_metadata(self, id: str) -> Optional[Dict[str, Any]]:
        """Get metadata from Pinecone."""
        try:
            import pinecone

            pinecone.init(api_key=self.api_key, environment=self.environment)
            index = pinecone.Index(self.index_name)
            result = index.fetch(ids=[id])
            return result["vectors"][0]["metadata"] if result["vectors"] else None
        except ImportError:
            logger.error("pinecone-client not installed")
            raise


def create_backend(
    backend_type: str,
    **kwargs: Any,
) -> VectorDBBackend:
    """Factory function to create vector DB backend.

    Args:
        backend_type: Type of backend (qdrant, chroma, pinecone, memory)
        **kwargs: Backend-specific configuration

    Returns:
        Initialized backend instance

    Example:
        >>> backend = create_backend("qdrant", url="http://localhost:6333")
        >>> backend = create_backend("chroma", host="localhost", port=8000)
        >>> backend = create_backend("pinecone", api_key="pk-...", environment="us-west1")
    """
    logger.info(f"Creating {backend_type} backend")

    backends = {
        "qdrant": QdrantBackend,
        "chroma": ChromaBackend,
        "pinecone": PineconeBackend,
    }

    if backend_type not in backends:
        logger.error(f"Unknown backend: {backend_type}")
        raise ValueError(f"Unknown backend: {backend_type}")

    return backends[backend_type](**kwargs)
