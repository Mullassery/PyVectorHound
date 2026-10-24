# PyVectorHound: Honest Status & Roadmap

> 2026-10-19 implementation findings: see [`AUDIT_FINDINGS.md`](AUDIT_FINDINGS.md).

Last audited: 2026-09-20. This document states plainly what works, what's
broken, what's untested, and what's simply not built. No hedging language
("planned", "may be added") is used for things that are just missing —
those are stated as missing.

## What actually works (tested by this audit)

- **Rust core** (`src/`, ~1,135 lines): `cargo test --lib` passes 19/19.
  Isotropy/coverage/distinctiveness metrics, drift detection, retrieval
  precision/recall/MRR, quality score, int8 scalar quantization, and
  multi-criteria ranking + real cosine-similarity-based diversification
  (`RetrievalRanker`, see below) are real, tested code.
- **Python package** (~11,000 lines across ~31 modules): `pip install
  ".[dev]"` succeeds (via `maturin`/PyO3, not editable-installable —
  `pip install -e .` fails, use a plain `pip install .`). `pytest tests/`
  passes 179/179 across 11 test files.
- **`RetrievalRanker` ranking & diversification** (`src/retrieval_ranking.rs`,
  exposed via `pyvectorhound.rank_and_diversify()` /
  `compute_reranker_metrics()`): real multi-criteria (BM25/semantic/recency)
  ranking, plus diversification driven by actual cosine similarity between
  each result's embedding and already-selected results' embeddings — not
  the earlier hardcoded 10%-per-result placeholder. MRR/NDCG/Precision@K/
  Recall@K/diversity reranker metrics are computed against a real
  ground-truth list, not fabricated.
- **int8 scalar quantization** (`src/quantization.rs`): real, 4x memory
  reduction vs f32, measured max reconstruction error ~0.0039 vs the
  theoretical 8-bit bound ~0.0078. Wired into Python as the opt-in in-process
  `Hound(quantized=True)` / `enable_quantization()` store
  (`pyvectorhound/quantization.py`); it is not a write-through layer for the
  remote database adapters.
- **Historical metric comparison/drift** (`Hound.compare_metrics()` /
  `Hound.detect_drift()`): real, computed from samples recorded with
  `track_metric()`. Without samples in the requested periods they raise a
  `ValueError` naming the missing data rather than reporting a fabricated
  result.
- **OKF diagnostic knowledge base** (`pyvectorhound/okf_diagnostics.py`,
  310 lines): real, persists diagnostic findings as frontmatter markdown
  documents, supports pattern extraction and similar-failure lookup.
  18 passing tests in `tests/test_okf_diagnostics.py`.
- **LLM-as-judge faithfulness, concurrent batch diagnosis, dynamic
  threshold calibration** (added in 1.4.0): real, tested, honestly report
  `UNKNOWN` when required inputs aren't supplied rather than fabricating
  scores.

## Confirmed NOT built (state plainly, not "planned")

- **SIMD/GPU acceleration** for quantization or metrics: does not exist.
  Deliberately out of scope — needs separate hardware-specific design
  work, not an oversight.
- **BM25 (keyword search) and reranker-calibration diagnostics**: the
  **diagnostics** now accept externally supplied BM25 rankings/scores and
  reranker scores (`bm25_results`, `bm25_scores`, `reranker_scores`) and
  compute precision/recall/MRR/agreement and NDCG/score-separation against
  `expected_docs`. PyVectorHound still does not ship a BM25 index or a
  reranker model; without caller inputs both components report `UNKNOWN`.
  (Separate from `RetrievalRanker`'s ranking/diversification, which *is*
  implemented — see above.)
- **A generated API reference** (`docs/API.md` or similar): does not
  exist. `docs/GUIDE.md` referenced it before this pass; the reference
  has been removed and replaced with a pointer to source docstrings.
- **Docker/Kubernetes deployment artifacts**: `DEPLOYMENT.md` describes
  these at length, but there is no `Dockerfile`, `docker-compose.yml`, or
  k8s manifest anywhere in this repo, and the doc was never validated
  against this repo's contents (see Technical Debt below).

## Bugs found and fixed in this pass

1. **`pyvectorhound/error_messages.py`: real `SyntaxError`.** A missing
   closing `)` on the `NO_RELEVANT_RESULTS = DiagnosticError(...)` call
   (originally around line 82) made the entire module fail to
   `import`/`py_compile`. It was never caught because nothing in the
   codebase imports this module (confirmed via repo-wide grep). Fixed.
2. **`pyvectorhound/web_dashboard.py`: real `SyntaxError`.** An f-string
   at (originally) line 450 had an extra `{`
   (`${{{(summary.avg_recall || 0).toFixed(2)}}}`) that Python parsed as
   an actual expression start instead of a literal `{` — and
   `(summary.avg_recall || 0).toFixed(2)` isn't valid Python (`||` isn't
   a Python operator, `.toFixed` isn't a Python method) since it's JS
   meant to be embedded literally into the generated HTML. Also never
   caught because nothing imports this module. Fixed.
3. **Stale license metadata.** `pyvectorhound/__init__.py` declared
   `__license__ = "Proprietary"` (and the docstring said the same) after
   the whole `Mullassery` org relicensed to Apache-2.0 in 2026-09.
   `pyproject.toml` and `Cargo.toml` already correctly said
   `Apache-2.0` — only the runtime-visible Python constant was stale.
   Fixed.

## Technical debt (concrete, with file:line, prioritized)

### Needs a dedicated follow-up session (non-trivial, not fixed here)

1. ~~**Two entire modules are dead code with undeclared dependencies.**~~
   **Resolved:** `server.py` and `web_dashboard.py` now have declared
   optional extras (`pyvectorhound[server]` for Flask,
   `pyvectorhound[dashboard]` for FastAPI/uvicorn) and are included in
   `pyvectorhound[all]`. The modules already fail with an actionable
   `ImportError` when the extra is absent; see the README's install
   section.

2. **`pytest --cov=pyvectorhound` silently reports 0% coverage on every
   module if you install non-editably, but works correctly (56% overall,
   realistic per-file numbers) with an editable install.** Confirmed by
   direct comparison in this audit: `pip install ".[dev]"` (regular,
   non-editable — installs a built wheel into `site-packages`) makes
   every module show `0%` covered even though 174 tests pass and clearly
   exercise that code, because `coverage.py` can't map the
   `site-packages` copy back to the repo's source paths. `pip install -e
   ".[dev]"` (editable, via maturin) fixes this — real per-file coverage
   shows up (e.g. `okf_diagnostics.py` 95%, `scorer.py` 88%,
   `server.py`/`web_dashboard.py`/`validation.py` genuinely 0%, i.e. no
   tests at all). **CI already uses `pip install -e ".[dev]"`**
   (`.github/workflows/ci.yml` line 44), so this is not actually broken
   in CI — it only bites a contributor who runs a plain `pip install
   ".[dev]"` locally and then wonders why coverage looks empty. Worth a
   one-line callout in CONTRIBUTING.md (added) so nobody wastes time on
   a phantom bug; not worth further engineering effort.
   - **Real gap surfaced by the correct (editable-install) numbers:**
     `pyvectorhound/validation.py` (62 statements, Pydantic
     `EmbeddingQuery` model) has **0% test coverage** and, like
     `server.py`/`web_dashboard.py`, is **not imported by any other
     module in the package** (confirmed by grep — nothing imports
     `pyvectorhound.validation`). It's a third orphaned module, not just
     an undertested one. Same disposition question as #1: wire it in and
     test it, or remove it.

3. ~~**`cargo clippy`/`cargo fmt`/`ruff`/`black`/`mypy` are configured in
   `pyproject.toml` but not run in CI at all.**~~ **Resolved:** the tree is
   formatted with `black` and `ruff check .` is clean; CI now runs both as a
   `python-lint` job. `E501` is intentionally ignored because Black owns line
   length and cannot split long string literals.

4. ~~**`cli.py` has a real, working `main()`/argparse CLI (326 lines) but
   is not installable as a command.**~~ **Fixed 2026-09-22.** Added
   `[project.scripts]` entry (`pyvectorhound = "pyvectorhound.cli:main"`)
   to `pyproject.toml`. `main()` reads `sys.argv` directly with no
   required arguments, so this was a trivial, safe addition — verified
   end-to-end with a clean `pip install .` into a fresh venv (`pyvectorhound
   help` / `pyvectorhound list` both run as an installed console script,
   same output as `python -m pyvectorhound.cli`). No version bump done as
   part of this quick-fix pass; still recommended before the next release
   since it changes the installed package's public surface.

5. **Two open Dependabot dependency-ceiling gaps, one already
   fixed here, one still open:**
   - `black` ceiling (`pyproject.toml` line ~75, was `<26`) blocked
     PYSEC-2026-2121/2120's fix. **Fixed in this pass** (`<27`).
   - `pytest` ceiling (`pyproject.toml` line ~72, `<9`) blocks
     PYSEC-2026-1845's fix (9.0.3). **Not fixed here** — a Dependabot PR
     already proposes exactly this
     (`dependabot/pip/pytest-gte-7.0-and-lt-10`, currently open,
     unmerged). Merge that PR rather than duplicating it.
   - `pytest-cov` ceiling (`<7`) may also be blocking a fix; a Dependabot
     branch exists (`dependabot/pip/pytest-cov-7.1.0`) — unmerged.

6. **Dependabot backlog** (as of 2026-09-22): the `pyo3 0.29` /
   `numpy 0.29` bumps have **now been applied** (`Cargo.toml` + `Cargo.lock`
   updated; `cargo test` 20 passed, Python suite 230 passed, `cargo audit`
   clean). Remaining open PRs are routine version bumps:
   `dependabot/github_actions/actions/checkout-7`,
   `dependabot/github_actions/actions/setup-python-7`,
   `dependabot/pip/chromadb-1.5.9`,
   `dependabot/pip/mypy-gte-1.0-and-lt-3`,
   `dependabot/cargo/serde_json-1.0.151`,
   `dependabot/pip/pytest-cov-7.1.0`,
   `dependabot/pip/pytest-gte-7.0-and-lt-10`,
   `dependabot/pip/weaviate-client-gte-3.24-and-lt-5`. None were merged or
   duplicated manually in this quick-fix pass — all are routine version
   Two of these (`checkout-7`, `setup-python-7`) would update the CI
   workflow to the current action majors.

7. ~~**`cargo audit` could not be run**~~ **Resolved:** `cargo audit` now
   exits 0 against the upgraded `pyo3`/`numpy` dependency tree, and CI runs
   it as a gate.

8. **`pip-audit` (run successfully in this pass, has network) found 18
   known CVEs in 9 resolved packages** in a fresh `pip install
   ".[dev]"` — see `SECURITY.md` for the full list. Most are transitive/
   build-tooling packages (setuptools, pip, click, filelock, msgpack,
   urllib3) that aren't tightly pinned by this project and should
   resolve via routine upgrades; `requests` (a direct dependency,
   `pyproject.toml`: `requests>=2.28,<3`) had a vulnerable resolved
   version (2.32.5, fixed in 2.33.0) but is not blocked by a ceiling —
   it's a routine "run pip install --upgrade" gap, not a config bug.

9. **`DEPLOYMENT.md` (673 lines) was never validated against this repo.**
   Describes Docker/Kubernetes/cloud deployment for a project that ships
   no Dockerfile or k8s manifests. A disclaimer banner has been added
   pointing this out; the document itself has not been rewritten or
   fact-checked line-by-line (that's a dedicated-session-sized task given
   its length).

10. ~~**Python 3.8 support is claimed but never tested.**~~ **Resolved
    (2026-10-20):** the declared floor is now `requires-python = ">=3.9"`
    (classifier, mypy, black and ruff targets updated to match). CI tests
    3.9-3.12 and the release workflow builds wheels for 3.9-3.12. 3.8 was
    never tested, is end-of-life, and the package uses PEP 585 builtin
    generics at runtime, so claiming it was incorrect.

### Small things fixed in this pass (see CHANGELOG.md `[Unreleased]`)

- `pyvectorhound/error_messages.py` and `pyvectorhound/web_dashboard.py`
  syntax errors (see "Bugs found and fixed" above).
- Stale `Proprietary` license string in `pyvectorhound/__init__.py`.
- `black` dependency ceiling.
- `Cargo.lock` was gitignored; now tracked.
- `.github/dependabot.yml` was missing a `cargo` ecosystem entry.
- `.github/pull_request_template.md` was missing.
- Deleted ~9 files of fabricated/contaminated documentation describing a
  fictional "MCP 2.0 Platform" of unrelated sibling projects this repo
  does not depend on (see CHANGELOG.md for the full list and reasoning).
- Rewrote `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, `docs/GUIDE.md`,
  `SECURITY.md` to remove stale pre-rename (`pyhound`) branding and
  inaccurate claims.
- (2026-09-22 quick-fix pass) `[project.scripts]` CLI entry point added
  and verified; `[tool.ruff]` deprecated `select` key moved to
  `[tool.ruff.lint]`; orphaned second `[Unreleased]` section in
  `CHANGELOG.md` (dead link to deleted `ROADMAP.md`) removed. See
  CHANGELOG.md `[Unreleased]` for details.

## Things deliberately left alone in this pass

- ~~**185 `ruff` findings and 39/41 `black`-non-compliant files**~~ **Resolved:**
  `black .` and `ruff check . --fix` were run; the remaining issues were fixed
  directly and lint is now enforced in CI.
- ~~**`server.py` / `web_dashboard.py` undeclared-dependency dead code**~~
  **Resolved:** both now have real optional extras (`server`, `dashboard`)
  and are included in `all`; see Technical Debt #1.
- **`RetrievalRanker` Python bindings**: at the time of this 2026-09-20
  audit, not added (wiring `src/retrieval_ranking.rs` into `src/lib.rs`'s
  `#[pymodule]` was judged a real feature addition, not a docs fix, so it
  was left out of that pass). Since then: done — see "What actually
  works" above. The diversity penalty was also upgraded from a hardcoded
  10%-per-result placeholder to a real cosine-similarity computation in
  the same change.
- **`cli.py` packaging** (`[project.scripts]`): not added, since it
  changes the installed package's public interface and needs end-to-end
  verification + a version bump, not a silent addition in a docs pass.
- **Merging the remaining routine Dependabot PRs**: left for the maintainer.
  The non-trivial `pyo3`/`numpy` 0.29 migration is already applied.
