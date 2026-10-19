"""Opt-in int8-quantized vector storage.

`QuantizedVectorStore` is a small in-process vector store that keeps each
embedding as signed 8-bit integers plus a per-vector ``(scale, offset)`` pair.
It uses the real Rust primitives exposed by :mod:`pyvectorhound._core`
(``py_quantize_batch`` / ``py_dequantize_batch``), not a Python approximation.

Quantization is scalar (per-vector min/max), not product quantization, and
it is not SIMD/GPU accelerated. Retrieval dequantizes the stored vectors to
``float32`` and computes cosine similarity, so reconstructed embeddings have
bounded error (at most ``(max - min) / 255`` per component) while the stored
representation is ~4x smaller than ``float32``.

This store is intentionally opt-in on :class:`pyvectorhound.hound.Hound`.
Without it, Hound keeps its default float path through the database adapter.
"""

from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from pyvectorhound.database import VectorDB

try:
    from pyvectorhound import _core
except ImportError:
    _core = None


def _require_core() -> None:
    if _core is None:
        raise RuntimeError(
            "pyvectorhound._core is not available (the compiled Rust extension "
            "failed to import), so int8 quantization cannot run. Reinstall "
            "pyvectorhound with the compiled extension (a wheel, or "
            "`maturin develop` from source) rather than falling back to a "
            "fake/Python-only quantizer."
        )


def _as_vector(value: Any, name: str) -> np.ndarray:
    vector = np.asarray(value, dtype=np.float32)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be a 1-D vector, got shape {vector.shape}")
    if vector.size == 0:
        raise ValueError(f"{name} must not be empty")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} contains NaN or infinite values")
    return vector


class QuantizedVectorStore(VectorDB):
    """In-process vector store backed by per-vector int8 quantization.

    Vectors are quantized on ``add()`` and dequantized when they are read
    back by ``search()``/``get_embeddings()``. Document ids are stringified,
    matching the adapters in :mod:`pyvectorhound.database`.
    """

    def __init__(self) -> None:
        self._values: Dict[str, np.ndarray] = {}
        self._scales: Dict[str, float] = {}
        self._offsets: Dict[str, float] = {}
        self._dimension: Optional[int] = None

    def connect(self) -> None:
        """No-op: this store is already in process."""

    def __len__(self) -> int:
        return len(self._values)

    @property
    def dimension(self) -> Optional[int]:
        """Vector dimension, or None while the store is empty."""
        return self._dimension

    @property
    def is_empty(self) -> bool:
        return not self._values

    @property
    def ids(self) -> List[str]:
        """Stored document ids, in insertion order."""
        return list(self._values.keys())

    @property
    def quantized_bytes(self) -> int:
        """Bytes used by the int8 payload itself (excluding scales/offsets)."""
        return sum(values.nbytes for values in self._values.values())

    @property
    def float32_bytes(self) -> int:
        """Bytes the same vectors would occupy as float32."""
        return self.quantized_bytes * 4

    def add(self, ids: Sequence[Any], vectors: Sequence[Any]) -> List[str]:
        """Quantize and store ``vectors`` under ``ids``.

        Args:
            ids: One document id per vector. Existing ids are overwritten.
            vectors: One 1-D, finite embedding vector per id.

        Returns:
            The stored (stringified) ids, in input order.

        Raises:
            RuntimeError: If the compiled Rust extension is unavailable.
            ValueError: On length mismatch, empty/non-1-D/non-finite
                vectors, or a dimension inconsistent with the store.
        """
        _require_core()

        id_list = [str(doc_id) for doc_id in ids]
        vector_list = [_as_vector(vector, f"vectors[{i}]") for i, vector in enumerate(vectors)]

        if len(id_list) != len(vector_list):
            raise ValueError(
                f"ids and vectors must have the same length, got {len(id_list)} and "
                f"{len(vector_list)}"
            )
        if not id_list:
            return []

        dimensions = {vector.shape[0] for vector in vector_list}
        if len(dimensions) != 1:
            raise ValueError(
                "All vectors in one add() call must have the same dimension, "
                f"got {sorted(dimensions)}"
            )
        dimension = dimensions.pop()
        if self._dimension is not None and dimension != self._dimension:
            raise ValueError(
                f"Vector dimension {dimension} does not match this store's "
                f"existing dimension {self._dimension}"
            )

        quantized = _core.py_quantize_batch([vector.tolist() for vector in vector_list])
        for doc_id, values, params in zip(id_list, quantized["values"], quantized["params"]):
            self._values[doc_id] = np.asarray(values, dtype=np.int8)
            self._scales[doc_id] = float(params["scale"])
            self._offsets[doc_id] = float(params["offset"])

        self._dimension = dimension
        return id_list

    def get_embeddings(self, doc_ids: List[str]) -> Dict[str, np.ndarray]:
        """Dequantize and return stored embeddings for ``doc_ids``.

        Missing ids are omitted, matching the database adapters.
        """
        _require_core()

        present = [str(doc_id) for doc_id in doc_ids if str(doc_id) in self._values]
        if not present:
            return {}

        dequantized = _core.py_dequantize_batch(
            [self._values[doc_id].tolist() for doc_id in present],
            [self._scales[doc_id] for doc_id in present],
            [self._offsets[doc_id] for doc_id in present],
        )
        return {
            doc_id: np.asarray(vector, dtype=np.float32)
            for doc_id, vector in zip(present, dequantized)
        }

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search the quantized vectors by cosine similarity.

        Stored vectors are dequantized for scoring/return; the store itself
        retains only the int8 payload plus scales/offsets.

        Returns:
            A list of ``{"id", "score", "embedding"}`` dicts ordered by
            descending cosine similarity. Empty when the store has no
            vectors or ``top_k <= 0``.
        """
        _require_core()

        query = _as_vector(query_embedding, "query_embedding")
        if self._dimension is not None and query.shape[0] != self._dimension:
            raise ValueError(
                f"Query dimension {query.shape[0]} does not match stored vector "
                f"dimension {self._dimension}"
            )
        if not self._values or top_k <= 0:
            return []

        doc_ids = list(self._values.keys())
        embeddings = self.get_embeddings(doc_ids)
        matrix = np.vstack([embeddings[doc_id] for doc_id in doc_ids])

        query_norm = float(np.linalg.norm(query))
        if query_norm == 0.0:
            raise ValueError("query_embedding must have non-zero magnitude")

        matrix_norms = np.linalg.norm(matrix, axis=1)
        scores = matrix @ query / (matrix_norms * query_norm + 1e-12)
        order = np.argsort(-scores, kind="stable")[:top_k]

        return [
            {
                "id": doc_ids[index],
                "score": float(scores[index]),
                "embedding": np.asarray(matrix[index], dtype=np.float32),
            }
            for index in order
        ]

    def corpus_size(self) -> int:
        """Number of stored vectors."""
        return len(self._values)

    def clear(self) -> None:
        """Remove all stored vectors and reset the dimension."""
        self._values.clear()
        self._scales.clear()
        self._offsets.clear()
        self._dimension = None
