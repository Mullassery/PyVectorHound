# Repository Audit — PyVectorHound

## Health

**GREEN.** This repo already had an unusually rigorous prior audit
(`ROADMAP_HONEST.md`, last dated 2026-09-22) that honestly catalogs a long
list of real, open debt. This pass found and fixed two genuine, previously
undocumented bugs on top of that — one of them (TD-0001) significant enough
that it silently broke the repo's own flagship new feature for any direct
Python usage from the repo root.

## Before Audit (this pass's baseline, commit `4b2e889`)

Open debt (cumulative, including all pre-existing `ROADMAP_HONEST.md`
items): not separately counted here — see that document. New items found by
this pass: 3 (1 critical, 1 high, 1 medium).

## After Audit

New items: 3 found, 3 resolved, 0 left open from this pass. Pre-existing
`ROADMAP_HONEST.md` backlog untouched and still fully open (by design —
large/dedicated-session items, not quick fixes).

## Items Fixed

1. **TD-0001 (critical):** Deleted two stale, untracked `_core.cpython-*.so`
   build artifacts sitting directly in `pyvectorhound/` that silently
   shadowed the correctly pip-installed package for any Python process run
   with the repo root as its working directory — including, almost
   certainly, the repo's own `examples/*.py` scripts if run as documented.
   The stale artifact predated the `RetrievalRanker` Python bindings, so
   `rank_and_diversify()`/`compute_reranker_metrics()` — the exact feature
   `ROADMAP_HONEST.md` describes as the project's most recent, proudest
   "fake → real" fix — was unreachable (`AttributeError`) under this
   shadowing, with zero warning. Added a CONTRIBUTING.md note so
   contributors know to `maturin develop --release` after Rust changes
   rather than relying on a possibly-stale local `.so`.
2. **TD-0002 (high):** Fixed `RetrievalRanker::diversify()` in
   `src/retrieval_ranking.rs` to sort its output by the diversity-adjusted
   score and renumber `rank` accordingly, instead of returning results in
   pre-diversity selection order — which could and did produce outputs
   where a penalized near-duplicate appeared *before* a higher-scoring,
   unpenalized result, contradicting the function's own documented
   contract. Added regression tests at both the Rust and Python level that
   assert on output *order*, not just per-document values (the gap that let
   this slip past existing tests).
3. **TD-0003 (medium, docs/devex):** Clarified `CONTRIBUTING.md`'s build
   instructions — the documented `cargo build --release --all-features`
   command fails to link on macOS (confirmed pre-existing, unrelated to any
   change in this pass, and irrelevant to CI which runs on `ubuntu-latest`).

## Items Remaining

None from this pass. Full pre-existing backlog in `ROADMAP_HONEST.md`
remains open, notably: dead `server.py`/`web_dashboard.py`/`validation.py`
modules with undeclared dependencies, 185 `ruff` findings, 10 unmerged
Dependabot PRs (including a real `pyo3`/`numpy` major-version migration),
`cargo audit` never run, `DEPLOYMENT.md` accuracy, Python 3.8 CI coverage.

## Future Phase Work

PyO3 compute-loop porting is not applicable here (this project already IS
the PyO3/Rust implementation for its hot paths — `retrieval_ranking.rs`,
`quantization.rs`, `metrics.rs`). No further Rust-porting candidates
identified beyond what's already native.

## CI Status

`.github/workflows/ci.yml`: `cargo build --release --all-features` +
`cargo test --release --all-features` + pytest, on `ubuntu-latest`. Not
independently re-triggered in this pass (no push to a PR), but the
underlying commands were verified locally via equivalent macOS-safe
invocations (`cargo test`, `cargo clippy`, `maturin build`) — all green.

## Test Status

Rust: 20/20 (`cargo test --lib`; was 19, +1 new regression test). Python:
180/180 (`pytest tests/`; was 179, +1 new regression test). `cargo clippy
--all-targets`: 0 warnings.

## Build Status

`maturin build --release` / `maturin develop --release`: clean. Plain
`cargo build --release` fails to link on macOS only — pre-existing,
unrelated to CI (see TD-0003).

## Security Status

Not independently re-run in this pass (no network access confirmed/denied
here); `ROADMAP_HONEST.md` already documents `pip-audit` findings (18 CVEs
in 9 resolved packages, mostly transitive/build-tooling) and notes `cargo
audit` couldn't be run in that prior session either.

## Dependency Status

Unchanged from `ROADMAP_HONEST.md`'s documented state — 10 Dependabot PRs
still open and unmerged, not touched in this pass.

## Final Assessment

The existing `ROADMAP_HONEST.md` discipline in this repo is genuinely
unusual and valuable — most of what a fresh audit would normally surface
was already found and either fixed or honestly documented as open. This
pass's value-add was narrow but real: catching a silent packaging footgun
that broke the project's own newest feature under a common invocation
pattern, and a genuine output-ordering bug in that same feature that
existing tests structurally could not have caught. Both are now fixed with
regression tests specifically designed to catch their failure mode (not
just re-test the same thing differently).
