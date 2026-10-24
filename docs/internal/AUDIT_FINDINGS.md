# Audit findings — 2026-10-19

Scope: the pending roadmap items in `ROADMAP_HONEST.md` for BM25 and
reranker-calibration diagnostics. No other roadmap items were started.

## Roadmap item addressed

`ROADMAP_HONEST.md` previously listed **"BM25 (keyword search) and
reranker-calibration diagnostics: not implemented"** and reported `UNKNOWN`
for both. The honest gap was not a missing metric — it was that `Diagnosis`
had no way to accept the keyword/reranker output the caller already has.

## What changed

- `Diagnosis` now accepts:
  - `bm25_results` — ranked document ids from an external BM25/keyword search.
  - `bm25_scores` — doc id → BM25 score (ranking derived when results are absent).
  - `reranker_scores` — doc id → reranker score for the retrieved results.
- BM25 diagnostics compute precision, recall, MRR, and top-k agreement with the
  vector results against `expected_docs`.
- Reranker diagnostics compute NDCG@k and a score-separation calibration proxy
  (0.5 = no separation, 1.0 = perfect) against `expected_docs`.
- `Hound.diagnose()` and `Hound.diagnose_batch()` pass these inputs through.
- Both components still report `UNKNOWN` when the caller supplies no input; no
  fabricated verdicts were added.
- README, `ROADMAP_HONEST.md`, and `CHANGELOG.md` now describe the real
  capability and the remaining boundary: PyVectorHound still does not ship a
  BM25 index or reranker model.

## Verification

```
python3 -m pytest tests/test_diagnosis.py -q
# 29 passed, 1 failed
```

The one failure is
`TestEmbeddingAnalysis::test_uses_real_embeddings_not_hardcoded_placeholders`,
which requires the compiled `pyvectorhound._core` extension. The extension is
not built for the Python 3.9 interpreter used in this environment
(`ModuleNotFoundError: pyvectorhound._core`), so the embedding metrics return
their documented `UNKNOWN` path. This is an environment/build issue, not a
regression from this change.

The full suite also cannot collect `tests/test_okf_diagnostics.py` because the
optional `python-frontmatter` dependency is not installed in this environment.

## Remaining work / follow-ups

- Add measured BM25/reranker cases to the public example or user guide.
- Wire the new metrics into `RecommendationEngine` if it should emit
  keyword/reranker-specific recommendations (today `Diagnosis.recommendations()`
  handles this path).
- Build `_core` in CI for every supported Python version so the embedding tests
  do not silently depend on a developer's local build.
- The older dead-module/coverage/lint debt documented in `ROADMAP_HONEST.md`
  remains untouched.
