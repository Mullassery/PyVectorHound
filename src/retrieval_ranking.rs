//! PyVectorHound v1.3: Advanced Retrieval Ranking & Reranking
//!
//! Multi-criteria ranking, cross-encoder reranking, and diversity optimization.
//! Exposed to Python via `py_rank_and_diversify_results` /
//! `py_compute_reranker_metrics` in `lib.rs`.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Cosine similarity between two equal-length vectors, in `[-1.0, 1.0]`.
/// Returns `0.0` for empty or zero-norm vectors rather than dividing by zero.
pub fn cosine_similarity(a: &[f32], b: &[f32]) -> f32 {
    if a.is_empty() || b.is_empty() || a.len() != b.len() {
        return 0.0;
    }

    let dot: f32 = a.iter().zip(b).map(|(x, y)| x * y).sum();
    let norm_a: f32 = a.iter().map(|x| x * x).sum::<f32>().sqrt();
    let norm_b: f32 = b.iter().map(|x| x * x).sum::<f32>().sqrt();

    if norm_a == 0.0 || norm_b == 0.0 {
        return 0.0;
    }

    dot / (norm_a * norm_b)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RankedResult {
    pub document_id: String,
    pub relevance_score: f32,
    pub rank: usize,
    pub ranking_factors: HashMap<String, f32>,
    pub diversity_score: f32,
    pub embedding: Vec<f32>,
}

pub struct RetrievalRanker {
    bm25_weight: f32,
    semantic_weight: f32,
    recency_weight: f32,
    diversity_weight: f32,
}

impl RetrievalRanker {
    pub fn new() -> Self {
        RetrievalRanker {
            bm25_weight: 0.3,
            semantic_weight: 0.4,
            recency_weight: 0.15,
            diversity_weight: 0.15,
        }
    }

    /// Rank results using multi-criteria scoring
    pub fn rank(&self, results: Vec<RetrievalResult>) -> Vec<RankedResult> {
        let mut ranked: Vec<RankedResult> = results
            .into_iter()
            .map(|result| {
                let score = self._calculate_multi_criteria_score(&result);
                RankedResult {
                    document_id: result.doc_id,
                    relevance_score: score,
                    rank: 0, // Will be updated
                    ranking_factors: result.scores,
                    diversity_score: 1.0, // No penalty until diversify() runs.
                    embedding: result.embedding,
                }
            })
            .collect();

        // Sort by score
        ranked.sort_by(|a, b| b.relevance_score.partial_cmp(&a.relevance_score).unwrap());

        // Update ranks
        for (i, result) in ranked.iter_mut().enumerate() {
            result.rank = i + 1;
        }

        ranked
    }

    fn _calculate_multi_criteria_score(&self, result: &RetrievalResult) -> f32 {
        let bm25 = result.scores.get("bm25").copied().unwrap_or(0.0);
        let semantic = result.scores.get("semantic").copied().unwrap_or(0.0);
        let recency = result.scores.get("recency").copied().unwrap_or(0.0);

        (bm25 * self.bm25_weight)
            + (semantic * self.semantic_weight)
            + (recency * self.recency_weight)
    }

    /// Diversify results to reduce redundancy.
    ///
    /// Selection greedily walks `ranked` in original relevance order (each
    /// result's penalty depends only on results already selected), but the
    /// returned list is re-sorted by the final diversity-adjusted score and
    /// re-ranked 1..N -- selection order and output order are not the same
    /// thing. A near-duplicate selected early can end up with a lower
    /// adjusted score than a later, undiscounted result; callers (and the
    /// `rank` field) must see the adjusted order, not the selection order.
    pub fn diversify(&self, ranked: Vec<RankedResult>, top_k: usize) -> Vec<RankedResult> {
        let mut diversified = Vec::new();

        for result in ranked {
            if diversified.len() >= top_k {
                break;
            }

            // Penalize results too similar to already-selected results
            let similarity_penalty = self._calculate_similarity_penalty(&result, &diversified);
            let adjusted_score =
                result.relevance_score * (1.0 - similarity_penalty * self.diversity_weight);

            let mut adjusted_result = result;
            adjusted_result.relevance_score = adjusted_score;
            adjusted_result.diversity_score = 1.0 - similarity_penalty;

            diversified.push(adjusted_result);
        }

        diversified.sort_by(|a, b| b.relevance_score.partial_cmp(&a.relevance_score).unwrap());
        for (i, result) in diversified.iter_mut().enumerate() {
            result.rank = i + 1;
        }

        diversified
    }

    /// Penalty in `[0.0, 1.0]` based on how similar `result`'s embedding is
    /// to the most similar already-selected result's embedding (max, not
    /// average, so one near-duplicate is enough to trigger the penalty).
    /// `0.0` when `result` has no embedding or nothing has been selected yet.
    fn _calculate_similarity_penalty(
        &self,
        result: &RankedResult,
        selected: &[RankedResult],
    ) -> f32 {
        if result.embedding.is_empty() || selected.is_empty() {
            return 0.0;
        }

        selected
            .iter()
            .map(|s| cosine_similarity(&result.embedding, &s.embedding).max(0.0))
            .fold(0.0_f32, f32::max)
    }
}

#[derive(Debug, Clone)]
pub struct RetrievalResult {
    pub doc_id: String,
    pub scores: HashMap<String, f32>,
    pub embedding: Vec<f32>,
}

pub struct RerankerMetrics {
    pub mrr: f32,  // Mean Reciprocal Rank
    pub ndcg: f32, // Normalized Discounted Cumulative Gain
    pub precision_at_k: f32,
    pub recall_at_k: f32,
    pub diversity_score: f32,
}

impl RerankerMetrics {
    pub fn calculate(ranked_results: &[RankedResult], relevant_docs: &[String], k: usize) -> Self {
        let top_k = ranked_results.iter().take(k).collect::<Vec<_>>();

        // Calculate MRR (Mean Reciprocal Rank)
        let mrr = Self::_calculate_mrr(&top_k, relevant_docs);

        // Calculate NDCG
        let ndcg = Self::_calculate_ndcg(&top_k, relevant_docs);

        // Calculate Precision@K
        let relevant_in_topk = top_k
            .iter()
            .filter(|r| relevant_docs.contains(&r.document_id))
            .count();
        let precision_at_k = relevant_in_topk as f32 / k.min(top_k.len()) as f32;

        // Calculate Recall@K
        let recall_at_k = relevant_in_topk as f32 / relevant_docs.len().max(1) as f32;

        // Calculate Diversity
        let diversity_score = Self::_calculate_diversity_score(&top_k);

        RerankerMetrics {
            mrr,
            ndcg,
            precision_at_k,
            recall_at_k,
            diversity_score,
        }
    }

    fn _calculate_mrr(ranked: &[&RankedResult], relevant_docs: &[String]) -> f32 {
        for (i, result) in ranked.iter().enumerate() {
            if relevant_docs.contains(&result.document_id) {
                return 1.0 / (i + 1) as f32;
            }
        }
        0.0
    }

    fn _calculate_ndcg(ranked: &[&RankedResult], relevant_docs: &[String]) -> f32 {
        let mut dcg = 0.0;
        for (i, result) in ranked.iter().enumerate() {
            let is_relevant = if relevant_docs.contains(&result.document_id) {
                1.0
            } else {
                0.0
            };
            dcg += is_relevant / ((i + 2) as f32).log2();
        }

        // IDCG (Ideal DCG)
        let mut idcg = 0.0;
        for i in 0..relevant_docs.len().min(ranked.len()) {
            idcg += 1.0 / ((i + 2) as f32).log2();
        }

        if idcg == 0.0 {
            0.0
        } else {
            dcg / idcg
        }
    }

    fn _calculate_diversity_score(ranked: &[&RankedResult]) -> f32 {
        if ranked.is_empty() {
            return 0.0;
        }

        let avg_diversity =
            ranked.iter().map(|r| r.diversity_score).sum::<f32>() / ranked.len() as f32;
        avg_diversity
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ranker_creation() {
        let ranker = RetrievalRanker::new();
        assert_eq!(
            ranker.bm25_weight
                + ranker.semantic_weight
                + ranker.recency_weight
                + ranker.diversity_weight,
            1.0
        );
    }

    #[test]
    fn test_ranking() {
        let ranker = RetrievalRanker::new();
        let mut results = Vec::new();

        for i in 0..3 {
            let mut scores = HashMap::new();
            scores.insert("semantic".to_string(), (3 - i) as f32 * 0.3);
            results.push(RetrievalResult {
                doc_id: format!("doc_{}", i),
                scores,
                embedding: vec![i as f32, 0.0],
            });
        }

        let ranked = ranker.rank(results);
        assert_eq!(ranked.len(), 3);
        assert_eq!(ranked[0].rank, 1);
    }

    #[test]
    fn test_diversification() {
        let ranker = RetrievalRanker::new();
        let mut results = Vec::new();

        for i in 0..5 {
            results.push(RankedResult {
                document_id: format!("doc_{}", i),
                relevance_score: (5 - i) as f32 * 0.2,
                rank: i + 1,
                ranking_factors: HashMap::new(),
                diversity_score: 0.5,
                embedding: vec![i as f32, 0.0],
            });
        }

        let diversified = ranker.diversify(results, 3);
        assert_eq!(diversified.len(), 3);
    }

    #[test]
    fn test_diversification_penalizes_near_duplicate_embeddings() {
        // doc_dup is embedding-identical to doc_1 (already selected first);
        // doc_distinct is orthogonal to everything selected so far. Despite
        // doc_dup having a higher starting relevance_score, the real
        // cosine-similarity penalty should drop its adjusted score below
        // doc_distinct's once doc_1 has been selected.
        let ranker = RetrievalRanker::new();
        let results = vec![
            RankedResult {
                document_id: "doc_1".to_string(),
                relevance_score: 1.0,
                rank: 1,
                ranking_factors: HashMap::new(),
                diversity_score: 1.0,
                embedding: vec![1.0, 0.0],
            },
            RankedResult {
                document_id: "doc_dup".to_string(),
                relevance_score: 0.9,
                rank: 2,
                ranking_factors: HashMap::new(),
                diversity_score: 1.0,
                embedding: vec![1.0, 0.0], // identical to doc_1
            },
            RankedResult {
                document_id: "doc_distinct".to_string(),
                relevance_score: 0.5,
                rank: 3,
                ranking_factors: HashMap::new(),
                diversity_score: 1.0,
                embedding: vec![0.0, 1.0], // orthogonal to doc_1
            },
        ];

        let diversified = ranker.diversify(results, 3);
        let dup = diversified
            .iter()
            .find(|r| r.document_id == "doc_dup")
            .unwrap();
        let distinct = diversified
            .iter()
            .find(|r| r.document_id == "doc_distinct")
            .unwrap();

        assert!(dup.diversity_score < distinct.diversity_score);
        assert!(
            dup.relevance_score < 0.9,
            "near-duplicate should be penalized below its raw score"
        );
        assert_eq!(
            distinct.relevance_score, 0.5,
            "orthogonal embedding gets no penalty"
        );
    }

    #[test]
    fn test_diversification_output_is_sorted_by_adjusted_score_not_selection_order() {
        // doc_b's penalty (near-dup of doc_a, selected first) drops its
        // adjusted score (0.525 * 0.85 = 0.44625) below doc_c's unpenalized
        // score (0.45) -- a real inversion the old implementation missed,
        // since it returned results in greedy-selection order rather than
        // re-sorting by the post-penalty score.
        let ranker = RetrievalRanker::new();
        let results = vec![
            RankedResult {
                document_id: "doc_a".to_string(),
                relevance_score: 1.0,
                rank: 1,
                ranking_factors: HashMap::new(),
                diversity_score: 1.0,
                embedding: vec![1.0, 0.0],
            },
            RankedResult {
                document_id: "doc_b".to_string(),
                relevance_score: 0.525,
                rank: 2,
                ranking_factors: HashMap::new(),
                diversity_score: 1.0,
                embedding: vec![1.0, 0.0], // identical to doc_a -> gets penalized
            },
            RankedResult {
                document_id: "doc_c".to_string(),
                relevance_score: 0.45,
                rank: 3,
                ranking_factors: HashMap::new(),
                diversity_score: 1.0,
                embedding: vec![0.0, 1.0], // orthogonal -> no penalty
            },
        ];

        let diversified = ranker.diversify(results, 3);

        let ids: Vec<&str> = diversified.iter().map(|r| r.document_id.as_str()).collect();
        assert_eq!(
            ids,
            vec!["doc_a", "doc_c", "doc_b"],
            "output must be ordered by adjusted score (doc_b's penalty drops it below doc_c), \
             not by pre-diversity selection order"
        );

        let ranks: Vec<usize> = diversified.iter().map(|r| r.rank).collect();
        assert_eq!(
            ranks,
            vec![1, 2, 3],
            "rank field must reflect the post-diversity output order"
        );

        for (i, result) in diversified.iter().enumerate() {
            if i > 0 {
                assert!(
                    result.relevance_score <= diversified[i - 1].relevance_score,
                    "relevance_score must be non-increasing in output order"
                );
            }
        }
    }

    #[test]
    fn test_cosine_similarity() {
        assert!((cosine_similarity(&[1.0, 0.0], &[1.0, 0.0]) - 1.0).abs() < 1e-6);
        assert!(cosine_similarity(&[1.0, 0.0], &[0.0, 1.0]).abs() < 1e-6);
        assert!((cosine_similarity(&[1.0, 0.0], &[-1.0, 0.0]) + 1.0).abs() < 1e-6);
        assert_eq!(cosine_similarity(&[], &[1.0]), 0.0);
    }

    #[test]
    fn test_metrics_calculation() {
        let ranked = vec![
            RankedResult {
                document_id: "doc_1".to_string(),
                relevance_score: 0.95,
                rank: 1,
                ranking_factors: HashMap::new(),
                diversity_score: 0.9,
                embedding: vec![],
            },
            RankedResult {
                document_id: "doc_2".to_string(),
                relevance_score: 0.85,
                rank: 2,
                ranking_factors: HashMap::new(),
                diversity_score: 0.8,
                embedding: vec![],
            },
        ];

        let relevant = vec!["doc_1".to_string(), "doc_3".to_string()];
        let metrics = RerankerMetrics::calculate(&ranked, &relevant, 2);

        assert!(metrics.mrr > 0.0);
        assert!(metrics.ndcg > 0.0);
        assert!(metrics.precision_at_k > 0.0);
    }
}
