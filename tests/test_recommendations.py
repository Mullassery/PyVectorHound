"""Tests for recommendations module."""

import pytest
from pyvectorhound.recommendations import (
    RecommendationEngine,
    FixRecommendation,
    DiagnosticReport,
    FailureCategory,
)


class TestFixRecommendation:
    """Test FixRecommendation."""

    def test_create_recommendation(self):
        """Test creating recommendation."""
        rec = FixRecommendation(
            id="rec_1",
            failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
            title="Reduce chunk size",
            description="Split into smaller chunks",
            root_cause="Chunks too large",
            confidence=0.88,
            effort_hours=2.0,
            expected_improvement_pct=27.0,
            implementation_steps=["Step 1", "Step 2"],
            risks=["Risk 1"],
        )
        assert rec.id == "rec_1"
        assert rec.confidence == 0.88

    def test_recommendation_roi(self):
        """Test ROI calculation."""
        rec = FixRecommendation(
            id="rec_1",
            failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
            title="Reduce chunk size",
            description="Split into smaller chunks",
            root_cause="Chunks too large",
            confidence=0.88,
            effort_hours=2.0,
            expected_improvement_pct=27.0,
            implementation_steps=["Step 1"],
            risks=[],
        )
        roi = rec.roi
        assert roi == 27.0 / 2.0  # improvement / hours

    def test_recommendation_to_dict(self):
        """Test converting recommendation to dict."""
        rec = FixRecommendation(
            id="rec_1",
            failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
            title="Reduce chunk size",
            description="Split into smaller chunks",
            root_cause="Chunks too large",
            confidence=0.88,
            effort_hours=2.0,
            expected_improvement_pct=27.0,
            implementation_steps=["Step 1"],
            risks=[],
        )
        d = rec.to_dict()
        assert d["id"] == "rec_1"
        assert d["title"] == "Reduce chunk size"


class TestDiagnosticReport:
    """Test DiagnosticReport."""

    def test_create_report(self):
        """Test creating report."""
        report = DiagnosticReport(
            query_id="query_1",
            query_text="test query",
            primary_failures=["chunking_problems"],
            confidence=0.88,
            failure_details={},
            recommendations=[],
            executive_summary="Summary",
            next_steps=["Step 1"],
        )
        assert report.query_id == "query_1"
        assert len(report.recommendations) == 0

    def test_report_to_dict(self):
        """Test converting report to dict."""
        report = DiagnosticReport(
            query_id="query_1",
            query_text="test query",
            primary_failures=[],
            confidence=0.88,
            failure_details={},
            recommendations=[],
            executive_summary="Summary",
            next_steps=[],
        )
        d = report.to_dict()
        assert d["query_id"] == "query_1"
        assert d["confidence"] == 0.88


class TestRecommendationEngine:
    """Test RecommendationEngine."""

    def test_engine_initialization(self):
        """Test initializing engine."""
        engine = RecommendationEngine()
        assert engine.llm_client is None
        assert len(engine._generated_reports) == 0

    def test_analyze_failure_chunking(self):
        """Test analyzing chunking failure."""
        engine = RecommendationEngine()

        diagnosis = {
            "chunking_issues": True,
            "embedding_quality_score": 0.9,
        }

        report = engine.analyze_failure(
            "query_1", "test query", diagnosis
        )

        assert report.query_id == "query_1"
        assert "chunking_problems" in report.primary_failures
        assert len(report.recommendations) > 0

    def test_analyze_failure_embedding(self):
        """Test analyzing embedding failure."""
        engine = RecommendationEngine()

        diagnosis = {
            "embedding_quality_score": 0.7,
            "chunking_issues": False,
        }

        report = engine.analyze_failure(
            "query_1", "test query", diagnosis
        )

        assert report.query_id == "query_1"
        assert "embedding_quality" in report.primary_failures

    def test_analyze_failure_metadata_filtering(self):
        """Test analyzing metadata filtering failure."""
        engine = RecommendationEngine()

        diagnosis = {
            "filter_reduction_pct": 75,
            "embedding_quality_score": 0.9,
        }

        report = engine.analyze_failure(
            "query_1", "test query", diagnosis
        )

        assert "metadata_filtering" in report.primary_failures

    def test_get_recommendation_summary(self):
        """Test getting recommendation summary."""
        engine = RecommendationEngine()

        diagnosis = {"chunking_issues": True}

        engine.analyze_failure("query_1", "test query", diagnosis)

        summary = engine.get_recommendation_summary("query_1")
        assert summary is not None
        assert summary["query_id"] == "query_1"
        assert "executive_summary" in summary

    def test_estimate_roi(self):
        """Test ROI estimation."""
        engine = RecommendationEngine()

        rec = FixRecommendation(
            id="rec_1",
            failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
            title="Reduce chunk size",
            description="Split into smaller chunks",
            root_cause="Chunks too large",
            confidence=0.88,
            effort_hours=2.0,
            expected_improvement_pct=35.0,
            implementation_steps=["Step 1"],
            risks=[],
        )

        roi = engine.estimate_roi(rec)
        assert roi["recommendation"] == "Reduce chunk size"
        assert roi["engineering_cost_usd"] == 300.0  # 2 hours * $150
        assert roi["estimated_value_usd"] == 35000.0  # 35% * $1000
        assert roi["roi_percent"] > 0

    def test_identify_primary_failures(self):
        """Test identifying failures."""
        engine = RecommendationEngine()

        diagnosis = {
            "embedding_quality_score": 0.7,
            "chunking_issues": True,
        }

        failures = engine._identify_primary_failures(diagnosis, None)
        assert len(failures) > 0
        assert "embedding_quality" in failures or "chunking_problems" in failures

    def test_calculate_confidence(self):
        """Test confidence calculation."""
        engine = RecommendationEngine()

        diagnosis = {
            "embedding_quality_score": 0.9,
            "chunking_issues": True,
            "filter_reduction_pct": 50,
        }

        confidence = engine._calculate_confidence(diagnosis)
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be higher with multiple signals

    def test_generate_chunking_fixes(self):
        """Test generating chunking fixes."""
        engine = RecommendationEngine()

        diagnosis = {"chunking_issues": True}

        fixes = engine._generate_chunking_fixes(diagnosis)
        assert len(fixes) > 0
        assert any("chunk" in f.title.lower() for f in fixes)

    def test_generate_embedding_fixes(self):
        """Test generating embedding fixes."""
        engine = RecommendationEngine()

        diagnosis = {"embedding_quality_score": 0.7}

        fixes = engine._generate_embedding_fixes(diagnosis)
        assert len(fixes) > 0
        assert any("embedding" in f.title.lower() for f in fixes)

    def test_generate_summary(self):
        """Test generating summary."""
        engine = RecommendationEngine()

        failures = ["chunking_problems"]
        recs = [
            FixRecommendation(
                id="rec_1",
                failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
                title="Reduce chunk size",
                description="Test description",
                root_cause="Test root cause",
                confidence=0.88,
                effort_hours=2.0,
                expected_improvement_pct=27.0,
                implementation_steps=["Step 1"],
                risks=[],
            )
        ]

        summary = engine._generate_summary(failures, recs)
        assert len(summary) > 0
        assert "Reduce chunk size" in summary

    def test_generate_next_steps(self):
        """Test generating next steps."""
        engine = RecommendationEngine()

        recs = [
            FixRecommendation(
                id="rec_1",
                failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
                title="Reduce chunk size",
                description="Test",
                root_cause="Test",
                confidence=0.88,
                effort_hours=2.0,
                expected_improvement_pct=27.0,
                implementation_steps=["Step 1"],
                risks=[],
            ),
            FixRecommendation(
                id="rec_2",
                failure_category=FailureCategory.EMBEDDING_QUALITY.value,
                title="Switch embedding model",
                description="Test",
                root_cause="Test",
                confidence=0.85,
                effort_hours=4.0,
                expected_improvement_pct=35.0,
                implementation_steps=["Step 1"],
                risks=[],
            ),
        ]

        steps = engine._generate_next_steps(recs)
        assert len(steps) >= 4
        assert any("Reduce chunk size" in step for step in steps)

    def test_full_analysis_workflow(self):
        """Test full analysis workflow."""
        engine = RecommendationEngine()

        diagnosis = {
            "embedding_quality_score": 0.75,
            "chunking_issues": True,
            "filter_reduction_pct": 40,
        }

        trace_analysis = {
            "num_vector_results": 3,
            "total_time_ms": 150,
        }

        report = engine.analyze_failure(
            "query_1", "test query", diagnosis, trace_analysis
        )

        assert report.query_id == "query_1"
        assert len(report.primary_failures) > 0
        assert len(report.recommendations) > 0
        assert len(report.next_steps) > 0
        assert "Executive" in report.executive_summary or len(report.executive_summary) > 0

        # Get summary
        summary = engine.get_recommendation_summary("query_1")
        assert summary is not None
        assert summary["num_recommendations"] > 0

        # Estimate ROI on top recommendation
        if report.recommendations:
            roi = engine.estimate_roi(report.recommendations[0])
            assert "roi_percent" in roi
