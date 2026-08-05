# PyVectorHound

**Fix your RAG before it breaks production. Find retrieval bugs instantly.**

Your RAG system is losing documents. PyVectorHound diagnoses why. Pinpoint indexing errors, embedding failures, ranking problems, and chunking mistakes—then get actionable fixes.

[![PyPI](https://img.shields.io/pypi/v/pyvectorhound)](https://pypi.org/project/pyvectorhound)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)
[![Tests Passing](https://img.shields.io/badge/tests-passing-success)](./tests)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-blue.svg)](./LICENSE)

---

## 30-Second Start

```python
from pyvectorhound import Hound

# Diagnose RAG failures
hound = Hound(vector_db="pinecone", embeddings="openai")

# Find what's wrong
diagnosis = hound.diagnose(
    query="How do I reset my password?",
    expected_docs=["FAQ.md", "UserGuide.md"]
)

print(f"Retrieval success: {diagnosis.success_rate:.0%}")
print(f"Problems found: {len(diagnosis.issues)}")
for issue in diagnosis.issues:
    print(f"  - {issue.problem}: {issue.solution}")
```

---

## Why PyVectorHound?

**The Problem:**
- Your RAG system returns wrong documents
- You don't know why (embedding issue? indexing? ranking?)
- Debugging takes hours of manual work
- No way to validate before launching

**The Solution:**
- Automatic root cause diagnosis
- Pinpoint the exact step that's failing
- Get specific, actionable fixes
- Validate RAG quality before production

---

## Key Features

- **Root Cause Analysis:** Find where retrieval breaks (embedding, indexing, ranking, chunking)
- **Quality Metrics:** Measure precision, recall, NDCG across your documents
- **Fix Recommendations:** Get specific, code-ready solutions
- **Before/After Testing:** Compare RAG quality across changes
- **Multi-DB Support:** Pinecone, Weaviate, Qdrant, Milvus, Elasticsearch
- **Embedding Validation:** Test different embedding models
- **Batch Diagnostics:** Analyze 100s of queries at once

---

## Real-World Use Cases

**Before Launching:**
```python
# Validate RAG quality before production
hound = Hound()
quality = hound.validate_quality(
    test_queries=100,
    min_success_rate=0.85  # 85% minimum
)

if quality.success_rate < 0.85:
    print(f"Not ready: {quality.issues}")
    # Don't deploy
```

**Debugging Failures:**
```python
# Why did this query fail?
diagnosis = hound.diagnose(
    query="What's your return policy?",
    actual_results=["Pricing.pdf"],  # Wrong!
    expected_docs=["Returns.pdf", "Policy.md"]
)

# Get the fix
print(diagnosis.root_cause)  # "Embeddings too similar"
print(diagnosis.solution)    # "Use embedding model X instead"
```

**Comparing Approaches:**
```python
# Which embedding model is better?
before = hound.quality_score(embedding_model="openai")
after = hound.quality_score(embedding_model="cohere")

improvement = (after - before) / before * 100
print(f"Model improved quality by {improvement:.1f}%")
```

---

## Diagnostics It Runs

| Issue | Detection | Fix |
|-------|-----------|-----|
| **Embedding** | Vectors too similar, not capturing meaning | Suggest better embedding model |
| **Indexing** | Documents not in vector DB or corrupted | Rebuild index with validation |
| **Ranking** | Right documents present but ranked low | Tune similarity metric or weights |
| **Chunking** | Documents split wrong, breaking context | Adjust chunk size or overlap |
| **Query** | Query phrasing doesn't match documents | Suggest rephrasing or expansion |

---

## Installation

```bash
pip install pyvectorhound
# or with uv
uv pip install pyvectorhound
```

---

## Documentation

- [Quick Diagnosis](docs/QUICKSTART.md) — Debug your first RAG issue
- [Fixing RAG](docs/FIXES.md) — Solutions for common problems
- [Quality Metrics](docs/METRICS.md) — How retrieval is scored
- [Examples](examples/) — Real-world diagnostics

---

## License

Proprietary License - Free to use with explicit attribution. See [LICENSE](LICENSE).

---

**PyVectorHound v2.0.0** | RAG diagnostics & debugging | Python 3.10+

## License

MIT

---

**MCP 2.0 Mega-Platform | v2.0.0 | Wheels-Only Distribution**
