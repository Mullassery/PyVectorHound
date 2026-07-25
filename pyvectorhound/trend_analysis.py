"""Time-series trend analysis and anomaly detection for retrieval systems.

Tracks embedding quality drift, performance regressions, and historical patterns
over time to enable proactive diagnostics and optimization.
"""

import statistics
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np


@dataclass
class TrendPoint:
    """Single data point in a trend."""

    timestamp: datetime
    value: float
    metric_name: str
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "metric_name": self.metric_name,
            "tags": self.tags,
        }


@dataclass
class DriftAnalysis:
    """Embedding quality drift analysis."""

    metric_name: str
    baseline_mean: float
    baseline_stddev: float
    current_mean: float
    current_stddev: float
    drift_magnitude: float
    drift_direction: str  # "up", "down", "stable"
    is_anomaly: bool
    confidence: float
    num_samples: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class RegressionAnalysis:
    """Performance regression analysis."""

    metric_name: str
    baseline_value: float
    current_value: float
    change_pct: float
    is_regression: bool
    severity: str  # "low", "medium", "high", "critical"
    window_days: int
    num_incidents: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class AnomalyDetection:
    """Anomaly detection result."""

    metric_name: str
    timestamp: datetime
    value: float
    expected_range: Tuple[float, float]
    anomaly_score: float
    is_anomaly: bool
    anomaly_type: str  # "spike", "drop", "drift"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "expected_range": self.expected_range,
            "anomaly_score": self.anomaly_score,
            "is_anomaly": self.is_anomaly,
            "anomaly_type": self.anomaly_type,
        }


class TimeSeries:
    """Time-series data container."""

    def __init__(self, metric_name: str):
        """Initialize time-series.

        Args:
            metric_name: Name of the metric
        """
        self.metric_name = metric_name
        self.points: List[TrendPoint] = []

    def add_point(
        self, value: float, timestamp: Optional[datetime] = None, **tags
    ) -> None:
        """Add data point to series.

        Args:
            value: Metric value
            timestamp: Timestamp (defaults to now)
            **tags: Optional tags for filtering
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        point = TrendPoint(
            timestamp=timestamp, value=value, metric_name=self.metric_name, tags=tags
        )
        self.points.append(point)

    def get_values(self, days: Optional[int] = None) -> List[float]:
        """Get values from recent period.

        Args:
            days: Number of days to look back (None = all)

        Returns:
            List of values
        """
        if days is None:
            return [p.value for p in self.points]

        cutoff = datetime.utcnow() - timedelta(days=days)
        return [p.value for p in self.points if p.timestamp >= cutoff]

    def get_points(self, days: Optional[int] = None) -> List[TrendPoint]:
        """Get points from recent period.

        Args:
            days: Number of days to look back (None = all)

        Returns:
            List of TrendPoint objects
        """
        if days is None:
            return self.points

        cutoff = datetime.utcnow() - timedelta(days=days)
        return [p for p in self.points if p.timestamp >= cutoff]

    def mean(self, days: Optional[int] = None) -> float:
        """Calculate mean value.

        Args:
            days: Number of days to look back (None = all)

        Returns:
            Mean value
        """
        values = self.get_values(days)
        if not values:
            return 0.0
        return statistics.mean(values)

    def stddev(self, days: Optional[int] = None) -> float:
        """Calculate standard deviation.

        Args:
            days: Number of days to look back (None = all)

        Returns:
            Standard deviation
        """
        values = self.get_values(days)
        if len(values) < 2:
            return 0.0
        return statistics.stdev(values)

    def trend_direction(self, days: int = 7) -> str:
        """Detect trend direction over recent period.

        Args:
            days: Number of days to analyze

        Returns:
            "up", "down", or "stable"
        """
        values = self.get_values(days)
        if len(values) < 2:
            return "stable"

        first_half = values[: len(values) // 2]
        second_half = values[len(values) // 2 :]

        first_mean = statistics.mean(first_half)
        second_mean = statistics.mean(second_half)

        if abs(second_mean - first_mean) < first_mean * 0.02:  # 2% threshold
            return "stable"

        return "up" if second_mean > first_mean else "down"


class TrendAnalyzer:
    """Analyze retrieval system trends over time.

    Tracks embedding quality drift, performance regressions, and identifies
    anomalies and patterns in retrieval metrics.
    """

    def __init__(self):
        """Initialize trend analyzer."""
        self.series: Dict[str, TimeSeries] = {}
        self._baseline_stats: Dict[str, Dict[str, float]] = {}
        self._anomalies: List[AnomalyDetection] = []

    def track_metric(
        self,
        metric_name: str,
        value: float,
        timestamp: Optional[datetime] = None,
        **tags,
    ) -> None:
        """Track a metric value over time.

        Args:
            metric_name: Name of metric (e.g., "embedding_isotropy")
            value: Metric value
            timestamp: Timestamp (defaults to now)
            **tags: Optional tags (e.g., db="qdrant", model="openai")
        """
        if metric_name not in self.series:
            self.series[metric_name] = TimeSeries(metric_name)

        self.series[metric_name].add_point(value, timestamp, **tags)

    def set_baseline(self, metric_name: str, baseline_stats: Dict[str, float]) -> None:
        """Set baseline statistics for a metric.

        Args:
            metric_name: Name of metric
            baseline_stats: Dict with "mean", "stddev" keys
        """
        self._baseline_stats[metric_name] = baseline_stats

    def detect_drift(
        self,
        metric_name: str,
        window_days: int = 7,
        threshold_stddevs: float = 2.0,
    ) -> Optional[DriftAnalysis]:
        """Detect drift in embedding quality metric.

        Args:
            metric_name: Name of metric to analyze
            window_days: Number of days to analyze
            threshold_stddevs: Number of standard deviations for anomaly threshold

        Returns:
            DriftAnalysis if drift detected, None otherwise
        """
        if metric_name not in self.series:
            return None

        ts = self.series[metric_name]
        baseline = self._baseline_stats.get(metric_name, {})

        if not baseline:
            # No baseline, use first half as baseline
            all_values = ts.get_values()
            if len(all_values) < 10:
                return None

            split = len(all_values) // 2
            baseline_values = all_values[:split]
            current_values = all_values[split:]

            baseline_mean = statistics.mean(baseline_values)
            baseline_stddev = statistics.stdev(baseline_values)
        else:
            baseline_mean = baseline["mean"]
            baseline_stddev = baseline["stddev"]

        current_values = ts.get_values(window_days)
        if not current_values:
            return None

        current_mean = statistics.mean(current_values)
        current_stddev = statistics.stdev(current_values) if len(current_values) > 1 else 0

        # Z-score based drift detection
        drift_magnitude = abs(current_mean - baseline_mean) / max(baseline_stddev, 0.01)
        is_anomaly = drift_magnitude > threshold_stddevs

        drift_direction = (
            "up" if current_mean > baseline_mean else "down" if current_mean < baseline_mean else "stable"
        )

        confidence = min(1.0, drift_magnitude / (threshold_stddevs * 2))

        return DriftAnalysis(
            metric_name=metric_name,
            baseline_mean=baseline_mean,
            baseline_stddev=baseline_stddev,
            current_mean=current_mean,
            current_stddev=current_stddev,
            drift_magnitude=drift_magnitude,
            drift_direction=drift_direction,
            is_anomaly=is_anomaly,
            confidence=confidence,
            num_samples=len(current_values),
        )

    def detect_regression(
        self,
        metric_name: str,
        window_days: int = 7,
        regression_threshold_pct: float = 5.0,
    ) -> Optional[RegressionAnalysis]:
        """Detect performance regression in a metric.

        Args:
            metric_name: Name of metric to analyze
            window_days: Number of days to analyze
            regression_threshold_pct: Percentage change threshold for regression

        Returns:
            RegressionAnalysis if regression detected, None otherwise
        """
        if metric_name not in self.series:
            return None

        ts = self.series[metric_name]
        all_values = ts.get_values()

        if len(all_values) < 2:
            return None

        # Use first half as baseline, second half as current
        split = len(all_values) // 2
        baseline_values = all_values[:split]
        current_values = all_values[split:]

        if not baseline_values or not current_values:
            return None

        baseline_value = statistics.mean(baseline_values)
        current_value = statistics.mean(current_values)

        # For latency metrics, higher = worse; for recall metrics, lower = worse
        change_pct = abs(current_value - baseline_value) / max(abs(baseline_value), 0.01) * 100

        is_regression = change_pct > regression_threshold_pct

        # Determine severity
        if change_pct > 20:
            severity = "critical"
        elif change_pct > 15:
            severity = "high"
        elif change_pct > 10:
            severity = "medium"
        else:
            severity = "low"

        return RegressionAnalysis(
            metric_name=metric_name,
            baseline_value=baseline_value,
            current_value=current_value,
            change_pct=change_pct,
            is_regression=is_regression,
            severity=severity,
            window_days=window_days,
            num_incidents=len(current_values),
        )

    def detect_anomalies(
        self, metric_name: str, window_days: int = 7
    ) -> List[AnomalyDetection]:
        """Detect anomalies using statistical methods.

        Args:
            metric_name: Name of metric to analyze
            window_days: Number of days to analyze

        Returns:
            List of detected anomalies
        """
        if metric_name not in self.series:
            return []

        ts = self.series[metric_name]
        values = ts.get_values(window_days)

        if len(values) < 3:
            return []

        mean = statistics.mean(values)
        stddev = statistics.stdev(values)

        anomalies = []
        points = ts.get_points(window_days)

        for point in points:
            # Z-score
            z_score = abs((point.value - mean) / max(stddev, 0.01))

            if z_score > 2.5:  # 2.5 standard deviations
                anomaly_type = self._classify_anomaly(point.value, mean, stddev)

                anomaly = AnomalyDetection(
                    metric_name=metric_name,
                    timestamp=point.timestamp,
                    value=point.value,
                    expected_range=(mean - 2 * stddev, mean + 2 * stddev),
                    anomaly_score=z_score,
                    is_anomaly=True,
                    anomaly_type=anomaly_type,
                )
                anomalies.append(anomaly)
                self._anomalies.append(anomaly)

        return anomalies

    def get_historical_comparison(
        self, metric_name: str, days_back: int = 30
    ) -> Optional[Dict[str, Any]]:
        """Compare current metrics with historical data.

        Args:
            metric_name: Name of metric
            days_back: Number of days to compare

        Returns:
            Dictionary with historical analysis
        """
        if metric_name not in self.series:
            return None

        ts = self.series[metric_name]
        all_values = ts.get_values()
        recent_values = ts.get_values(days_back)

        if len(all_values) < 2:
            return None

        return {
            "metric_name": metric_name,
            "historical_mean": statistics.mean(all_values),
            "historical_stddev": statistics.stdev(all_values),
            "recent_mean": statistics.mean(recent_values) if recent_values else 0,
            "recent_stddev": statistics.stdev(recent_values) if len(recent_values) > 1 else 0,
            "trend": ts.trend_direction(days_back),
            "min_all_time": min(all_values),
            "max_all_time": max(all_values),
            "current_value": all_values[-1] if all_values else None,
        }

    def get_trend_report(self, metric_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate comprehensive trend report.

        Args:
            metric_names: List of metrics to include (None = all)

        Returns:
            Dictionary with trend analysis for all metrics
        """
        metrics_to_report = metric_names or list(self.series.keys())

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics_analyzed": len(metrics_to_report),
            "total_anomalies": len(self._anomalies),
            "metrics": {},
        }

        for metric_name in metrics_to_report:
            if metric_name not in self.series:
                continue

            ts = self.series[metric_name]
            historical = self.get_historical_comparison(metric_name)
            drift = self.detect_drift(metric_name)
            regression = self.detect_regression(metric_name)
            anomalies = self.detect_anomalies(metric_name)

            report["metrics"][metric_name] = {
                "historical": historical,
                "drift": drift.to_dict() if drift else None,
                "regression": regression.to_dict() if regression else None,
                "recent_anomalies": len(anomalies),
            }

        return report

    def _classify_anomaly(self, value: float, mean: float, stddev: float) -> str:
        """Classify type of anomaly.

        Args:
            value: Observed value
            mean: Mean value
            stddev: Standard deviation

        Returns:
            Anomaly type: "spike", "drop", or "drift"
        """
        if value > mean + 2 * stddev:
            return "spike"
        elif value < mean - 2 * stddev:
            return "drop"
        return "drift"

    def get_metric_series(self, metric_name: str) -> Optional[TimeSeries]:
        """Get time-series for a metric.

        Args:
            metric_name: Name of metric

        Returns:
            TimeSeries object or None
        """
        return self.series.get(metric_name)
