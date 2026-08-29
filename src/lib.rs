// PyHound Core - Rust implementation of retrieval diagnostics
//
// High-performance embedding quality metrics, pipeline analysis, and diagnostics.

mod metrics;
mod quantization;
mod retrieval_ranking;

use metrics::{
    compute_coverage, compute_distinctiveness, compute_isotropy, compute_retrieval_metrics,
    detect_drift,
};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3::Bound;
use quantization::{dequantize, dequantize_batch, quantize, quantize_batch, QuantizationParams};

/// Build a Python dict from quantization params: {"scale", "offset", "min", "max"}.
fn params_to_dict<'py>(
    py: Python<'py>,
    params: &QuantizationParams,
) -> PyResult<Bound<'py, PyDict>> {
    let dict = PyDict::new(py);
    dict.set_item("scale", params.scale)?;
    dict.set_item("offset", params.offset)?;
    dict.set_item("min", params.min)?;
    dict.set_item("max", params.max)?;
    Ok(dict)
}

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
    let quality = (isotropy * 0.4 + coverage * 0.3 + distinctiveness * 0.3).clamp(0.0, 1.0);

    Ok(quality)
}

/// Quantize a single embedding vector to int8 for storage.
///
/// Returns a dict: `{"values": List[int], "scale": float, "offset": float,
/// "min": float, "max": float}`. `values` holds signed 8-bit integers
/// (-128..=127); `scale`/`offset` are required to dequantize.
#[pyfunction]
fn py_quantize_vector(py: Python, values: Vec<f32>) -> PyResult<PyObject> {
    let (quantized, params) = quantize(&values);

    let dict = PyDict::new(py);
    dict.set_item("values", quantized)?;
    dict.set_item("scale", params.scale)?;
    dict.set_item("offset", params.offset)?;
    dict.set_item("min", params.min)?;
    dict.set_item("max", params.max)?;

    Ok(dict.into())
}

/// Dequantize an int8 vector (produced by `py_quantize_vector`) back to f32.
#[pyfunction]
fn py_dequantize_vector(values: Vec<i8>, scale: f32, offset: f32) -> PyResult<Vec<f32>> {
    let params = QuantizationParams {
        scale,
        offset,
        min: 0.0,
        max: 0.0,
    };
    Ok(dequantize(&values, &params))
}

/// Quantize a batch of embedding vectors to int8, one set of quantization
/// parameters per vector (per-vector min/max scalar quantization).
///
/// Returns a dict: `{"values": List[List[int]], "params": List[dict]}`
/// where each entry of `params` has the same shape as
/// `py_quantize_vector`'s return dict.
#[pyfunction]
fn py_quantize_batch(py: Python, vectors: Vec<Vec<f32>>) -> PyResult<PyObject> {
    let (values, params) = quantize_batch(&vectors);

    let values_list = PyList::empty(py);
    for v in &values {
        values_list.append(v)?;
    }

    let params_list = PyList::empty(py);
    for p in &params {
        params_list.append(params_to_dict(py, p)?)?;
    }

    let dict = PyDict::new(py);
    dict.set_item("values", values_list)?;
    dict.set_item("params", params_list)?;

    Ok(dict.into())
}

/// Dequantize a batch of int8 vectors (produced by `py_quantize_batch`)
/// back to f32, given parallel `scales` and `offsets` lists.
#[pyfunction]
fn py_dequantize_batch(
    values: Vec<Vec<i8>>,
    scales: Vec<f32>,
    offsets: Vec<f32>,
) -> PyResult<Vec<Vec<f32>>> {
    if values.len() != scales.len() || values.len() != offsets.len() {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "values, scales, and offsets must have the same length",
        ));
    }

    let params: Vec<QuantizationParams> = scales
        .into_iter()
        .zip(offsets)
        .map(|(scale, offset)| QuantizationParams {
            scale,
            offset,
            min: 0.0,
            max: 0.0,
        })
        .collect();

    Ok(dequantize_batch(&values, &params))
}

/// PyHound Python module
#[pymodule]
fn _core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_compute_isotropy, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_coverage, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_distinctiveness, m)?)?;
    m.add_function(wrap_pyfunction!(py_detect_drift, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_retrieval_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(py_compute_quality_score, m)?)?;
    m.add_function(wrap_pyfunction!(py_quantize_vector, m)?)?;
    m.add_function(wrap_pyfunction!(py_dequantize_vector, m)?)?;
    m.add_function(wrap_pyfunction!(py_quantize_batch, m)?)?;
    m.add_function(wrap_pyfunction!(py_dequantize_batch, m)?)?;

    Ok(())
}
