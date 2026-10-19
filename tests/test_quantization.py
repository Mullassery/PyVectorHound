"""Tests for the opt-in int8-quantized vector store wired into Hound."""

import numpy as np
import pytest

pytest.importorskip("pyvectorhound._core")

from pyvectorhound import Hound


def _unit_vector(seed: int, dim: int = 384) -> np.ndarray:
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=dim).astype(np.float32)
    return vector / np.linalg.norm(vector)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class TestQuantizationOptIn:
    def test_default_hound_has_no_quantized_store(self):
        hound = Hound(db="qdrant")

        assert hound.quantized is False
        assert hound._quantized_store is None

        with pytest.raises(ValueError, match="not enabled"):
            hound.add_vectors([_unit_vector(1)])

    def test_constructor_flag_enables_store(self):
        hound = Hound(db="qdrant", quantized=True)

        assert hound.quantized is True
        assert hound._quantized_store is not None

    def test_enable_quantization_is_idempotent(self):
        hound = Hound(db="qdrant")

        first = hound.enable_quantization()
        second = hound.enable_quantization()

        assert first is second
        assert hound.quantized is True


class TestQuantizationRoundTrip:
    def test_round_trip_error_and_similarity_tolerance(self):
        vector = _unit_vector(42)
        hound = Hound(db="qdrant", quantized=True)

        ids = hound.add_vectors([vector], ids=["doc_1"])

        assert ids == ["doc_1"]
        stored = hound._quantized_store._values["doc_1"]
        assert stored.dtype == np.int8
        assert hound._quantized_store._scales["doc_1"] > 0

        restored = hound.get_stored_embeddings(["doc_1"])["doc_1"]

        assert restored.dtype == np.float32
        max_error = float(np.max(np.abs(vector - restored)))
        theoretical_bound = (float(np.max(vector)) - float(np.min(vector))) / 255.0
        assert max_error <= theoretical_bound + 1e-5
        assert _cosine(vector, restored) >= 0.9999

    def test_stored_payload_is_4x_smaller_than_float32(self):
        hound = Hound(db="qdrant", quantized=True)
        hound.add_vectors([_unit_vector(i) for i in range(3)])

        store = hound._quantized_store
        assert store.float32_bytes == store.quantized_bytes * 4

    def test_constant_and_zero_vectors_round_trip_exactly(self):
        constant = np.full(16, 3.5, dtype=np.float32)
        zeros = np.zeros(16, dtype=np.float32)
        hound = Hound(db="qdrant", quantized=True)

        hound.add_vectors([constant, zeros], ids=["constant", "zeros"])
        restored = hound.get_stored_embeddings(["constant", "zeros"])

        np.testing.assert_array_equal(restored["constant"], constant)
        np.testing.assert_array_equal(restored["zeros"], zeros)


class TestQuantizedRetrieval:
    def test_search_dequantizes_and_ranks_by_cosine(self):
        vectors = [
            np.array([1.0, 0.0, 0.0], dtype=np.float32),
            np.array([0.0, 1.0, 0.0], dtype=np.float32),
            np.array([-1.0, 0.0, 0.0], dtype=np.float32),
        ]
        hound = Hound(db="qdrant", quantized=True)
        hound.add_vectors(vectors, ids=["a", "b", "c"])

        results = hound.search_vectors(vectors[0], top_k=3)

        assert [result["id"] for result in results] == ["a", "b", "c"]
        assert results[0]["score"] >= 0.9999
        assert _cosine(vectors[0], results[0]["embedding"]) >= 0.9999
        assert all(result["embedding"].dtype == np.float32 for result in results)

    def test_diagnose_uses_populated_quantized_store_instead_of_adapter(self):
        class AdapterThatMustNotBeUsed:
            def search(self, query_embedding, top_k=5):
                raise AssertionError("external adapter should not be queried")

            def get_embeddings(self, doc_ids):
                raise AssertionError("external adapter should not be queried")

            def corpus_size(self):
                raise AssertionError("external adapter should not be queried")

        vectors = [
            np.array([1.0, 0.0, 0.0], dtype=np.float32),
            np.array([0.0, 1.0, 0.0], dtype=np.float32),
            np.array([-1.0, 0.0, 0.0], dtype=np.float32),
        ]
        hound = Hound(db="qdrant", quantized=True)
        hound.adapter = AdapterThatMustNotBeUsed()
        hound.add_vectors(vectors, ids=["a", "b", "c"])

        diagnosis = hound.diagnose(query="q", query_embedding=vectors[0], top_k=2)

        assert [result["id"] for result in diagnosis.results] == ["a", "b"]

    def test_empty_quantized_store_falls_back_to_adapter(self):
        class RecordingAdapter:
            def __init__(self):
                self.called = False

            def search(self, query_embedding, top_k=5):
                self.called = True
                return [{"id": "external", "score": 1.0, "embedding": query_embedding}]

            def get_embeddings(self, doc_ids):
                return {}

            def corpus_size(self):
                return 1

        adapter = RecordingAdapter()
        hound = Hound(db="qdrant", quantized=True)
        hound.adapter = adapter

        diagnosis = hound.diagnose(query="q", query_embedding=_unit_vector(1), top_k=1)

        assert adapter.called is True
        assert diagnosis.results[0]["id"] == "external"


class TestQuantizationErrorPaths:
    def test_mismatched_ids_and_vectors(self):
        hound = Hound(db="qdrant", quantized=True)

        with pytest.raises(ValueError, match="same length"):
            hound.add_vectors([_unit_vector(1)], ids=["a", "b"])

    def test_dimension_mismatch_with_existing_store(self):
        hound = Hound(db="qdrant", quantized=True)
        hound.add_vectors([np.ones(4, dtype=np.float32)], ids=["a"])

        with pytest.raises(ValueError, match="does not match"):
            hound.add_vectors([np.ones(5, dtype=np.float32)], ids=["b"])

    def test_non_finite_vector_rejected(self):
        hound = Hound(db="qdrant", quantized=True)
        bad = np.ones(4, dtype=np.float32)
        bad[0] = np.nan

        with pytest.raises(ValueError, match="NaN or infinite"):
            hound.add_vectors([bad], ids=["bad"])

    def test_search_query_dimension_mismatch(self):
        hound = Hound(db="qdrant", quantized=True)
        hound.add_vectors([np.ones(4, dtype=np.float32)], ids=["a"])

        with pytest.raises(ValueError, match="Query dimension"):
            hound.search_vectors(np.ones(5, dtype=np.float32))

    def test_search_zero_magnitude_query_rejected(self):
        hound = Hound(db="qdrant", quantized=True)
        hound.add_vectors([np.ones(4, dtype=np.float32)], ids=["a"])

        with pytest.raises(ValueError, match="non-zero magnitude"):
            hound.search_vectors(np.zeros(4, dtype=np.float32))

    def test_clear_removes_vectors_and_resets_dimension(self):
        hound = Hound(db="qdrant", quantized=True)
        hound.add_vectors([np.ones(4, dtype=np.float32)], ids=["a"])

        hound.clear_stored_vectors()

        assert hound.get_stored_embeddings() == {}
        assert hound._quantized_store.dimension is None
        hound.add_vectors([np.ones(7, dtype=np.float32)], ids=["b"])
