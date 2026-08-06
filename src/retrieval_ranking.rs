/// PyVectorHound v1.3: Advanced Retrieval Ranking & Reranking
///
/// Multi-criteria ranking, cross-encoder reranking, and diversity optimization

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RankedResult {
    pub document_id: String,
    pub relevance_score: f32,
    pub rank: usize,
    pub ranking_factors: HashMap<String, f32>,
    pub diversity_score: f32,
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
            .enumerate()
            .map(|(_, result)| {
                let score = self._calculate_multi_criteria_score(&result);
                RankedResult {
                    document_id: result.doc_id,
                    relevance_score: score,
                    rank: 0,  // Will be updated
                    ranking_factors: result.scores,
                    diversity_score: 0.5,  // Placeholder
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

    /// Diversify results to reduce redundancy
    pub fn diversify(&self, ranked: Vec<RankedResult>, top_k: usize) -> Vec<RankedResult> {
        let mut diversified = Vec::new();

        for result in ranked {
            if diversified.len() >= top_k {
                break;
            }

            // Penalize results too similar to already-selected results
            let similarity_penalty = self._calculate_similarity_penalty(&result, &diversified);
            let adjusted_score = result.relevance_score * (1.0 - similarity_penalty * self.diversity_weight);

            let mut adjusted_result = result;
            adjusted_result.relevance_score = adjusted_score;
            adjusted_result.diversity_score = 1.0 - similarity_penalty;

            diversified.push(adjusted_result);
        }

        diversified
    }

    fn _calculate_similarity_penalty(&self, _result: &RankedResult, _selected: &[RankedResult]) -> f32 {
        // Placeholder: would compute actual embedding similarity
        0.1  // 10% penalty per similar result
    }
}

#[derive(Debug, Clone)]
pub struct RetrievalResult {
    pub doc_id: String,
    pub scores: HashMap<String, f32>,
}

pub struct RerankerMetrics {
    pub mrr: f32,          // Mean Reciprocal Rank
    pub ndcg: f32,         // Normalized Discounted Cumulative Gain
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
        let relevant_in_topk = top_k.iter().filter(|r| relevant_docs.contains(&r.document_id)).count();
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
            let is_relevant = if relevant_docs.contains(&result.document_id) { 1.0 } else { 0.0 };
            dcg += is_relevant / ((i + 2) as f32).log2();
        }

        // IDCG (Ideal DCG)
        let mut idcg = 0.0;
        for i in 0..relevant_docs.len().min(ranked.len()) {
            idcg += 1.0 / ((i + 2) as f32).log2();
        }

        if idcg == 0.0 { 0.0 } else { dcg / idcg }
    }

    fn _calculate_diversity_score(ranked: &[&RankedResult]) -> f32 {
        if ranked.is_empty() {
            return 0.0;
        }

        let avg_diversity = ranked.iter().map(|r| r.diversity_score).sum::<f32>() / ranked.len() as f32;
        avg_diversity
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ranker_creation() {
        let ranker = RetrievalRanker::new();
        assert_eq!(ranker.bm25_weight + ranker.semantic_weight + ranker.recency_weight + ranker.diversity_weight, 1.0);
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
            });
        }

        let diversified = ranker.diversify(results, 3);
        assert_eq!(diversified.len(), 3);
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
            },
            RankedResult {
                document_id: "doc_2".to_string(),
                relevance_score: 0.85,
                rank: 2,
                ranking_factors: HashMap::new(),
                diversity_score: 0.8,
            },
        ];

        let relevant = vec!["doc_1".to_string(), "doc_3".to_string()];
        let metrics = RerankerMetrics::calculate(&ranked, &relevant, 2);

        assert!(metrics.mrr > 0.0);
        assert!(metrics.ndcg > 0.0);
        assert!(metrics.precision_at_k > 0.0);
    }
}
