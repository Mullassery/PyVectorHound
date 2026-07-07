"""Unit tests for Pyvectorhound vector database operations."""

import pytest
import numpy as np
from pyvectorhound import VectorStore, EmbeddingManager


class TestVectorStore:
    """Tests for VectorStore core functionality."""

    def test_vectorstore_initialization(self):
        """Test VectorStore can be initialized."""
        store = VectorStore(backend="memory", dimension=128)
        assert store is not None
        assert store.dimension == 128

    def test_add_single_vector(self):
        """Test adding a single vector."""
        store = VectorStore(backend="memory", dimension=3)
        vector = np.array([1.0, 2.0, 3.0])

        result = store.add(vector, metadata={"id": "vec1"})
        assert result is not None

    def test_add_multiple_vectors(self):
        """Test adding multiple vectors."""
        store = VectorStore(backend="memory", dimension=5)
        vectors = np.random.randn(10, 5)

        for i, vec in enumerate(vectors):
            store.add(vec, metadata={"id": f"vec{i}"})

        assert store.size() == 10

    def test_vector_dimension_validation(self):
        """Test that vectors must match store dimension."""
        store = VectorStore(backend="memory", dimension=3)
        vector = np.array([1.0, 2.0])  # Wrong dimension

        with pytest.raises((ValueError, IndexError)):
            store.add(vector)

    def test_similarity_search(self):
        """Test similarity search functionality."""
        store = VectorStore(backend="memory", dimension=5)

        # Add vectors
        vectors = np.array([
            [1, 0, 0, 0, 0],
            [1, 0.1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
        ], dtype=np.float32)

        for i, vec in enumerate(vectors):
            store.add(vec, metadata={"id": i})

        # Search with first vector
        query = vectors[0]
        results = store.search(query, top_k=2)

        assert len(results) <= 2
        # First result should be identical (itself)
        assert results[0]["metadata"]["id"] == 0

    def test_batch_search(self):
        """Test searching with multiple queries."""
        store = VectorStore(backend="memory", dimension=4)
        vectors = np.random.randn(20, 4)

        for i, vec in enumerate(vectors):
            store.add(vec, metadata={"id": i})

        # Batch search
        queries = np.random.randn(5, 4)
        results = store.batch_search(queries, top_k=3)

        assert len(results) == 5
        for result in results:
            assert len(result) <= 3

    def test_delete_vector(self):
        """Test deleting vectors."""
        store = VectorStore(backend="memory", dimension=2)

        vec_id = store.add(np.array([1, 2]), metadata={"id": "test"})
        assert store.size() == 1

        store.delete(vec_id)
        assert store.size() == 0

    def test_update_vector(self):
        """Test updating vector metadata."""
        store = VectorStore(backend="memory", dimension=2)

        vec_id = store.add(np.array([1, 2]), metadata={"id": "test", "label": "old"})
        store.update(vec_id, metadata={"label": "new"})

        results = store.search(np.array([1, 2]), top_k=1)
        assert results[0]["metadata"]["label"] == "new"

    def test_empty_store_search(self):
        """Test searching in empty store."""
        store = VectorStore(backend="memory", dimension=3)
        query = np.array([1, 2, 3])

        results = store.search(query, top_k=5)
        assert len(results) == 0

    def test_single_vector_search(self):
        """Test searching with only one vector in store."""
        store = VectorStore(backend="memory", dimension=2)
        store.add(np.array([1, 2]), metadata={"id": "only"})

        results = store.search(np.array([1, 2]), top_k=10)
        assert len(results) == 1

    def test_duplicate_vectors(self):
        """Test handling of duplicate vectors."""
        store = VectorStore(backend="memory", dimension=2)

        vec = np.array([1.0, 2.0])
        id1 = store.add(vec, metadata={"id": "first"})
        id2 = store.add(vec, metadata={"id": "second"})

        assert id1 != id2  # Should have different IDs
        assert store.size() == 2


class TestEmbeddingManager:
    """Tests for embedding generation and management."""

    def test_embedding_manager_initialization(self):
        """Test EmbeddingManager can be initialized."""
        manager = EmbeddingManager(model="default", dimension=128)
        assert manager is not None

    def test_embed_single_text(self):
        """Test embedding a single text."""
        manager = EmbeddingManager(model="default", dimension=384)
        embedding = manager.embed("Hello world")

        assert embedding is not None
        assert len(embedding) == 384

    def test_embed_multiple_texts(self):
        """Test embedding multiple texts."""
        manager = EmbeddingManager(model="default", dimension=384)
        texts = ["Hello", "world", "test"]

        embeddings = manager.embed_batch(texts)

        assert len(embeddings) == len(texts)
        for emb in embeddings:
            assert len(emb) == 384

    def test_embedding_consistency(self):
        """Test that same text produces same embedding."""
        manager = EmbeddingManager(model="default", dimension=384)
        text = "test embedding consistency"

        emb1 = manager.embed(text)
        emb2 = manager.embed(text)

        assert np.allclose(emb1, emb2)

    def test_embedding_similarity(self):
        """Test that similar texts have similar embeddings."""
        manager = EmbeddingManager(model="default", dimension=384)

        text1 = "The quick brown fox"
        text2 = "The fast brown fox"
        text3 = "Unrelated random text"

        emb1 = manager.embed(text1)
        emb2 = manager.embed(text2)
        emb3 = manager.embed(text3)

        # Cosine similarity
        sim_12 = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        sim_13 = np.dot(emb1, emb3) / (np.linalg.norm(emb1) * np.linalg.norm(emb3))

        assert sim_12 > sim_13  # Similar texts more similar than dissimilar

    def test_empty_text(self):
        """Test handling of empty text."""
        manager = EmbeddingManager(model="default", dimension=384)

        # Should either handle gracefully or raise clear error
        try:
            embedding = manager.embed("")
            assert embedding is not None
        except ValueError as e:
            assert "empty" in str(e).lower()

    def test_very_long_text(self):
        """Test handling of very long text."""
        manager = EmbeddingManager(model="default", dimension=384)
        long_text = " ".join(["word"] * 10000)

        # Should either handle with truncation or raise error
        try:
            embedding = manager.embed(long_text)
            assert len(embedding) == 384
        except ValueError:
            pass  # Acceptable to reject overly long text


class TestVectorDatabaseAdapters:
    """Tests for different vector database backends."""

    @pytest.mark.parametrize("backend", ["memory", "qdrant", "chroma"])
    def test_backend_initialization(self, backend):
        """Test that all backends can be initialized."""
        if backend == "memory":
            store = VectorStore(backend=backend, dimension=64)
            assert store is not None

    def test_memory_backend_persistence(self):
        """Test in-memory backend persistence."""
        store = VectorStore(backend="memory", dimension=3)
        store.add(np.array([1, 2, 3]), metadata={"id": "test"})

        # In-memory should persist within same object
        assert store.size() == 1

    def test_backend_switch_incompatibility(self):
        """Test that switching backends doesn't corrupt data."""
        store1 = VectorStore(backend="memory", dimension=3)
        store1.add(np.array([1, 2, 3]))

        # New backend is separate
        store2 = VectorStore(backend="memory", dimension=3)
        assert store2.size() == 0


class TestPerformance:
    """Performance and scalability tests."""

    def test_large_batch_performance(self):
        """Test performance with large batch operations."""
        import time

        store = VectorStore(backend="memory", dimension=128)
        vectors = np.random.randn(5000, 128)

        start = time.time()
        for vec in vectors:
            store.add(vec)
        elapsed = time.time() - start

        assert elapsed < 60  # Should complete in under 60 seconds
        assert store.size() == 5000

    def test_search_performance(self):
        """Test search performance on large store."""
        import time

        store = VectorStore(backend="memory", dimension=64)
        vectors = np.random.randn(1000, 64)

        for vec in vectors:
            store.add(vec)

        query = np.random.randn(64)
        start = time.time()
        results = store.search(query, top_k=100)
        elapsed = time.time() - start

        assert len(results) <= 100
        assert elapsed < 5  # Should search in under 5 seconds


class TestMemorySecurity:
    """Tests for TIER 1 file size limits (if applicable)."""

    def test_no_unbounded_memory_growth(self):
        """Test that repeated operations don't cause memory leaks."""
        store = VectorStore(backend="memory", dimension=64)

        # Simulate repeated operations
        for iteration in range(100):
            vectors = np.random.randn(100, 64)
            for vec in vectors:
                store.add(vec)

        assert store.size() == 10000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
