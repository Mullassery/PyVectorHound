# Queue status — 2026-10-19

This file records what was shipped, what is blocked/failed, and what is rejected for this repository. It complements `AUDIT_FINDINGS.md`.

## Shipped
- BM25/reranker diagnostics and HTML/JSON reports (1.8.0).

## Blocked / failed
- Verified adapter coverage tests for LlamaIndex/LangChain/pgvector.

## Rejected / deferred
- Generation-layer evaluation/UI — Ragas/Phoenix own it.

## Policy

Any future feature or upgrade must check `AUDIT_FINDINGS.md` and this file before implementation. A blocked item is retried only when its external dependency is available; a rejected item needs new user evidence or a design change to reopen.
