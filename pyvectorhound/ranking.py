"""Multi-criteria retrieval ranking, diversification, and reranker metrics.

Thin Python wrapper over the Rust `RetrievalRanker` (`src/retrieval_ranking.rs`,
exposed via `pyvectorhound._core`). Combines BM25/semantic/recency signals
into a single ranking, then diversifies the top results using real
cosine-similarity penalties computed from each document's embedding -- not a
fixed placeholder.
"""

from typing import Any, Dict, List, Sequence, Tuple

try:
    from pyvectorhound import _core
except ImportError:
    _core = None

RankingInput = Tuple[str, Dict[str, float], Sequence[float]]


def _require_core() -> None:
    if _core is None:
        raise RuntimeError(
            "pyvectorhound._core is not available (the compiled Rust extension "
            "failed to import). rank_and_diversify()/compute_reranker_metrics() "
            "have no pure-Python fallback -- reinstall pyvectorhound with the "
            "compiled extension (`pip install pyvectorhound` from a wheel, or "
            "`maturin develop` from source) rather than relying on a faked result."
        )


def rank_and_diversify(
    results: Sequence[RankingInput], top_k: int
) -> List[Dict[str, Any]]:
    """
    Rank `results` by multi-criteria score, then diversify the top `top_k`.

    Args:
        results: `(document_id, scores, embedding)` per candidate. `scores`
            may contain `"bm25"`, `"semantic"`, `"recency"` keys (missing
            keys default to 0.0, weighted 0.3/0.4/0.15 respectively).
            `embedding` is that document's real vector; pass `[]` to opt a
            document out of diversity scoring (it will never be penalized
            for, or penalize, similarity to other results).
        top_k: Number of results to keep after diversification.

    Returns:
        A list of dicts, ordered by the final diversity-adjusted score:
        `{"document_id", "relevance_score", "rank", "diversity_score",
        "ranking_factors"}`. `diversity_score` is `1.0` for a result with no
        similar already-selected result, down to `0.0` for a near-duplicate
        of one.

    Example:
        >>> results = [
        ...     ("doc_1", {"semantic": 0.9}, [1.0, 0.0]),
        ...     ("doc_dup", {"semantic": 0.8}, [1.0, 0.0]),
        ...     ("doc_distinct", {"semantic": 0.5}, [0.0, 1.0]),
        ... ]
        >>> rank_and_diversify(results, top_k=3)[1]["diversity_score"]
        0.0
    """
    _require_core()
    return _core.py_rank_and_diversify_results(
        [(doc_id, dict(scores), list(embedding)) for doc_id, scores, embedding in results],
        top_k,
    )


def compute_reranker_metrics(
    ranked_document_ids: Sequence[str],
    diversity_scores: Sequence[float],
    relevant_docs: Sequence[str],
    k: int,
) -> Dict[str, float]:
    """
    Compute MRR, NDCG, Precision@K, Recall@K, and average diversity score
    for an already-ranked result list.

    Args:
        ranked_document_ids: Document IDs in rank order (index 0 = rank 1).
        diversity_scores: Parallel to `ranked_document_ids` -- typically the
            `diversity_score` values from `rank_and_diversify()`'s output.
            Pass all `1.0` if diversification wasn't run.
        relevant_docs: Ground-truth relevant document IDs.
        k: Cutoff for Precision@K/Recall@K/NDCG@K.

    Returns:
        `{"mrr", "ndcg", "precision_at_k", "recall_at_k", "diversity_score"}`.
    """
    _require_core()
    return _core.py_compute_reranker_metrics(
        list(ranked_document_ids), list(diversity_scores), list(relevant_docs), k
    )
