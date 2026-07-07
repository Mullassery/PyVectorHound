// Embedding quality metrics calculation
// These are the core diagnostics that power PyHound

use std::f32;

/// Compute isotropy of embeddings (how uniformly distributed they are)
///
/// Isotropy measures how well embeddings use the full vector space.
/// High isotropy (close to 1.0) means vectors are spread throughout space.
/// Low isotropy (close to 0.0) means vectors cluster in a small region.
pub fn compute_isotropy(embeddings: &[Vec<f32>]) -> f32 {
    if embeddings.is_empty() || embeddings[0].is_empty() {
        return 0.0;
    }

    let n = embeddings.len();
    let _d = embeddings[0].len();

    if n < 2 {
        return 0.0;
    }

    // Normalize embeddings
    let normalized: Vec<Vec<f32>> = embeddings
        .iter()
        .map(|v| {
            let norm: f32 = v.iter().map(|x| x * x).sum::<f32>().sqrt();
            if norm > 0.0 {
                v.iter().map(|x| x / norm).collect()
            } else {
                v.clone()
            }
        })
        .collect();

    // Compute average pairwise similarity
    let mut sum_sim = 0.0;
    let mut count = 0;

    for i in 0..n {
        for j in (i + 1)..n {
            let sim: f32 = normalized[i]
                .iter()
                .zip(&normalized[j])
                .map(|(a, b)| a * b)
                .sum();
            sum_sim += sim.abs();
            count += 1;
        }
    }

    let avg_sim = if count > 0 { sum_sim / count as f32 } else { 0.0 };

    // Isotropy is inversely related to average similarity
    // Lower similarity = higher isotropy
    // Map to 0..1 range
    (1.0 - avg_sim.min(1.0)).max(0.0)
}

/// Compute coverage of embeddings (diversity of semantic space)
///
/// Coverage measures how much of the semantic space is represented.
/// High coverage means embeddings span diverse concepts.
pub fn compute_coverage(embeddings: &[Vec<f32>]) -> f32 {
    if embeddings.is_empty() || embeddings[0].is_empty() {
        return 0.0;
    }

    let n = embeddings.len();
    let d = embeddings[0].len();

    if n < 2 {
        return 0.0;
    }

    // Compute centroid
    let mut centroid = vec![0.0; d];
    for emb in embeddings {
        for (i, &val) in emb.iter().enumerate() {
            centroid[i] += val;
        }
    }
    for val in &mut centroid {
        *val /= n as f32;
    }

    // Compute variance from centroid
    let mut variance = vec![0.0; d];
    for emb in embeddings {
        for (i, &val) in emb.iter().enumerate() {
            let diff = val - centroid[i];
            variance[i] += diff * diff;
        }
    }
    for val in &mut variance {
        *val /= n as f32;
    }

    // Average variance across dimensions (normalized)
    let avg_variance: f32 = variance.iter().sum::<f32>() / d as f32;

    // Coverage is bounded by 0..1
    // Normalize by expected variance
    (avg_variance / (1.0 + avg_variance)).min(1.0)
}

/// Compute distinctiveness of embeddings (semantic separation)
///
/// Distinctiveness measures how semantically different embeddings are.
/// High distinctiveness means concepts are well-separated.
pub fn compute_distinctiveness(embeddings: &[Vec<f32>]) -> f32 {
    if embeddings.is_empty() || embeddings[0].is_empty() {
        return 0.0;
    }

    let n = embeddings.len();

    if n < 2 {
        return 0.0;
    }

    // Normalize embeddings
    let normalized: Vec<Vec<f32>> = embeddings
        .iter()
        .map(|v| {
            let norm: f32 = v.iter().map(|x| x * x).sum::<f32>().sqrt();
            if norm > 0.0 {
                v.iter().map(|x| x / norm).collect()
            } else {
                v.clone()
            }
        })
        .collect();

    // Compute pairwise similarities and find min/max
    let mut similarities = Vec::new();

    for i in 0..n {
        for j in (i + 1)..n {
            let sim: f32 = normalized[i]
                .iter()
                .zip(&normalized[j])
                .map(|(a, b)| a * b)
                .sum();
            similarities.push(sim);
        }
    }

    if similarities.is_empty() {
        return 0.0;
    }

    // Distinctiveness is measured by spread of similarities
    // We want low average similarity (high distinctiveness)
    // and high variance in similarities (some diversity)

    let avg_sim: f32 = similarities.iter().sum::<f32>() / similarities.len() as f32;
    let variance: f32 = similarities
        .iter()
        .map(|s| (s - avg_sim).powi(2))
        .sum::<f32>()
        / similarities.len() as f32;

    // Distinctiveness combines low average similarity and high variance
    let distinctiveness = (1.0 - avg_sim.abs()) * (1.0 + variance.sqrt());

    distinctiveness.min(1.0).max(0.0)
}

/// Detect drift in embedding quality
///
/// Compares current embeddings against baseline to detect degradation.
pub fn detect_drift(baseline: &[Vec<f32>], current: &[Vec<f32>]) -> f32 {
    if baseline.is_empty() || current.is_empty() {
        return 0.0;
    }

    let baseline_isotropy = compute_isotropy(baseline);
    let baseline_coverage = compute_coverage(baseline);
    let baseline_distinctiveness = compute_distinctiveness(baseline);

    let current_isotropy = compute_isotropy(current);
    let current_coverage = compute_coverage(current);
    let current_distinctiveness = compute_distinctiveness(current);

    // Compute relative drift (normalized to 0..1)
    let isotropy_drift = (baseline_isotropy - current_isotropy).abs() / (1.0 + baseline_isotropy);
    let coverage_drift = (baseline_coverage - current_coverage).abs() / (1.0 + baseline_coverage);
    let distinctiveness_drift =
        (baseline_distinctiveness - current_distinctiveness).abs() / (1.0 + baseline_distinctiveness);

    // Average drift across metrics
    (isotropy_drift + coverage_drift + distinctiveness_drift) / 3.0
}

/// Compute retrieval metrics for results
#[derive(Debug, Clone)]
pub struct RetrievalMetrics {
    pub precision: f32,
    pub recall: f32,
    pub f1_score: f32,
    pub mrr: f32,  // Mean Reciprocal Rank
    pub ndcg: f32, // Normalized Discounted Cumulative Gain
}

/// Compute precision, recall, and F1 score
pub fn compute_retrieval_metrics(
    retrieved: &[usize],        // Retrieved document indices (in order)
    relevant: &[usize],         // Relevant document indices (ground truth)
    top_k: usize,
) -> RetrievalMetrics {
    let retrieved_set: std::collections::HashSet<_> = retrieved.iter().cloned().collect();
    let relevant_set: std::collections::HashSet<_> = relevant.iter().cloned().collect();

    // Precision: how many retrieved are relevant
    let tp = retrieved_set.intersection(&relevant_set).count();
    let precision = if !retrieved.is_empty() {
        tp as f32 / retrieved.len().min(top_k) as f32
    } else {
        0.0
    };

    // Recall: how many relevant are retrieved
    let recall = if !relevant.is_empty() {
        tp as f32 / relevant.len() as f32
    } else {
        0.0
    };

    // F1 score
    let f1_score = if precision + recall > 0.0 {
        2.0 * (precision * recall) / (precision + recall)
    } else {
        0.0
    };

    // MRR: position of first relevant result
    let mut mrr = 0.0;
    for (i, &doc) in retrieved.iter().enumerate() {
        if relevant_set.contains(&doc) {
            mrr = 1.0 / (i as f32 + 1.0);
            break;
        }
    }

    // NDCG@k
    let mut dcg = 0.0;
    for (i, &doc) in retrieved.iter().take(top_k).enumerate() {
        if relevant_set.contains(&doc) {
            dcg += 1.0 / (i as f32 + 1.0).log2().max(1.0);
        }
    }

    let ideal_dcg: f32 = (0..relevant.len().min(top_k))
        .map(|i| 1.0 / (i as f32 + 1.0).log2().max(1.0))
        .sum();

    let ndcg = if ideal_dcg > 0.0 { dcg / ideal_dcg } else { 0.0 };

    RetrievalMetrics {
        precision: precision.max(0.0).min(1.0),
        recall: recall.max(0.0).min(1.0),
        f1_score: f1_score.max(0.0).min(1.0),
        mrr: mrr.max(0.0).min(1.0),
        ndcg: ndcg.max(0.0).min(1.0),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_isotropy() {
        let embeddings = vec![
            vec![1.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0],
            vec![0.0, 0.0, 1.0],
        ];
        let isotropy = compute_isotropy(&embeddings);
        assert!(isotropy > 0.8); // Orthogonal vectors = high isotropy
    }

    #[test]
    fn test_coverage() {
        // Well-spread embeddings should score meaningfully higher than a tightly
        // clustered set. (compute_coverage uses a saturating normalization
        // `var/(1+var)`, so absolute scores stay in 0..~0.5 for unit vectors —
        // the meaningful signal is diverse > clustered.)
        let diverse = vec![
            vec![1.0, 0.0],
            vec![-1.0, 0.0],
            vec![0.0, 1.0],
            vec![0.0, -1.0],
        ];
        let clustered = vec![
            vec![1.0, 0.0],
            vec![0.99, 0.01],
            vec![1.0, 0.02],
            vec![0.98, 0.0],
        ];
        let cov_diverse = compute_coverage(&diverse);
        let cov_clustered = compute_coverage(&clustered);
        assert!(cov_diverse > cov_clustered, "diverse ({cov_diverse}) should exceed clustered ({cov_clustered})");
        assert!(cov_diverse > 0.3, "diverse coverage was {cov_diverse}");
    }

    #[test]
    fn test_retrieval_metrics() {
        let retrieved = vec![0, 1, 2];
        let relevant = vec![0, 2, 3];
        let metrics = compute_retrieval_metrics(&retrieved, &relevant, 3);

        assert_eq!(metrics.precision, 2.0 / 3.0); // 2 out of 3 retrieved are relevant
        assert_eq!(metrics.recall, 2.0 / 3.0);   // 2 out of 3 relevant are retrieved
        assert!(metrics.f1_score > 0.0);
    }
}
