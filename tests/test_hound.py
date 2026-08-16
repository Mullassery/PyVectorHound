"""Tests for Hound class."""

import numpy as np
import pytest
from pyvectorhound import Hound
from pyvectorhound.diagnosis import Diagnosis


class TestHound:
    """Test Hound initialization and basic functionality."""

    def test_init_qdrant(self):
        """Test Hound initialization with Qdrant."""
        hound = Hound(db="qdrant", endpoint="localhost:6333")
        assert hound.db == "qdrant"
        assert hound.endpoint == "localhost:6333"
        assert hound.index_name == "documents"

    def test_init_chroma(self):
        """Test Hound initialization with Chroma."""
        hound = Hound(db="chroma", endpoint="localhost:8000")
        assert hound.db == "chroma"
        assert hound.endpoint == "localhost:8000"

    def test_unsupported_db(self):
        """Test that unsupported database raises error."""
        with pytest.raises(ValueError, match="Unsupported database"):
            Hound(db="not_a_real_db")

    def test_diagnose(self):
        """Test that diagnose() searches via the adapter and returns a real Diagnosis."""
        hound = Hound(db="qdrant")

        class FakeAdapter:
            def __init__(self):
                self.search_calls = []

            def search(self, query_embedding, top_k=5):
                self.search_calls.append((query_embedding, top_k))
                return [{"id": "doc_1", "score": 0.9, "embedding": query_embedding}]

            def get_embeddings(self, doc_ids):
                return {}

        fake_adapter = FakeAdapter()
        hound.adapter = fake_adapter

        query_embedding = np.random.randn(8).astype(np.float32)
        diagnosis = hound.diagnose(
            query="quantum computing", query_embedding=query_embedding, top_k=3
        )

        assert isinstance(diagnosis, Diagnosis)
        assert diagnosis.query == "quantum computing"
        assert diagnosis.results == [
            {"id": "doc_1", "score": 0.9, "embedding": fake_adapter.search_calls[0][0]}
        ]
        assert len(fake_adapter.search_calls) == 1
        assert fake_adapter.search_calls[0][1] == 3

    def test_diagnose_without_embedding_or_embed_fn_raises(self):
        """diagnose() must not silently fabricate a query embedding (e.g. a random
        vector) when none is supplied -- a diagnosis run against a meaningless
        vector would itself be meaningless. It should raise instead."""
        hound = Hound(db="qdrant")

        class RecordingAdapter:
            def __init__(self):
                self.called = False

            def search(self, query_embedding, top_k=5):
                self.called = True
                return []

        recording_adapter = RecordingAdapter()
        hound.adapter = recording_adapter

        with pytest.raises(ValueError, match="query_embedding"):
            hound.diagnose(query="no embedding provided")

        assert recording_adapter.called is False

    def test_diagnose_uses_embed_fn_when_no_embedding_given(self):
        """If Hound was configured with embed_fn, diagnose() should use it to embed
        the query rather than requiring a precomputed query_embedding."""

        def fake_embed(text: str) -> np.ndarray:
            return np.full(8, len(text), dtype=np.float32)

        hound = Hound(db="qdrant", embed_fn=fake_embed)

        class RecordingAdapter:
            def __init__(self):
                self.received_embedding = None

            def search(self, query_embedding, top_k=5):
                self.received_embedding = query_embedding
                return []

        recording_adapter = RecordingAdapter()
        hound.adapter = recording_adapter

        hound.diagnose(query="no embedding provided")

        assert recording_adapter.received_embedding is not None
        assert isinstance(recording_adapter.received_embedding, np.ndarray)
        np.testing.assert_array_equal(
            recording_adapter.received_embedding, fake_embed("no embedding provided")
        )

    def test_quality_scorer(self):
        """Test quality scorer initialization."""
        hound = Hound(db="qdrant")
        scorer = hound.quality_scorer()
        assert scorer is not None


class TestDiagnosis:
    """Test Diagnosis class."""

    def test_diagnosis_hunt(self):
        """Test getting plain English diagnosis."""
        from pyvectorhound.diagnosis import Diagnosis

        diagnosis = Diagnosis(query="test query", results=[])
        report = diagnosis.hunt()
        assert isinstance(report, str)
        assert "test query" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
