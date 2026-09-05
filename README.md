# PyVectorHound

**Diagnose why your RAG retrieval is returning the wrong documents.**

PyVectorHound is a component-level diagnostic engine for retrieval-augmented
generation (RAG) pipelines. Point it at a set of search results (from your
own pipeline, or from a live Qdrant/Chroma/Milvus/pgvector/Weaviate
instance) and it isolates *which stage* is failing — embedding quality or
vector search ranking — and gives you plain-English, ranked recommendations.

[![PyPI](https://img.shields.io/pypi/v/pyvectorhound)](https://pypi.org/project/pyvectorhound)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![Tests](https://github.com/Mullassery/PyVectorHound/actions/workflows/ci.yml/badge.svg)](https://github.com/Mullassery/PyVectorHound/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

---

## What this actually does today

PyVectorHound does **not** run an embedding model, a reranker, or BM25 for
you, and it is **not** a vector database. It's a diagnostic layer that sits
on top of retrieval results you already have (or that it fetches from your
vector DB) and tells you, with real computed metrics, what's wrong:

- **Embedding-space diagnostics** (isotropy, coverage, distinctiveness) —
  computed by a Rust extension (`pyvectorhound._core`, built via PyO3) from
  the real per-document embeddings your database adapter's `get_embeddings()`
  returns.
- **Vector search accuracy** (precision, recall, MRR) — computed against
  `expected_docs` you supply as ground truth.
- **LLM-as-judge faithfulness / contradiction checking** — pass
  `document_texts` and an `llm_judge_fn` (no LLM client bundled, same
  pattern as `embed_fn`) and `Diagnosis` will flag retrieved documents that
  score well on embedding similarity but are actually irrelevant to or
  contradict the query — the failure mode pure distance metrics can't see.
- **Root cause + ranked recommendations** — plain-English output combining
  the above.
- **Concurrent batch evaluation** — `Hound.diagnose_batch()` runs many
  queries at once on a thread pool (with automatic retry/backoff on
  `embed_fn`/`llm_judge_fn` calls) instead of one at a time, for large-scale
  evaluation runs.
- **Model-agnostic quality thresholds** — once you've tracked a few
  diagnoses with `Hound.track_metric()`, GOOD/MODERATE/WEAK status is
  computed relative to your own historical baseline instead of a fixed
  cutoff, so it doesn't drift when you switch embedding models.

BM25 (keyword search) and reranker diagnostics are reported as `"UNKNOWN"`:
PyVectorHound doesn't run a keyword-search index or a reranker itself, and
`Diagnosis` doesn't yet accept external BM25/reranker scores as input, so
rather than fabricate a number for a component it can't measure, it says so.

If a component doesn't have enough input to measure honestly (no `adapter`,
fewer than 2 documents with embeddings, or no `expected_docs`), it's
reported as `"UNKNOWN"` with an explanation of what to supply — never a
made-up number.

**PyVectorHound does not bundle an embedding model.** If you want
`Hound.diagnose()` to embed your query text for you, pass it an `embed_fn`
(a thin wrapper around whatever you already use — OpenAI, Cohere,
sentence-transformers, etc.). Without one, pass a precomputed
`query_embedding` per call. It will not silently generate a random vector
and pretend the resulting diagnosis means something.

### New: advanced retrieval ranking (Rust core)

`src/retrieval_ranking.rs` adds a `RetrievalRanker` that combines BM25,
semantic, recency, and diversity signals into a single multi-criteria
ranking, plus cross-encoder-style reranking support. It's compiled into the
native `_core` extension but not yet exposed as a Python-callable function —
if you need it from Python today, treat it as in-progress internal
infrastructure rather than a public API.

### New: int8 scalar quantization (Rust core)

`src/quantization.rs` adds per-vector int8 scalar quantization for shrinking
the memory footprint of large local vector indices. Each `f32` vector is
mapped linearly to the `i8` range (-128..=127) using that vector's own
min/max, alongside a `(scale, offset)` pair needed to dequantize it back to
an approximate `f32` vector. This is scalar quantization, not product
quantization, and it isn't SIMD/GPU accelerated — both are out of scope for
this feature.

**Tradeoff:** storing `i8` instead of `f32` is a **4x memory reduction**
for the vector data (1 byte/dim vs 4 bytes/dim), at the cost of bounded
reconstruction error — max absolute error per element is at most
`(max - min) / 255` for the vector being quantized (half a quantization
step in practice). For a typical normalized embedding in `[-1, 1]`, that's
a worst-case error bound of about `0.0078` per dimension; measured max
error on a random 384-dim `[-1, 1]` vector in the test suite was `~0.0039`.
Constant vectors (including all-zero) round-trip exactly.

Exposed to Python via `pyvectorhound._core`:

```python
from pyvectorhound import _core

# Single vector
result = _core.py_quantize_vector([0.12, -0.87, 0.5, 0.0])
# {"values": [i8, ...], "scale": float, "offset": float, "min": float, "max": float}
restored = _core.py_dequantize_vector(result["values"], result["scale"], result["offset"])

# Batch (one scale/offset per vector)
batch = _core.py_quantize_batch([[0.1, 0.2], [-1.0, 1.0]])
# {"values": [[i8, ...], ...], "params": [{"scale":..., "offset":..., "min":..., "max":...}, ...]}
restored_batch = _core.py_dequantize_batch(
    batch["values"],
    [p["scale"] for p in batch["params"]],
    [p["offset"] for p in batch["params"]],
)
```

This is currently a low-level building block (quantize/dequantize
primitives) rather than integrated into `Hound`'s storage/retrieval path —
if you want quantized on-disk storage for your own index today, call these
functions directly.

### Not yet real (known limitations)

Being upfront about what's still a stub, rather than leaving it to look
finished:

- `ModelComparison` / `Hound.compare_models()` reports real, published
  cost/latency metadata for known models, but has no way to measure quality
  (F1/NDCG) on its own — pass `quality_fn` for real numbers, or it reports
  quality as unmeasured.
- `Hound.compare_metrics()` and `Hound.detect_drift()` raise
  `NotImplementedError`; `QualityScorer.trend_analysis()` instead returns a
  dict with `"direction": "unknown"` and an explanation. None of the three
  has a historical data store to compute a real trend from. Use
  `Hound.track_metric()` + `Hound.get_trend_report()` (backed by the real,
  tested `TrendAnalyzer`) instead.
- As of v1.4.0, PyPI carries a macOS arm64 / CPython 3.9 wheel plus a source
  distribution (`sdist`). The wheel is still single-platform/single-ABI (no
  `abi3` build yet — see below), but the sdist means `pip install
  pyvectorhound` on any other interpreter or OS now builds the current
  version from source instead of silently falling back to an old release,
  as long as a Rust toolchain is available locally. If the sdist build
  fails for you, install straight from the repo instead:
  `pip install git+https://github.com/Mullassery/PyVectorHound.git`.
  A proper multi-platform wheel matrix (built in CI, `abi3` so one wheel
  covers multiple CPython versions) is still open work.
- GitHub Actions CI (the badge above) is currently red on every job across
  recent pushes to `main` — not because of failing tests, but because
  `.github/workflows/ci.yml`'s `dtolnay/rust-toolchain@v1` step is missing
  its required `toolchain` input, so every job fails in the setup step
  before any code runs. The local test suite itself passes (159/159 as of
  this writing, run via `pytest tests/ -v` with the Rust extension built).
- OpenTelemetry / LangChain / LlamaIndex / MCP integrations, the CLI, and
  the REST server exist and have passing tests but have seen far less
  real-world use than the core `Hound`/`Diagnosis` path above.

---

## Installation

```bash
pip install pyvectorhound
```

Optional vector database clients (only install the one(s) you use):

```bash
pip install pyvectorhound[qdrant]     # Qdrant
pip install pyvectorhound[chroma]     # Chroma
pip install pyvectorhound[milvus]     # Milvus
pip install pyvectorhound[weaviate]   # Weaviate
pip install pyvectorhound[pgvector]   # PostgreSQL + pgvector
```

Requires Python 3.8+.

---

## Quick start: diagnose results you already have

This is the fastest way to try it — no live database or embedding model
needed. `Diagnosis` fetches per-document embeddings for you via a small
adapter object (anything with a `get_embeddings(doc_ids) -> dict` method);
without one, the embedding component honestly reports `"UNKNOWN"` instead
of a fabricated score.

```python
from pyvectorhound import Diagnosis

class InMemoryAdapter:
    """Anything with get_embeddings(doc_ids) works -- swap in your own
    QdrantAdapter/ChromaAdapter/etc., or a wrapper around your pipeline."""
    def __init__(self, embeddings_by_id):
        self._embeddings_by_id = embeddings_by_id

    def get_embeddings(self, doc_ids):
        return {d: self._embeddings_by_id[d] for d in doc_ids if d in self._embeddings_by_id}

results = [
    {"id": "pricing.pdf", "score": 0.91},
    {"id": "onboarding.md", "score": 0.84},
    {"id": "faq.md", "score": 0.79},
]

diagnosis = Diagnosis(
    query="What's your return policy?",
    results=results,
    expected_docs=["returns.pdf", "policy.md"],  # ground truth
    adapter=InMemoryAdapter(my_document_embeddings),
)
diagnosis.analyze()

print(diagnosis.root_cause())
for rec in diagnosis.recommendations():
    print(f"[{rec['priority']}] {rec['action']}")

print(diagnosis.hunt())  # full plain-English report
```

A runnable version (with synthetic embeddings so it works with no setup) is
in [`examples/retrieval_debug.py`](examples/retrieval_debug.py).

## Quick start: diagnose against a live vector database

```python
from pyvectorhound import Hound

hound = Hound(
    db="qdrant",                      # qdrant | chroma | milvus | weaviate | postgres
    endpoint="localhost:6333",
    index_name="documents",
    # PyVectorHound doesn't ship an embedding model -- wrap whatever you use:
    embed_fn=lambda text: my_embedding_client.embed(text),
)

diagnosis = hound.diagnose(
    query="What's your return policy?",
    expected_docs=["returns.pdf", "policy.md"],
    top_k=5,
)
print(diagnosis.hunt())
```

`Hound` connects lazily — constructing it doesn't require a live server,
only calling `diagnose()` (or another querying method) does. `diagnose()`
already passes `self.adapter` into `Diagnosis`, so embedding-space
diagnostics work out of the box against your real database.

---

## Diagnostics it runs

| Component | What it measures | Requires |
|---|---|---|
| **Embedding** | Isotropy, coverage, distinctiveness of the retrieved documents' real embeddings | An `adapter` with `get_embeddings()`, and ≥2 retrieved documents |
| **Vector search** | Precision, recall, MRR | `expected_docs` (ground truth) |
| **Faithfulness** | LLM-judge contradiction/relevance check | `document_texts` + `llm_judge_fn` |
| **BM25 (keyword)** | Not implemented — reports `UNKNOWN` | n/a |
| **Reranker** | Not implemented — reports `UNKNOWN` | n/a |

Every measured component is computed for real from the input you give it;
nothing is guessed when the input isn't there.

---

## Faithfulness checking and batch evaluation

```python
from pyvectorhound import Hound

def judge(query: str, doc_texts: list[str]) -> dict:
    # Wrap whatever LLM client you already use -- PyVectorHound doesn't
    # bundle one. Must return at least a "contradiction_score" (0.0-1.0,
    # lower is more faithful) and/or "faithful"/"contradicted_count".
    response = my_llm_client.judge_faithfulness(query, doc_texts)
    return {
        "contradiction_score": response.score,
        "contradicted_count": response.contradicted,
        "reasoning": response.explanation,
    }

hound = Hound(db="qdrant", embed_fn=my_embed_fn, llm_judge_fn=judge)

diagnosis = hound.diagnose(
    query="What's your return policy?",
    document_texts={"returns.pdf": "...", "policy.md": "..."},  # doc_id -> text
)
print(diagnosis.metrics()["faithfulness"])

# Evaluate many queries concurrently instead of one at a time:
diagnoses = hound.diagnose_batch(
    queries=["query 1", "query 2", "query 3"],
    document_texts=[{"a": "..."}, None, {"b": "..."}],  # per-query, optional
    max_workers=8,
)
```

Track a few diagnoses over time and quality-status classification switches
from a fixed cutoff to your own historical baseline automatically:

```python
hound.track_metric("vector_search_precision", diagnosis.metrics()["vector_search"]["precision"])
# After ~5+ tracked points, later diagnose() calls classify status
# (GOOD/MODERATE/WEAK) relative to that baseline instead of a fixed number.
```

---

## Other tools

- `hound.quality_scorer()` — `QualityScorer` for scoring an embedding's
  validity, and (given corpus neighbors via the adapter) real
  isotropy/coverage/distinctiveness against the corpus.
- `hound.benchmark()` — `PerformanceBenchmark` for latency percentiles and
  database/embedding-model comparisons.
- `hound.analyze_trends()` — `TrendAnalyzer` for tracking metrics over time
  and detecting drift, regressions, and anomalies from real tracked values.
- `hound.tracer()` / `hound.replayer()` — capture a retrieval pipeline run
  and replay it under different configurations to compare recall/latency.

See [`examples/`](examples/) for runnable scripts, and
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) / [`docs/GUIDE.md`](docs/GUIDE.md)
for more detail.

---

## Development

```bash
git clone https://github.com/Mullassery/PyVectorHound.git
cd PyVectorHound
pip install maturin
maturin develop --release   # builds the Rust extension in place
pip install -e ".[dev]"
pytest tests/ -v
```

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
