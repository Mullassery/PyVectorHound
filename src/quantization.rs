//! Int8 scalar quantization for vector storage.
//!
//! Large local vector indices stored as `Vec<f32>` cost 4 bytes per
//! dimension. Scalar quantization maps each vector's float components
//! linearly into the `i8` range (-128..=127), storing them as 1 byte per
//! dimension plus a small per-vector `(scale, offset)` pair needed to
//! reconstruct approximate float values. This gives a ~4x memory reduction
//! for the vector data itself, at the cost of bounded reconstruction error.
//!
//! This is *scalar* quantization (per-vector min/max), not product
//! quantization, and it is not SIMD/GPU accelerated — both are explicitly
//! out of scope here.

use serde::{Deserialize, Serialize};

/// Parameters needed to dequantize an `i8` vector back to `f32`.
///
/// Reconstruction: `f32_value = i8_value as f32 * scale + offset`.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct QuantizationParams {
    /// Multiplier applied to the raw i8 value.
    pub scale: f32,
    /// Additive offset applied after scaling.
    pub offset: f32,
    /// Original minimum value of the vector (kept for introspection).
    pub min: f32,
    /// Original maximum value of the vector (kept for introspection).
    pub max: f32,
}

/// Quantize a single `f32` vector into `i8` values plus the parameters
/// needed to dequantize it.
///
/// Uses per-vector min/max scalar quantization: the vector's min and max
/// are mapped to the full `i8` range (-128..=127), and every other value is
/// linearly interpolated between them. This is standard for embedding
/// vectors, where per-vector dynamic range is usually similar across a
/// batch but not identical.
///
/// An empty input returns an empty output with a degenerate
/// (scale = 0, offset = 0) parameter set.
///
/// A constant vector (min == max, including all-zero) maps every value to
/// `0i8` and reconstructs exactly via `offset` (scale = 0), so round-trip
/// error is zero in that case.
pub fn quantize(values: &[f32]) -> (Vec<i8>, QuantizationParams) {
    if values.is_empty() {
        return (
            Vec::new(),
            QuantizationParams {
                scale: 0.0,
                offset: 0.0,
                min: 0.0,
                max: 0.0,
            },
        );
    }

    let mut min = values[0];
    let mut max = values[0];
    for &v in values.iter() {
        if v < min {
            min = v;
        }
        if v > max {
            max = v;
        }
    }

    // Degenerate case: every value identical. Store the value itself as
    // `offset`, use a zero scale, and quantize everything to 0 so
    // dequantization is exact.
    if min == max {
        let params = QuantizationParams {
            scale: 0.0,
            offset: min,
            min,
            max,
        };
        return (vec![0i8; values.len()], params);
    }

    // Map [min, max] -> [-128, 127] (255 steps).
    let scale = (max - min) / 255.0;
    let offset = min + scale * 128.0; // value that maps to raw i8 = 0

    let quantized: Vec<i8> = values
        .iter()
        .map(|&v| {
            let raw = ((v - min) / scale).round() - 128.0;
            raw.clamp(-128.0, 127.0) as i8
        })
        .collect();

    let params = QuantizationParams {
        scale,
        offset,
        min,
        max,
    };

    (quantized, params)
}

/// Dequantize `i8` values back into approximate `f32` values using the
/// scale/offset produced by [`quantize`].
pub fn dequantize(values: &[i8], params: &QuantizationParams) -> Vec<f32> {
    values
        .iter()
        .map(|&q| q as f32 * params.scale + params.offset)
        .collect()
}

/// Quantize a batch of vectors independently (one `QuantizationParams` per
/// vector). This is the typical entry point for shrinking a whole local
/// vector index.
pub fn quantize_batch(vectors: &[Vec<f32>]) -> (Vec<Vec<i8>>, Vec<QuantizationParams>) {
    let mut out_values = Vec::with_capacity(vectors.len());
    let mut out_params = Vec::with_capacity(vectors.len());
    for v in vectors {
        let (q, p) = quantize(v);
        out_values.push(q);
        out_params.push(p);
    }
    (out_values, out_params)
}

/// Dequantize a batch of vectors produced by [`quantize_batch`].
pub fn dequantize_batch(values: &[Vec<i8>], params: &[QuantizationParams]) -> Vec<Vec<f32>> {
    values
        .iter()
        .zip(params.iter())
        .map(|(v, p)| dequantize(v, p))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Deterministic pseudo-random f32 generator (xorshift) so tests don't
    /// need an external `rand` dependency.
    fn pseudo_random_floats(seed: u64, n: usize, lo: f32, hi: f32) -> Vec<f32> {
        let mut state = seed.wrapping_add(0x9E3779B97F4A7C15);
        (0..n)
            .map(|_| {
                // xorshift64
                state ^= state << 13;
                state ^= state >> 7;
                state ^= state << 17;
                let unit = (state % 1_000_000) as f32 / 1_000_000.0; // [0, 1)
                lo + unit * (hi - lo)
            })
            .collect()
    }

    fn max_abs_error(original: &[f32], reconstructed: &[f32]) -> f32 {
        original
            .iter()
            .zip(reconstructed.iter())
            .map(|(a, b)| (a - b).abs())
            .fold(0.0f32, f32::max)
    }

    #[test]
    fn test_round_trip_unit_range() {
        // Typical normalized-embedding range [-1, 1].
        let values = pseudo_random_floats(42, 384, -1.0, 1.0);
        let (quantized, params) = quantize(&values);
        assert_eq!(quantized.len(), values.len());

        let reconstructed = dequantize(&quantized, &params);
        let err = max_abs_error(&values, &reconstructed);

        // Expected bound for 8-bit quantization: half a quantization step,
        // i.e. range / 255 (using <= with a small epsilon for float
        // rounding slack).
        let expected_bound = (params.max - params.min) / 255.0;
        assert!(
            err <= expected_bound + 1e-4,
            "max abs error {err} exceeded expected bound {expected_bound}"
        );
    }

    #[test]
    fn test_round_trip_zero_to_one_range() {
        // Typical unnormalized embedding range [0, 1].
        let values = pseudo_random_floats(7, 768, 0.0, 1.0);
        let (quantized, params) = quantize(&values);
        let reconstructed = dequantize(&quantized, &params);
        let err = max_abs_error(&values, &reconstructed);

        let expected_bound = (params.max - params.min) / 255.0;
        assert!(
            err <= expected_bound + 1e-4,
            "max abs error {err} exceeded expected bound {expected_bound}"
        );
    }

    #[test]
    fn test_round_trip_wide_range() {
        // Wider range to make sure scale/offset math generalizes beyond
        // [-1, 1] / [0, 1].
        let values = pseudo_random_floats(1234, 512, -50.0, 75.0);
        let (quantized, params) = quantize(&values);
        let reconstructed = dequantize(&quantized, &params);
        let err = max_abs_error(&values, &reconstructed);

        let expected_bound = (params.max - params.min) / 255.0;
        assert!(
            err <= expected_bound + 1e-4,
            "max abs error {err} exceeded expected bound {expected_bound}"
        );
    }

    #[test]
    fn test_all_zero_vector_is_exact() {
        let values = vec![0.0f32; 128];
        let (quantized, params) = quantize(&values);
        assert!(quantized.iter().all(|&q| q == 0));

        let reconstructed = dequantize(&quantized, &params);
        let err = max_abs_error(&values, &reconstructed);
        assert_eq!(err, 0.0, "all-zero vector should round-trip exactly");
    }

    #[test]
    fn test_single_value_constant_vector_is_exact() {
        let values = vec![3.5f32; 64];
        let (quantized, params) = quantize(&values);
        let reconstructed = dequantize(&quantized, &params);
        let err = max_abs_error(&values, &reconstructed);
        assert_eq!(err, 0.0, "constant vector should round-trip exactly");
        assert!(reconstructed.iter().all(|&v| v == 3.5));
    }

    #[test]
    fn test_single_element_vector() {
        let values = vec![-0.234f32];
        let (quantized, params) = quantize(&values);
        assert_eq!(quantized.len(), 1);
        let reconstructed = dequantize(&quantized, &params);
        // A single element is trivially min == max -> exact round trip.
        assert_eq!(reconstructed[0], values[0]);
    }

    #[test]
    fn test_empty_vector() {
        let values: Vec<f32> = Vec::new();
        let (quantized, params) = quantize(&values);
        assert!(quantized.is_empty());
        let reconstructed = dequantize(&quantized, &params);
        assert!(reconstructed.is_empty());
    }

    #[test]
    fn test_extremes_map_to_i8_bounds() {
        let values = vec![-1.0f32, 0.0, 0.5, 1.0];
        let (quantized, _params) = quantize(&values);
        assert_eq!(*quantized.first().unwrap(), -128);
        assert_eq!(*quantized.last().unwrap(), 127);
    }

    #[test]
    fn test_memory_footprint_is_4x_smaller() {
        // i8 storage is 1 byte per dim vs 4 bytes for f32 -- this is the
        // whole point of scalar quantization for large local indices.
        let values = pseudo_random_floats(99, 1536, -1.0, 1.0);
        let (quantized, _params) = quantize(&values);

        let f32_bytes = values.len() * std::mem::size_of::<f32>();
        let i8_bytes = quantized.len() * std::mem::size_of::<i8>();

        assert_eq!(f32_bytes, i8_bytes * 4);
    }

    #[test]
    fn test_quantize_batch_round_trip() {
        let vectors = vec![
            pseudo_random_floats(1, 256, -1.0, 1.0),
            pseudo_random_floats(2, 256, 0.0, 1.0),
            vec![0.0; 256],
        ];
        let (quantized, params) = quantize_batch(&vectors);
        let reconstructed = dequantize_batch(&quantized, &params);

        for (orig, recon) in vectors.iter().zip(reconstructed.iter()) {
            let err = max_abs_error(orig, recon);
            let bound = {
                let min = orig.iter().cloned().fold(f32::INFINITY, f32::min);
                let max = orig.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                (max - min) / 255.0
            };
            assert!(
                err <= bound + 1e-4,
                "batch round-trip error {err} exceeded bound {bound}"
            );
        }
    }
}
