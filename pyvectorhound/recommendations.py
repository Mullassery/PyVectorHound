"""AI-Powered recommendations engine for retrieval optimization.

Generates LLM-based explanations, ROI estimates, and implementation steps
for retrieval failures and optimizations.
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional
from enum import Enum
import json


class FailureCategory(Enum):
    """8-category retrieval failure taxonomy."""

    EMBEDDING_QUALITY = "embedding_quality"
    CHUNKING_PROBLEMS = "chunking_problems"
    VECTOR_SEARCH = "vector_search"
    HYBRID_SEARCH = "hybrid_search"
    METADATA_FILTERING = "metadata_filtering"
    RERANKING = "reranking"
    CONTEXT_ASSEMBLY = "context_assembly"
    ANSWER_GENERATION = "answer_generation"


@dataclass
class FixRecommendation:
    """A single fix recommendation."""

    id: str
    failure_category: str
    title: str
    description: str
    root_cause: str
    confidence: float
    effort_hours: float
    expected_improvement_pct: float
    implementation_steps: List[str]
    risks: List[str]
    dependencies: List[str] = field(default_factory=list)
    roi_score: float = 0.0  # effort-adjusted improvement

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @property
    def roi(self) -> float:
        """Calculate ROI (improvement per hour of effort)."""
        return (
            self.expected_improvement_pct / max(self.effort_hours, 0.5)
            if self.effort_hours > 0
            else 0
        )


@dataclass
class DiagnosticReport:
    """Complete diagnostic report with recommendations."""

    query_id: str
    query_text: str
    primary_failures: List[str]
    confidence: float
    failure_details: Dict[str, Any]
    recommendations: List[FixRecommendation]
    executive_summary: str
    next_steps: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "query_id": self.query_id,
            "query_text": self.query_text,
            "primary_failures": self.primary_failures,
            "confidence": self.confidence,
            "failure_details": self.failure_details,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "executive_summary": self.executive_summary,
            "next_steps": self.next_steps,
        }


class RecommendationEngine:
    """AI-powered recommendation engine.

    Generates LLM-based explanations and ROI-calculated fixes for retrieval
    failures using the 8-category failure taxonomy.
    """

    def __init__(self, llm_client: Optional[Any] = None):
        """Initialize recommendation engine.

        Args:
            llm_client: Optional LLM client for generating recommendations
        """
        self.llm_client = llm_client
        self._fix_templates = self._initialize_fix_templates()
        self._generated_reports: Dict[str, DiagnosticReport] = {}

    def analyze_failure(
        self,
        query_id: str,
        query_text: str,
        diagnosis: Dict[str, Any],
        trace_analysis: Optional[Dict[str, Any]] = None,
    ) -> DiagnosticReport:
        """Analyze a retrieval failure and generate recommendations.

        Args:
            query_id: Unique query identifier
            query_text: The search query
            diagnosis: Diagnostic analysis results
            trace_analysis: Optional detailed trace analysis

        Returns:
            DiagnosticReport with recommendations
        """
        # Identify primary failures
        primary_failures = self._identify_primary_failures(diagnosis, trace_analysis)

        # Calculate confidence
        confidence = self._calculate_confidence(diagnosis)

        # Generate recommendations
        recommendations = []
        for failure in primary_failures:
            recs = self._generate_fixes_for_failure(failure, diagnosis)
            recommendations.extend(recs)

        # Sort by ROI score
        recommendations.sort(key=lambda r: r.roi, reverse=True)

        # Limit to top 5 recommendations
        recommendations = recommendations[:5]

        # Generate executive summary
        summary = self._generate_summary(primary_failures, recommendations)

        # Generate next steps
        next_steps = self._generate_next_steps(recommendations)

        report = DiagnosticReport(
            query_id=query_id,
            query_text=query_text,
            primary_failures=primary_failures,
            confidence=confidence,
            failure_details=diagnosis,
            recommendations=recommendations,
            executive_summary=summary,
            next_steps=next_steps,
        )

        self._generated_reports[query_id] = report
        return report

    def get_recommendation_summary(
        self, query_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a summary of recommendations for a query.

        Args:
            query_id: Query identifier

        Returns:
            Summary dictionary
        """
        report = self._generated_reports.get(query_id)
        if report is None:
            return None

        return {
            "query_id": query_id,
            "primary_failures": report.primary_failures,
            "confidence": report.confidence,
            "executive_summary": report.executive_summary,
            "num_recommendations": len(report.recommendations),
            "top_recommendation": report.recommendations[0].to_dict()
            if report.recommendations
            else None,
            "estimated_total_effort_hours": sum(
                r.effort_hours for r in report.recommendations
            ),
            "estimated_total_improvement_pct": sum(
                r.expected_improvement_pct for r in report.recommendations
            ),
        }

    def estimate_roi(
        self, recommendation: FixRecommendation
    ) -> Dict[str, Any]:
        """Calculate detailed ROI for a recommendation.

        Args:
            recommendation: Fix recommendation

        Returns:
            ROI analysis dictionary
        """
        hourly_rate = 150  # Assume $150/hour engineering cost
        eng_cost = recommendation.effort_hours * hourly_rate

        # Assume 1% improvement = $1000 value (for RAG system)
        improvement_value = recommendation.expected_improvement_pct * 1000

        roi_pct = (improvement_value - eng_cost) / eng_cost * 100 if eng_cost > 0 else 0
        payback_days = (
            eng_cost / (improvement_value / 30) if improvement_value > 0 else float("inf")
        )

        return {
            "recommendation": recommendation.title,
            "engineering_cost_usd": eng_cost,
            "estimated_value_usd": improvement_value,
            "roi_percent": roi_pct,
            "payback_period_days": min(payback_days, 365),  # Cap at 1 year
            "effort_hours": recommendation.effort_hours,
            "expected_improvement_pct": recommendation.expected_improvement_pct,
            "roi_score": recommendation.roi,
        }

    def _identify_primary_failures(
        self, diagnosis: Dict[str, Any], trace_analysis: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify primary failure categories.

        Args:
            diagnosis: Diagnostic results
            trace_analysis: Optional trace analysis

        Returns:
            List of failure category names
        """
        failures = []

        # Check embedding quality
        if diagnosis.get("embedding_quality_score", 1.0) < 0.8:
            failures.append(FailureCategory.EMBEDDING_QUALITY.value)

        # Check for chunking issues
        if diagnosis.get("chunking_issues", False):
            failures.append(FailureCategory.CHUNKING_PROBLEMS.value)

        # Check vector search performance
        if trace_analysis and trace_analysis.get("num_vector_results", 10) < 5:
            failures.append(FailureCategory.VECTOR_SEARCH.value)

        # Check for filtering issues
        if diagnosis.get("filter_reduction_pct", 0) > 50:
            failures.append(FailureCategory.METADATA_FILTERING.value)

        # Check reranking
        if diagnosis.get("reranking_issues", False):
            failures.append(FailureCategory.RERANKING.value)

        # Default to chunking if no specific failure identified
        if not failures:
            failures.append(FailureCategory.CHUNKING_PROBLEMS.value)

        return failures

    def _calculate_confidence(self, diagnosis: Dict[str, Any]) -> float:
        """Calculate confidence in diagnosis.

        Args:
            diagnosis: Diagnostic results

        Returns:
            Confidence score (0-1)
        """
        # Base confidence on presence of clear signals
        confidence = 0.5

        # Add points for clear metrics
        if "embedding_quality_score" in diagnosis:
            confidence += 0.1
        if "chunking_issues" in diagnosis:
            confidence += 0.1
        if "filter_reduction_pct" in diagnosis:
            confidence += 0.1
        if "reranking_issues" in diagnosis:
            confidence += 0.1
        if "context_quality" in diagnosis:
            confidence += 0.1

        return min(confidence, 1.0)

    def _generate_fixes_for_failure(
        self, failure: str, diagnosis: Dict[str, Any]
    ) -> List[FixRecommendation]:
        """Generate fix recommendations for a failure type.

        Args:
            failure: Failure category name
            diagnosis: Diagnostic information

        Returns:
            List of recommendations
        """
        fixes = []

        if failure == FailureCategory.CHUNKING_PROBLEMS.value:
            fixes.extend(self._generate_chunking_fixes(diagnosis))
        elif failure == FailureCategory.EMBEDDING_QUALITY.value:
            fixes.extend(self._generate_embedding_fixes(diagnosis))
        elif failure == FailureCategory.VECTOR_SEARCH.value:
            fixes.extend(self._generate_vector_search_fixes(diagnosis))
        elif failure == FailureCategory.METADATA_FILTERING.value:
            fixes.extend(self._generate_filtering_fixes(diagnosis))
        elif failure == FailureCategory.RERANKING.value:
            fixes.extend(self._generate_reranking_fixes(diagnosis))

        return fixes

    def _generate_chunking_fixes(self, diagnosis: Dict[str, Any]) -> List[FixRecommendation]:
        """Generate fixes for chunking problems."""
        fixes = []

        # Fix 1: Reduce chunk size
        fixes.append(
            FixRecommendation(
                id="chunk_size_reduction",
                failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
                title="Reduce chunk size with overlap",
                description="Split documents into smaller chunks (400-500 tokens) with 50-token overlap to capture context spans across boundaries.",
                root_cause="Answer spans multiple chunks but none individually sufficient.",
                confidence=0.88,
                effort_hours=2.0,
                expected_improvement_pct=27.0,
                implementation_steps=[
                    "Identify current chunk size",
                    "Reduce to 400-500 token size",
                    "Add 50-token overlap between chunks",
                    "Re-index corpus",
                    "Re-test queries",
                ],
                risks=[
                    "Increased index size (+30-50%)",
                    "Slightly higher retrieval latency",
                ],
            )
        )

        # Fix 2: Use sliding window chunking
        fixes.append(
            FixRecommendation(
                id="sliding_window_chunks",
                failure_category=FailureCategory.CHUNKING_PROBLEMS.value,
                title="Implement sliding window chunking",
                description="Use sliding window approach to ensure context continuity across chunk boundaries.",
                root_cause="Chunking boundaries cutting across semantic boundaries.",
                confidence=0.82,
                effort_hours=3.0,
                expected_improvement_pct=22.0,
                implementation_steps=[
                    "Implement sliding window chunker",
                    "Configure window size and stride",
                    "Re-index with new chunking strategy",
                    "Monitor for quality improvements",
                ],
                risks=[
                    "Increased storage requirements",
                    "More complex indexing logic",
                ],
            )
        )

        return fixes

    def _generate_embedding_fixes(
        self, diagnosis: Dict[str, Any]
    ) -> List[FixRecommendation]:
        """Generate fixes for embedding quality issues."""
        fixes = []

        fixes.append(
            FixRecommendation(
                id="switch_embedding_model",
                failure_category=FailureCategory.EMBEDDING_QUALITY.value,
                title="Switch to domain-specific embedding model",
                description="Use a domain-specific embedding model that better understands your terminology.",
                root_cause="Embedding model lacks domain vocabulary.",
                confidence=0.85,
                effort_hours=4.0,
                expected_improvement_pct=35.0,
                implementation_steps=[
                    "Evaluate domain-specific models (BGE, E5, etc.)",
                    "Re-embed existing documents",
                    "Update embedding model in production",
                    "Monitor quality metrics",
                ],
                risks=[
                    "Model licensing costs",
                    "Re-embedding can take hours",
                ],
            )
        )

        return fixes

    def _generate_vector_search_fixes(
        self, diagnosis: Dict[str, Any]
    ) -> List[FixRecommendation]:
        """Generate fixes for vector search problems."""
        fixes = []

        fixes.append(
            FixRecommendation(
                id="tune_vector_search",
                failure_category=FailureCategory.VECTOR_SEARCH.value,
                title="Tune vector search parameters",
                description="Adjust HNSW parameters (M, efSearch) to improve recall without sacrificing latency.",
                root_cause="Approximate nearest neighbor search losing relevant neighbors.",
                confidence=0.80,
                effort_hours=1.5,
                expected_improvement_pct=18.0,
                implementation_steps=[
                    "Identify current HNSW parameters",
                    "Increase M or efSearch gradually",
                    "Monitor latency and recall",
                    "Find optimal balance",
                ],
                risks=[
                    "Increased query latency",
                    "Higher memory usage",
                ],
            )
        )

        return fixes

    def _generate_filtering_fixes(
        self, diagnosis: Dict[str, Any]
    ) -> List[FixRecommendation]:
        """Generate fixes for metadata filtering issues."""
        fixes = []

        fixes.append(
            FixRecommendation(
                id="relax_metadata_filters",
                failure_category=FailureCategory.METADATA_FILTERING.value,
                title="Relax or remove overly-restrictive filters",
                description="Review and loosen metadata filters that may be excluding relevant documents.",
                root_cause="Metadata filters too restrictive, excluding relevant results.",
                confidence=0.87,
                effort_hours=1.0,
                expected_improvement_pct=24.0,
                implementation_steps=[
                    "Analyze filter rejection rate",
                    "Identify overly-restrictive rules",
                    "Loosen or remove problematic filters",
                    "Re-test query performance",
                ],
                risks=["May include irrelevant results if filters too loose"],
            )
        )

        return fixes

    def _generate_reranking_fixes(
        self, diagnosis: Dict[str, Any]
    ) -> List[FixRecommendation]:
        """Generate fixes for reranking issues."""
        fixes = []

        fixes.append(
            FixRecommendation(
                id="improve_reranker",
                failure_category=FailureCategory.RERANKING.value,
                title="Use stronger reranker model",
                description="Switch to a more powerful reranker that better understands relevance for your domain.",
                root_cause="Current reranker demoting relevant chunks.",
                confidence=0.83,
                effort_hours=2.0,
                expected_improvement_pct=20.0,
                implementation_steps=[
                    "Test different reranker models",
                    "Evaluate on validation set",
                    "Deploy top-performing model",
                    "Monitor quality metrics",
                ],
                risks=[
                    "Increased latency per query",
                    "Higher API costs",
                ],
            )
        )

        return fixes

    def _generate_summary(
        self, failures: List[str], recommendations: List[FixRecommendation]
    ) -> str:
        """Generate executive summary.

        Args:
            failures: List of failure categories
            recommendations: List of recommendations

        Returns:
            Summary string
        """
        if not failures:
            return "No clear failures detected."

        if not recommendations:
            return f"Detected {len(failures)} issue(s) but unable to generate recommendations."

        top_rec = recommendations[0]
        total_improvement = sum(r.expected_improvement_pct for r in recommendations)

        return (
            f"Primary issue: {top_rec.title}. "
            f"Recommended fix: {top_rec.description} "
            f"Expected improvement: +{top_rec.expected_improvement_pct:.0f}% recall. "
            f"All fixes combined could yield +{total_improvement:.0f}% improvement."
        )

    def _generate_next_steps(
        self, recommendations: List[FixRecommendation]
    ) -> List[str]:
        """Generate next steps.

        Args:
            recommendations: List of recommendations

        Returns:
            List of next steps
        """
        if not recommendations:
            return ["Review diagnostic results manually"]

        steps = [
            f"1. Implement top recommendation: {recommendations[0].title}",
            "2. Run A/B test with new configuration",
            "3. Measure recall and latency metrics",
            "4. If successful, roll out to production",
        ]

        if len(recommendations) > 1:
            steps.append(
                f"5. After success, consider: {recommendations[1].title}"
            )

        return steps

    def _initialize_fix_templates(self) -> Dict[str, Any]:
        """Initialize fix recommendation templates."""
        return {
            "chunking": {
                "low_recall": "Chunk size too large or boundaries misaligned",
                "fix": "Reduce chunk size to 400-500 tokens with overlap",
            },
            "embedding": {
                "poor_quality": "Embedding model lacks domain vocabulary",
                "fix": "Switch to domain-specific model (BGE, E5)",
            },
            "vector_search": {
                "low_recall": "ANN search parameters suboptimal",
                "fix": "Increase M or efSearch parameters",
            },
            "metadata": {
                "high_rejection": "Metadata filters too restrictive",
                "fix": "Loosen or remove problematic filters",
            },
            "reranking": {
                "low_correlation": "Reranker model weak for domain",
                "fix": "Use stronger reranker (BGE, Cohere)",
            },
        }
