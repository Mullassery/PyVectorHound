# PyVectorHound User Guide

## Getting Started

### Installation

```bash
pip install pyvectorhound
```

### Basic Workflow

```python
from pyvectorhound import Hound

# 1. Initialize PyVectorHound with your database
hound = Hound(db="qdrant", endpoint="localhost:6333")

# 2. Diagnose a retrieval issue
diagnosis = hound.diagnose(query="your search query", top_k=5)

# 3. Get insights
print(diagnosis.hunt())  # Plain English report
```

## Common Tasks

### Task 1: Diagnose Retrieval Quality Drop

You noticed your retrieval F1-score dropped. What happened?

```python
# Get diagnosis
diagnosis = hound.diagnose(
    query="your problematic query",
    top_k=5,
    expected_docs=["doc1", "doc2"]  # optional ground truth
)

# View the report
print(diagnosis.hunt())

# Get metrics for deep dive
metrics = diagnosis.metrics()
print(metrics)

# Get recommendations
recommendations = diagnosis.recommendations()
for rec in recommendations:
    print(f"[{rec['priority']}] {rec['action']}")
```

### Task 2: Choose Between Embedding Models

You want to upgrade your embedding model. Which one is best?

```python
# Compare models
comparison = hound.compare_models(
    model_type="embedding",
    candidates=[
        "text-embedding-3-small",    # current
        "text-embedding-3-large",    # expensive
        "cohere-v3",                 # alternative
    ]
)

# View comparison
print(comparison.report())

# Get Pareto frontier
frontier = comparison.pareto_frontier()
print(f"Best quality: {frontier['best_quality']}")
print(f"Best value: {frontier['best_value']}")
print(f"Best budget: {frontier['best_budget']}")

# A/B test before committing
ab_test = comparison.ab_test(
    model_a="text-embedding-3-small",
    model_b="text-embedding-3-large",
    duration_days=7
)
```

### Task 3: Monitor Embedding Quality

Track embedding quality over time in production.

```python
# Get quality scorer
scorer = hound.quality_scorer()

# Score individual embeddings
quality = scorer.score(embedding_vector)
print(f"Quality status: {quality['status']}")
print(f"Isotropy: {quality['isotropy']:.2%}")

# Monitor corpus health
health = scorer.corpus_health()
if health['drift'] > 0.15:
    alert(f"Embedding quality degraded {health['drift']:.1%}")

# Detect anomalies
anomalies = scorer.detect_anomalies(embedding_list)
if anomalies['low_isotropy']:
    print(f"Found {len(anomalies['low_isotropy'])} low-isotropy embeddings")
```

### Task 4: Measure Improvement

You applied a fix (e.g., upgraded embedding model). What got better?

```python
# Compare before/after metrics
improvement = hound.compare_metrics(
    before="2026-06-15",  # before change
    after="2026-06-20"    # after change
)

# See breakdown by component
breakdown = improvement["breakdown"]
print(f"Overall F1: {breakdown['overall_f1']:.2%}")
print(f"Vector precision: {breakdown['vector']['precision']:.2%}")
print(f"BM25 precision: {breakdown['bm25']['precision']:.2%}")
```

### Task 5: Detect Drift

Get alerts when embedding quality degrades.

```python
# Detect drift over a period
drift = hound.detect_drift(
    baseline_date="2026-01-01",
    current_date="2026-06-20"
)

if drift['significant']:
    print(f"Drift detected: {drift['amount']:.1%} degradation")
    print(f"Recommendation: {drift['recommendation']}")
```

## Database Setup

### Qdrant

```python
hound = Hound(
    db="qdrant",
    endpoint="http://localhost:6333",
    index_name="documents"
)
```

**Prerequisites:**
```bash
# Start Qdrant locally (Docker)
docker run -p 6333:6333 qdrant/qdrant
```

### Chroma

```python
hound = Hound(
    db="chroma",
    endpoint="http://localhost:8000",
    index_name="documents"
)
```

**Prerequisites:**
```bash
# Start Chroma server
chroma run --server --host localhost --port 8000
```

### Milvus

```python
hound = Hound(
    db="milvus",
    endpoint="localhost:19530",
    index_name="documents"
)
```

### Weaviate

```python
hound = Hound(
    db="weaviate",
    endpoint="http://localhost:8080",
    index_name="Documents"
)
```

### PostgreSQL (pgvector)

```python
hound = Hound(
    db="postgres",
    endpoint="localhost:5432",
    index_name="embeddings",
    username="postgres",
    password="your_password",
    database="your_db"
)
```

**Prerequisites:**
```bash
# Install pgvector extension
psql -U postgres -d your_db -c "CREATE EXTENSION IF NOT EXISTS vector"

# Install Python dependencies
pip install pyvectorhound[postgres]
```

**Example Table Structure:**
```sql
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),
    CONSTRAINT embedding_dimension_check CHECK (array_length(embedding, 1) = 1536)
);

CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

## API Reference

### Hound

Main interface for diagnostics.

```python
hound = Hound(
    db="qdrant",                    # Database type
    endpoint="localhost:6333",      # Database endpoint
    index_name="documents",         # Index/collection name
    api_key=None,                   # Optional API key
)
```

**Methods:**

- `diagnose(query, top_k, expected_docs)` → `Diagnosis`
- `compare_models(model_type, candidates)` → `ModelComparison`
- `compare_metrics(before, after)` → `Dict`
- `quality_scorer()` → `QualityScorer`
- `detect_drift(baseline_date, current_date)` → `Dict`

### Diagnosis

Analysis results for a query.

```python
diagnosis = hound.diagnose(query="...")

# Get reports
diagnosis.hunt()              # Plain English report
diagnosis.metrics()           # Raw metrics
diagnosis.recommendations()   # Ranked recommendations
diagnosis.root_cause()        # Root cause explanation
diagnosis.summary()           # Concise summary
```

### ModelComparison

Compare models for selection.

```python
comparison = hound.compare_models(
    model_type="embedding",
    candidates=["model1", "model2"]
)

# Get analysis
comparison.report()           # Plain English comparison
comparison.metrics()          # Raw metrics
comparison.pareto_frontier()  # Optimal models
comparison.ab_test(model_a, model_b)  # A/B testing
```

### QualityScorer

Monitor embedding quality.

```python
scorer = hound.quality_scorer()

# Score individual embeddings
scorer.score(embedding_vector)

# Monitor corpus
scorer.corpus_health()

# Detect issues
scorer.detect_anomalies(embedding_list)
scorer.trend_analysis(baseline_date, current_date)
```

## Troubleshooting

### Issue: "Database connection failed"

Check that your database is running:

```bash
# Qdrant
curl http://localhost:6333/health

# Chroma
curl http://localhost:8000/api/v1/version
```

### Issue: "Index not found"

Make sure the index name matches your database:

```python
# Check what exists
# In Qdrant: http://localhost:6333/api/collections
```

### Issue: "Slow diagnostics"

PyVectorHound is optimized for <100ms per query. If slower:

1. Check database latency (run `search` separately)
2. Reduce `top_k` for faster testing
3. Check network latency to database

## Best Practices

### 1. Regular Monitoring

Set up periodic quality checks:

```python
import schedule

def check_quality():
    health = scorer.corpus_health()
    if health['drift'] > 0.1:
        alert_team(f"Drift: {health['drift']:.1%}")

schedule.every().day.at("10:00").do(check_quality)
```

### 2. A/B Test Model Changes

Always test before deploying:

```python
# Test new embedding model
ab_test = comparison.ab_test(
    model_a="current_model",
    model_b="new_model",
    duration_days=7
)

# Only deploy if winner is clear
if ab_test['p_value'] < 0.05:
    deploy(ab_test['winner'])
```

### 3. Track Changes

Document what changed and its impact:

```python
# Before change
before = hound.diagnose(query="sample", top_k=5)

# Apply change (e.g., upgrade model)
apply_change()

# After change
after = hound.diagnose(query="sample", top_k=5)

# Compare impact
compare = hound.compare_metrics(before_date, after_date)
log_change(change_description, compare['improvement'])
```

### 4. Use Ground Truth

When diagnosing, provide expected results:

```python
diagnosis = hound.diagnose(
    query="quantum computing",
    expected_docs=["doc_1", "doc_3", "doc_5"],  # docs that should be retrieved
    top_k=10
)
# PyVectorHound will calculate precision/recall against ground truth
```

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [examples/](../examples/) for integration examples
- Read the docstrings in `pyvectorhound/hound.py`, `diagnosis.py`,
  `comparison.py`, and `scorer.py` for full API details — there is no
  separate generated API reference yet
- Open an issue on [GitHub](https://github.com/Mullassery/PyVectorHound) for questions
