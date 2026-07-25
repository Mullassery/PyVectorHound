"""Tests for trend analysis module."""

import pytest
from datetime import datetime, timedelta
from pyvectorhound.trend_analysis import (
    TrendAnalyzer,
    TimeSeries,
    TrendPoint,
    DriftAnalysis,
    RegressionAnalysis,
    AnomalyDetection,
)


class TestTrendPoint:
    """Test TrendPoint data class."""

    def test_trend_point_creation(self):
        """Test creating trend point."""
        timestamp = datetime.utcnow()
        point = TrendPoint(
            timestamp=timestamp, value=0.92, metric_name="embedding_isotropy"
        )
        assert point.value == 0.92
        assert point.metric_name == "embedding_isotropy"

    def test_trend_point_with_tags(self):
        """Test trend point with tags."""
        timestamp = datetime.utcnow()
        point = TrendPoint(
            timestamp=timestamp,
            value=0.92,
            metric_name="embedding_isotropy",
            tags={"db": "qdrant", "model": "openai"},
        )
        assert point.tags["db"] == "qdrant"

    def test_trend_point_to_dict(self):
        """Test converting trend point to dict."""
        timestamp = datetime.utcnow()
        point = TrendPoint(timestamp=timestamp, value=0.92, metric_name="test")
        d = point.to_dict()
        assert "timestamp" in d
        assert d["value"] == 0.92


class TestTimeSeries:
    """Test TimeSeries class."""

    def test_timeseries_creation(self):
        """Test creating time series."""
        ts = TimeSeries("embedding_isotropy")
        assert ts.metric_name == "embedding_isotropy"
        assert len(ts.points) == 0

    def test_add_point(self):
        """Test adding point to series."""
        ts = TimeSeries("embedding_isotropy")
        ts.add_point(0.92)
        assert len(ts.points) == 1
        assert ts.points[0].value == 0.92

    def test_add_multiple_points(self):
        """Test adding multiple points."""
        ts = TimeSeries("embedding_isotropy")
        for i in range(5):
            ts.add_point(0.90 + i * 0.01)
        assert len(ts.points) == 5

    def test_get_values(self):
        """Test getting values from series."""
        ts = TimeSeries("embedding_isotropy")
        for i in range(5):
            ts.add_point(0.90 + i * 0.01)

        values = ts.get_values()
        assert len(values) == 5
        assert values[0] == 0.90

    def test_get_values_with_time_filter(self):
        """Test getting values within time window."""
        ts = TimeSeries("embedding_isotropy")

        # Add old point
        old_time = datetime.utcnow() - timedelta(days=10)
        ts.add_point(0.85, timestamp=old_time)

        # Add recent points
        for i in range(5):
            ts.add_point(0.90 + i * 0.01)

        # Get last 7 days
        recent_values = ts.get_values(days=7)
        assert len(recent_values) == 5  # Only recent points

    def test_mean(self):
        """Test calculating mean."""
        ts = TimeSeries("embedding_isotropy")
        ts.add_point(0.90)
        ts.add_point(0.92)
        ts.add_point(0.94)

        mean = ts.mean()
        assert abs(mean - 0.92) < 0.001

    def test_stddev(self):
        """Test calculating standard deviation."""
        ts = TimeSeries("embedding_isotropy")
        ts.add_point(0.90)
        ts.add_point(0.92)
        ts.add_point(0.94)

        stddev = ts.stddev()
        assert stddev > 0

    def test_trend_direction_up(self):
        """Test detecting upward trend."""
        ts = TimeSeries("embedding_isotropy")
        # First half: low values
        for i in range(5):
            ts.add_point(0.80 + i * 0.01)
        # Second half: high values
        for i in range(5):
            ts.add_point(0.90 + i * 0.01)

        direction = ts.trend_direction()
        assert direction == "up"

    def test_trend_direction_down(self):
        """Test detecting downward trend."""
        ts = TimeSeries("embedding_isotropy")
        # First half: high values
        for i in range(5):
            ts.add_point(0.95 - i * 0.01)
        # Second half: low values
        for i in range(5):
            ts.add_point(0.85 - i * 0.01)

        direction = ts.trend_direction()
        assert direction == "down"

    def test_trend_direction_stable(self):
        """Test detecting stable trend."""
        ts = TimeSeries("embedding_isotropy")
        for i in range(10):
            ts.add_point(0.90)  # Same value

        direction = ts.trend_direction()
        assert direction == "stable"


class TestDriftAnalysis:
    """Test DriftAnalysis data class."""

    def test_drift_analysis_creation(self):
        """Test creating drift analysis."""
        drift = DriftAnalysis(
            metric_name="embedding_isotropy",
            baseline_mean=0.90,
            baseline_stddev=0.02,
            current_mean=0.85,
            current_stddev=0.03,
            drift_magnitude=2.5,
            drift_direction="down",
            is_anomaly=True,
            confidence=0.95,
            num_samples=100,
        )
        assert drift.metric_name == "embedding_isotropy"
        assert drift.is_anomaly is True


class TestRegressionAnalysis:
    """Test RegressionAnalysis data class."""

    def test_regression_analysis_creation(self):
        """Test creating regression analysis."""
        regression = RegressionAnalysis(
            metric_name="query_latency",
            baseline_value=50.0,
            current_value=57.5,
            change_pct=15.0,
            is_regression=True,
            severity="high",
            window_days=7,
            num_incidents=100,
        )
        assert regression.metric_name == "query_latency"
        assert regression.is_regression is True


class TestAnomalyDetection:
    """Test AnomalyDetection data class."""

    def test_anomaly_detection_creation(self):
        """Test creating anomaly detection."""
        anomaly = AnomalyDetection(
            metric_name="embedding_isotropy",
            timestamp=datetime.utcnow(),
            value=0.50,
            expected_range=(0.85, 0.95),
            anomaly_score=3.5,
            is_anomaly=True,
            anomaly_type="drop",
        )
        assert anomaly.is_anomaly is True
        assert anomaly.anomaly_type == "drop"


class TestTrendAnalyzer:
    """Test TrendAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test initializing trend analyzer."""
        analyzer = TrendAnalyzer()
        assert len(analyzer.series) == 0
        assert len(analyzer._anomalies) == 0

    def test_track_metric(self):
        """Test tracking a metric."""
        analyzer = TrendAnalyzer()
        analyzer.track_metric("embedding_isotropy", 0.92)
        assert "embedding_isotropy" in analyzer.series

    def test_track_multiple_metrics(self):
        """Test tracking multiple metrics."""
        analyzer = TrendAnalyzer()
        analyzer.track_metric("embedding_isotropy", 0.92)
        analyzer.track_metric("query_latency", 45.5)
        assert len(analyzer.series) == 2

    def test_set_baseline(self):
        """Test setting baseline statistics."""
        analyzer = TrendAnalyzer()
        analyzer.set_baseline(
            "embedding_isotropy", {"mean": 0.90, "stddev": 0.02}
        )
        assert "embedding_isotropy" in analyzer._baseline_stats

    def test_detect_drift(self):
        """Test detecting drift."""
        analyzer = TrendAnalyzer()

        # Set baseline
        analyzer.set_baseline("embedding_isotropy", {"mean": 0.90, "stddev": 0.02})

        # Add degraded values
        for _ in range(10):
            analyzer.track_metric("embedding_isotropy", 0.75)

        drift = analyzer.detect_drift("embedding_isotropy")
        assert drift is not None
        assert drift.is_anomaly is True
        assert drift.drift_direction == "down"

    def test_detect_drift_no_baseline(self):
        """Test drift detection without explicit baseline."""
        analyzer = TrendAnalyzer()

        # Add initial values
        for i in range(5):
            analyzer.track_metric("embedding_isotropy", 0.90 + i * 0.01)

        # Add degraded values
        for _ in range(5):
            analyzer.track_metric("embedding_isotropy", 0.75)

        drift = analyzer.detect_drift("embedding_isotropy")
        assert drift is not None

    def test_detect_drift_no_metric(self):
        """Test drift detection for non-existent metric."""
        analyzer = TrendAnalyzer()
        drift = analyzer.detect_drift("nonexistent")
        assert drift is None

    def test_detect_regression(self):
        """Test detecting performance regression."""
        analyzer = TrendAnalyzer()

        # Add baseline values
        for _ in range(5):
            analyzer.track_metric("query_latency", 50.0)

        # Add degraded values
        for _ in range(5):
            analyzer.track_metric("query_latency", 60.0)

        regression = analyzer.detect_regression("query_latency")
        assert regression is not None
        assert regression.is_regression is True

    def test_detect_anomalies(self):
        """Test detecting anomalies."""
        analyzer = TrendAnalyzer()

        # Add normal values
        for i in range(10):
            analyzer.track_metric("embedding_isotropy", 0.90 + i * 0.01)

        # Add anomalous value
        analyzer.track_metric("embedding_isotropy", 0.30)

        anomalies = analyzer.detect_anomalies("embedding_isotropy")
        assert len(anomalies) > 0
        assert anomalies[0].is_anomaly is True

    def test_anomaly_classification_spike(self):
        """Test classifying spike anomaly."""
        analyzer = TrendAnalyzer()

        for i in range(10):
            analyzer.track_metric("query_latency", 50.0)

        # Spike
        analyzer.track_metric("query_latency", 200.0)

        anomalies = analyzer.detect_anomalies("query_latency")
        assert len(anomalies) > 0
        assert anomalies[-1].anomaly_type == "spike"

    def test_anomaly_classification_drop(self):
        """Test classifying drop anomaly."""
        analyzer = TrendAnalyzer()

        for i in range(10):
            analyzer.track_metric("embedding_isotropy", 0.90)

        # Drop
        analyzer.track_metric("embedding_isotropy", 0.20)

        anomalies = analyzer.detect_anomalies("embedding_isotropy")
        assert len(anomalies) > 0
        assert anomalies[-1].anomaly_type == "drop"

    def test_get_historical_comparison(self):
        """Test getting historical comparison."""
        analyzer = TrendAnalyzer()

        # Add values
        for i in range(10):
            analyzer.track_metric("embedding_isotropy", 0.90 + i * 0.005)

        comparison = analyzer.get_historical_comparison("embedding_isotropy")
        assert comparison is not None
        assert "historical_mean" in comparison
        assert "trend" in comparison

    def test_get_trend_report(self):
        """Test getting trend report."""
        analyzer = TrendAnalyzer()

        analyzer.track_metric("embedding_isotropy", 0.92)
        analyzer.track_metric("query_latency", 45.5)

        report = analyzer.get_trend_report()
        assert "timestamp" in report
        assert "metrics_analyzed" in report
        assert len(report["metrics"]) > 0

    def test_get_trend_report_specific_metrics(self):
        """Test getting report for specific metrics."""
        analyzer = TrendAnalyzer()

        analyzer.track_metric("embedding_isotropy", 0.92)
        analyzer.track_metric("query_latency", 45.5)
        analyzer.track_metric("recall", 0.85)

        report = analyzer.get_trend_report(["embedding_isotropy", "query_latency"])
        assert len(report["metrics"]) == 2
        assert "recall" not in report["metrics"]

    def test_get_metric_series(self):
        """Test getting metric series."""
        analyzer = TrendAnalyzer()

        analyzer.track_metric("embedding_isotropy", 0.92)

        series = analyzer.get_metric_series("embedding_isotropy")
        assert series is not None
        assert series.metric_name == "embedding_isotropy"

    def test_get_metric_series_nonexistent(self):
        """Test getting non-existent metric series."""
        analyzer = TrendAnalyzer()

        series = analyzer.get_metric_series("nonexistent")
        assert series is None

    def test_integration_tracking_and_analysis(self):
        """Test end-to-end tracking and analysis."""
        analyzer = TrendAnalyzer()

        # Establish baseline (stable period)
        for i in range(10):
            analyzer.track_metric("embedding_isotropy", 0.90 + i * 0.001)

        # Simulate degradation
        for i in range(5):
            analyzer.track_metric("embedding_isotropy", 0.85 - i * 0.02)

        # Get full report
        report = analyzer.get_trend_report()

        assert report["metrics_analyzed"] >= 1
        assert len(report["metrics"]) > 0

        # Check that drift was detected
        drift = analyzer.detect_drift("embedding_isotropy")
        assert drift is not None

        # Check that regression was detected
        regression = analyzer.detect_regression("embedding_isotropy")
        assert regression is not None
