# Changelog

All notable changes to PyHound are documented in this file.

## [1.3.1] - Unreleased

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
