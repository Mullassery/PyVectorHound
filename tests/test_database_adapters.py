"""Tests for pyvectorhound.database adapters (the VectorDB implementations used
directly by Hound, as opposed to the separate db_adapters.py mock-based interface).

These adapters had zero test coverage before this file: MilvusAdapter.get_embeddings()
in particular was a stub that unconditionally returned an empty dict, discarding the
doc_ids it was given instead of actually querying Milvus for the stored vectors.
"""

import numpy as np
import pytest

from pyvectorhound.database import (
    ChromaAdapter,
    MilvusAdapter,
    QdrantAdapter,
    get_adapter,
)


class FakeMilvusClient:
    """Stand-in for pymilvus.MilvusClient, keyed by the real MilvusClient.get/search shape."""

    def __init__(self, records):
        # records: dict[str, list[float]] keyed by id
        self._records = records

    def get(self, collection_name, ids, output_fields=None):
        results = []
        for doc_id in ids:
            if doc_id not in self._records:
                continue
            record = {"id": doc_id}
            if output_fields is None or "vector" in output_fields:
                record["vector"] = self._records[doc_id]
            results.append(record)
        return results

    def search(self, collection_name, data, limit, output_fields=None):
        ids = list(self._records.keys())[:limit]
        return [[{"id": doc_id, "distance": 0.9} for doc_id in ids]]

    def get_collection_stats(self, collection_name):
        return {"row_count": len(self._records)}


class TestMilvusAdapter:
    """MilvusAdapter is exercised via an injected fake client so these tests run
    without pymilvus installed and without a live Milvus server."""

    def test_get_adapter_factory_returns_milvus_adapter(self):
        adapter = get_adapter("milvus", endpoint="http://localhost:19530", index_name="docs")
        assert isinstance(adapter, MilvusAdapter)
        assert adapter.endpoint == "http://localhost:19530"
        assert adapter.index_name == "docs"

    def test_get_embeddings_returns_real_vectors_for_requested_ids(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")
        adapter.client = FakeMilvusClient(
            {
                "doc_1": [1.0, 2.0, 3.0],
                "doc_2": [4.0, 5.0, 6.0],
                "doc_3": [7.0, 8.0, 9.0],
            }
        )
        adapter.collection = "docs"

        embeddings = adapter.get_embeddings(["doc_1", "doc_3"])

        assert set(embeddings.keys()) == {"doc_1", "doc_3"}
        np.testing.assert_array_equal(embeddings["doc_1"], np.array([1.0, 2.0, 3.0], dtype=np.float32))
        np.testing.assert_array_equal(embeddings["doc_3"], np.array([7.0, 8.0, 9.0], dtype=np.float32))
        assert embeddings["doc_1"].dtype == np.float32

    def test_get_embeddings_skips_unknown_ids_instead_of_fabricating_data(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")
        adapter.client = FakeMilvusClient({"doc_1": [1.0, 2.0, 3.0]})
        adapter.collection = "docs"

        embeddings = adapter.get_embeddings(["doc_1", "doc_missing"])

        assert set(embeddings.keys()) == {"doc_1"}

    def test_get_embeddings_empty_input_returns_empty_without_querying(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")
        adapter.client = FakeMilvusClient({"doc_1": [1.0, 2.0, 3.0]})
        adapter.collection = "docs"

        assert adapter.get_embeddings([]) == {}

    def test_get_embeddings_uses_configured_vector_field_name(self):
        class RenamedFieldClient(FakeMilvusClient):
            def get(self, collection_name, ids, output_fields=None):
                return [{"id": doc_id, "embedding": self._records[doc_id]} for doc_id in ids if doc_id in self._records]

        adapter = MilvusAdapter(
            endpoint="http://localhost:19530", index_name="docs", vector_field="embedding"
        )
        adapter.client = RenamedFieldClient({"doc_1": [1.0, 2.0]})
        adapter.collection = "docs"

        embeddings = adapter.get_embeddings(["doc_1"])
        np.testing.assert_array_equal(embeddings["doc_1"], np.array([1.0, 2.0], dtype=np.float32))

    def test_search_maps_id_and_score_from_client_results(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")
        adapter.client = FakeMilvusClient({"doc_1": [1.0, 2.0, 3.0], "doc_2": [4.0, 5.0, 6.0]})
        adapter.collection = "docs"

        results = adapter.search(np.array([1.0, 2.0, 3.0]), top_k=2)

        assert len(results) == 2
        assert results[0]["id"] == "doc_1"
        assert results[0]["score"] == 0.9

    def test_corpus_size_reflects_real_collection_stats(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")
        adapter.client = FakeMilvusClient({"doc_1": [1.0], "doc_2": [2.0], "doc_3": [3.0]})
        adapter.collection = "docs"

        assert adapter.corpus_size() == 3

    def test_connect_without_pymilvus_installed_raises_actionable_import_error(self):
        adapter = MilvusAdapter(endpoint="http://localhost:19530", index_name="docs")
        with pytest.raises(ImportError, match="pymilvus"):
            adapter.connect()


class FakeQdrantPoint:
    def __init__(self, id, vector):
        self.id = id
        self.vector = vector


class FakeQdrantResult:
    def __init__(self, id, score):
        self.id = id
        self.score = score


class FakeQdrantClient:
    def __init__(self, records):
        self._records = records

    def search(self, collection_name, query_vector, limit):
        return [FakeQdrantResult(doc_id, 0.5) for doc_id in list(self._records.keys())[:limit]]

    def retrieve(self, collection_name, ids):
        return [FakeQdrantPoint(i, self._records[i]) for i in ids if i in self._records]


class TestQdrantAdapter:
    def test_get_embeddings_returns_real_vectors(self):
        adapter = QdrantAdapter(endpoint="http://localhost:6333", index_name="docs")
        adapter.client = FakeQdrantClient({1: [1.0, 2.0], 2: [3.0, 4.0]})

        embeddings = adapter.get_embeddings(["1", "2"])

        assert set(embeddings.keys()) == {"1", "2"}
        np.testing.assert_array_equal(embeddings["1"], np.array([1.0, 2.0]))


class FakeChromaCollection:
    def __init__(self, records):
        self._records = records

    def query(self, query_embeddings, n_results):
        ids = list(self._records.keys())[:n_results]
        return {"ids": [ids], "distances": [[0.1 for _ in ids]]}

    def get(self, ids, include):
        return {"ids": ids, "embeddings": [self._records[i] for i in ids]}

    def count(self):
        return len(self._records)


class TestChromaAdapter:
    def test_get_embeddings_returns_real_vectors(self):
        adapter = ChromaAdapter(endpoint="", index_name="docs")
        adapter.collection = FakeChromaCollection({"a": [1.0, 1.0], "b": [2.0, 2.0]})

        embeddings = adapter.get_embeddings(["a", "b"])

        assert set(embeddings.keys()) == {"a", "b"}
        np.testing.assert_array_equal(embeddings["b"], np.array([2.0, 2.0]))

    def test_corpus_size_matches_collection_count(self):
        adapter = ChromaAdapter(endpoint="", index_name="docs")
        adapter.collection = FakeChromaCollection({"a": [1.0], "b": [2.0], "c": [3.0]})

        assert adapter.corpus_size() == 3
