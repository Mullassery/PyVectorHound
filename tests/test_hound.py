"""Tests for Hound class."""

import pytest
from pyvectorhound import Hound


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
        # TODO: Should raise ValueError for unsupported DB
        pass

    def test_diagnose(self):
        """Test basic diagnosis."""
        hound = Hound(db="qdrant")
        # TODO: Mock database and test diagnosis
        pass

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
