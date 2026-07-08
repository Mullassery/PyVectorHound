// PyHound Core - Rust implementation of retrieval diagnostics
//
// High-performance embedding quality metrics, pipeline analysis, and diagnostics.

mod metrics;

use metrics::{
    compute_coverage, compute_distinctiveness, compute_isotropy, compute_retrieval_metrics,
    detect_drift,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::Bound;

/// Compute isotropy of embeddings (vector space utilization)
#[pyfunction]
fn py_compute_isotropy(embeddings: Vec<Vec<f32>>) -> PyResult<f32> {
    Ok(compute_isotropy(&embeddings))
}

/// Compute coverage of embeddings (diversity of semantic space)
#[pyfunction]
fn py_compute_coverage(embeddings: Vec<Vec<f32>>) -> PyResult<f32> {
    Ok(compute_coverage(&embeddings))
}

/// Compute distinctiveness of embeddings (semantic separation)
#[pyfunction]
fn py_compute_distinctiveness(embeddings: Vec<Vec<f32>>) -> PyResult<f32> {
    Ok(compute_distinctiveness(&embeddings))
}

/// Detect drift in embedding quality
#[pyfunction]
fn py_detect_drift(
    baseline_embeddings: Vec<Vec<f32>>,
    current_embeddings: Vec<Vec<f32>>,
) -> PyResult<f32> {
    Ok(detect_drift(&baseline_embeddings, &current_embeddings))
}

/// Compute retrieval metrics (precision, recall, F1, MRR, NDCG)
#[pyfunction]
fn py_compute_retrieval_metrics(
    py: Python,
    retrieved: Vec<usize>,
    relevant: Vec<usize>,
    top_k: usize,
) -> PyResult<PyObject> {
    let metrics = compute_retrieval_metrics(&retrieved, &relevant, top_k);

    let dict = PyDict::new(py);
    dict.set_item("precision", metrics.precision)?;
    dict.set_item("recall", metrics.recall)?;
    dict.set_item("f1_score", metrics.f1_score)?;
    dict.set_item("mrr", metrics.mrr)?;
    dict.set_item("ndcg", metrics.ndcg)?;

    Ok(dict.into())
}

/// Compute embedding quality score (composite metric)
#[pyfunction]
fn py_compute_quality_score(embeddings: Vec<Vec<f32>>) -> PyResult<f32> {
    if embeddings.is_empty() {
        return Ok(0.0);
    }

    let isotropy = compute_isotropy(&embeddings);
    let coverage = compute_coverage(&embeddings);
    let distinctiveness = compute_distinctiveness(&embeddings);

    // Composite score: weighted average
    let quality = (isotropy * 0.4 + coverage * 0.3 + distinctiveness * 0.3)
        .max(0.0)
        .min(1.0);

    Ok(quality)
}

/// PyHound Python module
#[pymodule]
fn pyhound_core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_compute_isotropy, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_coverage, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_distinctiveness, m)?)?;
    m.add_function(wrap_pyfunction!(py_detect_drift, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_retrieval_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_quality_score, m)?)?;

    Ok(())
}
