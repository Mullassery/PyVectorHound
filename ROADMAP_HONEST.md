# PyVectorHound: Honest Status & Roadmap

Last audited: 2026-09-20. This document states plainly what works, what's
broken, what's untested, and what's simply not built. No hedging language
("planned", "may be added") is used for things that are just missing —
those are stated as missing.

## What actually works (tested by this audit)

- **Rust core** (`src/`, ~1,105 lines): `cargo build --release
  --all-features` succeeds; `cargo test --release --all-features` passes
  17/17; `cargo fmt --check` is clean; `cargo clippy --release
  --all-features` reports no warnings. Isotropy/coverage/distinctiveness
  metrics, drift detection, retrieval precision/recall/MRR, quality
  score, and int8 scalar quantization are real, tested code.
- **Python package** (~9,800 lines across ~30 modules): `pip install
  ".[dev]"` succeeds (via `maturin`/PyO3, not editable-installable —
  `pip install -e .` fails, use a plain `pip install .`). `pytest tests/`
  passes 174/174 across 10 test files.
- **int8 scalar quantization** (`src/quantization.rs`): real, 4x memory
  reduction vs f32, measured max reconstruction error ~0.0039 vs the
  theoretical 8-bit bound ~0.0078.
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
- **BM25 (keyword search) and reranker diagnostics**: not implemented.
  `Diagnosis` reports `"UNKNOWN"` for these rather than a fabricated
  number — this is honest, working-as-designed behavior, not a bug.
- **`RetrievalRanker`** (`src/retrieval_ranking.rs`, 280 lines, compiled
  into `_core`): the Rust code exists and has unit tests, but is **not
  exposed as a callable Python function** — `src/lib.rs`'s `#[pymodule]`
  block never wraps or registers it. It is unreachable from Python today.
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

1. **Two entire modules are dead code with undeclared dependencies.**
   - `pyvectorhound/server.py` (86 statements): a Flask REST API wrapper.
     `from flask import Flask` (line ~170) but `flask` is **not declared
     anywhere in `pyproject.toml`** — installing `pyvectorhound[all]`
     will not get you Flask, and this module will `ImportError` for
     anyone who tries to use it. Zero tests, zero references from
     `examples/`, `README.md`, or `USER_GUIDE.md`.
   - `pyvectorhound/web_dashboard.py` (501 lines): its own footer HTML
     says "Powered by FastAPI", but `fastapi` is likewise **not declared
     anywhere in `pyproject.toml`**. Zero tests, zero references
     elsewhere in the repo.
   - Fix requires a decision: either declare `flask`/`fastapi` as real
     optional-dependency extras and write tests, or delete both modules
     as unshipped/unmaintained. Currently they are neither — shipped but
     unusable and unverified.

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

3. **`cargo clippy`/`cargo fmt`/`ruff`/`black`/`mypy` are configured in
   `pyproject.toml` but not run in CI at all.** `.github/workflows/ci.yml`
   only runs `cargo build`, `cargo test`, and `pytest`. Confirmed by
   direct run in this audit:
   - `ruff check .` → **185 errors** (50 line-too-long, 43 unused-import,
     40 blank-line-with-whitespace, 31 unsorted-imports, plus smaller
     categories). 108 are auto-fixable with `ruff check . --fix`.
   - `black --check pyvectorhound/ tests/` → **39 of 41 files** would be
     reformatted.
   - `pyproject.toml`'s `[tool.ruff]` section uses the deprecated
     top-level `select` key instead of `[tool.ruff.lint] select`; current
     `ruff` versions emit a deprecation warning on every invocation.
   None of this is enforced, so it will keep drifting. A dedicated pass
   should either wire these into CI or drop the dead config.

4. **`cli.py` has a real, working `main()`/argparse CLI (326 lines) but
   is not installable as a command.** There is no `[project.scripts]`
   entry in `pyproject.toml`. The only way to invoke it is `python -m
   pyvectorhound.cli`, which is undocumented anywhere in
   `README.md`/`USER_GUIDE.md`. Needs a `[project.scripts]` entry plus
   verification the CLI still works end-to-end, and a version bump since
   it changes the installed package's public surface.

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

6. **8 open Dependabot branches sitting unmerged on the remote** (as of
   this audit): `dependabot/cargo/numpy-0.29`,
   `dependabot/cargo/pyo3-0.29`,
   `dependabot/github_actions/actions/checkout-7`,
   `dependabot/github_actions/actions/setup-python-7`,
   `dependabot/pip/chromadb-1.5.9`, `dependabot/pip/mypy-2.3.0`,
   `dependabot/pip/pytest-cov-7.1.0`,
   `dependabot/pip/pytest-gte-7.0-and-lt-10`,
   `dependabot/pip/weaviate-client-gte-3.24-and-lt-5`. Two of these
   (`checkout-7`, `setup-python-7`) would fix the CI workflow using
   outdated `actions/checkout@v4`/`actions/setup-python@v4`. The
   `pyo3-0.29`/`numpy-0.29` bumps are non-trivial: `Cargo.toml` pins
   `pyo3 = "0.23"` / `numpy = "0.23"`, and jumping to 0.29 is a real PyO3
   API migration (multiple breaking changes across that version range),
   not a drop-in bump — needs a dedicated session to validate.
   Dependabot itself is correctly configured and finding real gaps; the
   gap is that nobody has been merging its PRs.

7. **`cargo audit` could not be run** in this sandbox (no network access
   to `https://github.com/RustSec/advisory-db.git`). The Rust dependency
   tree (`pyo3 0.23`, `numpy 0.23`, `serde 1.0`, `serde_json 1.0`) has
   not been checked against RustSec advisories. Should be run with
   network access before the next release.

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

10. **Python 3.8 support is claimed but never tested.**
    `pyproject.toml`: `requires-python = ">=3.8"` and a `Python :: 3.8`
    classifier, but `.github/workflows/ci.yml`'s test matrix is `["3.9",
    "3.10", "3.11", "3.12"]` — 3.8 has never run in CI. Given
    `python-frontmatter` was already capped below 1.2.0 specifically "to
    restore Python 3.9 support" (see CHANGELOG 1.x history), 3.8 support
    should be considered unverified, not guaranteed, until it's actually
    added to the CI matrix or the floor is honestly raised to 3.9.

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

## Things deliberately left alone in this pass

- **185 `ruff` findings and 39/41 `black`-non-compliant files**: not
  auto-fixed. Running `ruff check . --fix` / `black .` now would produce
  a large, hard-to-review diff across most of the codebase, unrelated to
  this documentation-focused pass. Left for a dedicated cleanup session
  (see Technical Debt #3).
- **`server.py` / `web_dashboard.py` undeclared-dependency dead code**:
  not deleted, not given tests, not given real `pyproject.toml` extras.
  Needs a maintainer decision on whether these are worth keeping (see
  Technical Debt #1).
- **`RetrievalRanker` Python bindings**: not added. Wiring
  `src/retrieval_ranking.rs` into `src/lib.rs`'s `#[pymodule]` and giving
  it a Python-facing API is a real feature addition, not a docs fix.
- **`cli.py` packaging** (`[project.scripts]`): not added, since it
  changes the installed package's public interface and needs end-to-end
  verification + a version bump, not a silent addition in a docs pass.
- **Merging any of the 8 open Dependabot PRs**: left for the maintainer;
  two are simple version bumps, two (pyo3/numpy to 0.29) require real
  API migration work.
