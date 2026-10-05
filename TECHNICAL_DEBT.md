# Complete Technical Debt Register — PyVectorHound

This repo already maintains an unusually thorough `ROADMAP_HONEST.md` from
prior audit passes (last dated 2026-09-22) with its own numbered items. This
register captures what THIS pass (2026-10-05) found and fixed, and
cross-references rather than duplicates `ROADMAP_HONEST.md`'s existing
content. See that file for the full pre-existing backlog (Dependabot PRs,
dead `server.py`/`web_dashboard.py`/`validation.py` modules, 185 ruff
findings, DEPLOYMENT.md accuracy, Python 3.8 support, etc.) — all of it
remains open and is not re-litigated here.

## Executive Summary (this pass only)

Total new items found: 3
Fixed: 2 (TD-0001, TD-0002)
Open: 1 (TD-0003, documentation-only, fixed as part of this pass — see below)

## P0 — Critical

| ID | Category | Description | Source | Status | Fix |
|---|---|---|---|---|---|
| TD-0001 | BUG | Stale untracked `_core.cpython-*.so` build artifacts in `pyvectorhound/` silently shadowed the correctly-installed package for any Python invocation with repo root as CWD, missing the newest `RetrievalRanker` bindings entirely (`AttributeError`) and risking silent use of outdated algorithm code for older functions | SOURCE_CODE (INFERRED) | RESOLVED | Deleted the two stale artifacts; documented the `maturin develop`-after-every-Rust-change requirement in CONTRIBUTING.md so it doesn't recur silently |

## P1 — High

| ID | Category | Description | Source | Status | Fix |
|---|---|---|---|---|---|
| TD-0002 | BUG | `RetrievalRanker::diversify()` returned results in pre-diversity selection order instead of sorted by the final diversity-adjusted score, contradicting its own doc comment and `ranking.py`'s docstring ("ordered by the final diversity-adjusted score"). A near-duplicate result selected early could end up with a lower adjusted score than a later, unpenalized result, yet still appear first in the output, with a `rank` field that didn't match the actual score order. Existing tests didn't catch this because they checked each document's score/diversity *value* via dict lookup, never the output list's *order*. | SOURCE_CODE (INFERRED) | RESOLVED | `src/retrieval_ranking.rs`: re-sort `diversified` by `relevance_score` descending and renumber `rank` 1..N after the greedy selection loop. Added `test_diversification_output_is_sorted_by_adjusted_score_not_selection_order` (Rust) and `test_output_order_reflects_diversity_adjusted_score_not_selection_order` (Python), both asserting on list order/rank, not just per-doc values |

## P2 — Medium

| ID | Category | Description | Source | Status | Fix |
|---|---|---|---|---|---|
| TD-0003 | DOCUMENTATION / DEVEX | `CONTRIBUTING.md`'s documented build workflow (`cargo build --release --all-features`) fails to link on macOS ("symbol(s) not found ... _Py_IsInitialized") — a standard PyO3 extension-module + macOS-linker interaction, not a real bug, and does not affect CI (runs on `ubuntu-latest`, where it succeeds). Confirmed pre-existing by reproducing against unmodified `origin/main` before any of this pass's changes. | INFERRED | RESOLVED | Rewrote the "Building from Source" section of `CONTRIBUTING.md`: lead with `cargo test`/`cargo clippy` (link fine on both platforms), added `maturin develop --release` as the correct way to refresh the Python-visible extension, and added an explicit macOS-note explaining the linker asymmetry so contributors don't mistake it for a bug |

## Explicit TODOs / Stubs / Partial Implementations / Planned Features / CI/Test/Dependency/Security/Architecture/Documentation Debt

All pre-existing and fully cataloged in `ROADMAP_HONEST.md` — not duplicated here. Notable items still open after this pass: dead `server.py`/`web_dashboard.py`/`validation.py` modules (undeclared Flask/FastAPI deps, zero tests); 185 `ruff` findings / 39-of-41 `black`-non-compliant files (deliberately not auto-fixed — large unrelated diff); 10 open Dependabot PRs including a non-trivial `pyo3`/`numpy` 0.23→0.29 migration; `cargo audit` never run (no network access in that prior session); `DEPLOYMENT.md` describes Docker/K8s artifacts that don't exist in the repo; Python 3.8 claimed but not in CI's test matrix.

## Resolved Historical Issues

See `ROADMAP_HONEST.md` "Bugs found and fixed in this pass" (2026-09-20/22 audits) and `CHANGELOG.md` for the full prior history — `error_messages.py`/`web_dashboard.py` syntax errors, stale `Proprietary` license string, `black` dependency ceiling, un-gitignored `Cargo.lock`, missing `dependabot.yml` cargo ecosystem, missing PR template, ~9 files of fabricated documentation, CLI `[project.scripts]` entry point, `[tool.ruff]` deprecated key — all previously fixed, not re-verified line-by-line in this pass beyond the spot-checks noted above (version strings, test counts, clippy/test status all reconfirmed current and accurate).
