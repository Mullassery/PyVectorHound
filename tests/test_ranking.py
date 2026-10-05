"""Tests for pyvectorhound.ranking.

`RetrievalRanker.diversify()` in `src/retrieval_ranking.rs` used to compute
a hardcoded 10% similarity penalty regardless of the actual embeddings
involved (`_calculate_similarity_penalty` was an explicit placeholder that
never looked at embedding data). These tests verify the diversity penalty
now actually responds to real cosine similarity between embeddings.
"""

import pytest

from pyvectorhound.ranking import compute_reranker_metrics, rank_and_diversify


def test_near_duplicate_embedding_is_penalized_more_than_distinct_one():
    # doc_dup and doc_distinct start with nearly identical raw semantic
    # scores (0.52 vs 0.50), so the diversity penalty -- not the initial
    # score gap -- has to be what decides their final order.
    results = [
        ("doc_1", {"semantic": 0.9}, [1.0, 0.0]),
        ("doc_dup", {"semantic": 0.52}, [1.0, 0.0]),  # identical to doc_1
        ("doc_distinct", {"semantic": 0.50}, [0.0, 1.0]),  # orthogonal to doc_1
    ]

    ranked = rank_and_diversify(results, top_k=3)
    by_id = {r["document_id"]: r for r in ranked}

    assert by_id["doc_1"]["diversity_score"] == 1.0  # first selected, nothing to compare against
    assert by_id["doc_dup"]["diversity_score"] == 0.0  # fully redundant with doc_1
    assert by_id["doc_distinct"]["diversity_score"] == 1.0  # orthogonal, no penalty

    # doc_dup started with a higher raw semantic score than doc_distinct but
    # its diversity-adjusted relevance_score should now be lower, since it's
    # a near-duplicate of an already-selected result.
    assert by_id["doc_dup"]["relevance_score"] < by_id["doc_distinct"]["relevance_score"]


def test_documents_without_embeddings_get_no_penalty():
    results = [
        ("doc_1", {"semantic": 0.9}, [1.0, 0.0]),
        ("doc_2", {"semantic": 0.8}, []),  # no embedding supplied
    ]

    ranked = rank_and_diversify(results, top_k=2)
    by_id = {r["document_id"]: r for r in ranked}

    assert by_id["doc_2"]["diversity_score"] == 1.0


def test_top_k_truncates_after_ranking():
    results = [(f"doc_{i}", {"semantic": (5 - i) * 0.1}, [float(i), 0.0]) for i in range(5)]
    ranked = rank_and_diversify(results, top_k=2)
    assert len(ranked) == 2
    assert ranked[0]["document_id"] == "doc_0"  # highest semantic score


def test_compute_reranker_metrics_against_ground_truth():
    results = [
        ("doc_1", {"semantic": 0.9}, [1.0, 0.0]),
        ("doc_2", {"semantic": 0.5}, [0.0, 1.0]),
        ("doc_3", {"semantic": 0.1}, [0.5, 0.5]),
    ]
    ranked = rank_and_diversify(results, top_k=3)
    ids = [r["document_id"] for r in ranked]
    diversity_scores = [r["diversity_score"] for r in ranked]

    metrics = compute_reranker_metrics(ids, diversity_scores, ["doc_1", "doc_3"], k=3)

    assert metrics["mrr"] == 1.0  # doc_1 (the only exact first-rank relevant doc) is rank 1
    assert metrics["recall_at_k"] == 1.0  # both relevant docs retrieved within k=3
    assert 0.0 <= metrics["ndcg"] <= 1.0


def test_mismatched_lengths_raises():
    with pytest.raises(Exception):
        compute_reranker_metrics(["doc_1", "doc_2"], [1.0], ["doc_1"], k=2)
