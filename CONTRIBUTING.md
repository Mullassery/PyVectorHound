# Contributing to PyVectorHound

Thank you for considering contributing to PyVectorHound! We welcome contributions of all kinds.

## Getting Started

### Prerequisites
- Python 3.9+ (the package declares `>=3.8` in `pyproject.toml`, but CI only tests 3.9-3.12 — 3.8 is unverified, see ROADMAP_HONEST.md)
- Rust 1.97 (pinned in `rust-toolchain.toml`)
- pip or uv

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Mullassery/PyVectorHound.git
cd PyVectorHound

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install ".[dev]"
```

Note: this project builds a native Rust extension via `maturin`/PyO3. A
modern `pip` (verified with 26.0.1) can do `pip install -e ".[dev]"` for
an editable install; you'll still need to re-run it (or `maturin develop
--release`) after Rust source changes, since editable-install for a
compiled extension only skips the Python-side rebuild, not the Rust
build. On macOS you may need:

```bash
RUSTFLAGS="-C link-args=-undefined -C link-args=dynamic_lookup" pip install -e ".[dev]"
```

### Building from Source

```bash
# Build the Rust extension in place (for `cargo test`/`cargo clippy`)
cargo build --release --all-features

# Run Rust tests
cargo test --release --all-features

# Run Python tests (after `pip install ".[dev]"` above)
pytest tests/

# Run linting (not currently enforced in CI — see ROADMAP_HONEST.md)
black pyvectorhound/ tests/
ruff check pyvectorhound/ tests/
mypy pyvectorhound/
```

## Code Style

We follow:
- **Python:** PEP 8 via Black (line length: 100)
- **Rust:** Standard Rust conventions via `cargo fmt`
- **Type hints:** Full type annotations for Python

```bash
# Format code
black pyvectorhound/ tests/
cargo fmt

# Check types
mypy pyvectorhound/

# Lint
ruff check pyvectorhound/ tests/
```

**Current state (be aware before you run these):** as of this writing,
`black --check` reformats 39 of 41 files and `ruff check .` reports 185
issues (mostly unused imports, long lines, and unsorted imports). Neither
is enforced in CI. If your PR touches a file that's already
non-compliant, it's fine to leave unrelated pre-existing issues alone —
don't let an unrelated `black`/`ruff` diff balloon your PR.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyvectorhound

# Run specific test file
pytest tests/test_diagnosis.py

# Run specific test
pytest tests/test_diagnosis.py::test_basic_diagnosis
```

Note: coverage only reports correctly if you installed with `pip install
-e ".[dev]"` (editable — what CI does). A plain, non-editable `pip
install ".[dev]"` will make `pytest --cov=pyvectorhound` report 0% for
every module even though the tests are really running and passing,
because `coverage.py` can't map the installed `site-packages` copy back
to this source tree. See ROADMAP_HONEST.md for details, including two
genuinely-0%-covered modules this exposes once measured correctly.

Write tests for new features:
```python
# tests/test_feature.py
def test_new_feature():
    """Test description."""
    hound = Hound(db="mock")
    result = hound.new_feature()
    assert result is not None
```

## Commit Messages

Follow conventional commits:
```
feat: Add new feature
fix: Fix a bug
docs: Update documentation
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

Example:
```
feat: Add embedding quality scorer with isotropy metric

- Implement isotropy calculation in Rust core
- Add QualityScorer Python API
- Add tests for edge cases
- Update documentation
```

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Write/update tests
5. Update documentation if needed
6. Run `pytest` and, ideally, `cargo test` if you touched Rust code
7. Push to your fork
8. Submit a pull request

### PR Guidelines
- Keep PRs focused on a single feature/fix
- Include test coverage for new code
- Update docs if applicable
- Add entry to CHANGELOG.md under `[Unreleased]`
- Link related issues

## Documentation

Documentation lives at the repo root and in `docs/`:
- `README.md` — overview, install, quick start
- `USER_GUIDE.md` / `docs/GUIDE.md` — usage guides
- `docs/ARCHITECTURE.md` — architecture overview
- `ROADMAP_HONEST.md` — honest status, known gaps, and technical debt
- `CHANGELOG.md` — release history

Update docs when:
- Adding new features
- Changing APIs
- Improving explanations

## Reporting Issues

Report bugs with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Python/Rust version
- Traceback if applicable

Use the issue templates on GitHub.

## Questions?

- Open a GitHub Discussion
- Check existing issues/discussions
- Email: mullassery@gmail.com

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

**Thank you for contributing to PyVectorHound!**
