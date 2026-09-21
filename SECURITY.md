# Security Policy

## Reporting Security Issues

**DO NOT** open public GitHub issues for security vulnerabilities.

If you discover a security vulnerability, please email: **mullassery@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if you have one)

## Current status (as of 2026-09-20, version 1.5.0)

- This is a small, young open-source project. There has been no formal
  external security audit. `PRODUCTION_AUDIT_REPORT.md`, referenced by an
  earlier version of this file, does not exist in this repository — that
  reference was stale and has been removed.
- No SOC 2 / HIPAA / GDPR / PCI DSS / ISO 27001 certification, and none is
  planned. If your use case requires one of these, PyVectorHound does not
  meet it.
- Supported Python: CI (`.github/workflows/ci.yml`) tests 3.9, 3.10, 3.11,
  3.12. `pyproject.toml` declares `requires-python = ">=3.8"` and lists a
  `Python :: 3.8` classifier, but 3.8 is never actually tested in CI —
  treat 3.8 support as unverified, not guaranteed.
- Rust toolchain: pinned to 1.97 via `rust-toolchain.toml`.

## Known dependency vulnerabilities (found via `pip-audit`, 2026-09-20)

Running `pip-audit` against a fresh `pip install ".[dev]"` found 18 known
CVEs across 9 packages in the resolved dependency tree. Two are
structurally relevant to this repo (a version ceiling in `pyproject.toml`
prevented the fix from ever being installed, even by Dependabot):

- **`black`** — `pyproject.toml`'s dev-dependency ceiling was `<26`,
  which blocked the fix for PYSEC-2026-2121/PYSEC-2026-2120 (fixed in
  26.3.0+). Raised to `<27` in this pass. Note: `black` 26.x requires
  Python >=3.10, so this only takes effect for contributors on 3.10+;
  on 3.9 `pip` will still resolve 25.11.0.
- **`pytest`** — ceiling was `<9`, blocking the fix for PYSEC-2026-1845
  (fixed in 9.0.3+). A Dependabot PR (`dependabot/pip/pytest-gte-7.0-and-lt-10`)
  already proposes exactly this change upstream; it has not been merged.

The rest (`click`, `filelock`, `msgpack`, `pip`, `requests`, `setuptools`,
`urllib3`) are transitive or build-tooling dependencies not directly
pinned by this project narrowly enough to have caused the vulnerable
version; routine `pip install --upgrade` / Dependabot merges should
resolve them. `cargo audit` could not be run in this environment (no
network access to the RustSec advisory database) — this has not been
checked for the Rust dependency tree (`pyo3`, `numpy`, `serde`,
`serde_json` in `Cargo.toml`) and should be run with network access
before a release.

See `ROADMAP_HONEST.md` for the full technical debt list, including
several currently-open, unmerged Dependabot PRs.

## Security Updates

Security patches will be released as minor/patch versions when
vulnerabilities are discovered. There is no current CVE tracking process
beyond this document and Dependabot alerts.

## Development Security

When contributing:
- Do not commit secrets, credentials, or API keys
- Use environment variables for sensitive configuration
- `ruff check .` and `cargo clippy` are configured but **not enforced in
  CI** (`.github/workflows/ci.yml` only runs `cargo build`/`cargo test`/
  `pytest`) — running them locally before a PR is on you, not gated
- Write tests for security-related code

## Questions?

For security questions (non-vulnerability): open a GitHub Discussion.
