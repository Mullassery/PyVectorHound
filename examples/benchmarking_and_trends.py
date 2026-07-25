"""Example: Performance Benchmarking and Trend Analysis.

Demonstrates how to use PyVectorHound's v0.3 features for:
- Measuring and benchmarking query performance
- Tracking metrics over time
- Detecting performance regressions and anomalies
- Comparing embedding models and databases
"""

from pyvectorhound import (
    Hound,
    PerformanceBenchmark,
    TrendAnalyzer,
)
import time


def example_performance_benchmarking():
    """Benchmark retrieval performance across components."""
    print("\n=== Performance Benchmarking Example ===\n")

    # Initialize Hound (connected to a vector database)
    # hound = Hound(db="qdrant", endpoint="localhost:6333")

    # Create benchmark engine
    benchmark = PerformanceBenchmark()

    # Example 1: Measure query latency
    def mock_query():
        """Simulate a vector search query."""
        time.sleep(0.001)  # 1ms

    print("Measuring query latency...")
    query_latency = benchmark.measure_query_latency(mock_query, num_iterations=100)
    print(f"  Mean: {query_latency.mean:.2f}ms")
    print(f"  P95:  {query_latency.p95:.2f}ms")
    print(f"  P99:  {query_latency.p99:.2f}ms")
    print(f"  Samples: {query_latency.samples}")

    # Example 2: Compare databases
    print("\nComparing database performance...")

    def query_qdrant():
        time.sleep(0.0008)  # 0.8ms

    def query_chroma():
        time.sleep(0.0012)  # 1.2ms

    db_comparison = benchmark.compare_databases(
        {"qdrant": query_qdrant, "chroma": query_chroma},
        num_iterations=50
    )

    for db_name, metrics in db_comparison.items():
        print(f"  {db_name}:")
        print(f"    Mean: {metrics['mean_ms']:.2f}ms")
        print(f"    P95:  {metrics['p95_ms']:.2f}ms")

    # Example 3: Compare embedding models
    print("\nComparing embedding models...")
    model_configs = {
        "openai-3-small": {
            "quality_metrics": {
                "isotropy": 0.92,
                "coverage": 0.88,
                "distinctiveness": 0.85
            },
            "latency_ms": 15.2,
            "recall": 0.87,
            "cost_per_1m": 0.02,
        },
        "cohere-v3": {
            "quality_metrics": {
                "isotropy": 0.89,
                "coverage": 0.90,
                "distinctiveness": 0.83
            },
            "latency_ms": 22.5,
            "recall": 0.84,
            "cost_per_1m": 0.03,
        },
    }

    comparisons = benchmark.compare_embedding_models(model_configs, [])
    for comparison in comparisons:
        print(f"  {comparison.model_a} vs {comparison.model_b}:")
        print(f"    Recall difference: {comparison.recall_diff:+.2%}")
        print(f"    Latency: {comparison.latency_a_ms:.1f}ms vs {comparison.latency_b_ms:.1f}ms")
        print(f"    Cost: ${comparison.cost_per_1m_tokens_a} vs ${comparison.cost_per_1m_tokens_b} per 1M tokens")


def example_trend_analysis():
    """Track metrics over time and detect issues."""
    print("\n=== Trend Analysis Example ===\n")

    analyzer = TrendAnalyzer()

    # Example 1: Track embedding quality over time
    print("Tracking embedding quality metrics...")

    # Simulate a week of stable performance
    for day in range(7):
        for hour in range(24):
            value = 0.90 + (hour % 3) * 0.01  # Slight hourly variation
            analyzer.track_metric("embedding_isotropy", value, day=day, hour=hour)

    # Simulate degradation on day 8
    print("  Simulating degradation on day 8...")
    for hour in range(24):
        value = 0.82 - (hour % 5) * 0.02  # Significant drop
        analyzer.track_metric("embedding_isotropy", value, day=8, hour=hour)

    # Detect drift
    drift = analyzer.detect_drift("embedding_isotropy")
    if drift and drift.is_anomaly:
        print(f"\n  DRIFT DETECTED!")
        print(f"  Metric: {drift.metric_name}")
        print(f"  Baseline: {drift.baseline_mean:.3f} ± {drift.baseline_stddev:.4f}")
        print(f"  Current:  {drift.current_mean:.3f} ± {drift.current_stddev:.4f}")
        print(f"  Magnitude: {drift.drift_magnitude:.2f}σ (confidence: {drift.confidence:.1%})")

    # Example 2: Detect performance regression
    print("\n\nTracking query latency...")

    # Baseline period
    for i in range(50):
        analyzer.track_metric("query_latency_ms", 45.0 + i * 0.1, period="baseline")

    # Degraded period
    for i in range(50):
        analyzer.track_metric("query_latency_ms", 60.0 + i * 0.1, period="degraded")

    regression = analyzer.detect_regression("query_latency_ms")
    if regression and regression.is_regression:
        print(f"\n  REGRESSION DETECTED!")
        print(f"  Metric: {regression.metric_name}")
        print(f"  Change: {regression.change_pct:+.1f}%")
        print(f"  Severity: {regression.severity}")

    # Example 3: Detect anomalies
    print("\n\nDetecting anomalies...")

    analyzer2 = TrendAnalyzer()

    # Add normal values
    for i in range(30):
        analyzer2.track_metric("recall_at_5", 0.85 + (i % 3) * 0.01)

    # Add anomalous spike
    analyzer2.track_metric("recall_at_5", 0.95)
    analyzer2.track_metric("recall_at_5", 0.98)

    # Add anomalous drop
    analyzer2.track_metric("recall_at_5", 0.45)
    analyzer2.track_metric("recall_at_5", 0.42)

    anomalies = analyzer2.detect_anomalies("recall_at_5")
    if anomalies:
        print(f"  Found {len(anomalies)} anomalies:")
        for anomaly in anomalies:
            print(f"    - {anomaly.anomaly_type.upper()}: value={anomaly.value:.2f} " +
                  f"(expected: {anomaly.expected_range[0]:.2f}-{anomaly.expected_range[1]:.2f})")


def example_using_hound_api():
    """Use benchmarking and trend analysis through Hound API."""
    print("\n=== Using Hound API Example ===\n")

    # Initialize Hound (would connect to real database)
    # hound = Hound(db="qdrant", endpoint="localhost:6333")

    # Note: These examples show the API, but would need a running database

    print("Available benchmarking methods:")
    print("  - hound.benchmark()              # Get benchmarking engine")
    print("  - hound.measure_query_latency(fn, iterations)")
    print("  - hound.get_performance_report()")

    print("\nAvailable trend analysis methods:")
    print("  - hound.analyze_trends()         # Get trend analyzer")
    print("  - hound.track_metric(name, value, **tags)")
    print("  - hound.get_trend_report()")

    print("\nExample usage:")
    print("""
    # Track metrics from your application
    hound.track_metric("embedding_isotropy", 0.92, model="openai")
    hound.track_metric("query_latency_ms", 45.2, db="qdrant")

    # Get analysis reports
    perf_report = hound.get_performance_report()
    trend_report = hound.get_trend_report()

    # Detect issues
    analyzer = hound.analyze_trends()
    drift = analyzer.detect_drift("embedding_isotropy")
    regression = analyzer.detect_regression("query_latency_ms")
    anomalies = analyzer.detect_anomalies("recall_at_5")
    """)


if __name__ == "__main__":
    print("PyVectorHound v0.3: Performance Benchmarking & Trend Analysis")
    print("=" * 60)

    example_performance_benchmarking()
    example_trend_analysis()
    example_using_hound_api()

    print("\n" + "=" * 60)
    print("Examples complete!")
