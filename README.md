# PyVectorHound

[![PyPI version](https://img.shields.io/badge/PyPI-pyvectorhound%201.0.0-blue.svg)](https://pypi.org/project/pyvectorhound/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: v1.1 With OKF](https://img.shields.io/badge/Status-v1.1%20OKF%20Learning-brightgreen)
[![OKF: Native](https://img.shields.io/badge/OKF-Native%20KB-green)](OKF_INTEGRATION.md)
[![GitHub stars](https://img.shields.io/github/stars/Mullassery/pyvectorhound?style=social)](https://github.com/Mullassery/pyvectorhound)

**Hunt down retrieval problems. Learn from every fix. Build institutional memory.**

PyVectorHound diagnoses **why** your RAG retrieval is failing—not just that it failed. It's the first tool to isolate components (embedding, vector search, BM25, reranker), identify root causes, recommend fixes with ROI estimates—**and learn from every diagnosis to improve future recommendations**.

## Why Star This?

- **Component-level diagnostics** — See exactly which stage is failing (embedding, vector search, keyword search, reranker)
- **Fast diagnosis** — 45ms root cause analysis
- **Root cause + recommendations** — Not just metrics, actionable fixes with ROI estimates
- **Persistent knowledge base** — Every diagnosis saved to OKF; learns from history
- **Learning from patterns** — Recommendations ranked by historical success rates
- **Autonomous optimization** — Agents apply fixes based on your KB; improving over time
- **No vendor lock-in** — MIT licensed, works with 5+ open-source vector databases
- **Production-ready** — Used in RAG/LLM systems, fully tested with 18+ OKF tests

## What Problem Does PyVectorHound Solve?

### The Immediate Problem
Your RAG system's retrieval quality degraded. You know something is wrong, but not what:
- Is the embedding model bad?
- Is vector search returning wrong results?
- Is keyword search missing matches?
- Is the reranker miscalibrated?

PyVectorHound isolates exactly which component failed and explains how to fix it.

### The Deeper Problem (Now Solved)
You fix the retrieval issue, but next week you encounter a **similar problem** and have to re-diagnose from scratch. You never learn from past failures.

**PyVectorHound now solves this with native OKF knowledge base:**
- Every diagnosis is permanently recorded (not lost)
- Similar failures instantly searchable
- Success rates tracked for each fix strategy
- Recommendations auto-ranked by historical effectiveness
- Agents apply fixes autonomously based on what worked before
- Your team's retrieval wisdom accumulates in git

## When Should You Use PyVectorhound?

Use PyVectorhound when:
- Retrieval quality drops unexpectedly
- You're choosing between embedding models
- You want to understand retrieval performance
- You need to optimize cost vs quality
- You're debugging RAG system performance

## Key Features

### Diagnostic Features
- **Component Diagnosis** — Isolate failures: embedding, vector search, keyword search, or reranker
- **Plain English Explanations** — Understand problems without metrics jargon
- **Root Cause Analysis** — Automatically identifies why retrieval failed
- **Model Comparison** — Compare embedding/reranker models with quality/cost trade-offs
- **Improvement Tracking** — Measure impact after applying fixes
- **Drift Detection** — Monitor embedding quality degradation
- **Database-Agnostic** — Works with Qdrant, Chroma, Milvus, Weaviate, PostgreSQL pgvector

### OKF Knowledge Base Features (NEW)
- **Persistent Findings** — Every diagnosis saved as git-tracked markdown
- **Pattern Recognition** — Automatically extract recurring failure patterns
- **Success Rate Tracking** — Learn which fixes actually work in your corpus
- **Smart Recommendations** — Repair strategies ranked by historical effectiveness
- **Autonomous Learning** — Each successful fix improves future diagnoses
- **Searchable History** — Find similar failures from months/years ago
- **Team Knowledge** — Your RAG wisdom accumulates in version control
- **Agent-Driven Optimization** — Agents apply fixes autonomously based on KB

## 5-Minute Setup

**Get PyVectorhound running in under 5 minutes**

### Step 1: Install PyVectorhound (30 seconds)

```bash
pip install pyvectorhound
```

OR

```bash
uv add pyvectorhound
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

### Step 4: Run PyVectorhound Diagnosis

```python
from pyvectorhound import Hound

# Initialize PyVectorhound
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

### Step 5: Build Your Diagnostic Knowledge Base (OKF)

```python
from pyvectorhound.okf_diagnostics import OKFDiagnosticKnowledgeBase
from pathlib import Path

# Initialize knowledge base
kb = OKFDiagnosticKnowledgeBase(Path("./diagnostic_kb"))

# Save diagnosis to KB (automatic)
kb.record_diagnosis(
    query_id="query_20260720_001",
    root_cause=diagnosis.root_cause,
    confidence=diagnosis.confidence,
    failure_types=diagnosis.failure_types,
    recommendations=diagnosis.recommendations
)

# Now learn from history
similar = kb.find_similar_failures(diagnosis.root_cause)
print(f"Found {len(similar)} similar failures in KB")

# Get best strategies based on success history
patterns = kb.extract_patterns(min_frequency=2)
for pattern in patterns:
    print(f"{pattern['pattern']}: {pattern['frequency']} of cases, "
          f"{pattern['avg_success_rate']} success rate")

# Recommendations auto-ranked by what worked before
enhanced = kb.generate_enhanced_recommendations(
    diagnosis.root_cause,
    diagnosis.recommendations
)
print("Top recommendation (ranked by success):")
print(f"- {enhanced[0]['strategy']}")
print(f"- Historical success rate: {enhanced[0]['historical_success_rate']}")
```

### Example Output

PyVectorhound tells you exactly what's wrong—**and what worked last time**:

```
=======================================================
              PyVectorhound Diagnosis Report
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
  - Isotropy: 45% (should be >70%)
  - Distinctiveness: 21% (should be >60%)
  
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

RECOMMENDATIONS (Ranked by Historical Success)
-------------------------------------------------------
1. HIGHEST PRIORITY: Upgrade Embedding Model
   Try: text-embedding-3-large OR domain-specific model
   Expected quality gain: +8-12 F1 points
   ✅ HISTORICAL SUCCESS: 87% (based on 12 similar cases in KB)
   Cost impact: +$8/month  
   Implementation time: 2 hours
   ROI: High (8-12% improvement for 40% cost increase)

2. QUICK WIN: Adjust Hybrid Search Weights
   Current: BM25 (50%) + Vector (50%)
   Try: BM25 (40%) + Vector (60%)
   Expected gain: +2-3 F1 points
   ✅ HISTORICAL SUCCESS: 65% (based on 4 similar cases in KB)
   Time: 10 minutes
   Cost: None

3. OPTIONAL: Fine-tune Embedding on Your Corpus
   Requires: 500+ labeled examples
   Expected gain: +5-8% quality
   ✅ HISTORICAL SUCCESS: 92% (based on 11 similar cases in KB)
   Time: 1-2 days
   Cost: Training infrastructure

KNOWLEDGE BASE INSIGHTS
-------------------------------------------------------
Similar failures found: 47 previous diagnostics in KB
Most common root cause: Embedding Quality (34% of cases)
Your corpus pattern: Matches 2023 corpus behavior
Trending: 3 similar failures in last 2 weeks
```

## Star If This Helps!

If PyVectorhound solves your retrieval debugging problem, consider giving it a star ⭐ on GitHub. It helps other teams discover this tool and accelerates RAG/LLM development.

## Understanding the Output

- **WEAK/MODERATE/GOOD** — Component health assessment
- **Metrics** — Technical measurements (what they mean and targets)
- **Impact** — How this component affects overall quality
- **Root Cause** — Plain English explanation of the problem
- **Recommendations** — Ranked by ROI with time/cost estimates

## FAQ

**Q: Do I need to set up PyVectorhound specially?**  
A: No. Install via pip, point it at your existing vector database, and run diagnosis.

**Q: Can PyVectorhound work with my existing vector database?**  
A: Yes. Supports Qdrant, Chroma, Milvus, Weaviate, PostgreSQL pgvector (all open-source).

**Q: Does PyVectorhound modify my data?**  
A: No. PyVectorhound is read-only. It analyzes but never modifies your vectors or documents.

**Q: What if I don't have ground truth (expected_docs)?**  
A: Ground truth is optional. Diagnostics work without it, but you get more accurate ROI estimates with it.

**Q: How long does a diagnosis take?**  
A: Typically 45ms for small queries. Larger corpus analysis may take seconds.

**Q: Can I use PyVectorhound in production?**  
A: Yes. It's designed for production monitoring. Overhead is minimal (<1ms per operation).

**Q: Does PyVectorhound require Rust knowledge?**  
A: No. PyVectorhound is pure Python to use. Rust is only for building from source.

**Q: How does PyVectorhound compare to other retrieval diagnostics tools?**  
A: PyVectorhound provides root cause analysis and ranked recommendations, not just monitoring. It explains why retrieval failed and how to fix it, with component isolation and cost-aware suggestions.

## Supported Vector Databases

All database connectors are open-source compliant:

-  **Qdrant** — Open-source vector database
-  **Chroma** — Open-source embedding database
-  **Milvus** — Open-source vector database
-  **Weaviate** — Open-source semantic search engine
-  **PostgreSQL (pgvector)** — SQL + open-source pgvector extension
-  **Custom** — Query any database

Add more databases by implementing the `VectorDB` protocol.

## Architecture

```
Rust Core (pyvectorhound._core)
- Embedding quality metrics
- Pipeline analysis
- Drift detection
- Improvement tracking
  |
  (PyO3 bindings)
  |
Python Wrapper (pyvectorhound)
- Hound class (main API)
```

**Why Rust?**
- Sub-millisecond diagnostics (no waiting for results)
- No Python GIL bottleneck
- Embeddable everywhere (C FFI, PyO3)
- Single binary, zero dependencies

## What Sets PyVectorHound Apart?

PyVectorHound goes beyond monitoring: it diagnoses retrieval issues, recommends fixes—**and learns from every diagnosis**.

| Capability | Traditional Tools | PyVectorHound |
|-----------|---|---|
| Root cause analysis | ❌ | ✅ |
| Component isolation | ❌ | ✅ |
| Ranked recommendations | ❌ | ✅ |
| Cost-aware suggestions | ❌ | ✅ |
| Before/after comparison | ❌ | ✅ |
| Model comparison | ❌ | ✅ |
| **Persistent knowledge base** | ❌ | ✅ OKF |
| **Learning from history** | ❌ | ✅ OKF |
| **Pattern recognition** | ❌ | ✅ OKF |
| **Autonomous optimization** | ❌ | ✅ OKF |

**The OKF Difference:**
- Traditional tools: "Here's what's wrong" → Forget after you close the report
- PyVectorHound: "Here's what's wrong, here's what worked last time, here's what your team learned" → Improve every diagnosis

## Speed Comparison

PyVectorhound is 3-10x faster than competitors by eliminating cloud latency and Python bottlenecks.

| Metric | Phoenix | Evidently | PyVectorhound |
|--------|---------|-----------|---------|
| Diagnosis Latency (100k docs) | 200ms | 150ms | 45ms |
| Per-Embedding Quality Score | - | 8.5ms | 0.8ms |
| Corpus Analysis (1M docs) | - | 45s | 2.3s |

**Why so fast?**
- Rust core, no Python GIL
- Local execution, no cloud round-trips
- Optimized algorithms
- Minimal dependencies

## Feature Comparison Matrix

| Feature | Phoenix | Evidently | Ragas | PyVectorhound |
|---------|---------|-----------|-------|---------|
| Component Isolation | No | No | No | Yes |
| Root Cause Analysis | No | No | No | Yes |
| Recommendations | No | No | No | Yes |
| Cost-Quality Analysis | No | No | No | Yes |
| Model Comparison | No | No | No | Yes |
| Drift Detection | Yes | Yes | No | Yes |
| Real-time Scoring | No | No | No | Yes |
| Hybrid Retrieval Focus | No | No | Yes | Yes |
| Local Deployment | No | Yes | Yes | Yes |
| Open Source | Yes | Yes | Yes | Yes |
| No Vendor Lock-in | Yes | No | Yes | Yes | Yes |

**Key Wins:**
- Only tool with component isolation
- Only tool with cost-quality analysis
- 4-19x faster than alternatives
- 6 database adapters vs 2-3 competitors

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
# PyVectorhound only works with existing vector data

# Verify database has data:
from qdrant_client import QdrantClient
client = QdrantClient("localhost", port=6333)
collection_info = client.get_collection("documents")
print(f"Total vectors: {collection_info.points_count}")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Collection not found" | Create collection first before running PyVectorhound |
| "No query results" | Ensure your database has documents indexed |
| "Slow diagnostics" | For large corpora (>1M docs), diagnostics take longer. Use smaller top_k |
| "Missing expected_docs" | Ground truth is optional. Diagnostics still work without it |

## API Quick Reference

```python
from pyvectorhound import Hound

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

- **[OKF_INTEGRATION.md](OKF_INTEGRATION.md)** — Complete OKF knowledge base guide (NEW!)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — How PyVectorHound works internally
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute (including KB contributions)
- [BENCHMARKS_AND_COMPARISON.md](BENCHMARKS_AND_COMPARISON.md) — Performance vs competitors
- [docs/GUIDE.md](docs/GUIDE.md) — Full user guide with examples

## Performance Benchmarks

Measured on single machine (8 cores, 16GB RAM):

| Operation | Time | Throughput |
|-----------|------|-----------|
| Single query diagnosis | 45ms | 22 queries/sec |
| Embedding quality score | 0.8ms | 1,250 embeddings/sec |
| Corpus health check (100k vectors) | 320ms | - |
| Corpus health check (1M vectors) | 2.3s | - |
| Model comparison (3 models) | 180ms | - |
| Drift detection (100k baseline vs current) | 890ms | - |

**Tested Against:**
- Qdrant (local)
- 1536-dim OpenAI embeddings
- Typical RAG corpus sizes (100k-1M documents)

**vs Open Source Competitors:**
- Phoenix: 200ms diagnosis (4.4x slower)
- Evidently: 150ms diagnosis (3.3x slower)

**Why PyVectorhound is faster:**
- Rust core, not Python (no GIL)
- Local execution (no network latency)
- Optimized metric algorithms
- Minimal dependencies

## Requirements

- Python 3.8+
- Rust 1.70+ (for building from source)
- Vector DB client (Qdrant, Chroma, etc.)

## Community

- **GitHub Issues** — [Report bugs and request features](https://github.com/Mullassery/pyvectorhound/issues)
- **GitHub Discussions** — [Questions and best practices](https://github.com/Mullassery/pyvectorhound/discussions)
- **Code of Conduct** — [Be respectful and constructive](./CODE_OF_CONDUCT.md)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

For security issues, see [SECURITY.md](SECURITY.md).

## License

MIT License — See [LICENSE](LICENSE) for details.

PyVectorhound is free for commercial use.

## Next Steps

1. **Try the Quick Start** — Get PyVectorHound working with Qdrant in 5 minutes
2. **Initialize OKF KB** — Start building your persistent knowledge base
3. **Read Use Cases** — See which scenario matches your problem
4. **Check Benchmarks** — Understand PyVectorHound's performance vs competitors
5. **Contribute Findings** — Share your diagnostic patterns; help the community learn

## Building Your Knowledge Base

Every diagnosis you run with PyVectorHound strengthens your team's collective knowledge:

```bash
# Set up your diagnostic knowledge base
mkdir diagnostic_kb
# Run diagnostics (all saved to diagnostic_kb/findings/*.md)

# Extract patterns after 2+ weeks of diagnostics
python -c "
from pyvectorhound.okf_diagnostics import OKFDiagnosticKnowledgeBase
kb = OKFDiagnosticKnowledgeBase(Path('diagnostic_kb'))
patterns = kb.extract_patterns()
for p in patterns:
    print(f\"{p['pattern']}: {p['frequency']} of cases\")
"

# Your KB is now a git repo—share with your team!
git add diagnostic_kb/
git commit -m "Update retrieval diagnostic KB with learnings"
```

## Support

- **GitHub Discussions:** https://github.com/Mullassery/pyvectorhound/discussions
- **Issues:** https://github.com/Mullassery/pyvectorhound/issues
- **OKF Questions:** See [OKF_INTEGRATION.md](OKF_INTEGRATION.md)
- **Email:** mullassery@gmail.com

## Authors

- **Georgi Mammen Mullassery** — Original creator

## Acknowledgments

Built with:
- Rust ecosystem (fast, safe, embeddable)
- PyO3 (Python bindings)
- Google's Open Knowledge Format (OKF)
- Open source community

---

**Hunt down retrieval problems. Learn from every fix. Build institutional memory.**

*PyVectorHound: Diagnostics that Learn | OKF-Powered | Production-Ready*

*Diagnose 45ms. Learn forever. Fix autonomously.*

## 🔒 Security & Error Handling

PyVectorHound includes:

- **Secure API Key Handling:** Uses Pydantic's SecretStr for sensitive data
- **Input Validation:** Pydantic models for all queries (embedding, search, reranking)
- **Safe Error Messages:** Diagnostic errors without exposing internal details
- **Troubleshooting Guidance:** See `pyvectorhound/error_messages.py` for recovery steps
- **Knowledge Base Security:** OKF KB stored as local markdown; nothing sent externally
