"""
PyVectorHound Example: Debugging RAG Retrieval

This example shows the two ways to run a diagnosis:

1. `Diagnosis` directly, when you already have retrieved results (e.g. from
   your own search pipeline) and just want them diagnosed. No live vector
   database required -- this is what's run below. To get real embedding-space
   metrics (isotropy/coverage/distinctiveness), `Diagnosis` fetches per-document
   vectors via `adapter.get_embeddings(doc_ids)`, so we pass a tiny in-memory
   adapter here; without one, the embedding component honestly reports
   "UNKNOWN" rather than a fabricated score.
2. `Hound`, which also runs the search for you against a live vector
   database (Qdrant, Chroma, Milvus, pgvector, or Weaviate). See the
   commented-out block at the bottom.

Run it: `python examples/retrieval_debug.py`
"""

import numpy as np

from pyvectorhound import Diagnosis


class InMemoryAdapter:
    """Minimal stand-in for a real VectorDB adapter, just for this example.

    Only implements `get_embeddings()`, since that's all `Diagnosis` needs
    to compute real embedding-space metrics. A real adapter (QdrantAdapter,
    ChromaAdapter, etc.) also implements `search()`/`connect()`/`corpus_size()`
    against your actual database.
    """

    def __init__(self, embeddings_by_id):
        self._embeddings_by_id = embeddings_by_id

    def get_embeddings(self, doc_ids):
        return {
            doc_id: self._embeddings_by_id[doc_id]
            for doc_id in doc_ids
            if doc_id in self._embeddings_by_id
        }


# A retrieval failure captured from your own RAG pipeline.
# (Random vectors here stand in for real document embeddings -- swap these
# for the real ones from your pipeline / vector DB.)
rng = np.random.default_rng(seed=0)
embeddings_by_id = {
    "pricing.pdf": rng.normal(size=384).astype(np.float32),
    "onboarding.md": rng.normal(size=384).astype(np.float32),
    "faq.md": rng.normal(size=384).astype(np.float32),
}
results = [
    {"id": doc_id, "score": score}
    for doc_id, score in [("pricing.pdf", 0.91), ("onboarding.md", 0.84), ("faq.md", 0.79)]
]

# The documents that *should* have been retrieved for this query.
expected_docs = ["returns.pdf", "policy.md"]

diagnosis = Diagnosis(
    query="What's your return policy?",
    results=results,
    expected_docs=expected_docs,
    adapter=InMemoryAdapter(embeddings_by_id),
)
diagnosis.analyze()

# Component-level metrics (embedding space health + retrieval accuracy).
# Real numbers computed via the Rust core (pyvectorhound._core) when it's
# built; "UNKNOWN"/"UNAVAILABLE" with an explanation otherwise -- never a
# fabricated placeholder.
metrics = diagnosis.metrics()
print("Embedding component:", metrics["embedding"]["status"])
print("Vector search component:", metrics["vector_search"]["status"])
print("BM25 component:", metrics["bm25"]["status"], "(no BM25 subsystem in this codebase)")
print("Reranker component:", metrics["reranker"]["status"], "(no reranker-score input on Diagnosis)")

# Root cause, in plain English
print(f"\nRoot cause: {diagnosis.root_cause()}")

# Ranked, actionable recommendations
for rec in diagnosis.recommendations():
    print(f"[{rec['priority']}] {rec['action']} (impact: {rec['impact']})")

# Full human-readable report
print(diagnosis.hunt())

# --- Using Hound against a live vector database ---------------------------
#
# from pyvectorhound import Hound
#
# hound = Hound(
#     db="qdrant",
#     endpoint="localhost:6333",
#     index_name="documents",
#     # PyVectorHound doesn't bundle an embedding model -- give it one:
#     embed_fn=lambda text: my_embedding_client.embed(text),
# )
# diagnosis = hound.diagnose(
#     query="What's your return policy?",
#     expected_docs=["returns.pdf", "policy.md"],
#     top_k=5,
# )
# print(diagnosis.hunt())
