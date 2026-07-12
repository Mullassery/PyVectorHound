# PyVectorhound Roadmap

**Current Version:** v1.0.0  
**Last Updated:** July 2026  
**Status:** Good for debugging RAG systems; production monitoring not ready

---

## Known Limitations (v1.0.0)

### 🔴 Blocking Issues
None identified for debugging use case.

### 🟡 Experimental Features
- **Latency claims:** README claims "45ms diagnosis" but **unvalidated**
  - [ ] Timing depends heavily on embedding model, vector DB, dataset size
  - [ ] Claim is based on limited test data
  - [ ] Real-world latency unknown on your data
  - **Impact:** Don't rely on latency guarantees for production
  - **Fix timeline:** v1.1.0 (Q3 2026) with real benchmarking

- **Competitor benchmarks:** "4-19x faster than Phoenix/Arize" is **unvalidated**
  - [ ] Comparison based on limited tests
  - [ ] Different use cases may have different results
  - **Impact:** Use for evaluation, not comparison decisions
  - **Fix timeline:** v2.0.0 (Q1 2027) with independent validation

- **Root cause analysis:** Listed as feature but actually **recommendations**
  - [ ] Provides suggestions, not always root causes
  - [ ] Requires human interpretation
  - **Impact:** Use as guidance, not automatic fixes
  - **Fix timeline:** v1.2.0 (Q4 2026) with better explanations

- **Drift detection:** Listed in features but **incomplete**
  - [ ] Skeleton exists
  - [ ] Statistical tests not implemented
  - **Impact:** No built-in drift monitoring; track embedding quality separately
  - **Fix timeline:** v1.3.0 (Q4 2026)

### 🟢 Shipping/Stable (v1.0.0)
- ✅ Component isolation (embedding, vector search, keyword, reranker)
- ✅ Database-agnostic (Qdrant, Chroma, Milvus, Weaviate, pgvector)
- ✅ Embedding quality evaluation
- ✅ Model comparison framework
- ✅ Actionable recommendations (plain English)

---

## 🔒 Security Issues (See SECURITY_AUDIT.md)

### CRITICAL — v1.0.1
- [ ] **Audit SQL injection patterns** (5 instances found)

### HIGH — v1.0.1
- [ ] **Pin all dependency versions** (0 pinned, 16 floating)
- [ ] **Secure API key handling** (use SecretStr from pydantic)

### MEDIUM — v1.1.0
- [ ] **Input validation** (malformed query objects)
- [ ] **Error handling** (don't leak database schema)

---

## TODOs in Code
3 found related to:
- Latency benchmarking
- Drift detection implementation
- Competitor comparison validation

---

## Roadmap

### v1.0.1 (Q3 2026) — Documentation
- [ ] Update README: Remove unvalidated latency claims
- [ ] Remove Phoenix/Arize comparison (or add disclaimer)
- [ ] Clarify recommendations vs root causes
- [ ] Add real-world examples

### v1.1.0 (Q3 2026) — Benchmarking
- [ ] Actual latency testing on multiple datasets
- [ ] Hardware-specific performance profiles
- [ ] Recommended configurations for <100ms diagnosis

### v1.2.0 (Q4 2026) — Better Diagnostics
- [ ] More detailed root cause analysis
- [ ] Automated fix suggestions with ROI
- [ ] Confidence scores for recommendations

### v1.3.0 (Q4 2026) — Drift Detection
- [ ] Embedding quality monitoring
- [ ] Vector DB performance tracking
- [ ] Alerting on degradation

### v2.0.0 (Q1 2027) — Production Monitoring
- [ ] Continuous monitoring (not one-off diagnostics)
- [ ] Dashboard for RAG metrics
- [ ] Integration with observability platforms
- [ ] Historical tracking

---

## Not Planned
- Automatic remediation (recommendations only)
- Real-time inference patching
- Custom embedding model training
- Closed-loop improvement loops
