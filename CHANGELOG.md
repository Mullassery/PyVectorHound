# Changelog

All notable changes to PyVectorHound are documented in this file.

## [1.4.0]

### Added

- **LLM-as-judge faithfulness / semantic contradiction scoring.** `Diagnosis`
  accepts optional `document_texts` (doc_id -> text) and `llm_judge_fn`
  (`(query, doc_texts) -> dict`) — mirrors the existing `embed_fn` pattern,
  no LLM client bundled. Adds a `faithfulness` component to
  `metrics()`/`hunt()`/`recommendations()`/`root_cause()` that catches
  retrieved documents that are embedding-similar but semantically
  contradict or are irrelevant to the query, a failure mode distance
  metrics alone can't see. Reports `UNKNOWN` honestly when the required
  inputs aren't supplied.
- **`Hound.diagnose_batch()`** — runs many queries concurrently on a thread
  pool instead of serially, for large-scale evaluation runs. `embed_fn`
  and `llm_judge_fn` calls now retry with exponential backoff + jitter
  (`pyvectorhound/_retry.py`).
- **Dynamic threshold calibration.** `scorer.py` and `diagnosis.py`'s
  GOOD/MODERATE/WEAK quality-status cutoffs now classify relative to a
  tracked `TrendAnalyzer` baseline (z-score based) when one is available,
  instead of a fixed numeric cutoff — so status doesn't silently drift
  when you swap embedding models. Falls back to the original fixed
  cutoffs on cold start (no baseline yet). `Hound.diagnose()` and
  `Hound.quality_scorer()` wire this up automatically.

## [1.3.3] - Unreleased

This release reconciles two independent fix passes that diverged from the
same base commit (`165cc80`) without knowledge of each other:

1. The repo owner's own prior work (now `1.3.2`, below): the v1.3 retrieval
   ranking feature, a real Milvus `get_embeddings`, and a fix for the
   `_core` extension / fabricated-diagnosis bug.
2. A separate remediation pass, done from a stale local clone that had not
   pulled (1), which fixed the *same* `_core`/fabrication bug independently
   (briefly published to PyPI as `1.3.0` before this reconciliation) and
   also fixed a number of other, non-overlapping fabrication bugs the
   `1.3.2` pass didn't touch.

Where both passes fixed the same thing (`diagnosis.py`, `scorer.py`,
`src/lib.rs`'s `_core` symbol, the `pyhound` import), `1.3.2`'s
implementation was kept as authoritative and the duplicate was discarded.
Everything below is what pass (2) fixed that pass (1) did not; it's applied
on top of `1.3.2` unchanged.

### Fixed
- `Hound.diagnose()` fabricated the query embedding: a query with no
  `query_embedding` got `np.random.randn(768)`, silently producing a
  meaningless diagnosis dressed up with real-looking metrics. It now
  requires a `query_embedding` or a configured `embed_fn` and raises a
  clear `ValueError` otherwise. **Breaking change** for callers that relied
  on the old silent random-vector fallback; `tests/test_hound.py` was
  updated to assert the new behavior (and a new `embed_fn`-path test) in
  place of the old test that asserted the fabricated vector was generated.
- `Hound.__init__` eagerly called `adapter.connect()`, requiring the
  optional client library and a live server just to construct a `Hound`.
  Connection is now lazy, matching every adapter method's own
  lazy-connect behavior.
- Database adapters' `search()` (Qdrant, Chroma, Milvus, pgvector,
  Weaviate) returned the *query* embedding as every result's `"embedding"`
  field instead of the real per-document vector, corrupting any downstream
  embedding-space analysis that reads it directly from search results.
  They now fetch and return the actual per-document embedding where the
  underlying client supports it. (Milvus's `search()` additionally now
  requests `vector_field`/`id_field` per `1.3.2`'s configurable field
  names, alongside this fix.)
- `pydantic` is used in `database.py` (`SecretStr`) but was missing from
  `pyproject.toml` dependencies, so a clean install could fail on import
  if pydantic wasn't already present transitively. Added as a dependency.
  Also moved the `from pydantic import SecretStr` statement below the
  module docstring -- it previously preceded it, which silently discarded
  the module's `__doc__`.
- Base and optional dependencies were pinned to exact old versions (e.g.
  `numpy==1.20.0`, `black==23.0.0`) with no compatible wheels for some of
  the Python versions this package claims to support (3.8-3.12), breaking
  `pip install .[dev]`. Relaxed to compatible ranges.
- CI's Python test job referenced a nonexistent `python/` subdirectory and
  never built the Rust extension via `maturin`, so it always ran against
  whatever `_core` state happened to exist (or silently skipped tests
  entirely). It now runs `maturin develop --release` before installing
  dependencies and running pytest, at the actual repo root.
- Adapter `ImportError` messages told users to `pip install pyhound[...]`
  -- `pyhound` is this project's old name and is not the installable
  package; corrected to `pyvectorhound[...]` across all five adapters.
- `ModelComparison`/`Hound.compare_models()` fabricated quality scores
  (`f1_score`, `ndcg`, etc.) derived from `hash(model_name)`. It now
  reports only real, published cost/latency metadata unless a `quality_fn`
  is supplied for real, measured quality numbers; unmeasured quality is
  reported as `None` with `quality_measured: False` rather than a fake
  number.
- `Hound.compare_metrics()` and `Hound.detect_drift()` returned fixed
  placeholder output (zeros / `"No action needed"`) regardless of input,
  with no backing data store. They now raise `NotImplementedError`
  pointing at the real, tested alternative (`track_metric()` +
  `get_trend_report()` / `TrendAnalyzer.detect_drift()`).
- Removed `tests/test_vector_operations.py`: it tested `VectorStore` and
  `EmbeddingManager` classes that do not exist anywhere in this codebase
  and are outside this package's scope (diagnosing failures in databases
  you already run, not being one).
- Removed stale `README.md.bak` and `pyvectorhound/__init__.py.bak` files
  left over from a previous edit.
- `pyvectorhound/diagnosis.py`'s `hunt()` report header still read
  "PyHound Diagnosis Report" after the project's rename; corrected to
  "PyVectorHound", with the matching test assertion updated.
- The CLI (`cli.py`) and REST server (`server.py`) never threaded
  `query_embedding`/`embed_fn` through to `Hound.diagnose()`, so both would
  hit the `ValueError` above unconditionally once the random-embedding
  fallback was removed. Both now accept and forward a precomputed
  `query_embedding`.
- `README.md` and `examples/retrieval_debug.py` described a fictional API
  (`VectorHound`, `hound.validate_quality()`, `quality_score()`, DB
  support for Pinecone/Elasticsearch that isn't implemented) instead of
  the real `Hound`/`Diagnosis` classes. Rewritten to match the actual,
  reconciled API, including `embed_fn` and lazy connection.

## [1.3.2] - Unreleased

### Fixed
- The compiled Rust scoring engine (`pyvectorhound._core`) could never actually load, for two independent reasons: (1) the `#[pymodule]` function was named `pyhound_core` in Rust while `Cargo.toml`/`pyproject.toml` both expect the extension's init symbol to be `_core`; (2) `diagnosis.py` and `scorer.py` imported it as `from pyhound import _core` -- `pyhound` was this project's old name before it was renamed to `pyvectorhound`, and that import was never updated. Both are fixed; `_core` now loads and its isotropy/coverage/distinctiveness/quality-score functions are actually reachable for the first time.
- `Diagnosis._analyze_embedding()` returned hardcoded placeholder numbers (isotropy 0.72, coverage 0.85, distinctiveness 0.68) and an unconditional `"GOOD"` status regardless of the actual retrieved documents. It now fetches the real per-document embeddings via `adapter.get_embeddings()` and computes real metrics via `_core`, honestly reporting `UNKNOWN` when there isn't enough real data to compute them (fewer than 2 embeddings, no adapter, or `_core` unavailable) rather than a fabricated score.
- `Diagnosis._analyze_vector_search()`'s MRR was a hardcoded `0.85 if any relevant doc was retrieved, else 0.0`, ignoring rank entirely. It's now a real reciprocal-rank calculation based on the position of the first relevant result.
- `Diagnosis._analyze_bm25()` and `_analyze_reranker()` unconditionally reported `"GOOD"` with fabricated precision/recall/calibration/NDCG numbers even though no BM25 index or reranker-score subsystem exists anywhere in this codebase. They now honestly report `UNKNOWN` with an explanation, instead of a fake positive verdict. `root_cause()`/`recommendations()` updated so they no longer misinterpret an honest `UNKNOWN` as a real quality problem.
- `QualityScorer.score()` computed a real `overall` score via `_core` but returned hardcoded `isotropy`/`coverage`/`distinctiveness`/`query_relevance` values alongside it regardless of the input embedding. It now samples real nearest-neighbor embeddings from the corpus via the adapter and computes all four metrics for real (or reports `UNKNOWN` if no adapter/corpus data is available, rather than a fake middling score).
- `QualityScorer.corpus_health()` returned fixed `avg_isotropy`/`avg_coverage`/`avg_distinctiveness`/`drift`/`trend` values regardless of the actual corpus. It now samples real corpus embeddings and computes real quality metrics; `drift`/`trend` honestly report as not-measured (this class doesn't persist historical snapshots) instead of a fabricated `"stable"`.
- `QualityScorer.trend_analysis()` returned a fixed `"stable"` direction and `0.02` magnitude for any date range, without looking at any data. It now honestly reports that no historical tracking is wired up, and points callers at `TrendAnalyzer` (which does real time-series tracking) instead.
- `__version__` in `pyvectorhound/__init__.py` was hardcoded to `"1.2.1"` and had drifted from the actual package version; now reads it from installed package metadata.

### Added
- Real test coverage in `tests/test_diagnosis.py` and new `tests/test_scorer.py` asserting the above methods respond to real input data instead of returning fixed constants.

### Fixed
- `MilvusAdapter.get_embeddings()` was a stub that unconditionally returned an empty dict, discarding the requested document IDs instead of querying Milvus. It now retrieves the real stored vectors via `MilvusClient.get()`, with configurable `vector_field`/`id_field` names to match the caller's collection schema.
- `MilvusAdapter.search()` used a hardcoded `"id"` output field instead of the configurable `id_field`.
- `pyproject.toml` was still at 1.2.1 while `Cargo.toml` had already moved to 1.3.0 in a prior commit; synced both.

### Added
- Real test coverage for `pyvectorhound/database.py`'s adapters (`MilvusAdapter`, `QdrantAdapter`, `ChromaAdapter`), which previously had zero tests — only the separate mock-based `db_adapters.py` interface was tested.
- Replaced two stub tests in `tests/test_hound.py` (`test_unsupported_db`, `test_diagnose`) that were empty `pass` statements with `# TODO` comments — they now actually exercise `Hound`'s real error path and its real adapter-search-to-Diagnosis flow.

## [0.1.1] - 2025-01-20

### Added
- Component-level diagnostics for retrieval pipelines
- Root cause analysis for embedding failures
- Recommendations engine with ROI estimates
- Support for Elasticsearch, Weaviate, and Pinecone
- BM25 keyword search diagnostics
- Reranker performance analysis

### Fixed
- Memory efficiency improvements in large batch processing
- Vector similarity computation accuracy

## [0.1.0] - 2024-12-15

### Added
- Initial release
- Core retrieval diagnostics engine
- Embedding quality assessment
- Vector search performance profiling
- MIT license

### Known Issues
- Streaming RAG pipelines not yet supported
- LLamaIndex integration in progress

## [Unreleased]

### Planned
- Streaming RAG support
- LLamaIndex integration
- Custom metric definitions
- Dashboard UI
- API server mode

For details, see [ROADMAP.md](../ROADMAP.md).
