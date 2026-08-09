# Changelog

All notable changes to PyHound are documented in this file.

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
