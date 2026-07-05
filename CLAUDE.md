# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

PyVectorhound is a hybrid Rust/Python library for diagnosing RAG and LLM retrieval failures. It isolates failing components (embedding quality, vector search, BM25, reranker) and recommends fixes.

**Structure**:
- `src/` (Rust) — Core diagnostics engine
  - `lib.rs` — PyO3 entry point, Python API surface
  - `diagnostics/` — Component-level analysis
    - `embeddings.rs` — Embedding model quality (drift, coverage, consistency)
    - `vector_search.rs` — Vector search performance (recall, precision, neighbors analysis)
    - `keyword.rs` — BM25 keyword search effectiveness
    - `reranker.rs` — Reranker calibration and bias detection
  - `database/` — Vector database adapters
    - `qdrant.rs`, `chroma.rs`, `milvus.rs`, `weaviate.rs`, `postgres.rs` — Database-agnostic protocol abstraction
  - `recommendations.rs` — Fix suggestions with ROI estimates

- `pyvectorhound/` (Python) — High-level API
  - `_core.pyi` — Type stubs for Rust-compiled extension
  - `api.py` — Public diagnostic API surface
  - `loaders.py` — Database connection helpers (Qdrant, Chroma, etc.)

**Key design**: Diagnosis is **O(n)** with linear scans, not O(n²) metric computation like Phoenix/Arize. Results are plain-English explanations, not dashboards.

## Build & Test Commands

**Install**:
```bash
pip install pyvectorhound
pip install "pyvectorhound[qdrant,chroma,milvus]"  # With database support
pip install -e ".[dev]"                              # From source (dev)
```

**Build Rust extension**:
```bash
maturin develop          # Dev wheel with hot reload
maturin build --release  # Release wheel for PyPI
```

**Tests**:
```bash
pytest                    # All tests
pytest -v tests/test_embeddings.py  # Single module
pytest --cov=pyvectorhound          # With coverage
```

**Format & lint**:
```bash
black .
ruff check . --fix
mypy pyvectorhound
```

**Benchmarks**:
```bash
pytest benches/ -v
```

## Important Implementation Details

- **Component isolation**: Each diagnostic module (embeddings, vector search, BM25, reranker) runs independently. Failures in one don't cascade to others.
- **Embedding quality**: Measures drift (distance from baseline), coverage (how many queries have good matches), and consistency (variance in similarity scores).
- **Vector search analysis**: Computes recall@k, precision@k, and neighbor stability (how much results change with small embedding perturbations).
- **Database abstraction**: Adapter pattern per database type. Each adapter implements `search()`, `get_metadata()`, `list_collections()` uniformly.
- **Recommendations**: Each suggestion includes estimated effort (minutes/hours), expected quality gain (% improvement), and cost impact (queries reduced, latency improved).
- **Plain English**: Diagnostics return human-readable explanations, not metrics. E.g., "Embedding model drift detected: cosine similarity decreased 15%. Consider fine-tuning on recent data."
- **Database support**: Qdrant (native HTTP API), Chroma (local/server), Milvus, Weaviate (GraphQL API), PostgreSQL pgvector (SQL). Zero configuration — auto-detects database type.
