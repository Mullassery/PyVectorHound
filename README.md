# PyHound

**Hunt down retrieval problems. Fix them fast.**

PyHound diagnoses why your RAG retrieval is failing. It breaks down hybrid retrieval (embedding + keyword + reranking) into components, identifies root causes, and recommends fixes with ROI estimates.

## What Problem Does PyHound Solve?

Your RAG system's retrieval quality degraded. You know something is wrong, but not what:
- Is the embedding model bad?
- Is vector search returning wrong results?
- Is keyword search missing matches?
- Is the reranker miscalibrated?

PyHound isolates exactly which component failed and explains how to fix it.

## When Should You Use PyHound?

Use PyHound when:
- Retrieval quality drops unexpectedly
- You're choosing between embedding models
- You want to understand retrieval performance
- You need to optimize cost vs quality
- You're debugging RAG system performance

## Key Features

- **Component Diagnosis** — Isolate failures: embedding, vector search, keyword search, or reranker
- **Plain English Explanations** — Understand problems without metrics jargon
- **Root Cause Analysis** — Automatically identifies why retrieval failed
- **Model Comparison** — Compare embedding/reranker models with quality/cost trade-offs
- **Improvement Tracking** — Measure impact after applying fixes
- **Drift Detection** — Monitor embedding quality degradation
- **Database-Agnostic** — Works with Qdrant, Chroma, Pinecone, Milvus, Weaviate, PostgreSQL pgvector

## 5-Minute Setup

### Step 1: Install PyHound

```bash
pip install pyhound
```

### Step 2: Set Up a Vector Database (Local Example)

```bash
# Using Docker - start Qdrant locally
docker run -p 6333:6333 qdrant/qdrant
```

### Step 3: Index Your Documents

```python
from qdrant_client import QdrantClient
import numpy as np

client = QdrantClient("localhost", port=6333)

# Create a collection
client.recreate_collection(
    collection_name="documents",
    vectors_config={"size": 1536, "distance": "Cosine"}
)

# Add sample embeddings
vectors = np.random.rand(5, 1536).tolist()
client.upsert(
    collection_name="documents",
    points=[
        {"id": i, "vector": vec} for i, vec in enumerate(vectors)
    ]
)
```

### Step 4: Run PyHound Diagnosis

```python
from pyhound import Hound

# Initialize PyHound
hound = Hound(db="qdrant", endpoint="localhost:6333")

# Diagnose retrieval quality
diagnosis = hound.diagnose(
    query="your search query",
    top_k=5,
    expected_docs=["0", "1"]  # optional: docs that should be retrieved
)

# Get actionable report
print(diagnosis.hunt())
```

### Example Output

PyHound tells you exactly what's wrong in plain English:

```
=======================================================
              PyHound Diagnosis Report
=======================================================

Query: "quantum computing"
Status: RETRIEVAL DEGRADED (F1: 0.52)

COMPONENT BREAKDOWN
-------------------------------------------------------

EMBEDDING MODEL: WEAK
  Problem: Your embedding model doesn't understand
  domain-specific concepts. Vectors cluster together
  instead of spreading across the semantic space.
  
  Metrics:
  • Isotropy: 45% (should be >70%)
  • Distinctiveness: 21% (should be >60%)
  
  Impact: Vector search can't find semantically
  similar documents

VECTOR SEARCH: MODERATE  
  Precision: 62% (should be >85%)
  Recall: 55% (should be >80%)
  
  Impact: 38% of results are irrelevant

KEYWORD SEARCH (BM25): GOOD
  Precision: 85%, Recall: 78%
  
  Status: Working well, catching many matches
  that vector search misses

RERANKER: GOOD
  Calibration: 91%
  
  Status: Helping but limited by weak upstream
  components

ROOT CAUSE
-------------------------------------------------------
Your embedding model (text-embedding-3-small) is too
generic. It was trained on general web data, not your
domain-specific corpus.

RECOMMENDATIONS (Ranked by Impact)
-------------------------------------------------------
1. HIGHEST PRIORITY: Upgrade Embedding Model
   Try: text-embedding-3-large OR domain-specific model
   Expected quality gain: +8-12 F1 points
   Cost impact: +$8/month  
   Implementation time: 2 hours
   ROI: High (8-12% improvement for 40% cost increase)

2. QUICK WIN: Adjust Hybrid Search Weights
   Current: BM25 (50%) + Vector (50%)
   Try: BM25 (40%) + Vector (60%)
   Expected gain: +2-3 F1 points
   Time: 10 minutes
   Cost: None

3. OPTIONAL: Fine-tune Embedding on Your Corpus
   Requires: 500+ labeled examples
   Expected gain: +5-8% quality
   Time: 1-2 days
   Cost: Training infrastructure
```

## Understanding the Output

- **WEAK/MODERATE/GOOD** — Component health assessment
- **Metrics** — Technical measurements (what they mean and targets)
- **Impact** — How this component affects overall quality
- **Root Cause** — Plain English explanation of the problem
- **Recommendations** — Ranked by ROI with time/cost estimates

## FAQ

**Q: Do I need to set up PyHound specially?**  
A: No. Install via pip, point it at your existing vector database, and run diagnosis.

**Q: Can PyHound work with my existing vector database?**  
A: Yes. Supports Qdrant, Chroma, Pinecone, Milvus, Weaviate, PostgreSQL pgvector.

**Q: Does PyHound modify my data?**  
A: No. PyHound is read-only. It analyzes but never modifies your vectors or documents.

**Q: What if I don't have ground truth (expected_docs)?**  
A: Ground truth is optional. Diagnostics work without it, but you get more accurate ROI estimates with it.

**Q: How long does a diagnosis take?**  
A: Typically 45ms for small queries. Larger corpus analysis may take seconds.

**Q: Can I use PyHound in production?**  
A: Yes. It's designed for production monitoring. Overhead is minimal (<1ms per operation).

**Q: Does PyHound require Rust knowledge?**  
A: No. PyHound is pure Python to use. Rust is only for building from source.

**Q: What's the difference between PyHound and Phoenix/Arize?**  
A: PyHound diagnoses WHY retrieval failed (root cause + fixes). Phoenix/Arize monitor THAT it failed (observability). Use both together.

## Supported Vector Databases

-  **Qdrant** — Full support
-  **Chroma** — Full support
-  **Pinecone** — Full support
-  **Milvus** — Full support
-  **Weaviate** — Full support
-  **PostgreSQL (pgvector)** — Full support
-  **Custom** — Query any database

Add more databases by implementing the `VectorDB` protocol.

## Architecture

```
Rust Core (pyhound_core)
├─ Embedding quality metrics
├─ Pipeline analysis
├─ Drift detection
└─ Improvement tracking
    ↓ (PyO3 bindings)
Python Wrapper
└─ Hound class (main API)
```

**Why Rust?**
- Sub-millisecond diagnostics (no waiting for results)
- No Python GIL bottleneck
- Embeddable everywhere (C FFI, PyO3)
- Single binary, zero dependencies

## PyHound vs Observability Tools

PyHound is **not** a replacement for observability platforms like Phoenix, Arize, or Helicone.

| Tool | Purpose | Answers |
|------|---------|---------|
| **Phoenix/Arize** | Monitor what's happening | "Is something broken?" |
| **PyHound** | Diagnose problems | "What's broken and why?" |
| **PyHound** | Guide solutions | "How do I fix it?" |
| **PyHound** | Measure results | "Did my fix work?" |

**Ideal setup:** Use both—observability alerts you, PyHound diagnoses and fixes.

## Common Use Cases

### Use Case 1: Diagnose Production Drop

```python
# Your retrieval quality suddenly dropped
hound = Hound(db="qdrant", endpoint="prod-db:6333")
diagnosis = hound.diagnose(query="search term", top_k=5)
print(diagnosis.hunt())
# Get: component breakdown, root cause, fixes ranked by ROI
```

### Use Case 2: Choose Best Embedding Model

```python
# Should you upgrade to a larger embedding model?
comparison = hound.compare_models(
    model_type="embedding",
    candidates=["3-small", "3-large", "cohere-v3"]
)
print(comparison.report())
# Get: quality metrics, cost impact, ROI analysis
```

### Use Case 3: Monitor Quality Over Time

```python
# Track embedding quality in production
scorer = hound.quality_scorer()

# Score embeddings in real-time
quality = scorer.score(embedding_vector)
if quality["status"] == "WEAK":
    alert("Embedding quality degraded")

# Detect gradual drift
health = scorer.corpus_health()
if health["drift"] > 0.15:
    alert(f"15% quality degradation detected")
```

## Troubleshooting

### Error: "Database connection failed"

```python
# Make sure your vector database is running
# For Qdrant:
docker run -p 6333:6333 qdrant/qdrant

# For Chroma:
pip install chromadb
# Chroma runs in-process by default
```

### No results from diagnosis

```python
# Make sure you have embeddings in your database
# PyHound only works with existing vector data

# Verify database has data:
from qdrant_client import QdrantClient
client = QdrantClient("localhost", port=6333)
collection_info = client.get_collection("documents")
print(f"Total vectors: {collection_info.points_count}")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Collection not found" | Create collection first before running PyHound |
| "No query results" | Ensure your database has documents indexed |
| "Slow diagnostics" | For large corpora (>1M docs), diagnostics take longer. Use smaller top_k |
| "Missing expected_docs" | Ground truth is optional. Diagnostics still work without it |

## API Quick Reference

```python
from pyhound import Hound

hound = Hound(db="qdrant", endpoint="localhost:6333")

# Core Methods
diagnosis = hound.diagnose(query="...", top_k=5, expected_docs=[...])
comparison = hound.compare_models(model_type="embedding", candidates=[...])
scorer = hound.quality_scorer()

# Diagnosis methods
diagnosis.hunt()              # Plain English report
diagnosis.metrics()           # Raw metrics by component
diagnosis.recommendations()   # Ranked fixes
diagnosis.root_cause()        # Root cause explanation

# Comparison methods
comparison.report()           # Side-by-side comparison
comparison.metrics()          # Quality/cost/latency data
comparison.pareto_frontier()  # Optimal models
comparison.ab_test(...)       # Setup A/B test

# Scorer methods
scorer.score(embedding)       # Score single embedding
scorer.corpus_health()        # Corpus-wide metrics
scorer.detect_anomalies(...)  # Find problematic embeddings
scorer.trend_analysis(...)    # Historical trends
```

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — How PyHound works internally
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute
- [BENCHMARKS_AND_COMPARISON.md](BENCHMARKS_AND_COMPARISON.md) — Performance vs competitors
- [docs/GUIDE.md](docs/GUIDE.md) — Full user guide with examples

## Performance

- **Diagnosis latency:** <100ms per query
- **Quality scoring:** <1ms per embedding
- **Corpus analysis:** <500ms for 100k documents

## Requirements

- Python 3.8+
- Rust 1.70+ (for building from source)
- Vector DB client (Qdrant, Chroma, etc.)

## License

MIT License — See [LICENSE](LICENSE) for details.

PyHound is free for commercial use.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

- **v0.1** — Embedding Inspector + basic diagnostics
- **v0.2** — Hybrid retrieval engine (BM25 + vector + reranker)
- **v0.3** — Embedding versioning with zero-downtime migrations
- **v1.0** — Advanced optimization tools, full observability integration

## Next Steps

1. **Try the Quick Start** — Get PyHound working with Qdrant in 5 minutes
2. **Read Use Cases** — See which scenario matches your problem
3. **Check Benchmarks** — Understand PyHound's performance vs competitors
4. **Explore Roadmap** — See what's planned (v0.2-v1.0)

## Support

- GitHub Discussions: https://github.com/Mullassery/pyhound/discussions
- Issues: https://github.com/Mullassery/pyhound/issues
- Email: mullassery@gmail.com

## Authors

- **Georgi Mammen Mullassery** — Original creator

## Acknowledgments

Built with:
- Rust ecosystem (fast, safe, embeddable)
- PyO3 (Python bindings)
- Open source community

---

**Hunt down retrieval problems. Fix them fast.** 
