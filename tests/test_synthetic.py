"""Ragas-style eval-set conversion tests."""

from __future__ import annotations

import pytest

from pyvectorhound.synthetic import from_ragas_rows, generate_testset, to_hound_batch

ROWS = [
    {
        "user_input": "What is the refund window?",
        "reference": "30 days",
        "reference_contexts": ["Refunds within 30 days."],
        "expected_docs": ["policy-1"],
    }
]


def test_from_ragas_rows_maps_fields():
    cases = from_ragas_rows(ROWS)
    assert cases[0].query == "What is the refund window?"
    assert cases[0].ground_truth == "30 days"
    assert cases[0].expected_docs == ["policy-1"]


def test_generate_testset_with_custom_generator():
    cases = generate_testset({"doc": "text"}, test_size=1, generator=lambda docs, n: ROWS)
    assert len(cases) == 1


def test_to_hound_batch():
    queries, expected = to_hound_batch(from_ragas_rows(ROWS))
    assert queries == ["What is the refund window?"]
    assert expected == [["policy-1"]]


def test_missing_generator_is_actionable(monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "ragas", None)
    with pytest.raises(Exception, match="pyvectorhound\\[ragas\\]"):
        generate_testset({"doc": "text"})
