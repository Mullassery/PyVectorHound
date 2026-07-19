# OKF Integration Guide for PyVectorHound

**Status:** Phase 1-2 Complete  
**Version:** v0.1  
**Date:** 2026-07-20

---

## Overview

PyVectorHound now features a native OKF-based diagnostic knowledge base that persists, learns, and improves recommendations from every retrieval failure analyzed.

OKF enables:
- **Persistent memory** — Every diagnosis becomes searchable history
- **Pattern learning** — Identify recurring failures automatically
- **Success tracking** — Learn which fixes actually work
- **Autonomous optimization** — Agents access diagnostic KB directly

---

## Quick Start

### 1. Initialize Diagnostic KB

```python
from pathlib import Path
from pyvectorhound.okf_diagnostics import OKFDiagnosticKnowledgeBase

# Create KB (auto-creates directory structure)
kb = OKFDiagnosticKnowledgeBase(Path("./diagnostic_kb"))
```

### 2. Record Diagnostic Findings

```python
# After diagnosing a retrieval failure
kb.record_diagnosis(
    query_id="query_20260720_001",
    root_cause="Chunking Problems",
    confidence=0.91,
    failure_types=["Chunking Problems", "Context Assembly Problems"],
    recommendations=[
        {
            "strategy": "Split to 400-token chunks with 50-token overlap",
            "effort_hours": 2,
            "expected_improvement": 0.27,
            "roi": "10-50x"
        },
        {
            "strategy": "Use overlapping chunks",
            "effort_hours": 1,
            "expected_improvement": 0.15,
            "roi": "5-20x"
        }
    ],
    context={
        "corpus_size": "1GB",
        "embedding_model": "text-embedding-3-small",
        "chunk_size_current": 2000
    }
)
```

### 3. Learn from Historical Patterns

```python
# Find similar failures
similar = kb.find_similar_failures("Chunking Problems", max_results=5)

for finding in similar:
    print(f"Query {finding.query_id}: {finding.confidence*100:.0f}% confidence")
    print(f"Recommendations: {[r['strategy'] for r in finding.recommendations]}")

# Extract recurring patterns
patterns = kb.extract_patterns(min_frequency=2)

for pattern in patterns:
    print(f"{pattern['pattern']}: {pattern['frequency']} of cases")
    print(f"  Success rate: {pattern['avg_success_rate']}")
```

### 4. Enhanced Recommendations from History

```python
# Get recommendations ranked by historical success
initial_recs = [
    {
        "strategy": "Split to 400-token chunks",
        "effort_hours": 2,
        "expected_improvement": 0.27
    },
    {
        "strategy": "Switch to domain-specific embedding",
        "effort_hours": 4,
        "expected_improvement": 0.35
    }
]

enhanced = kb.generate_enhanced_recommendations("Chunking Problems", initial_recs)

for i, rec in enumerate(enhanced, 1):
    print(f"{i}. {rec['strategy']}")
    if rec.get('historical_success_rate') is not None:
        print(f"   Historical success: {rec['historical_success_rate']*100:.1f}%")
    print(f"   Effort: {rec['effort_hours']}h, ROI: {rec['roi']}")
```

---

## Directory Structure

```
diagnostic_kb/
├── findings/                 # Individual diagnosis records
│   ├── query_001.md
│   ├── query_002.md
│   └── query_003.md
├── playbooks/                # Repair strategy guides
│   ├── chunking_problems_playbook.md
│   ├── embedding_quality_playbook.md
│   └── vector_search_issues_playbook.md
├── patterns/                 # Recurring failure analysis
├── component_profiles/       # Embedding/DB/Reranker profiles
└── [Auto-generated indices]
```

---

## OKF Document Examples

### Diagnostic Finding (`findings/query_001.md`)
```yaml
---
type: diagnosis-finding
query_id: query_20260720_001
root_cause: Chunking Problems
confidence: 0.91
failure_types:
  - Chunking Problems
  - Context Assembly Problems
recommendations:
  - strategy: Split to 400-token chunks
    effort_hours: 2
    expected_improvement: 0.27
    roi: "10-50x"
  - strategy: Use overlapping chunks
    effort_hours: 1
    expected_improvement: 0.15
    roi: "5-20x"
timestamp: 2026-07-20T12:30:00
corpus_size: "1GB"
embedding_model: text-embedding-3-small
chunk_size_current: 2000
---

# Query query_20260720_001 - Retrieval Failure Diagnosis

## Root Cause
**Chunking Problems** (91% confidence)

## Failure Analysis
- Chunking Problems
- Context Assembly Problems

## Recommendations

### Recommendation 1: Split to 400-token chunks
- Effort: 2 hours
- Expected Improvement: 27.0%
- ROI: 10-50x

### Recommendation 2: Use overlapping chunks
- Effort: 1 hours
- Expected Improvement: 15.0%
- ROI: 5-20x
```

---

## API Reference

### OKFDiagnosticKnowledgeBase

```python
from pyvectorhound.okf_diagnostics import OKFDiagnosticKnowledgeBase

kb = OKFDiagnosticKnowledgeBase(Path("./diagnostic_kb"))

# Record a diagnosis
path = kb.record_diagnosis(
    query_id="query_001",
    root_cause="Root Cause",
    confidence=0.85,
    failure_types=["Type1", "Type2"],
    recommendations=[{"strategy": "Fix", "effort_hours": 1}],
    context={"key": "value"}
)

# Find similar failures
similar = kb.find_similar_failures("Root Cause", max_results=10)
for finding in similar:
    print(f"{finding.query_id}: {finding.confidence*100:.0f}%")

# Get success rate for a strategy
rate = kb.get_success_rate_for_strategy("Split to 400-token chunks")
if rate:
    print(f"Success rate: {rate*100:.1f}%")

# Extract patterns
patterns = kb.extract_patterns(min_frequency=2)
for pattern in patterns:
    print(f"{pattern['pattern']}: {pattern['frequency']}")

# Enhance recommendations
enhanced = kb.generate_enhanced_recommendations(
    "Chunking Problems",
    initial_recommendations
)

# Reload from disk
kb.reload()
```

### Pattern Analysis

```python
# Get all patterns
all_patterns = kb.extract_patterns(min_frequency=1)

# Filter by frequency
common_patterns = kb.extract_patterns(min_frequency=5)

# Each pattern includes:
# - pattern: Root cause name
# - frequency: "23.4%"
# - count: 12
# - avg_success_rate: "78.5%"
# - okf_link: Path to playbook
```

---

## Integration with Hound

### Auto-Save Findings

```python
from pyvectorhound.hound import Hound
from pyvectorhound.okf_diagnostics import OKFDiagnosticKnowledgeBase

hound = Hound(db="qdrant", endpoint="http://localhost:6333")
kb = OKFDiagnosticKnowledgeBase(Path("./diagnostic_kb"))

# Diagnose a retrieval failure
diagnosis = hound.diagnose(
    queries=["find customer named John"],
    retrieved_docs=retrieved,
    relevant_docs=relevant
)

# Auto-save to OKF
kb.record_diagnosis(
    query_id=diagnosis.query_id,
    root_cause=diagnosis.root_cause,
    confidence=diagnosis.confidence,
    failure_types=diagnosis.failure_types,
    recommendations=diagnosis.recommendations
)

# Use enhanced recommendations from KB
enhanced = kb.generate_enhanced_recommendations(
    diagnosis.root_cause,
    diagnosis.recommendations
)

print("Top recommendation (ranked by success):")
print(f"- {enhanced[0]['strategy']}")
print(f"- Success rate: {enhanced[0].get('historical_success_rate', 'N/A')}")
```

### Pattern-Driven Optimization

```python
# Detect emerging patterns
patterns = kb.extract_patterns(min_frequency=3)

for pattern in patterns:
    print(f"Alert: {pattern['pattern']} affects {pattern['frequency']} of cases")

# When pattern frequency > threshold, create alert
critical_patterns = [p for p in patterns if float(p['frequency'].rstrip('%')) > 20]

if critical_patterns:
    print("Critical failure patterns detected:")
    for p in critical_patterns:
        print(f"  - {p['pattern']}: {p['frequency']}")
        print(f"    Success rate of existing fixes: {p['avg_success_rate']}")
```

---

## Advanced Usage

### Agent-Driven Autonomous Debugging

```python
from pyvectorhound.okf_diagnostics import OKFDiagnosticKnowledgeBase

kb = OKFDiagnosticKnowledgeBase(Path("./diagnostic_kb"))

# Agent workflow
async def autonomous_rag_debugger(queries):
    for query in queries:
        # 1. Diagnose
        diagnosis = hound.diagnose(query)
        
        # 2. Check historical patterns
        similar = kb.find_similar_failures(diagnosis.root_cause)
        
        # 3. Get enhanced recommendations
        enhanced = kb.generate_enhanced_recommendations(
            diagnosis.root_cause,
            diagnosis.recommendations
        )
        
        # 4. Execute highest-success recommendation
        if enhanced and enhanced[0].get('historical_success_rate', 0) > 0.7:
            fix = apply_fix(enhanced[0]['strategy'])
            
            # 5. Monitor results
            new_diagnosis = hound.diagnose(query)
            
            # 6. Record outcome
            kb.record_diagnosis(
                query_id=new_diagnosis.query_id,
                root_cause=new_diagnosis.root_cause,
                confidence=new_diagnosis.confidence,
                failure_types=new_diagnosis.failure_types,
                recommendations=enhanced,
                context={
                    "fix_applied": enhanced[0]['strategy'],
                    "actual_improvement": calculate_improvement(diagnosis, new_diagnosis)
                }
            )
```

### Tracking Fix Outcomes

```python
# After applying a fix, record the actual improvement
kb.record_diagnosis(
    query_id="query_001_retry",
    root_cause=initial_diagnosis.root_cause,
    confidence=0.5,  # Lower since we're retesting
    failure_types=initial_diagnosis.failure_types,
    recommendations=initial_diagnosis.recommendations,
    context={
        "fix_applied": "Split to 400-token chunks",
        "actual_improvement": 0.28,  # Measured improvement
        "parent_query": "query_001"
    }
)

# Now the KB learns from outcomes
success_rate = kb.get_success_rate_for_strategy("Split to 400-token chunks")
# Returns (0.28 + 0.27) / 2 = 0.275 = 27.5%
```

---

## Testing

Run OKF diagnostic tests:
```bash
python -m pytest tests/test_okf_diagnostics.py -v
```

All tests pass (18 tests):
- Document loading
- KB operations
- Pattern extraction
- Strategy success tracking
- Recommendation enhancement
- KB reloading

---

## Migration Guide

### From Transient Diagnostics to Persistent KB

**Before:**
```python
hound = Hound()
diagnosis = hound.diagnose(...)
print(diagnosis)
# Findings are lost!
```

**After:**
```python
hound = Hound()
kb = OKFDiagnosticKnowledgeBase(Path("./diagnostic_kb"))

diagnosis = hound.diagnose(...)
kb.record_diagnosis(...)  # Persist finding
kb.reload()

# KB now contains searchable history
similar = kb.find_similar_failures(diagnosis.root_cause)
patterns = kb.extract_patterns()
```

---

## Future Enhancements

**Planned (v0.3+):**
- Cross-project linking with PyStreamMCP query plans
- Autonomous recommendation ranking based on KB statistics
- Visual failure pattern dashboards
- Export patterns to GitHub issues
- Playbook generation from successful cases

**Roadmap:**
- Integration with Langfuse/LangSmith
- Cost-benefit analysis per recommendation
- A/B testing framework
- Multi-tenant KB support

---

## Contributing

Diagnostic findings improve the entire community:

1. Make fixes and record outcomes
2. KB learns patterns from your data
3. Submit patterns to GitHub discussions
4. Community benefits from your insights

Share successful fixes by creating PRs to `diagnostic_kb/playbooks/`

---

## References

- **Google OKF Spec:** https://github.com/GoogleCloudPlatform/knowledge-catalog
- **PyVectorHound Docs:** https://github.com/Mullassery/PyVectorHound
- **Retrieval Failure Taxonomy:** See strategic vision document
