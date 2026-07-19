"""OKF diagnostic knowledge base for PyVectorHound.

Stores and retrieves retrieval failure diagnostics as OKF documents.
Enables pattern learning and autonomous recommendations from historical findings.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import frontmatter
except ImportError:
    raise ImportError(
        "python-frontmatter is required for OKF support. "
        "Install with: pip install python-frontmatter"
    )


class OKFDiagnosticDocument:
    """Represents a diagnostic finding as an OKF document."""

    def __init__(self, path: Path):
        """Load diagnostic document from disk.

        Args:
            path: Path to .md file with diagnostic finding
        """
        self.path = path
        self.post = frontmatter.load(str(path))
        self.metadata = self.post.metadata
        self.content = self.post.content

    @property
    def query_id(self) -> str:
        """Unique query identifier."""
        return self.metadata.get("query_id", self.path.stem)

    @property
    def root_cause(self) -> str:
        """Root cause of retrieval failure."""
        return self.metadata.get("root_cause", "unknown")

    @property
    def confidence(self) -> float:
        """Confidence score (0-1)."""
        return self.metadata.get("confidence", 0.0)

    @property
    def failure_types(self) -> List[str]:
        """List of failure categories detected."""
        return self.metadata.get("failure_types", [])

    @property
    def recommendations(self) -> List[Dict[str, Any]]:
        """List of repair recommendations."""
        return self.metadata.get("recommendations", [])

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get arbitrary metadata field."""
        return self.metadata.get(key, default)


class OKFDiagnosticKnowledgeBase:
    """Persistent OKF-based diagnostic knowledge base."""

    def __init__(self, kb_dir: Path):
        """Initialize diagnostic knowledge base.

        Args:
            kb_dir: Root directory for diagnostic storage
        """
        self.kb_dir = Path(kb_dir)
        self.findings: Dict[str, OKFDiagnosticDocument] = {}
        self.patterns: Dict[str, List[OKFDiagnosticDocument]] = {}
        self._ensure_structure()
        self._load_all()

    def _ensure_structure(self) -> None:
        """Create KB directory structure if missing."""
        subdirs = ["findings", "playbooks", "patterns", "component_profiles"]
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        for subdir in subdirs:
            (self.kb_dir / subdir).mkdir(exist_ok=True)

    def _load_all(self) -> None:
        """Load all diagnostic findings from disk."""
        self.findings.clear()
        self.patterns.clear()

        findings_dir = self.kb_dir / "findings"
        if findings_dir.exists():
            for doc_path in findings_dir.glob("*.md"):
                try:
                    doc = OKFDiagnosticDocument(doc_path)
                    self.findings[doc.query_id] = doc

                    # Index by root cause pattern
                    root_cause = doc.root_cause
                    if root_cause not in self.patterns:
                        self.patterns[root_cause] = []
                    self.patterns[root_cause].append(doc)
                except Exception as e:
                    print(f"Warning: Failed to load {doc_path}: {e}")

    def record_diagnosis(self, query_id: str, root_cause: str,
                        confidence: float, failure_types: List[str],
                        recommendations: List[Dict[str, Any]],
                        context: Optional[Dict[str, Any]] = None) -> Path:
        """Save a diagnosis as OKF document.

        Args:
            query_id: Unique identifier for this query
            root_cause: Primary failure category
            confidence: Confidence score (0-1)
            failure_types: List of failure categories detected
            recommendations: Repair strategies with ROI estimates
            context: Additional context about the failure

        Returns:
            Path to saved document
        """
        if context is None:
            context = {}

        # Render recommendation section
        recs_md = ""
        for i, rec in enumerate(recommendations, 1):
            recs_md += f"""### Recommendation {i}: {rec.get('strategy', 'Unknown')}
- Effort: {rec.get('effort_hours', 0)} hours
- Expected Improvement: {rec.get('expected_improvement', 0)*100:.1f}%
- ROI: {rec.get('roi', 'N/A')}

"""

        content = f"""# Query {query_id} - Retrieval Failure Diagnosis

## Root Cause
**{root_cause}** ({confidence*100:.0f}% confidence)

## Failure Analysis
"""

        for failure_type in failure_types:
            content += f"- {failure_type}\n"

        content += f"\n## Recommendations\n{recs_md}"

        # Create frontmatter metadata
        metadata = {
            "type": "diagnosis-finding",
            "query_id": query_id,
            "root_cause": root_cause,
            "confidence": confidence,
            "failure_types": failure_types,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat(),
            **context
        }

        # Save as OKF document
        doc_path = self.kb_dir / "findings" / f"{query_id}.md"

        post = frontmatter.Post(content)
        post.metadata = metadata
        doc_path.write_text(frontmatter.dumps(post))

        # Reload to sync index
        self._load_all()

        return doc_path

    def find_similar_failures(self, root_cause: str, max_results: int = 10) -> List[OKFDiagnosticDocument]:
        """Find historical failures matching a root cause.

        Args:
            root_cause: Root cause to search for
            max_results: Maximum results to return

        Returns:
            List of matching diagnostic documents
        """
        matching = self.patterns.get(root_cause, [])

        # Sort by confidence (highest first)
        sorted_matches = sorted(
            matching,
            key=lambda doc: doc.confidence,
            reverse=True
        )

        return sorted_matches[:max_results]

    def get_playbook(self, failure_type: str) -> Optional[Path]:
        """Get repair playbook for a failure type.

        Args:
            failure_type: Type of failure

        Returns:
            Path to playbook file or None
        """
        playbook_path = self.kb_dir / "playbooks" / f"{failure_type}_playbook.md"
        return playbook_path if playbook_path.exists() else None

    def extract_patterns(self, min_frequency: int = 3) -> List[Dict[str, Any]]:
        """Extract recurring failure patterns from KB.

        Args:
            min_frequency: Minimum occurrence count to be considered a pattern

        Returns:
            List of pattern dictionaries
        """
        pattern_list = []
        total_findings = len(self.findings)

        if total_findings == 0:
            return pattern_list

        for root_cause, findings in self.patterns.items():
            count = len(findings)
            percentage = (count / total_findings) * 100

            if count >= min_frequency:
                # Calculate average success of recommendations
                avg_success_rate = 0.0
                if findings:
                    success_rates = []
                    for finding in findings:
                        actual_improvement = finding.get_metadata("actual_improvement", 0)
                        if actual_improvement:
                            success_rates.append(actual_improvement)

                    if success_rates:
                        avg_success_rate = sum(success_rates) / len(success_rates)

                pattern_list.append({
                    "pattern": root_cause,
                    "frequency": f"{percentage:.1f}%",
                    "count": count,
                    "avg_success_rate": f"{avg_success_rate*100:.1f}%",
                    "okf_link": f"playbooks/{root_cause.lower().replace(' ', '_')}_playbook.md"
                })

        # Sort by frequency
        return sorted(pattern_list, key=lambda x: float(x["frequency"].rstrip("%")), reverse=True)

    def get_success_rate_for_strategy(self, strategy: str) -> Optional[float]:
        """Calculate historical success rate for a repair strategy.

        Args:
            strategy: Strategy name to analyze

        Returns:
            Success rate (0-1) or None if no data
        """
        success_rates = []

        for finding in self.findings.values():
            for rec in finding.recommendations:
                if rec.get("strategy") == strategy:
                    actual_improvement = finding.get_metadata("actual_improvement")
                    if actual_improvement is not None:
                        success_rates.append(actual_improvement)

        if not success_rates:
            return None

        return sum(success_rates) / len(success_rates)

    def generate_enhanced_recommendations(self, root_cause: str,
                                         recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance recommendations with historical success data.

        Args:
            root_cause: Root cause of failure
            recommendations: Initial recommendations

        Returns:
            Enhanced recommendations ranked by success rate
        """
        enhanced = []

        for rec in recommendations:
            strategy = rec.get("strategy")
            success_rate = self.get_success_rate_for_strategy(strategy)

            enhanced_rec = rec.copy()
            if success_rate is not None:
                enhanced_rec["historical_success_rate"] = success_rate
                enhanced_rec["confidence_boost"] = success_rate * 0.2  # 20% confidence boost per success rate
            else:
                enhanced_rec["historical_success_rate"] = None

            enhanced.append(enhanced_rec)

        # Sort by historical success rate
        enhanced.sort(
            key=lambda r: r.get("historical_success_rate") or 0,
            reverse=True
        )

        return enhanced

    def reload(self) -> None:
        """Reload KB from disk (useful after external changes)."""
        self._load_all()
