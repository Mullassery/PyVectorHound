"""Optional synthetic evaluation sets (Ragas-compatible).

PyVectorHound diagnoses retrieval, but teams often lack labeled queries. This
adapter converts Ragas-style generated test rows into PyVectorHound inputs
(query + expected document ids) and can delegate generation to a caller-supplied
generator. It does not fabricate questions or ground truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Optional


class RagasUnavailable(RuntimeError):  # noqa: N818
    """Raised when a Ragas generator is requested but unavailable."""


@dataclass
class EvalCase:
    query: str
    ground_truth: str = ""
    contexts: list[str] = field(default_factory=list)
    expected_docs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "ground_truth": self.ground_truth,
            "contexts": self.contexts,
            "expected_docs": self.expected_docs,
        }


def from_ragas_rows(rows: Iterable[dict[str, Any]]) -> list[EvalCase]:
    """Map Ragas-style rows (user_input/reference/reference_contexts) to cases."""
    cases: list[EvalCase] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        query = row.get("user_input") or row.get("question") or row.get("query")
        if not query:
            continue
        contexts = row.get("reference_contexts") or row.get("contexts") or []
        if isinstance(contexts, str):
            contexts = [contexts]
        expected = row.get("expected_docs") or row.get("expected_document_ids") or []
        if isinstance(expected, str):
            expected = [expected]
        cases.append(
            EvalCase(
                query=str(query),
                ground_truth=str(row.get("reference") or row.get("ground_truth") or ""),
                contexts=[str(c) for c in contexts],
                expected_docs=[str(d) for d in expected],
            )
        )
    return cases


def generate_testset(
    documents: dict[str, str],
    *,
    test_size: int = 10,
    generator: Optional[Callable[[dict[str, str], int], Iterable[dict[str, Any]]]] = None,
) -> list[EvalCase]:
    """Generate cases through a caller-provided generator.

    A generator is preferred because Ragas's generator API changes across
    versions and may require an LLM. If ``generator`` is omitted, this function
    raises with the exact dependency/usage guidance rather than inventing data.
    """
    if generator is None:
        try:
            import ragas  # noqa: F401
        except ImportError as exc:
            raise RagasUnavailable(
                "Ragas is not installed. Install with "
                '`pip install "pyvectorhound[ragas]"` and pass a generator, '
                "or supply your own generator callable."
            ) from exc
        raise RagasUnavailable(
            "Pass a generator callable (documents, test_size) -> Ragas-style rows; "
            "Ragas generator APIs vary by version and require an LLM."
        )
    return from_ragas_rows(generator(documents, test_size))


def to_hound_batch(cases: Iterable[EvalCase]) -> tuple[list[str], list[list[str]]]:
    """Return (queries, expected_docs) ready for ``Hound.diagnose_batch``."""
    cases = list(cases)
    return [case.query for case in cases], [case.expected_docs for case in cases]


__all__ = [
    "EvalCase",
    "RagasUnavailable",
    "from_ragas_rows",
    "generate_testset",
    "to_hound_batch",
]
