# PyVectorHound

**Diagnose why your RAG retrieval is returning the wrong documents.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pyvectorhound)](https://pypi.org/project/pyvectorhound/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org)
[![Tests](https://github.com/Mullassery/PyVectorHound/actions/workflows/ci.yml/badge.svg)](https://github.com/Mullassery/PyVectorHound/actions/workflows/ci.yml)
[![Graphify](https://img.shields.io/badge/Graphify-knowledge%20graph-blue)](https://github.com/Graphify-Labs/graphify)

> **Not to be confused with [PyAgentHound](https://github.com/Mullassery/PyAgentHound):** PyVectorHound diagnoses RAG retrieval failures; PyAgentHound traces and root-causes AI agent execution failures.

## Which project do I need?

Part of the Mullassery open-source family. These tools have similar names — here is the short version of who does what:

| If you need to… | Use |
| --- | --- |
| Build a repository's dependency graph and match it against vulnerability advisories (Python, Rust, Node, containers) | [PyDeepMesh](https://github.com/Mullassery/PyDeepMesh) |
| Understand *why* a Python dependency exists, who added it, and whether it is actually used | [PyDependencyCheck](https://github.com/Mullassery/PyDependencyCheck) |
| Statically analyze a **dbt** project (risky tests, test blast radius, cost) | [PyDBTGuard](https://github.com/Mullassery/PyDBTGuard) |
| Statically analyze **Apache Beam / Dataflow** pipelines (cost, hot keys, reliability) | [PyBeamGuard](https://github.com/Mullassery/PyBeamGuard) |
| Validate **Airflow** DAGs and dbt runs | [PyAirflowTester](https://github.com/Mullassery/PyAirflowTester) |
| Simulate cascading-failure **blast radius** across infrastructure, data pipelines, and AI systems | [PyBlastRadius](https://github.com/Mullassery/PyBlastRadius) |
| Check the **quality of the data itself** at runtime (schema, drift, anomalies) | [StatGuardian](https://github.com/Mullassery/StatGuardian) |
| Discover **devices, services, and vulnerabilities on a network** | [PyNetworkIntel](https://github.com/Mullassery/PyNetworkIntel) |
| Discover and score **API security** risk (real traffic, agent/MCP, Cedar policy) | [PyAPICheck](https://github.com/Mullassery/PyAPICheck) |
| Trace and root-cause **AI agent** failures | [PyAgentHound](https://github.com/Mullassery/PyAgentHound) |
| Diagnose **RAG retrieval** failures | [PyVectorHound](https://github.com/Mullassery/PyVectorHound) |
| Orchestrate **local, dependency-aware tasks** (DAG scheduler + content-addressed cache) | [PyTaskWireCheck](https://github.com/Mullassery/PyTaskWireCheck) |

[Browse all projects →](https://github.com/Mullassery?tab=repositories)

## What it is

PyVectorHound is a component-level diagnostic engine for retrieval-augmented generation
(RAG) pipelines. Point it at a set of search results (from your own pipeline, or from a live
Qdrant/Chroma/Milvus/pgvector/Weaviate instance) and it isolates *which stage* is failing —
embedding quality or vector search ranking — and gives you plain-English, ranked
recommendations. It does **not** run an embedding model, a reranker, or BM25 for you, and it
is **not** a vector database: it's a diagnostic layer that sits on top of retrieval results
you already have and tells you, with real computed metrics, what's wrong.

## Features

- **Embedding-space diagnostics** (isotropy, coverage, distinctiveness) computed by a Rust
  extension (`pyvectorhound._core`, built via PyO3) from the real per-document embeddings
  your database adapter's `get_embeddings()` returns.
- **Vector search accuracy** (precision, recall, MRR) computed against `expected_docs` you
  supply as ground truth.
- **LLM-as-judge faithfulness / contradiction checking** — pass `document_texts` and an
  `llm_judge_fn` (no LLM client bundled) and `Diagnosis` flags retrieved documents that
  score well on embedding similarity but are actually irrelevant to or contradict the query.
- **BM25/keyword diagnostics** — pass the ranked output (or scores) of the keyword
  search you already run and PyVectorHound measures its precision, recall, MRR, and
  top-k agreement with your vector results. It does not ship a BM25 index.
- **Reranker diagnostics** — pass `reranker_scores` for the retrieved results and get
  NDCG@k plus a score-separation calibration proxy against your ground truth.
- **Root cause + ranked recommendations** in plain English, combining the above.
- **Shareable reports** — `Diagnosis.to_html()` / `to_json()` and
  `pyvectorhound report <hound> <query> out.html` produce escaped, standalone
  reports for PRs or CI artifacts.
- **Concurrent batch evaluation** via `Hound.diagnose_batch()`, with automatic
  retry/backoff on `embed_fn`/`llm_judge_fn` calls.
- **Model-agnostic quality thresholds** — `Hound.track_metric()` switches GOOD/MODERATE/WEAK
  status from a fixed cutoff to your own historical baseline.
- **Ranking & diversification** via `rank_and_diversify(results, top_k)`, combining BM25,
  semantic, and recency signals, then penalizing near-duplicates using real cosine
  similarity. `compute_reranker_metrics(...)` reports MRR/NDCG/Precision@K/Recall@K/diversity
  against your ground truth.
- **Opt-in int8 scalar quantization** via `Hound(..., quantized=True)` /
  `hound.enable_quantization()`: `add_vectors()` stores per-vector int8 payloads plus
  scales/offsets, and retrieval dequantizes them on the fly (4x smaller payload with
  bounded reconstruction error). The default float path is unchanged.
- **Historical metric comparison** via `Hound.compare_metrics()` / `Hound.detect_drift()`,
  computed from real values recorded with `Hound.track_metric()`.

## Who it's for

- **Teams whose RAG pipeline is returning irrelevant documents** and who don't know whether
  it's the embeddings or the ranking — `Diagnosis`/`Hound.diagnose()` isolates which stage is
  at fault instead of forcing you to eyeball cosine-similarity scores.
- **Anyone catching retrieved documents that look similar but contradict the query** — the
  LLM-as-judge faithfulness check, when pure distance metrics would score them as a good
  match.
- **Engineers comparing embedding models or database configs objectively** — track metrics
  over time with `Hound.track_metric()` so quality thresholds are relative to your own
  baseline, not a hardcoded cutoff.

## What it is not

- **Not an embedding model, reranker, or vector database.** It brings none of those, and
  won't silently generate a random vector and pretend the resulting diagnosis means
  something: pass an `embed_fn` or a precomputed `query_embedding`.
- **Not a BM25 index or reranker model.** It does not compute keyword search or rerank
  documents itself. It can, however, diagnose an external BM25 ranking and external
  reranker scores when you pass them in; without those inputs both components still
  report `UNKNOWN` rather than inventing a verdict.
- **Not a full retrieve-then-generate evaluator.** Unlike Ragas, PyVectorHound never
  requires an LLM to generate a final answer, so it has no visibility into a
  generation-layer failure.
- **Quantization is an in-process store, not a write-through layer for remote databases.**
  `Hound(..., quantized=True)` keeps a local int8 copy that you populate explicitly with
  `add_vectors()`; it does not change how Qdrant/Chroma/Milvus/Weaviate/pgvector store data.
- **`compare_metrics()` / `detect_drift()` need tracked history.** They compare only values
  recorded with `track_metric()` (optionally with explicit timestamps). They do not
  reconstruct past diagnoses; if the requested periods have no tracked samples, they raise
  a `ValueError` naming what is missing instead of inventing a result.
- **`ModelComparison`/`Hound.compare_models()`** reports real published cost/latency
  metadata but cannot measure quality unless you pass `quality_fn`.

## Audit findings

The 2026-10-19 implementation audit — including the BM25/reranker diagnostics
work, verification results, and remaining gaps — is recorded in
[`AUDIT_FINDINGS.md`](AUDIT_FINDINGS.md).

## Project status

**Production/Stable** per the package classifier (version 1.9.0), with the honest gaps
above. If a component doesn't have enough input to measure honestly (no `adapter`, fewer
than 2 documents with embeddings, or no `expected_docs`), it's reported as `UNKNOWN` with an
explanation of what to supply — never a made-up number. See
[`ROADMAP_HONEST.md`](ROADMAP_HONEST.md) for a plain list of what's not built, what's
untested, and known technical debt. Changes are tracked in [CHANGELOG.md](CHANGELOG.md).

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

Optional synthetic evaluation sets (Ragas-compatible). Ragas itself is optional:
`generate_testset` accepts a caller-supplied generator and never fabricates
questions, and raises an actionable `RagasUnavailable` when no generator is given
and Ragas is absent.

```bash
pip install pyvectorhound[ragas]
```

Requires Python 3.9+. The `pyvectorhound._core` extension is built per
interpreter (it is not `abi3`), so wheels are published for each supported
Python version.

**Supported wheel targets** (built by `.github/workflows/release.yml`):

| OS | Architectures | CPython |
| --- | --- | --- |
| Linux (glibc, manylinux_2_17) | x86_64, aarch64 | 3.9, 3.10, 3.11, 3.12 |
| macOS | arm64, x86_64 | 3.9, 3.10, 3.11, 3.12 |
| Windows | x86_64 | 3.9, 3.10, 3.11, 3.12 |

> **Current PyPI state:** the latest release ships an sdist plus a CPython 3.9 macOS arm64
> wheel. The release workflow builds and smoke-tests the other targets; those
> wheels reach PyPI when its upload job runs. Until then, install from source
> (a Rust toolchain is required) on unsupported targets:
>
> ```bash
> pip install git+https://github.com/Mullassery/PyVectorHound.git
> ```

## Quick start

### Diagnose results you already have

This is the fastest way to try it — no live database or embedding model needed. `Diagnosis`
fetches per-document embeddings for you via a small adapter object (anything with a
`get_embeddings(doc_ids) -> dict` method); without one, the embedding component honestly
reports `"UNKNOWN"` instead of a fabricated score.

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

A runnable version (with synthetic embeddings so it works with no setup) is in
[`examples/retrieval_debug.py`](examples/retrieval_debug.py).

### Diagnose against a live vector database

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

`Hound` connects lazily — constructing it doesn't require a live server, only calling
`diagnose()` (or another querying method) does.

## Synthetic evaluation sets (Ragas interop)

Convert Ragas-style generated questions into PyVectorHound's query +
expected-doc inputs:

```bash
pip install "pyvectorhound[ragas]"
```

```python
from pyvectorhound.synthetic import from_ragas_rows, to_hound_batch

cases = from_ragas_rows(ragas_rows)  # user_input/reference/reference_contexts
queries, expected_docs = to_hound_batch(cases)
diagnoses = hound.diagnose_batch(queries, expected_docs=expected_docs)
```

`generate_testset(documents, generator=...)` accepts a caller-supplied
generator because Ragas's generation API changes across versions and needs an
LLM. Nothing is invented: rows without a query are skipped and missing
documents produce empty expected sets.

## Usage

### Diagnostics it runs

| Component | What it measures | Requires |
|---|---|---|
| **Embedding** | Isotropy, coverage, distinctiveness of the retrieved documents' real embeddings | An `adapter` with `get_embeddings()`, and ≥2 retrieved documents |
| **Vector search** | Precision, recall, MRR | `expected_docs` (ground truth) |
| **Faithfulness** | LLM-judge contradiction/relevance check | `document_texts` + `llm_judge_fn` |
| **BM25 (keyword)** | Precision, recall, MRR, and top-k agreement with vector results from an external keyword ranking | `bm25_results` (ranked ids) or `bm25_scores` (id → score), plus `expected_docs` for precision/recall |
| **Reranker** | NDCG@k and a score-separation calibration proxy | `reranker_scores` (id → score), plus `expected_docs` |

Every measured component is computed for real from the input you give it; nothing is guessed
when the input isn't there.

### BM25 and reranker diagnostics

PyVectorHound does not run keyword search or reranking for you. If your pipeline already
does either, pass its output to `diagnose()` so the diagnosis covers that stage too:

```python
diagnosis = hound.diagnose(
    query="return policy for opened items",
    expected_docs=["returns.pdf", "policy.md"],
    # From your keyword search (BM25, Postgres FTS, Elasticsearch, etc.):
    bm25_results=["returns.pdf", "shipping.md", "policy.md"],
    # From your reranker:
    reranker_scores={"returns.pdf": 0.91, "shipping.md": 0.22, "policy.md": 0.83},
)
print(diagnosis.metrics()["bm25"])
print(diagnosis.metrics()["reranker"])
```

Without `expected_docs`, the components still report UNKNOWN for quality but BM25
agreement with the vector results is reported.

### Faithfulness checking and batch evaluation

```python
from pyvectorhound import Hound

def judge(query: str, doc_texts: list[str]) -> dict:
    # Wrap whatever LLM client you already use -- PyVectorHound doesn't bundle one.
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

Track a few diagnoses over time and quality-status classification switches from a fixed
cutoff to your own historical baseline automatically:

```python
hound.track_metric("vector_search_precision", diagnosis.metrics()["vector_search"]["precision"])
# After ~5+ tracked points, later diagnose() calls classify status
# (GOOD/MODERATE/WEAK) relative to that baseline instead of a fixed number.
```

### Ranking & diversification

```python
from pyvectorhound import rank_and_diversify, compute_reranker_metrics

results = [
    ("doc_1", {"semantic": 0.9}, [1.0, 0.0, 0.3]),     # (doc_id, scores, embedding)
    ("doc_2", {"semantic": 0.85}, [0.98, 0.1, 0.25]),  # near-duplicate of doc_1
    ("doc_3", {"semantic": 0.6}, [0.0, 1.0, 0.0]),
]
ranked = rank_and_diversify(results, top_k=3)
metrics = compute_reranker_metrics(
    [r["document_id"] for r in ranked],
    [r["diversity_score"] for r in ranked],
    relevant_docs=["doc_1", "doc_3"],
    k=3,
)
```

### int8 scalar quantization

`src/quantization.rs` maps each `f32` vector linearly to the `i8` range (-128..=127) using
that vector's own min/max, alongside a `(scale, offset)` pair needed to dequantize it. This
is scalar quantization, not product quantization, and it isn't SIMD/GPU accelerated. Storing
`i8` instead of `f32` is a **4x memory reduction**, at the cost of bounded reconstruction
error (max absolute error per element is at most `(max - min) / 255`). Constant vectors
(including all-zero) round-trip exactly.

Hound wires this into an opt-in local store. While it has vectors, `diagnose()` and
`search_vectors()` read from it instead of the database adapter; the default
`quantized=False` path keeps using the adapter exactly as before.

```python
from pyvectorhound import Hound

hound = Hound(db="qdrant", quantized=True)  # or hound.enable_quantization()
hound.add_vectors([embedding_a, embedding_b], ids=["doc_a", "doc_b"])

# Stored as int8 + per-vector scale/offset; dequantized on read.
results = hound.search_vectors(query_embedding, top_k=5)
restored = hound.get_stored_embeddings(["doc_a"])["doc_a"]
```

The rust primitives remain available directly too:

```python
from pyvectorhound import _core

result = _core.py_quantize_vector([0.12, -0.87, 0.5, 0.0])
# {"values": [i8, ...], "scale": float, "offset": float, "min": float, "max": float}
restored = _core.py_dequantize_vector(result["values"], result["scale"], result["offset"])
```

### Other tools

- `hound.quality_scorer()` — `QualityScorer` for scoring an embedding's validity and, given
  corpus neighbors via the adapter, real isotropy/coverage/distinctiveness.
- `hound.benchmark()` — latency percentiles and database/embedding-model comparisons.
- `hound.analyze_trends()` — track metrics over time and detect drift, regressions, and
  anomalies from real tracked values.
- `hound.tracer()` / `hound.replayer()` — capture a retrieval pipeline run and replay it
  under different configurations to compare recall/latency.

### vs Ragas

Ragas is the closest OSS competitor — the standard for RAG evaluation metrics. We ran both
against the same real corpus (168 real chunks from 3 live English Wikipedia articles), real
embeddings (`nomic-embed-text` via a local Ollama instance), and a real local LLM
judge/generator (`qwen2.5:7b-instruct` via Ollama — no cloud API keys used or needed),
across 4 real queries including 2 deliberately hard cases.

| Query | PyVectorHound `vector_search` | PyVectorHound `faithfulness` | Ragas `context_precision` | Ragas `context_recall` | Ragas `faithfulness` |
|---|---|---|---|---|---|
| "easy" (attention mechanism) | WEAK — 0% precision/recall | GOOD | 0.9999 | 1.0 | 1.0 |
| "cross_chunk" (how RAG reduces hallucination) | GOOD — 100% precision/recall | GOOD | 0.9999 | 1.0 | **0.0** |
| "no_answer" (a date not in corpus) | UNKNOWN (correctly declines to guess) | GOOD | **0.0** | 1.0 | 1.0 |
| "distractor" (self- vs cross-attention) | WEAK — 50% precision | GOOD | 0.9999 | 1.0 | 1.0 |

Two real methodological lessons came out of this, not bugs: (1) document-identity ground
truth is brittle — in the "easy"/"distractor" cases the retrieved chunks (from a different
article) still contained the answer, which answer-based metrics like Ragas's aren't fooled
by; (2) the "cross_chunk" row shows the real scope difference — PyVectorHound judges the
*retrieved passages*, Ragas judges the *generated answer* against context, so Ragas caught a
generation-layer failure PyVectorHound has no visibility into. That's the tradeoff: diagnose
the retrieval layer standalone (no generation step needed), or evaluate the full
retrieve-then-generate pipeline end to end.

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — architecture.
- [docs/GUIDE.md](docs/GUIDE.md) — usage guide.
- [ROADMAP_HONEST.md](ROADMAP_HONEST.md) — what's not built, what's untested, and known
  technical debt.
- [CHANGELOG.md](CHANGELOG.md) — release history.
- [examples/](examples/) — runnable scripts.

## Known issues and deferred work

**Blocked / failed:**
- Verified adapter coverage tests for LlamaIndex/LangChain/pgvector.

**Rejected / deferred:**
- Generation-layer evaluation/UI — Ragas/Phoenix own it.

Full shipped/blocked/rejected detail: [`QUEUE_STATUS.md`](QUEUE_STATUS.md).

## Contributing

```bash
git clone https://github.com/Mullassery/PyVectorHound.git
cd PyVectorHound
pip install maturin
maturin develop --release   # builds the Rust extension in place
pip install -e ".[dev]"
pytest tests/ -v
```

CI (the badge above) is green and runs the full test suite. OpenTelemetry / LangChain /
LlamaIndex / MCP integrations, the CLI, and the REST server exist and have passing tests but
have seen far less real-world use than the core `Hound`/`Diagnosis` path.

## Related projects

Other tools from the same family, for adjacent parts of the RAG/LLM stack:

- [PyAgentHound](https://github.com/Mullassery/PyAgentHound) — debug AI systems by tracing execution, detecting failures, identifying root causes, and explaining bad agent results.
- [PyStreamPDF](https://github.com/Mullassery/PyStreamPDF) — reduce RAG costs by extracting only what matters from PDFs: selective retrieval, structure analysis, token-efficient extraction.
- [PyStreamMCP](https://github.com/Mullassery/PyStreamMCP) — intelligence layer for AI agents: query planning, context discovery, and cost optimization.
- [PyTokenCalc](https://github.com/Mullassery/PyTokenCalc) — count tokens and estimate LLM costs across 20+ providers before you send a request.
- [OpenAnchor](https://github.com/Mullassery/OpenAnchor) — token intelligence middleware for multi-provider LLM usage: 6D attribution, pattern detection, recommendations, OTEL export.
- [StatGuardian](https://github.com/Mullassery/StatGuardian) — fast, declarative data quality framework (Rust): schema validation, drift detection, anomaly detection.

[Browse all projects →](https://github.com/Mullassery?tab=repositories)

## License

This project is licensed under the [Apache License 2.0](LICENSE).
