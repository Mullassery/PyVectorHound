# PyVectorHound: Retrieval Forensics Agent

## Core Mission

**When retrieval fails in production RAG, you tell users exactly where the failure occurred and how to fix it.**

Not: "Retrieved chunks look irrelevant."  
But: "Root cause: Chunk size 2000 tokens. Relevant answer split across 3 chunks, none individually sufficient. Fix: Split to 400-token chunks. Expected Recall@10 improvement: +31%."

---

## Market Position

**Retrieval Debugger for AI Applications**
- Like: Datadog for APM → PyVectorHound for Retrieval
- Like: Chrome DevTools → PyVectorHound for RAG Pipelines
- Like: Splunk → PyVectorHound for Retrieval Logs

**Why this matters:**
- Every RAG system fails at retrieval (the most common failure point)
- Teams currently have NO way to diagnose WHY
- Cost to debug: 20-40 engineering hours per incident
- You eliminate that debugging cost entirely

---

## The 8-Category Retrieval Failure Taxonomy

### 1. Embedding Quality Issues
**Questions:**
- Did the embedding model understand the query?
- Did it place relevant chunks close in vector space?
- Is the embedding model domain-appropriate?

**Diagnostics:**
- Query embedding visualization
- Chunk clustering analysis
- Embedding drift detection (model versioning issues)
- Similarity distribution analysis
- Vocabulary gap detection (domain-specific terminology)

**Example Finding:**
```
ROOT CAUSE: Embedding Quality
Confidence: 94%
Details: Query uses medical terminology ("nephrology", "glomerular"). 
Embedding model trained on general web text. Relevant chunks rank 
below position 200 while off-topic generic chunks rank higher.
Fix: Switch to domain-specific embeddings (e.g., SciBERT, BioBERT).
Expected improvement: Recall@10 +47%
```

### 2. Chunking Problems (Most Common Failure)
**Questions:**
- Is chunk size too large?
- Is chunk size too small?
- Was semantic boundary violated?

**Diagnostics:**
- Chunk overlap analysis
- Semantic boundary detection (table/code/list preservation)
- Parent-child chunk inspection
- Retrieval coverage score (does top-K contain answer?)

**Example Finding:**
```
ROOT CAUSE: Chunking Strategy
Confidence: 91%
Details: Answer spans 3 consecutive chunks. No single chunk contains 
sufficient evidence for retrieval. Chunk size = 2000 tokens (too large).
Relevant sentence buried at character position 1,800 in middle chunk.
Fix: Reduce chunk size to 500 tokens with 50-token overlap.
Expected improvement: Recall@10 +27%
```

### 3. Vector Search Problems
**Questions:**
- Is ANN search missing neighbors?
- Is recall acceptable?
- Is index configuration optimal?

**Diagnostics:**
- Exact KNN vs ANN comparison (Recall@K)
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (NDCG)
- Lost-neighbor analysis
- Index parameter diagnostics (HNSW M, efSearch, efConstruction)

**Example Finding:**
```
ROOT CAUSE: Vector Search Configuration
Confidence: 88%
Details: HNSW index with efSearch=40 missing 28% of relevant 
documents vs exact search. Index construction underspecified.
Fix: Increase efSearch from 40 to 150. Rebuild index with 
efConstruction=600. Latency impact: +35ms.
Expected improvement: Recall@20 +28%, latency: 50ms → 85ms
```

### 4. Hybrid Search Problems
**Questions:**
- Should BM25 have found this?
- Did vector search fail but keyword search succeed?

**Diagnostics:**
- BM25 score distribution
- Dense vs Sparse comparison
- Fusion score analysis (RRF, weighted, etc.)
- Ranking correlation

**Example Finding:**
```
ROOT CAUSE: Hybrid Search Imbalance
Confidence: 85%
Details: Dense retrieval ranks correct chunk at #89. 
BM25 ranks it at #2. Fusion (RRF) produces rank #5.
Issue: Dense embeddings underperforming for this query type 
(exact keyword matching critical). Fusion weights: Dense 0.6, Sparse 0.4.
Fix: Adjust fusion weights to Dense 0.3, Sparse 0.7 for factual queries.
Expected improvement: Recall@5 +18%
```

### 5. Metadata Filtering Problems (Common in Production)
**Questions:**
- Are filters excluding relevant results?
- Is metadata missing from indexed documents?

**Diagnostics:**
- Filter impact analysis (recall before/after)
- Missing metadata detection
- Overly restrictive filter detection

**Example Finding:**
```
ROOT CAUSE: Metadata Filter Suppression
Confidence: 96%
Details: Query filtered by Region=US excludes 92% of relevant 
documents. Answer is in UK documentation. ACL filter prevents 
access to cross-region knowledge base.
Fix: Expand region filter to EU OR US. Update ACL policy.
Expected improvement: Recall@10 +42%
```

### 6. Reranker Problems
**Questions:**
- Did reranking improve or harm results?
- Did reranking demote correct chunks?

**Diagnostics:**
- Before vs After ranking comparison
- Pairwise relevance analysis
- Rank movement charts (which chunks moved where and why)

**Example Finding:**
```
ROOT CAUSE: Reranker Miscalibration
Confidence: 89%
Details: Cross-encoder moved most relevant chunk from Rank 1 to Rank 12.
Reranker model trained on short-form content; fails on long documents.
Confidence scores: Rank 1 chunk: 0.92 → 0.31 after reranking.
Fix: Fine-tune reranker on enterprise document corpus or disable 
for documents > 1000 tokens.
Expected improvement: Recall@5 +35%
```

### 7. Context Assembly Problems
**Questions:**
- Retrieved correctly but assembled poorly?
- Context budget exhausted?

**Diagnostics:**
- Token budget utilization analysis
- Context truncation detection
- Duplicate chunk detection

**Example Finding:**
```
ROOT CAUSE: Context Truncation
Confidence: 93%
Details: Relevant chunk #2 retrieved successfully (top 10).
Token budget: 2000 tokens. Chunks #1-#3 injected, but chunk #3 
truncated at 80% completion before reaching LLM context window.
Fix: Increase context budget to 3000 tokens or prioritize chunks 
by BM25 score.
Expected improvement: Answer completeness +22%
```

### 8. Answer Generation Problems
**Questions:**
- Retrieval perfect but model ignored context?
- Did model hallucinate?

**Diagnostics:**
- Citation coverage analysis
- Grounding score (how much answer grounded in context)
- Context utilization score

**Example Finding:**
```
ROOT CAUSE: LLM Hallucination
Confidence: 82%
Details: Top 5 retrieved chunks contain "pricing starts at $299/month".
LLM answer states "starts at $199/month" (hallucinated, not in context).
Grounding score: 34% (low). Model ignoring retrieval evidence.
Fix: Use stronger grounding constraint or switch to smaller model 
with better instruction-following.
Expected improvement: Factual accuracy +41%
```

---

## Product Architecture: The Retrieval Inspection Pipeline

```
User Query
    ↓
┌─────────────────────────────────┐
│   Query Understanding Inspector │
│  - Ambiguity detection          │
│  - Entity extraction            │
│  - Query rewriting analysis     │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Embedding Quality Inspector    │
│  - Model compatibility          │
│  - Vocabulary gaps              │
│  - Embedding drift              │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Vector Search Inspector        │
│  - Recall@K metrics             │
│  - Exact vs ANN comparison      │
│  - Index diagnostics            │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  BM25 Search Inspector          │
│  - Keyword coverage             │
│  - Term frequency analysis      │
│  - Sparse retrieval quality     │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Metadata Filter Inspector      │
│  - Filter impact (recall loss)  │
│  - Missing metadata detection   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Fusion & Reranking Inspector   │
│  - Fusion effectiveness         │
│  - Rank movement analysis       │
│  - Reranker calibration         │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Context Assembly Inspector     │
│  - Token budget analysis        │
│  - Truncation detection         │
│  - Duplicate detection          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Answer Grounding Inspector     │
│  - Citation coverage            │
│  - Hallucination detection      │
│  - Context utilization          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Root Cause Engine              │
│  - Synthesize failures          │
│  - Confidence scoring           │
│  - Causal inference             │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Recommendation Engine          │
│  - Immediate fixes              │
│  - Medium-term improvements     │
│  - Long-term architecture       │
│  - ROI estimation               │
└─────────────────────────────────┘
    ↓
Forensic Report (Executive + Technical)
```

---

## Killer Feature: Retrieval Replay Mode

Like Chrome DevTools Network tab, but for RAG retrieval.

**For every query, capture:**
```json
{
  "query": "What is our enterprise pricing?",
  "embedding_model": "text-embedding-3-large",
  "retrieved": {
    "rank_1": {"chunk": "...", "score": 0.89},
    "rank_2": {"chunk": "...", "score": 0.87},
    "rank_3": {"chunk": "...", "score": 0.84}
  },
  "reranked": {
    "rank_1": {"chunk": "...", "score": 0.95},
    "rank_2": {"chunk": "...", "score": 0.89},
    "rank_3": {"chunk": "...", "score": 0.87}
  },
  "context_injected": ["chunk_A", "chunk_B"],
  "answer": "...",
  "grounding_score": 0.87
}
```

**Then enable instant replay by swapping components:**

- 🔄 Swap embedding models (OpenAI → Voyage → BGE)
- 🔄 Swap chunk sizes (512 → 1024 → 2048 tokens)
- 🔄 Swap vector DB (Qdrant → Weaviate → Pinecone)
- 🔄 Swap rerankers (None → BGE → Cohere)
- 🔄 Swap hybrid search fusion (RRF → weighted → custom)
- 🔄 Swap metadata filters (apply/remove)

**Instant feedback:**
```
Before: Recall@10 = 42%
After (chunk_size=500): Recall@10 = 76% ✅
Time to recompute: 340ms
```

This single feature eliminates 80% of RAG debugging iterations.

---

## AI-Powered Root Cause Analysis

**The Real Moat:**

Not dashboards. Not charts. But an agent that says:

> "Retrieval failed because:
> 
> **Primary:** Chunk size 2000 tokens (91% confidence)  
> Evidence: Relevant answer spans 3 non-overlapping chunks.
> 
> **Secondary:** Embedding model gap (67% confidence)  
> Evidence: Medical terminology ranked below generic content.
> 
> **Recommended Fix:** Split to 400-token chunks with 50-token overlap.
> This requires: 2 hours engineering + 1 hour reindexing.
> Expected result: Recall@10 improves from 42% to 76%.
> Cost impact: Index size +18%, query latency -2% (fewer chunks to rerank)."

This is **single-sentence problem diagnosis** + **structured fix recommendations** + **ROI estimates**.

---

## Enterprise Integration Roadmap

### Database Support (Phase 1)
- ✓ Qdrant (HTTP API)
- ✓ Weaviate (GraphQL API)
- ✓ Milvus (gRPC + REST)
- ✓ Chroma (local + server)
- ✓ PostgreSQL pgvector (SQL)
- ◐ Pinecone (API)
- ◐ Elasticsearch (REST)
- ◐ OpenSearch (REST)
- ◐ Vespa (REST)

### Framework Integration (Phase 2)
- ◐ LangChain integration
- ◐ LlamaIndex integration
- ◐ OpenAI Responses API integration
- ◐ Anthropic Claude integration

### Observability (Phase 3)
- ◐ Distributed tracing (OpenTelemetry)
- ◐ Prometheus metrics export
- ◐ JSON/JSONL logging
- ◐ Cloud logging (CloudWatch, GCP Logging, Datadog)

### Testing & Regression (Phase 4)
- ◐ Golden query datasets
- ◐ Evaluation benchmarks (Recall, NDCG, MRR)
- ◐ Retrieval regression testing
- ◐ Retrieval CI/CD pipelines
- ◐ Performance SLA tracking

### Advanced Analytics (Phase 5)
- ◐ Embedding drift detection (monitor distribution changes over time)
- ◐ Relevance score calibration
- ◐ Cost optimization recommendations
- ◐ Latency analysis and bottleneck detection

---

## Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| **Time to Root Cause** | <5 min | vs 20-40 hours manual debugging |
| **Fix Confidence** | >85% | Correct diagnosis first time |
| **Adoption** | 40%+ RAG teams | Every team debugging retrieval |
| **ROI** | 10-50x | Massive engineering time savings |
| **MTTR** | <15 min | Incident resolution time |

---

## Competitive Advantages

| Feature | Datadog | LangSmith | Arize | **PyVectorHound** |
|---------|---------|-----------|-------|------------------|
| Query-level diagnostics | ❌ | ❌ | ❌ | ✅ |
| Retrieval replay mode | ❌ | ✅ (partial) | ❌ | ✅ |
| 8-category failure taxonomy | ❌ | ❌ | ❌ | ✅ |
| Embedding quality analysis | ❌ | ❌ | ✅ | ✅ |
| Chunking diagnostics | ❌ | ❌ | ❌ | ✅ |
| Vector search recall@K | ❌ | ❌ | ✅ | ✅ |
| BM25 analysis | ❌ | ❌ | ❌ | ✅ |
| Hybrid search diagnostics | ❌ | ❌ | ❌ | ✅ |
| Context assembly analysis | ❌ | ❌ | ❌ | ✅ |
| Answer grounding score | ✅ | ✅ | ✅ | ✅ |
| Root cause automation | ❌ | ❌ | ❌ | ✅ |
| Multi-DB support (10+) | ❌ | ✅ | ❌ | ✅ |

---

## MVP Definition

### Phase 1: Core Diagnostics (Weeks 1-4)
Implement all 8 inspectors:
1. ✓ Query Understanding Inspector
2. ✓ Embedding Quality Inspector
3. ✓ Vector Search Inspector (Recall@K)
4. ✓ BM25 Inspector
5. ✓ Metadata Filter Inspector
6. ✓ Reranker Inspector
7. ✓ Context Assembly Inspector
8. ✓ Answer Grounding Inspector

**Output:** Forensic Report with structured diagnosis

### Phase 2: Root Cause Engine (Weeks 5-6)
1. Synthesize failures across inspectors
2. Rank by confidence
3. Output: "Primary cause: X (89% confidence)"

### Phase 3: Replay Mode (Weeks 7-8)
1. Capture full retrieval trace
2. Implement embedding model swapping
3. Implement chunk size swapping
4. Implement vector DB swapping
5. Implement reranker swapping

### Phase 4: AI-Powered Recommendations (Weeks 9-10)
1. LLM-generated fix suggestions
2. ROI estimation (engineering effort + expected gain)
3. Side-effect analysis (latency, cost impact)

### Phase 5: Enterprise Integration (Weeks 11-12)
1. Database adapters (Qdrant, Weaviate, Milvus, Pinecone)
2. Framework integrations (LangChain, LlamaIndex)
3. Cloud logging (OpenTelemetry)

---

## Positioning Statement

### NOT:
- "Another RAG platform"
- "Another vector database"
- "Another observability dashboard"

### YES:
**"Retrieval Debugger for AI Applications"**

*When your RAG retrieval fails, PyVectorHound tells you exactly where and why — then recommends fixes with ROI estimates. Like Chrome DevTools for retrieval pipelines.*

---

## The End-to-End User Experience

### Step 1: Setup (2 minutes)
```python
from pyvectorhound import Hound

hound = Hound(
    vector_db="qdrant",
    vector_db_url="http://localhost:6333",
    embeddings_model="text-embedding-3-large"
)
```

### Step 2: Capture Query (Automatic)
```python
# In your RAG pipeline:
query = "What is our enterprise pricing?"
retrieved_chunks = vector_db.search(query, top_k=10)
answer = llm.generate(context=retrieved_chunks, prompt=query)

# One-liner diagnosis:
diagnosis = hound.diagnose(
    query=query,
    retrieved_chunks=retrieved_chunks,
    answer=answer
)
```

### Step 3: Get Forensic Report
```
RETRIEVAL FORENSICS REPORT
==========================

Query: "What is our enterprise pricing?"

PRIMARY FAILURE
Root Cause: Chunking Strategy
Confidence: 91%
Explanation: Answer spans 3 chunks but no single chunk sufficient. 
            Chunk size = 2000 tokens (too large).

SECONDARY FAILURES
- Embedding model gap (67% confidence)
- Context truncation (45% confidence)

RECOMMENDED FIXES

Immediate (0.5 hours):
  → Reduce chunk size 2000 → 500 tokens (50-token overlap)
  → Expected improvement: Recall@10 +27%
  → Latency impact: +15ms
  → Cost impact: +12% index size

Medium-term (4 hours):
  → Fine-tune embeddings on domain-specific corpus
  → Expected improvement: Recall@10 +15%

Long-term (20 hours):
  → Implement hierarchical retrieval (chunk → section → document)
  → Expected improvement: NDCG@5 +22%

NEXT STEPS
1. Apply chunk size fix (estimated benefit: +27% recall)
2. Run A/B test: old vs new chunking on 100 golden queries
3. Monitor for regressions
```

### Step 4: Instant Replay
```python
# Try different settings:
replay = hound.replay(
    query=query,
    settings={
        'chunk_size': 500,          # was 2000
        'embedding_model': 'BGE',   # was OpenAI
        'reranker': 'cohere'        # was none
    }
)

print(f"Recall@10 before: 42%")
print(f"Recall@10 after:  76%")  # ← Real-time feedback
```

---

## Why PyVectorHound Wins

1. **Solves the #1 RAG failure point** — Retrieval, not generation
2. **Saves 20-40 engineering hours per incident** — Eliminates manual debugging
3. **Works with ANY vector database** — Qdrant, Weaviate, Pinecone, pgvector, Milvus
4. **Works with ANY framework** — LangChain, LlamaIndex, custom
5. **Single diagnosis → single fix** — Not "maybe it's X, maybe Y"
6. **ROI transparent** — Every fix shows expected improvement + effort + cost
7. **Replay mode** — Test 100 variations instantly (not days of manual testing)
8. **No hallucinations** — Every diagnosis backed by empirical data

---

## The Future

Year 1: Become the industry standard for retrieval debugging (every RAG team using PyVectorHound)

Year 2: Expand to observability (real-time retrieval monitoring, anomaly detection, drift detection)

Year 3: Retrieval-aware model selection (which embedding model / reranker / chunk strategy for YOUR data?)
