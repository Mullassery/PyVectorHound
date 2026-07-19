"""Tests for OKF diagnostic knowledge base."""

import tempfile
from pathlib import Path

import pytest

from pyvectorhound.okf_diagnostics import (
    OKFDiagnosticDocument,
    OKFDiagnosticKnowledgeBase,
)


@pytest.fixture
def temp_kb():
    """Create temporary KB directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield OKFDiagnosticKnowledgeBase(Path(tmpdir))


@pytest.fixture
def populated_kb(temp_kb):
    """Create KB with sample diagnostic findings."""
    kb = temp_kb

    # Record chunking failure
    kb.record_diagnosis(
        query_id="query_001",
        root_cause="Chunking Problems",
        confidence=0.91,
        failure_types=["Chunking Problems", "Context Assembly Problems"],
        recommendations=[
            {
                "strategy": "Split to 400-token chunks",
                "effort_hours": 2,
                "expected_improvement": 0.27,
                "roi": "10-50x"
            }
        ],
        context={"corpus_size": "1GB", "actual_improvement": 0.28}
    )

    # Record embedding quality failure
    kb.record_diagnosis(
        query_id="query_002",
        root_cause="Embedding Quality Issues",
        confidence=0.78,
        failure_types=["Embedding Quality Issues"],
        recommendations=[
            {
                "strategy": "Switch to domain-specific embedding",
                "effort_hours": 4,
                "expected_improvement": 0.35,
                "roi": "20-40x"
            }
        ],
        context={"domain": "legal", "actual_improvement": 0.30}
    )

    # Record another chunking failure
    kb.record_diagnosis(
        query_id="query_003",
        root_cause="Chunking Problems",
        confidence=0.87,
        failure_types=["Chunking Problems"],
        recommendations=[
            {
                "strategy": "Split to 400-token chunks",
                "effort_hours": 2,
                "expected_improvement": 0.25,
                "roi": "10-50x"
            }
        ],
        context={"corpus_size": "2GB", "actual_improvement": 0.26}
    )

    return kb


class TestOKFDiagnosticDocumentLoading:
    """Test loading diagnostic documents."""

    def test_load_diagnostic_document(self, populated_kb):
        """Test loading a diagnostic finding."""
        findings = list(populated_kb.findings.values())
        assert len(findings) >= 1

        doc = findings[0]
        assert doc.query_id is not None
        assert doc.root_cause is not None

    def test_document_metadata(self, populated_kb):
        """Test accessing diagnostic metadata."""
        doc = populated_kb.findings.get("query_001")
        assert doc is not None

        assert doc.query_id == "query_001"
        assert doc.root_cause == "Chunking Problems"
        assert doc.confidence == 0.91
        assert "Chunking Problems" in doc.failure_types

    def test_document_recommendations(self, populated_kb):
        """Test accessing recommendations."""
        doc = populated_kb.findings.get("query_001")
        assert len(doc.recommendations) > 0

        rec = doc.recommendations[0]
        assert rec["strategy"] == "Split to 400-token chunks"
        assert rec["effort_hours"] == 2


class TestOKFDiagnosticKBOperations:
    """Test KB search and retrieval."""

    def test_record_diagnosis(self, temp_kb):
        """Test recording a diagnostic finding."""
        path = temp_kb.record_diagnosis(
            query_id="test_001",
            root_cause="Test Failure",
            confidence=0.85,
            failure_types=["Test"],
            recommendations=[{"strategy": "Test", "effort_hours": 1}]
        )

        assert path.exists()
        assert "findings" in str(path)

    def test_find_similar_failures(self, populated_kb):
        """Test finding similar failures."""
        similar = populated_kb.find_similar_failures("Chunking Problems")

        assert len(similar) >= 2  # Should find both chunking failures
        for finding in similar:
            assert finding.root_cause == "Chunking Problems"

    def test_find_similar_with_limit(self, populated_kb):
        """Test limiting similar failure results."""
        similar = populated_kb.find_similar_failures("Chunking Problems", max_results=1)
        assert len(similar) <= 1

    def test_find_nonexistent_pattern(self, populated_kb):
        """Test searching for non-existent pattern."""
        similar = populated_kb.find_similar_failures("Nonexistent Failure")
        assert len(similar) == 0

    def test_kb_directory_structure(self, temp_kb):
        """Test that KB creates proper structure."""
        expected_dirs = ["findings", "playbooks", "patterns", "component_profiles"]

        for subdir in expected_dirs:
            assert (temp_kb.kb_dir / subdir).exists()


class TestOKFPatternExtraction:
    """Test pattern learning from KB."""

    def test_extract_patterns(self, populated_kb):
        """Test extracting recurring patterns."""
        patterns = populated_kb.extract_patterns(min_frequency=1)

        assert len(patterns) > 0
        # Chunking should be the most frequent
        pattern_names = [p["pattern"] for p in patterns]
        assert "Chunking Problems" in pattern_names

    def test_pattern_frequency(self, populated_kb):
        """Test pattern frequency calculation."""
        patterns = populated_kb.extract_patterns(min_frequency=1)

        for pattern in patterns:
            assert "frequency" in pattern
            assert "count" in pattern
            assert "%" in pattern["frequency"]

    def test_pattern_success_rate(self, populated_kb):
        """Test success rate tracking in patterns."""
        patterns = populated_kb.extract_patterns(min_frequency=1)

        for pattern in patterns:
            assert "avg_success_rate" in pattern
            # Should have a percentage
            assert "%" in pattern["avg_success_rate"]

    def test_min_frequency_filtering(self, populated_kb):
        """Test that patterns are filtered by frequency."""
        # Should include patterns with 2+ occurrences
        common_patterns = populated_kb.extract_patterns(min_frequency=2)

        # Should NOT include patterns with less than 2 occurrences
        rare_patterns = populated_kb.extract_patterns(min_frequency=100)

        if common_patterns:
            # Common patterns should have fewer/equal count than all patterns
            assert len(common_patterns) <= len(populated_kb.extract_patterns(min_frequency=1))


class TestOKFStrategySuccess:
    """Test tracking strategy success rates."""

    def test_get_success_rate(self, populated_kb):
        """Test retrieving success rate for a strategy."""
        rate = populated_kb.get_success_rate_for_strategy("Split to 400-token chunks")

        assert rate is not None
        assert 0 <= rate <= 1

    def test_success_rate_averaging(self, populated_kb):
        """Test success rate is averaged across uses."""
        rate = populated_kb.get_success_rate_for_strategy("Split to 400-token chunks")

        # Should be average of 0.28 and 0.26
        expected = (0.28 + 0.26) / 2
        assert abs(rate - expected) < 0.01

    def test_nonexistent_strategy_rate(self, populated_kb):
        """Test retrieving rate for non-existent strategy."""
        rate = populated_kb.get_success_rate_for_strategy("Nonexistent Strategy")
        assert rate is None


class TestOKFRecommendationEnhancement:
    """Test recommendation ranking with historical data."""

    def test_enhance_recommendations(self, populated_kb):
        """Test enhancing recommendations with success data."""
        initial_recs = [
            {
                "strategy": "Split to 400-token chunks",
                "effort_hours": 2,
                "expected_improvement": 0.25
            }
        ]

        enhanced = populated_kb.generate_enhanced_recommendations(
            "Chunking Problems",
            initial_recs
        )

        assert len(enhanced) > 0
        rec = enhanced[0]
        assert "historical_success_rate" in rec
        assert rec["historical_success_rate"] is not None

    def test_recommendations_sorted_by_success(self, populated_kb):
        """Test recommendations are sorted by success rate."""
        initial_recs = [
            {
                "strategy": "Split to 400-token chunks",
                "effort_hours": 2,
                "expected_improvement": 0.25
            },
            {
                "strategy": "Nonexistent Strategy",
                "effort_hours": 1,
                "expected_improvement": 0.50
            }
        ]

        enhanced = populated_kb.generate_enhanced_recommendations(
            "Chunking Problems",
            initial_recs
        )

        # Should be sorted with known strategies first
        if enhanced[0]["historical_success_rate"] is not None:
            # First recommendation should have success data
            assert enhanced[0]["strategy"] == "Split to 400-token chunks"


class TestOKFReload:
    """Test KB reloading."""

    def test_reload_syncs_index(self, temp_kb):
        """Test that reload picks up new findings."""
        initial_count = len(temp_kb.findings)

        temp_kb.record_diagnosis(
            query_id="reload_test",
            root_cause="Test",
            confidence=0.8,
            failure_types=["Test"],
            recommendations=[]
        )

        temp_kb.reload()
        new_count = len(temp_kb.findings)

        assert new_count > initial_count
