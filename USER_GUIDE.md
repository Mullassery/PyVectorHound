# PyVectorHound User Guide

Complete guide for using PyVectorHound to diagnose and optimize retrieval systems.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [Trace Capture](#trace-capture)
4. [Performance Analysis](#performance-analysis)
5. [Trend Analysis](#trend-analysis)
6. [Interactive Replay](#interactive-replay)
7. [Recommendations](#recommendations)
8. [Advanced Analytics](#advanced-analytics)
9. [Framework Integration](#framework-integration)
10. [Best Practices](#best-practices)

---

## Getting Started

### Installation

```bash
pip install pyvectorhound
```

### Quick Start

```python
from pyvectorhound import Hound

# Initialize Hound
hound = Hound(
    db="qdrant",
    endpoint="localhost:6333",
    index_name="documents"
)

# Diagnose a query
diagnosis = hound.diagnose(
    query="your search query",
    top_k=10
)

print(diagnosis.hunt())  # Plain English diagnosis
```

---

## Core Concepts

### The 5 Layers of Diagnostics

PyVectorHound analyzes retrieval systems at 5 levels:

1. **Tracing** — Capture complete pipeline execution
2. **Benchmarking** — Measure performance metrics
3. **Trending** — Track metrics over time
4. **Replay** — Test configurations interactively
5. **Recommendations** — Get AI-powered fixes with ROI

### 8-Category Failure Taxonomy

PyVectorHound categorizes retrieval failures into:

1. **Embedding Quality** — Model lacks domain vocabulary
2. **Chunking Problems** — Answer spans multiple chunks
3. **Vector Search** — ANN losing relevant neighbors
4. **Hybrid Search** — Dense vs sparse misalignment
5. **Metadata Filtering** — Overly restrictive filters
6. **Reranking** — Model demoting correct results
7. **Context Assembly** — Truncation or token budget
8. **Answer Generation** — LLM hallucination/ignoring context

---

## Trace Capture

### Capture Pipeline State

```python
from pyvectorhound import Hound
import numpy as np

hound = Hound(db="qdrant", endpoint="localhost:6333")
tracer = hound.tracer()

# Start tracing a query
tracer.start_trace("query_1", "search text", "openai-3-small")

# Record embedding
query_vector = np.random.randn(768)
tracer.record_embedding(query_vector, latency_ms=15.2)

# Record search results
from pyvectorhound.retrieval_tracing import SearchResult

results = [
    SearchResult(
        doc_id="doc_1",
        content="relevant content",
        score=0.92,
        metadata={"source": "wiki"},
        rank=0
    ),
    SearchResult(
        doc_id="doc_2",
        content="somewhat relevant",
        score=0.78,
        metadata={"source": "blog"},
        rank=1
    ),
]

tracer.record_vector_search_results(results)

# Record LLM response
tracer.record_llm_response("The answer is...")

# End trace
trace = tracer.end_trace()

# Analyze trace
analysis = hound.tracer().get_trace_analysis("query_1")
print(f"Slowest phase: {analysis['slowest_phase']}")
print(f"Total time: {analysis['total_time_ms']}ms")
```

---

## Performance Analysis

### Measure Query Latency

```python
# Measure latency with percentile analysis
def query_func():
    return hound.diagnose("test query")

metrics = hound.measure_query_latency(query_func, num_iterations=100)

print(f"Mean: {metrics.mean:.2f}ms")
print(f"P95: {metrics.p95:.2f}ms")
print(f"P99: {metrics.p99:.2f}ms")
```

### Compare Databases

```python
# Compare performance across databases
benchmark = hound.benchmark()

results = benchmark.compare_databases(
    {
        "qdrant": lambda: qdrant_search(),
        "chroma": lambda: chroma_search(),
        "milvus": lambda: milvus_search(),
    },
    num_iterations=50
)

for db_name, metrics in results.items():
    print(f"{db_name}: {metrics['mean_ms']:.2f}ms")
```

### Compare Embedding Models

```python
# Compare embedding models
model_configs = {
    "openai-3-small": {
        "quality_metrics": {"isotropy": 0.92, "coverage": 0.88},
        "latency_ms": 15.2,
        "recall": 0.87,
        "cost_per_1m": 0.02,
    },
    "cohere-v3": {
        "quality_metrics": {"isotropy": 0.89, "coverage": 0.90},
        "latency_ms": 22.5,
        "recall": 0.84,
        "cost_per_1m": 0.03,
    },
}

comparisons = benchmark.compare_embedding_models(model_configs, [])

for comp in comparisons:
    print(f"{comp.model_a} vs {comp.model_b}")
    print(f"  Recall difference: {comp.recall_diff:+.2%}")
    print(f"  Cost difference: ${comp.cost_per_1m_tokens_a - comp.cost_per_1m_tokens_b}")
```

---

## Trend Analysis

### Track Metrics Over Time

```python
from pyvectorhound import Hound

hound = Hound(db="qdrant", endpoint="localhost:6333")
analyzer = hound.analyze_trends()

# Track embedding quality
analyzer.track_metric("embedding_isotropy", 0.92, model="openai")
analyzer.track_metric("embedding_isotropy", 0.91, model="openai")
analyzer.track_metric("embedding_isotropy", 0.88, model="openai")

# Track query latency
analyzer.track_metric("query_latency_ms", 45.2, db="qdrant")
analyzer.track_metric("query_latency_ms", 48.1, db="qdrant")
analyzer.track_metric("query_latency_ms", 52.3, db="qdrant")
```

### Detect Drift

```python
# Set baseline
analyzer.set_baseline(
    "embedding_isotropy",
    {"mean": 0.92, "stddev": 0.02}
)

# Add degraded values
for _ in range(10):
    analyzer.track_metric("embedding_isotropy", 0.75)

# Detect drift
drift = analyzer.detect_drift("embedding_isotropy")

if drift and drift.is_anomaly:
    print(f"DRIFT DETECTED!")
    print(f"Baseline: {drift.baseline_mean:.3f}")
    print(f"Current: {drift.current_mean:.3f}")
    print(f"Confidence: {drift.confidence:.1%}")
```

### Detect Regressions

```python
# Track metric in two periods
for _ in range(10):
    analyzer.track_metric("recall_at_5", 0.85)

for _ in range(10):
    analyzer.track_metric("recall_at_5", 0.75)

# Detect regression
regression = analyzer.detect_regression("recall_at_5")

if regression and regression.is_regression:
    print(f"REGRESSION: {regression.change_pct:+.1f}%")
    print(f"Severity: {regression.severity}")
```

### Detect Anomalies

```python
# Add normal values
for i in range(20):
    analyzer.track_metric("latency_ms", 50.0)

# Add anomalies
analyzer.track_metric("latency_ms", 200.0)  # Spike
analyzer.track_metric("latency_ms", 10.0)   # Drop

# Detect anomalies
anomalies = analyzer.detect_anomalies("latency_ms")

for anomaly in anomalies:
    print(f"{anomaly.anomaly_type.upper()}: {anomaly.value:.1f}ms")
    print(f"Expected range: {anomaly.expected_range}")
```

---

## Interactive Replay

### Create Configurations

```python
from pyvectorhound.retrieval_replay import ComponentType

replayer = hound.replayer()

# Test different chunk sizes
for chunk_size in [256, 512, 1024, 2048]:
    replayer.create_configuration(
        f"chunk_{chunk_size}",
        {ComponentType.CHUNK_SIZE: chunk_size},
        f"Test with {chunk_size} token chunks"
    )

# Test different embedding models
for model in ["openai-3-small", "cohere-v3", "bge-large"]:
    replayer.create_configuration(
        f"embedding_{model}",
        {ComponentType.EMBEDDING_MODEL: model},
        f"Test with {model}"
    )
```

### Run Replays

```python
# Register handler for chunk size swapping
def chunk_handler(trace, chunk_size, results):
    # Apply chunk size adjustment
    # Return modified results and metadata
    return results, {"chunk_size": chunk_size}

replayer.register_component_handler(
    ComponentType.CHUNK_SIZE,
    chunk_handler
)

# Replay with different configurations
for config_id in replayer.configurations.keys():
    result = replayer.replay(trace, config_id)
    print(f"{config_id}: Recall@5={result.recall_at_k[5]:.2f}, Latency={result.latency_ms:.1f}ms")
```

### Compare Results

```python
# Compare two configurations
comparison = replayer.compare_configurations("chunk_512", "chunk_1024")

print(f"Latency difference: {comparison.latency_diff_pct:+.1f}%")
print(f"Recall improvement: {comparison.recall_improvement_pct:+.1f}%")
print(f"Recommendation: {comparison.recommendation}")

# Rank configurations
ranked = replayer.rank_configurations_by_efficiency()
for i, result in enumerate(ranked[:3], 1):
    print(f"{i}. {result.config_id}")
```

---

## Recommendations

### Get AI-Powered Fixes

```python
# Analyze failure and get recommendations
diagnosis = {
    "embedding_quality_score": 0.7,
    "chunking_issues": True,
    "filter_reduction_pct": 40,
}

recommendations = hound.get_recommendations(
    "query_1",
    "your search query",
    diagnosis
)

print(f"Primary failures: {recommendations['primary_failures']}")
print(f"Confidence: {recommendations['confidence']:.1%}")
print(f"Executive summary: {recommendations['executive_summary']}")

# View recommendations
for rec in recommendations['recommendations'][:3]:
    print(f"\n{rec['title']}")
    print(f"  Root cause: {rec['root_cause']}")
    print(f"  Expected improvement: +{rec['expected_improvement_pct']:.0f}%")
    print(f"  Effort: {rec['effort_hours']} hours")
    print(f"  ROI: {rec['roi_score']:.1f}x")
```

### Estimate ROI

```python
from pyvectorhound.recommendations import FixRecommendation

rec = recommendations['recommendations'][0]

# Estimate ROI
roi_analysis = hound.get_recommendation_summary("query_1")

print(f"Engineering cost: ${roi_analysis['engineering_cost_usd']:.0f}")
print(f"Expected value: ${roi_analysis['estimated_value_usd']:.0f}")
print(f"ROI: {roi_analysis['roi_percent']:.0f}%")
print(f"Payback period: {roi_analysis['payback_period_days']:.0f} days")
```

---

## Advanced Analytics

### Compare Databases

```python
from pyvectorhound.advanced_analytics import AdvancedAnalytics

analytics = AdvancedAnalytics()

# Register performance data
analytics.register_performance_data(
    "Qdrant",
    avg_latency_ms=50.0,
    p95_latency_ms=85.0,
    p99_latency_ms=120.0,
    throughput_qps=1000,
    recall_avg=0.85,
    scalability_score=80.0
)

analytics.register_performance_data(
    "Pinecone",
    avg_latency_ms=45.0,
    p95_latency_ms=80.0,
    p99_latency_ms=115.0,
    throughput_qps=1200,
    recall_avg=0.88,
    scalability_score=85.0
)

# Compare
comparison = analytics.compare_databases(
    ["Qdrant", "Pinecone"],
    optimization_goal="balanced"
)

for db in comparison["databases"]:
    print(f"{db['name']}: Efficiency={db['efficiency_score']:.0f}")
```

### Estimate Costs

```python
# Estimate monthly costs
costs = analytics.estimate_monthly_cost(
    "Qdrant",
    num_documents=1_000_000,
    queries_per_day=100_000
)

print(f"Query cost: ${costs['query_cost']:.2f}")
print(f"Storage cost: ${costs['storage_cost']:.2f}")
print(f"Total monthly: ${costs['total_monthly']:.2f}")
print(f"Cost per query: ${costs['cost_per_query']:.6f}")
```

### Forecast Performance

```python
# Forecast with 2x growth
forecast = analytics.forecast_performance(
    "Qdrant",
    growth_factor=2.0
)

print(f"Current latency: {forecast['current_latency_ms']:.1f}ms")
print(f"Forecast latency: {forecast['forecast_latency_ms']:.1f}ms")
print(f"Latency increase: {forecast['latency_increase_pct']:.1f}%")
```

### Get Recommendations

```python
from pyvectorhound.advanced_analytics import PerformanceCharacteristics

current_perf = PerformanceCharacteristics(
    database_name="Qdrant",
    avg_query_latency_ms=50.0,
    p95_query_latency_ms=85.0,
    p99_query_latency_ms=120.0,
    throughput_qps=1000,
    recall_avg=0.85,
    scalability_score=75.0,
)

recommendations = analytics.get_optimization_recommendations(
    "Qdrant",
    current_perf,
    constraints={
        "max_latency_ms": 40,
        "max_monthly_cost": 5000,
    }
)

for rec in recommendations:
    print(f"Recommended: {rec.recommended_database}")
    print(f"Reason: {rec.rationale}")
    print(f"Cost savings: ${rec.estimated_cost_savings_monthly:.0f}/month")
```

---

## Framework Integration

### LangChain Integration

```python
from langchain.retrievers import Retriever
from pyvectorhound.langchain_integration import InstrumentedRetriever, create_diagnostic_qa_chain

# Wrap your existing retriever
base_retriever = your_langchain_retriever
instrumented = InstrumentedRetriever(base_retriever, hound)

# Use like normal retriever
docs = instrumented.get_relevant_documents("query")

# Or use diagnostic QA
chain = create_diagnostic_qa_chain(
    retriever=base_retriever,
    llm=your_llm,
    hound=hound
)

response = chain.invoke({"query": "your question"})
```

### LlamaIndex Integration

```python
from llamaindex.retrievers import VectorIndexRetriever
from pyvectorhound.llamaindex_integration import (
    instrument_llamaindex_engine,
    instrument_llamaindex_retriever
)

# Wrap retriever
base_retriever = VectorIndexRetriever(index=vector_index)
diagnostic_retriever = instrument_llamaindex_retriever(base_retriever, hound)

# Wrap query engine
base_engine = index.as_query_engine()
diagnostic_engine = instrument_llamaindex_engine(base_engine, hound)

# Use like normal
response = diagnostic_engine.query("your question")
```

---

## Best Practices

### 1. Regular Performance Monitoring

```python
# Set up periodic monitoring
import schedule

def monitor_retrieval():
    metrics = hound.measure_query_latency(
        lambda: hound.diagnose("test query"),
        num_iterations=10
    )
    hound.track_metric("avg_latency_ms", metrics.mean)

schedule.every(1).hour.do(monitor_retrieval)
```

### 2. Establish Baselines

```python
# Set quality baselines
analyzer = hound.analyze_trends()

# Collect baseline data
for i in range(100):
    analyzer.track_metric("recall_at_5", 0.85)

# Calculate baseline statistics
baseline_stats = {
    "mean": 0.85,
    "stddev": 0.02,
}

analyzer.set_baseline("recall_at_5", baseline_stats)
```

### 3. Automated Alerting

```python
# Alert on anomalies
analyzer = hound.analyze_trends()

def check_anomalies():
    anomalies = analyzer.detect_anomalies("latency_ms")
    if anomalies:
        for anomaly in anomalies:
            if anomaly.anomaly_score > 3:
                send_alert(f"Critical: {anomaly.anomaly_type} detected")
```

### 4. Documentation

```python
# Document configuration decisions
config_notes = {
    "chunk_size": 512,
    "reasoning": "Balances context and coverage",
    "tested_sizes": [256, 512, 1024],
    "best_recall": 0.87,
    "deployment_date": "2026-07-26",
}
```

---

**Last Updated**: 2026-07-26  
**Version**: 1.0.0
