.PHONY: install install-dev build test lint fmt clean help setup-hooks

help:
	@echo "pyvectorhound development tasks:"
	@echo "  make install         Install pre-commit hooks"
	@echo "  make build           Build release wheel"
	@echo "  make test            Run all tests"
	@echo "  make test-cov        Run tests with coverage"
	@echo "  make lint            Run linters (clippy, black, ruff, mypy)"
	@echo "  make fmt             Format code"
	@echo "  make fmt-check       Check format without changing"
	@echo "  make clean           Remove build artifacts"

install: setup-hooks
	@echo "✓ Development environment ready"

setup-hooks:
	@command -v pre-commit >/dev/null 2>&1 || pip install pre-commit
	pre-commit install

build:
	maturin build --release

test:
	pytest -v

test-cov:
	pytest -v --cov=pyvectorhound --cov-report=term-missing

lint:
	cargo clippy --all-targets
	black --check .
	ruff check .
	mypy pyvectorhound

fmt:
	cargo fmt --all
	black .
	ruff check . --fix

fmt-check:
	cargo fmt --all -- --check
	black --check .

clean:
	cargo clean
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache
