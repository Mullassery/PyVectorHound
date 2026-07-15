# PyVectorHound Architecture & PyStreamMCP Integration

## Mission

**Debug & Optimize Retrieval**

Core Question: Why did this retrieval work (or fail)? How do we improve it?

## Core Responsibility

PyVectorHound is **exclusively responsible** for:

- **Retrieval Debugging** — Understanding why queries returned specific results
- **Relevance Analysis** — Scoring retrieved documents for relevance
- **Failure Analysis** — Root-cause analysis of retrieval failures
- **Replay & Forensics** — Replaying queries to debug issues
- **Quality Scoring** — Measuring retrieval quality
- **Attribution Analysis** — Tracing why a result was retrieved

## What We Do NOT Own

### ❌ Query Optimization (PyStreamMCP)
- Query planning
- Source discovery
- Token optimization
- Streaming retrieval
- Cost estimation

**Our role:** Debug & analyze queries that PyStreamMCP produces.

### ❌ Data Validation (StatGuardian)
- Schema validation
- Data freshness
- Drift detection

**Our role:** Assume data is valid, focus on why it was/wasn't retrieved.

## Critical: Use PyStreamMCP, Don't Rebuild It

**IMPORTANT:** PyVectorHound must integrate with PyStreamMCP rather than rebuilding query functionality.

### Architecture Pattern

```
Query
    ↓
PyStreamMCP (Optimization & Execution)
    ↓
Retrieval Results
    ↓
PyVectorHound (Debug & Analyze)
    ↓
Root Cause Analysis & Insights
    ↓
Feedback Loop to PyStreamMCP
```

### Integration Example

```python
# ✅ CORRECT: Use PyStreamMCP's query execution
from pystreammcp import Agent, QueryExecutor
from pyvectorhound import RetrievalDebugger

# Create query with PyStreamMCP
agent = Agent(agent_id="debug_query")
query_result = agent.query("customer data")

# Debug why this query returned these results
debugger = RetrievalDebugger(query_result)
analysis = debugger.analyze()
# - Why were these documents retrieved?
# - What sources were queried?
# - What was the token cost?
# - Could we have done better?

# Get root causes
root_causes = analysis.root_causes()
# - Low relevance due to source X
# - Token budget exceeded, missing source Y
# - Query optimization missed source Z

# Recommend improvements
improvements = analysis.recommend_improvements()
# - Use token_efficient strategy
# - Include source Z in next run
# - Adjust relevance threshold
```

### What NOT to Do

❌ **WRONG: Don't rebuild PyStreamMCP's functionality**

```python
# ❌ DO NOT DO THIS
class QueryOptimizer:
    def discover_sources(self):  # ← PyStreamMCP owns this
        pass
    
    def optimize_for_tokens(self):  # ← PyStreamMCP owns this
        pass
    
    def estimate_cost(self):  # ← PyStreamMCP owns this
        pass
```

Instead, use PyStreamMCP's QueryExecutor:
```python
# ✅ DO THIS
from pystreammcp import QueryExecutor

executor = QueryExecutor()
result = executor.execute_query(optimized_query)

# Then debug the result
debugger = RetrievalDebugger(result)
```

### Why?

PyStreamMCP already provides:
- ✓ Query planning & optimization
- ✓ Context discovery (6+ framework integrations)
- ✓ 7 optimization techniques
- ✓ Cost tracking & estimation
- ✓ Token efficiency (60-75% reduction)
- ✓ Streaming execution
- ✓ Multi-agent optimization

Rebuilding this in PyVectorHound would:
- Duplicate 1000+ lines of code
- Miss learned optimizations
- Create maintenance burden
- Break integration with PyStreamMCP

## Focused Responsibility

PyVectorHound excels at what it's built for:

✓ **Why did retrieval fail?**
- Which sources had no matches?
- Why were expected documents missing?
- Did token budget cause truncation?
- Was relevance threshold too high?

✓ **Can we do better?**
- Which optimization would help most?
- Should we use different sources?
- Can we adjust token allocation?
- What does the replay show?

✓ **Root Cause Analysis**
- 8-failure taxonomy
- Automatic classification
- Replay debugging
- Forensic analysis

## Integration Points

### With PyStreamMCP (Primary Integration)

```python
from pystreammcp import QueryExecutor, Agent
from pyvectorhound import RetrievalDebugger, RootCauseAnalyzer

# Execute query using PyStreamMCP
executor = QueryExecutor()
result = executor.execute_query(
    query="customer data",
    strategy="token_efficient"
)

# Debug the result
debugger = RetrievalDebugger(result)
analysis = debugger.analyze()

# Get root causes using PyVectorHound's forensics
analyzer = RootCauseAnalyzer()
causes = analyzer.analyze(analysis)

# Example causes:
# - TokenBudgetExceeded: "Missing source X due to token limit"
# - LowRelevanceScore: "Document below 0.5 threshold"
# - SourceNotQueried: "Source Y not discovered by PyStreamMCP"
```

### With StatGuardian

```python
from statguardian import ValidationGate
from pyvectorhound import RetrievalDebugger

# Check if data is valid before analyzing
validation = ValidationGate.check(source="customer_data")

if validation.is_valid():
    # Safe to debug
    debugger = RetrievalDebugger(result)
else:
    # Data quality issue, not a retrieval issue
    print(f"Data quality issue: {validation.error}")
```

## Module Structure

```
src/
├── debugger.rs           # Core retrieval debugging
├── analyzer.rs           # Root cause analysis
├── failure_taxonomy.rs   # 8 failure types
├── replay.rs             # Query replay for debugging
├── forensics/            # Forensic analysis
│   ├── source_analysis.rs
│   ├── relevance_analysis.rs
│   └── token_analysis.rs
└── storage/              # Debug data persistence
```

## Philosophy

PyVectorHound is to retrieval debugging what a debugger is to code execution.

- A code debugger doesn't write programs, it debugs them
- A database profiler doesn't optimize queries, it analyzes them
- PyVectorHound doesn't optimize retrieval, it debugs it

PyStreamMCP handles optimization. PyVectorHound explains why it worked or didn't.

## Outcome

When properly integrated:

```
Query Submitted
        ↓
PyStreamMCP executes with optimizations
        ↓
Results Retrieved
        ↓
PyVectorHound analyzes the result
        ↓
Root cause identified
        ↓
Feedback to PyStreamMCP for next run
        ↓
Continuous Improvement
```

PyStreamMCP optimizes. PyVectorHound debugs. Together they form a complete retrieval intelligence system.
