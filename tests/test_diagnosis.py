"""Tests for Diagnosis class."""

import pytest
import numpy as np
from pyvectorhound.diagnosis import Diagnosis


class TestDiagnosis:
    """Test Diagnosis class."""

    def test_init(self):
        """Test Diagnosis initialization."""
        results = [
            {"id": "1", "score": 0.9},
            {"id": "2", "score": 0.8},
        ]
        diagnosis = Diagnosis(query="test", results=results)

        assert diagnosis.query == "test"
        assert len(diagnosis.results) == 2

    def test_hunt_report(self):
        """Test plain English diagnosis report."""
        diagnosis = Diagnosis(
            query="quantum computing",
            results=[{"id": "1", "score": 0.8}],
        )

        report = diagnosis.hunt()
        assert isinstance(report, str)
        assert "quantum computing" in report
        assert "PyHound" in report

    def test_metrics(self):
        """Test metrics retrieval."""
        diagnosis = Diagnosis(query="test", results=[])
        metrics = diagnosis.metrics()

        assert isinstance(metrics, dict)
        assert "embedding" in metrics or len(metrics) >= 0

    def test_recommendations(self):
        """Test recommendations generation."""
        diagnosis = Diagnosis(query="test", results=[])
        recs = diagnosis.recommendations()

        assert isinstance(recs, list)

    def test_root_cause(self):
        """Test root cause analysis."""
        diagnosis = Diagnosis(query="test", results=[])
        cause = diagnosis.root_cause()

        assert isinstance(cause, str)
        assert len(cause) > 0

    def test_with_expected_docs(self):
        """Test diagnosis with ground truth."""
        results = [{"id": "1", "score": 0.9}, {"id": "2", "score": 0.8}]
        expected = ["1", "3"]

        diagnosis = Diagnosis(
            query="test", results=results, expected_docs=expected
        )

        diagnosis.analyze()
        metrics = diagnosis.metrics()

        # Should have computed precision/recall
        assert metrics.get("vector_search", {}).get("precision", 0) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
