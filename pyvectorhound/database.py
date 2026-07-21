from pydantic import SecretStr
"""Database adapters for different vector databases."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import numpy as np


class VectorDB(ABC):
    """Abstract base class for vector database adapters."""

    @abstractmethod
    def connect(self) -> None:
        """Connect to the database."""
        pass

    @abstractmethod
    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings.

        Returns:
            List of results with 'id', 'text', 'embedding', 'score'
        """
        pass

    @abstractmethod
    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Get embeddings for specific document IDs."""
        pass

    @abstractmethod
    def corpus_size(self) -> int:
        """Get total number of documents in the corpus."""
        pass


class QdrantAdapter(VectorDB):
    """Adapter for Qdrant vector database."""

    def __init__(self, endpoint: str, index_name: str, api_key: Optional[SecretStr] = None):
        """
        Initialize Qdrant adapter.

        Args:
            endpoint: Qdrant endpoint (e.g., 'http://localhost:6333')
            index_name: Collection name
            api_key: Optional API key
        """
        self.endpoint = endpoint
        self.index_name = index_name
        if isinstance(api_key, str):
            self.api_key = SecretStr(api_key)
        else:
            self.api_key = api_key
        self.client = None

    def connect(self) -> None:
        """Connect to Qdrant."""
        try:
            from qdrant_client import QdrantClient

            if self.endpoint.startswith("http://") or self.endpoint.startswith("https://"):
                self.client = QdrantClient(url=self.endpoint, api_key=self.api_key)
            else:
                host, port = self.endpoint.split(":")
                self.client = QdrantClient(
                    host=host, port=int(port), api_key=self.api_key
                )
        except ImportError:
            raise ImportError("qdrant-client not installed. Run: pip install pyhound[qdrant]")

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search in Qdrant."""
        if self.client is None:
            self.connect()

        results = self.client.search(
            collection_name=self.index_name,
            query_vector=query_embedding.tolist(),
            limit=top_k,
        )

        return [
            {
                "id": result.id,
                "score": result.score,
                "embedding": query_embedding,  # Note: Qdrant doesn't return embeddings
            }
            for result in results
        ]

    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Get embeddings for documents."""
        if self.client is None:
            self.connect()

        embeddings = {}
        for doc_id in doc_ids:
            point = self.client.retrieve(
                collection_name=self.index_name, ids=[int(doc_id)]
            )
            if point:
                embeddings[doc_id] = np.array(point[0].vector)

        return embeddings

    def corpus_size(self) -> int:
        """Get corpus size."""
        if self.client is None:
            self.connect()

        collection_info = self.client.get_collection(self.index_name)
        return collection_info.points_count


class ChromaAdapter(VectorDB):
    """Adapter for Chroma vector database."""

    def __init__(self, endpoint: str, index_name: str, **kwargs):
        """
        Initialize Chroma adapter.

        Args:
            endpoint: Chroma endpoint
            index_name: Collection name
        """
        self.endpoint = endpoint
        self.index_name = index_name
        self.client = None
        self.collection = None

    def connect(self) -> None:
        """Connect to Chroma."""
        try:
            import chromadb

            if self.endpoint:
                self.client = chromadb.HttpClient(host=self.endpoint.split(":")[0])
            else:
                self.client = chromadb.Client()

            self.collection = self.client.get_collection(name=self.index_name)
        except ImportError:
            raise ImportError("chromadb not installed. Run: pip install pyhound[chroma]")

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search in Chroma."""
        if self.collection is None:
            self.connect()

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()], n_results=top_k
        )

        output = []
        for i, doc_id in enumerate(results["ids"][0]):
            output.append(
                {
                    "id": doc_id,
                    "score": results["distances"][0][i],
                    "embedding": query_embedding,
                }
            )

        return output

    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Get embeddings for documents."""
        if self.collection is None:
            self.connect()

        embeddings = {}
        results = self.collection.get(ids=doc_ids, include=["embeddings"])

        for doc_id, emb in zip(results["ids"], results["embeddings"]):
            embeddings[doc_id] = np.array(emb)

        return embeddings

    def corpus_size(self) -> int:
        """Get corpus size."""
        if self.collection is None:
            self.connect()

        return self.collection.count()


class MilvusAdapter(VectorDB):
    """Adapter for Milvus vector database."""

    def __init__(self, endpoint: str, index_name: str, **kwargs):
        """
        Initialize Milvus adapter.

        Args:
            endpoint: Milvus endpoint
            index_name: Collection name
        """
        self.endpoint = endpoint
        self.index_name = index_name
        self.client = None
        self.collection = None

    def connect(self) -> None:
        """Connect to Milvus."""
        try:
            from pymilvus import MilvusClient

            self.client = MilvusClient(uri=self.endpoint)
            self.collection = self.index_name
        except ImportError:
            raise ImportError("pymilvus not installed. Run: pip install pyhound[milvus]")

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search in Milvus."""
        if self.client is None:
            self.connect()

        results = self.client.search(
            collection_name=self.collection,
            data=[query_embedding.tolist()],
            limit=top_k,
            output_fields=["id"],
        )

        output = []
        for result in results[0]:
            output.append(
                {
                    "id": result["id"],
                    "score": result["distance"],
                    "embedding": query_embedding,
                }
            )

        return output

    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Get embeddings for documents."""
        if self.client is None:
            self.connect()

        # Milvus requires filtering; simplified approach
        embeddings = {}
        # TODO: Implement proper embedding retrieval from Milvus

        return embeddings

    def corpus_size(self) -> int:
        """Get corpus size."""
        if self.client is None:
            self.connect()

        return self.client.get_collection_stats(self.collection)["row_count"]


class PostgresVectorAdapter(VectorDB):
    """Adapter for PostgreSQL with pgvector extension."""

    def __init__(
        self,
        endpoint: str,
        index_name: str,
        username: str = "postgres",
        password: str = "password",
        database: str = "postgres",
        **kwargs: Any,
    ):
        """
        Initialize PostgreSQL pgvector adapter.

        Args:
            endpoint: PostgreSQL endpoint (host:port)
            index_name: Table name containing embeddings
            username: Database username
            password: Database password
            database: Database name
        """
        self.endpoint = endpoint
        self.index_name = index_name
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> None:
        """Connect to PostgreSQL."""
        try:
            import psycopg2

            host, port = self.endpoint.split(":")
            self.connection = psycopg2.connect(
                host=host,
                port=int(port),
                user=self.username,
                password=self.password,
                database=self.database,
            )
        except ImportError:
            raise ImportError(
                "psycopg2 not installed. Run: pip install pyhound[postgres]"
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search in PostgreSQL using pgvector similarity."""
        if self.connection is None:
            self.connect()

        cursor = self.connection.cursor()

        try:
            # pgvector uses <-> operator for cosine distance
            query_str = f"""
                SELECT id, embedding, 1 - (embedding <-> %s) AS similarity
                FROM {self.index_name}
                ORDER BY embedding <-> %s
                LIMIT %s
            """

            embedding_list = query_embedding.tolist()
            cursor.execute(
                query_str,
                (embedding_list, embedding_list, top_k),
            )

            results = []
            for row in cursor.fetchall():
                doc_id, embedding, similarity = row
                results.append(
                    {
                        "id": str(doc_id),
                        "score": similarity,
                        "embedding": query_embedding,
                    }
                )

            return results

        finally:
            cursor.close()

    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Get embeddings for documents."""
        if self.connection is None:
            self.connect()

        cursor = self.connection.cursor()

        try:
            placeholders = ",".join(["%s"] * len(doc_ids))
            query_str = f"SELECT id, embedding FROM {self.index_name} WHERE id IN ({placeholders})"

            cursor.execute(query_str, doc_ids)

            embeddings = {}
            for row in cursor.fetchall():
                doc_id, embedding = row
                embeddings[str(doc_id)] = np.array(embedding, dtype=np.float32)

            return embeddings

        finally:
            cursor.close()

    def corpus_size(self) -> int:
        """Get corpus size."""
        if self.connection is None:
            self.connect()

        cursor = self.connection.cursor()

        try:
            cursor.execute(f"SELECT COUNT(*) FROM {self.index_name}")
            count = cursor.fetchone()[0]
            return count

        finally:
            cursor.close()

    def __del__(self):
        """Close connection on cleanup."""
        if self.connection:
            self.connection.close()


class WeaviateAdapter(VectorDB):
    """Adapter for Weaviate vector database."""

    def __init__(self, endpoint: str, index_name: str, **kwargs):
        """
        Initialize Weaviate adapter.

        Args:
            endpoint: Weaviate endpoint
            index_name: Class name
        """
        self.endpoint = endpoint
        self.index_name = index_name
        self.client = None

    def connect(self) -> None:
        """Connect to Weaviate."""
        try:
            import weaviate

            self.client = weaviate.Client(self.endpoint)
        except ImportError:
            raise ImportError("weaviate-client not installed. Run: pip install pyhound[weaviate]")

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search in Weaviate."""
        if self.client is None:
            self.connect()

        results = self.client.query.get(self.index_name, ["_additional {distance vector}"]).with_near_vector(
            {"vector": query_embedding.tolist()}
        ).with_limit(top_k).do()

        output = []
        for result in results["data"]["Get"][self.index_name]:
            output.append(
                {
                    "id": result.get("_additional", {}).get("id", "unknown"),
                    "score": 1.0
                    - result.get("_additional", {}).get("distance", 1.0),
                    "embedding": query_embedding,
                }
            )

        return output

    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Get embeddings for documents."""
        if self.client is None:
            self.connect()

        embeddings = {}
        for doc_id in doc_ids:
            result = self.client.data_object.get_by_id(doc_id, class_name=self.index_name)
            if result and "_additional" in result and "vector" in result["_additional"]:
                embeddings[doc_id] = np.array(result["_additional"]["vector"])

        return embeddings

    def corpus_size(self) -> int:
        """Get corpus size."""
        if self.client is None:
            self.connect()

        result = (
            self.client.query.aggregate(self.index_name)
            .with_meta_count()
            .do()
        )

        return result["data"]["Aggregate"][self.index_name][0]["meta"]["count"]


def get_adapter(db: str, endpoint: str, index_name: str, **kwargs: Any) -> VectorDB:
    """Factory function to create appropriate adapter."""
    db = db.lower()

    adapters = {
        "qdrant": QdrantAdapter,
        "chroma": ChromaAdapter,
        "milvus": MilvusAdapter,
        "weaviate": WeaviateAdapter,
        "postgres": PostgresVectorAdapter,
        "postgresql": PostgresVectorAdapter,
        "pgvector": PostgresVectorAdapter,
    }

    if db not in adapters:
        raise ValueError(
            f"Unsupported database: {db}. Supported: {list(set(adapters.values()))}"
        )

    return adapters[db](endpoint=endpoint, index_name=index_name, **kwargs)
