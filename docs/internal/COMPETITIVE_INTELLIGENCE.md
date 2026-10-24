# Competitive intelligence in roadmap and upgrade work

**Policy date:** 2026-10-19

Competitive findings are an input to product decisions, not a one-off report.
Every pending roadmap item, new feature, and routine dependency upgrade should
check the repository's [`AUDIT_FINDINGS.md`](AUDIT_FINDINGS.md) before work
starts, and record the decision in the PR or changelog.

## Required check before building

1. **Read `AUDIT_FINDINGS.md`.** Find the relevant competitor row and the
   ranked next actions. If the finding is stale, update it with a dated source.
2. **Name the competitor and the user problem.** A feature is not justified by
   "competitor has it". State the workflow it unlocks, who needs it, and how
   often. Mark unverified demand as a hypothesis.
3. **Prefer reuse over new code.** Check whether an existing Mullassery repo
   already provides the capability (see `BUNDLES.md` in the profile repo and
   the bundle role file in this repo, when present). Typical reuse:
   - crawling/fetching/robots/SSRF → **MudFish**
   - architecture maps / PR diffs → **CodeAtlas**
   - data-quality contracts / validation → **StatGuardian**
   - token counting / cost tables → **PyTokenCalc**
   - dependency graph / advisories / SBOM → **PyDeepMesh**
   - segmentation / CLV / churn → **ClusterAudienceKit**
   - activation / lineage / PII → **PyReverseETL**
   - fleet state sync → **SyncFleet** (only after conflict resolution)
4. **Choose one disposition:** build, integrate, defer, or reject. Write it
   down. A rejection with a reason is a successful outcome.
5. **For routine upgrades**, check whether the upgrade closes a known
   competitor gap or breaks a differentiated capability. Run the tests that
   cover the affected path; do not merge a green build that silently changes a
   user-visible contract.

## PR / changelog checklist

- [ ] Competitor and source URL/date recorded (or "no direct competitor").
- [ ] User impact and frequency stated; unverified demand labelled.
- [ ] Reuse check done against sibling repos/bundles.
- [ ] Failure mode and rollback considered (especially auth, PII, cost).
- [ ] Docs/roadmap status updated honestly.
- [ ] Tests or a manual verification command included.

## Review cadence

- Refresh the competitor row when a release changes the capability.
- Re-check the full `AUDIT_FINDINGS.md` at least quarterly and before a major
  release.
- If a finding is wrong or stale, correct it in the same PR that relies on it.

## Non-goals

- Copying features for parity.
- Adding a dependency just because a competitor uses it.
- Treating star counts or download counts as proof of user need.

## OSS gap analysis — 2026-10-24

**What matters most here:** answer-layer evaluation and real judges. Stopping at retrieval means teams still need Ragas/TruLens, and a bare judge callback makes faithfulness depend on user code; add generation metrics and bundled judge providers.

Scope: Compared PyVectorHound's retrieval-stage diagnostics against four LLM/RAG evaluation frameworks, focusing on whether a team debugging bad retrieval would choose a diagnostic tool or a full eval platform.

### Comparable OSS projects
| Project | GitHub | License | Last activity | Why it is the comparison |
| --- | --- | --- | --- | --- |
| Ragas | https://github.com/vibrantlabsai/ragas | Apache-2.0 | v0.4.3, 2026-01-13 | Standard RAG metric suite; the project we benchmark against in our README |
| TruLens | https://github.com/truera/trulens | MIT | 2.16.0, 2026-10-19 | RAG triad + tracing + judge ensembles; overlaps diagnostics and observability |
| Arize Phoenix | https://github.com/Arize-ai/phoenix | Elastic License 2.0 | evals 3.9.4, 2026-10-24 | Retrieval evals + tracing + experiments in one platform |
| DeepEval | https://github.com/confident-ai/deepeval | Apache-2.0 | 4.3.1, 2026-10-17 | Pytest-native LLM eval with RAG metrics and test generation |

### Capability comparison
| Capability | Ours | Ragas | TruLens | Phoenix | DeepEval | Gap |
| --- | --- | --- | --- | --- | --- | --- |
| Retrieval precision/recall/MRR | Yes | Partial | Partial | Partial | Partial | Ahead |
| Embedding-space diagnostics | Yes | No | No | No | No | Ahead |
| BM25/keyword diagnostics | Yes | No | No | No | No | Ahead |
| Reranker NDCG + calibration | Yes | No | Partial | No | Partial | Ahead |
| LLM-judge faithfulness | Partial | Yes | Yes | Yes | Yes | Moderate |
| Answer/generation evaluation | No | Yes | Yes | Yes | Yes | Large |
| Synthetic test-set generation | Partial | Yes | Partial | Yes | Yes | Moderate |
| Tracing / eval UI / datasets | Partial | No | Yes | Yes | Partial | Large |
| Drift vs historical baseline | Yes | No | Partial | Partial | No | Ahead |
| Vector DB adapters | Yes | Partial | Partial | Partial | Partial | Ahead |
| int8 local vector store | Yes | No | No | No | No | Ahead |
| CI/pytest gating | Partial | Partial | Partial | Partial | Yes | Moderate |
| Install coverage (PyPI wheels) | Partial | Yes | Yes | Yes | Yes | Moderate |

Nuance: "Ours" is a diagnostic layer over results you already have, not a generator of answers, so the generation-eval column is a deliberate scope boundary rather than an oversight. Our LLM-judge path requires a caller-supplied `llm_judge_fn`; Ragas, TruLens, Phoenix, and DeepEval ship judge abstractions and provider integrations. Phoenix is ELv2, which restricts hosted-service use — a licensing opening for us, but not a capability one. Our own README benchmark already shows document-identity ground truth is brittle when the right answer appears in a different chunk.

### Gaps that matter (ranked)
1. **No answer/generation-layer evaluation** — Ragas, TruLens, Phoenix, and DeepEval all judge the generated answer against retrieved context; we stop at retrieval, so a team cannot use us as its only RAG eval. This is a missing capability, not a weaker one. Effort L to build, S to integrate.
2. **Judge support is a bare callback** — no bundled judge prompts, model providers, multi-judge ensembles, or score calibration; TruLens ships `Jury`/A-B judge testing and the others ship provider wrappers. Our faithfulness numbers therefore depend entirely on user code. Effort M.
3. **Test-set generation depends on Ragas** — `generate_testset` needs a caller-supplied generator and `[ragas]`; Ragas and DeepEval generate synthetic Q/A/context sets natively. This weakens the "no dataset? start here" workflow. Effort M.
4. **No persistent eval store or UI** — Phoenix and TruLens provide datasets, experiments, trace trees, and dashboards; our tracer/replayer and OTel hooks emit data but we own no store or comparison UI. Effort L, or integrate.
5. **Ground truth is document-identity based** — `expected_docs` marks whole documents relevant, so correct answers in other chunks count as failures (documented in our own Ragas comparison). Chunk-level or LLM-judged relevance would fix this. Effort M.
6. **Only a CPython 3.9 macOS arm64 wheel on PyPI** — README discloses this while every competitor installs broadly; a CI user on Linux cannot adopt us without a Rust toolchain. Effort S.

### Where we are differentiated
- Stage isolation: embedding-space vs vector-search vs BM25 vs reranker vs faithfulness, each reported separately with an explicit `UNKNOWN` instead of a fabricated score.
- Embedding-space metrics (isotropy, coverage, distinctiveness) computed from real per-document vectors — none of the eval frameworks expose this.
- Diagnoses externally produced BM25 and reranker output without shipping an index or model, which fits teams that already run hybrid search.
- Per-customer baseline drift detection and an opt-in int8 vector store, both absent from the comparables.

### Disposition
- **Build:** chunk/answer-level relevance and a first-class judge abstraction (provider adapters, prompt templates, multi-judge voting).
- **Integrate/reuse:** Ragas for synthetic test-set generation and Phoenix/OpenTelemetry for trace storage and UI; do not build a dashboard.
- **Defer/reject:** full generation-layer evaluation and a hosted eval platform; keep the product a retrieval-diagnosis layer that hands off to those tools.

### Sources
- https://github.com/vibrantlabsai/ragas (accessed 2026-10-24)
- https://github.com/truera/trulens (accessed 2026-10-24)
- https://github.com/Arize-ai/phoenix (accessed 2026-10-24)
- https://github.com/confident-ai/deepeval (accessed 2026-10-24)
- Repo files inspected: `README.md`, `COMPETITIVE_INTELLIGENCE.md`, `AUDIT_FINDINGS.md`, `docs/ARCHITECTURE.md`, `pyproject.toml`, `Cargo.toml`, `pyvectorhound/diagnosis.py`
