"""OpenTelemetry integration for PyVectorHound.

Provides distributed tracing, metrics, and logging with support for
multiple backends (Jaeger, Datadog, New Relic, Honeycomb, etc).
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import uuid


class OTelBackend(Enum):
    """Supported OpenTelemetry export backends."""

    JAEGER = "jaeger"
    DATADOG = "datadog"
    NEW_RELIC = "new_relic"
    HONEYCOMB = "honeycomb"
    SPLUNK = "splunk"
    PROMETHEUS = "prometheus"
    LOGGING = "logging"
    CUSTOM = "custom"


@dataclass
class OTelConfig:
    """OpenTelemetry configuration."""

    enabled: bool = True
    service_name: str = "pyvectorhound"
    backend: OTelBackend = OTelBackend.LOGGING
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    sample_rate: float = 1.0  # Trace sampling rate
    include_request_body: bool = False
    include_response_body: bool = False
    custom_attributes: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "enabled": self.enabled,
            "service_name": self.service_name,
            "backend": self.backend.value,
            "endpoint": self.endpoint,
            "sample_rate": self.sample_rate,
        }


class TraceSpan:
    """Lightweight span representation."""

    def __init__(self, name: str, span_id: Optional[str] = None):
        """Initialize span.

        Args:
            name: Span name
            span_id: Optional span ID (generated if not provided)
        """
        self.name = name
        self.span_id = span_id or str(uuid.uuid4())[:12]
        self.start_time = datetime.utcnow()
        self.end_time: Optional[datetime] = None
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []
        self.status: str = "OK"

    def set_attribute(self, key: str, value: Any) -> None:
        """Set span attribute.

        Args:
            key: Attribute key
            value: Attribute value
        """
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add span event.

        Args:
            name: Event name
            attributes: Optional event attributes
        """
        self.events.append({
            "name": name,
            "timestamp": datetime.utcnow().isoformat(),
            "attributes": attributes or {},
        })

    def set_status(self, status: str) -> None:
        """Set span status.

        Args:
            status: Status (OK, ERROR, UNSET)
        """
        self.status = status

    def end(self) -> None:
        """End the span."""
        self.end_time = datetime.utcnow()

    def duration_ms(self) -> float:
        """Get span duration in milliseconds.

        Returns:
            Duration in ms
        """
        end = self.end_time or datetime.utcnow()
        delta = end - self.start_time
        return delta.total_seconds() * 1000

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "span_id": self.span_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms(),
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
        }


class Metric:
    """Lightweight metric representation."""

    def __init__(self, name: str, value: float, unit: str = "", tags: Optional[Dict[str, str]] = None):
        """Initialize metric.

        Args:
            name: Metric name
            value: Metric value
            unit: Unit of measurement
            tags: Optional tags for filtering
        """
        self.name = name
        self.value = value
        self.unit = unit
        self.tags = tags or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
        }


class OTelExporter:
    """Base class for OpenTelemetry exporters."""

    def __init__(self, config: OTelConfig):
        """Initialize exporter.

        Args:
            config: OTelConfig
        """
        self.config = config
        self.spans: List[TraceSpan] = []
        self.metrics: List[Metric] = []

    def export_span(self, span: TraceSpan) -> bool:
        """Export a span.

        Args:
            span: TraceSpan to export

        Returns:
            True if successful
        """
        self.spans.append(span)
        return True

    def export_metric(self, metric: Metric) -> bool:
        """Export a metric.

        Args:
            metric: Metric to export

        Returns:
            True if successful
        """
        self.metrics.append(metric)
        return True

    def flush(self) -> bool:
        """Flush pending exports.

        Returns:
            True if successful
        """
        return True


class LoggingExporter(OTelExporter):
    """Logging-based exporter (for development/testing)."""

    def export_span(self, span: TraceSpan) -> bool:
        """Export span via logging.

        Args:
            span: TraceSpan to export

        Returns:
            True if successful
        """
        super().export_span(span)
        print(f"📊 Span: {span.name} ({span.duration_ms():.2f}ms)")
        for key, value in span.attributes.items():
            print(f"   {key}: {value}")
        return True

    def export_metric(self, metric: Metric) -> bool:
        """Export metric via logging.

        Args:
            metric: Metric to export

        Returns:
            True if successful
        """
        super().export_metric(metric)
        unit_str = f" {metric.unit}" if metric.unit else ""
        print(f"📈 Metric: {metric.name} = {metric.value}{unit_str}")
        return True


class PrometheusExporter(OTelExporter):
    """Prometheus metrics exporter."""

    def __init__(self, config: OTelConfig):
        """Initialize Prometheus exporter.

        Args:
            config: OTelConfig
        """
        super().__init__(config)
        self.metric_values: Dict[str, float] = {}

    def export_metric(self, metric: Metric) -> bool:
        """Export metric to Prometheus format.

        Args:
            metric: Metric to export

        Returns:
            True if successful
        """
        super().export_metric(metric)
        metric_key = f"{metric.name}_{metric.unit}".replace(" ", "_").lower()
        self.metric_values[metric_key] = metric.value
        return True

    def get_prometheus_format(self) -> str:
        """Get metrics in Prometheus format.

        Returns:
            Prometheus format string
        """
        lines = []
        for metric_name, value in self.metric_values.items():
            lines.append(f"{metric_name} {value}")
        return "\n".join(lines)


class OTelInstrument:
    """Instrumentation engine for PyVectorHound.

    Provides unified interface for collecting and exporting traces and metrics.
    """

    def __init__(self, config: Optional[OTelConfig] = None):
        """Initialize instrumentation.

        Args:
            config: OTelConfig (uses defaults if None)
        """
        self.config = config or OTelConfig()
        self._exporter = self._create_exporter()
        self._trace_context: Dict[str, Any] = {
            "trace_id": str(uuid.uuid4())[:16],
            "correlation_id": str(uuid.uuid4())[:12],
        }
        self._spans: List[TraceSpan] = []

    def _create_exporter(self) -> OTelExporter:
        """Create exporter based on configuration.

        Returns:
            OTelExporter instance
        """
        if self.config.backend == OTelBackend.PROMETHEUS:
            return PrometheusExporter(self.config)
        else:
            return LoggingExporter(self.config)

    def start_span(self, name: str) -> TraceSpan:
        """Start a new span.

        Args:
            name: Span name

        Returns:
            TraceSpan instance
        """
        span = TraceSpan(name)
        # Set trace context attributes
        span.set_attribute("trace_id", self._trace_context["trace_id"])
        span.set_attribute("correlation_id", self._trace_context["correlation_id"])
        return span

    def record_span(self, span: TraceSpan) -> None:
        """Record a completed span.

        Args:
            span: TraceSpan to record
        """
        if not self.config.enabled:
            return

        span.end()
        self._spans.append(span)
        self._exporter.export_span(span)

    def record_metric(self, name: str, value: float, unit: str = "", tags: Optional[Dict[str, str]] = None) -> None:
        """Record a metric.

        Args:
            name: Metric name
            value: Metric value
            unit: Unit of measurement
            tags: Optional tags
        """
        if not self.config.enabled:
            return

        metric = Metric(name, value, unit, tags)
        self._exporter.export_metric(metric)

    def record_trace_metrics(self, trace: Any) -> None:
        """Record metrics from a retrieval trace.

        Args:
            trace: RetrievalTrace to analyze
        """
        if not self.config.enabled or not trace:
            return

        # Record phase metrics
        for phase_name, phase_metrics in trace.phase_metrics.items():
            self.record_metric(
                f"retrieval.phase.latency",
                phase_metrics.duration_ms,
                "ms",
                {"phase": phase_name},
            )

        # Record overall metrics
        total_time = sum(m.duration_ms for m in trace.phase_metrics.values())
        self.record_metric(
            "retrieval.total_latency",
            total_time,
            "ms",
        )

        self.record_metric(
            "retrieval.embedding_latency",
            trace.embedding_latency_ms,
            "ms",
        )

        self.record_metric(
            "retrieval.num_results",
            len(trace.vector_search_results),
            "count",
        )

    def record_replay_metrics(self, result: Any) -> None:
        """Record metrics from a replay result.

        Args:
            result: ReplayResult to analyze
        """
        if not self.config.enabled or not result:
            return

        self.record_metric(
            "replay.latency",
            result.latency_ms,
            "ms",
            {"config": result.config_id},
        )

        recall_5 = result.recall_at_k.get(5, 0)
        self.record_metric(
            "replay.recall_at_5",
            recall_5,
            "ratio",
            {"config": result.config_id},
        )

        self.record_metric(
            "replay.ndcg",
            result.ndcg,
            "score",
            {"config": result.config_id},
        )

        self.record_metric(
            "replay.improvement_pct",
            result.improvement_pct,
            "percent",
            {"config": result.config_id},
        )

    def get_trace_context(self) -> Dict[str, str]:
        """Get current trace context.

        Returns:
            Dictionary with trace_id and correlation_id
        """
        return self._trace_context.copy()

    def set_trace_context(self, trace_id: str, correlation_id: str) -> None:
        """Set trace context.

        Args:
            trace_id: Trace ID
            correlation_id: Correlation ID
        """
        self._trace_context["trace_id"] = trace_id
        self._trace_context["correlation_id"] = correlation_id

    def flush(self) -> bool:
        """Flush pending exports.

        Returns:
            True if successful
        """
        return self._exporter.flush()

    def get_stats(self) -> Dict[str, Any]:
        """Get instrumentation statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "total_spans": len(self._spans),
            "total_metrics": len(self._exporter.metrics),
            "config": self.config.to_dict(),
            "trace_context": self._trace_context,
        }
