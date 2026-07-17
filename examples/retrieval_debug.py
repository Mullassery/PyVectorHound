"""
PyVectorhound Example: Debugging RAG Retrieval

This example shows how to:
1. Capture a retrieval failure
2. Diagnose root cause
3. Get optimization recommendations
"""

from pyvectorhound import VectorHound

# Initialize debugger
debugger = VectorHound()

# Your RAG query that's failing
query = "What is the capital of France?"
retrieved_docs = []  # Empty retrieval result

# Diagnose the failure
diagnosis = debugger.diagnose_failure(
    query=query,
    retrieved_docs=retrieved_docs,
    expected_answer="Paris"
)

# View component-level diagnostics
print("Embedding quality:", diagnosis.embedding_score)
print("Vector search quality:", diagnosis.vector_search_score)
print("Retrieval rank:", diagnosis.rank)

# Get root cause
root_cause = diagnosis.get_root_cause()
print(f"Root cause: {root_cause}")

# Get recommendations
recommendations = diagnosis.get_recommendations()
for rec in recommendations:
    print(f"✓ {rec['action']}: ROI = {rec['roi']}")
