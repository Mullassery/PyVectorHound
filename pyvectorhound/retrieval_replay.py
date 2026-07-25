"""Interactive retrieval replay mode for debugging and optimization.

Enables instant testing of different configurations by replaying captured
retrieval traces with different components (embeddings, chunk sizes, DBs, etc).
"""

import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import numpy as np


class ComponentType(Enum):
    """Types of replaceable components."""

    EMBEDDING_MODEL = "embedding_model"
    CHUNK_SIZE = "chunk_size"
    VECTOR_DB = "vector_db"
    RERANKER = "reranker"
    HYBRID_FUSION = "hybrid_fusion"
    METADATA_FILTER = "metadata_filter"


@dataclass
class ReplayConfiguration:
    """Configuration for a replay test."""

    config_id: str
    components: Dict[ComponentType, Any]
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "config_id": self.config_id,
            "components": {k.value: v for k, v in self.components.items()},
            "description": self.description,
        }


@dataclass
class ReplayResult:
    """Result of a replay test."""

    config_id: str
    latency_ms: float
    results: List[Any]
    recall_at_k: Dict[int, float]
    precision_at_k: Dict[int, float]
    ndcg: float
    mrr: float
    improvement_pct: float
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ReplayComparison:
    """Comparison between two replay configurations."""

    baseline_config_id: str
    test_config_id: str
    baseline_result: ReplayResult
    test_result: ReplayResult
    latency_diff_ms: float
    latency_diff_pct: float
    recall_improvement_pct: float
    precision_improvement_pct: float
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class RetrievalReplayer:
    """Interactive retrieval replay engine.

    Replays captured retrieval traces with different configurations to test
    optimizations and debug issues.
    """

    def __init__(self):
        """Initialize replayer."""
        self.configurations: Dict[str, ReplayConfiguration] = {}
        self.results: Dict[str, ReplayResult] = {}
        self.baseline_result: Optional[ReplayResult] = None
        self._component_handlers: Dict[ComponentType, Callable] = {}

    def register_component_handler(
        self, component_type: ComponentType, handler: Callable
    ) -> None:
        """Register a handler for component swapping.

        Args:
            component_type: Type of component
            handler: Callable that takes (trace, component_value) -> results
        """
        self._component_handlers[component_type] = handler

    def create_configuration(
        self,
        config_id: str,
        components: Dict[ComponentType, Any],
        description: str = "",
    ) -> ReplayConfiguration:
        """Create a replay configuration.

        Args:
            config_id: Unique configuration ID
            components: Dict mapping component types to values
            description: Optional description

        Returns:
            ReplayConfiguration
        """
        config = ReplayConfiguration(
            config_id=config_id,
            components=components,
            description=description,
        )
        self.configurations[config_id] = config
        return config

    def replay(
        self,
        trace: Any,
        config_id: str,
        measure_latency: bool = True,
    ) -> ReplayResult:
        """Replay a trace with a specific configuration.

        Args:
            trace: RetrievalTrace to replay
            config_id: Configuration to use
            measure_latency: Whether to measure latency

        Returns:
            ReplayResult
        """
        config = self.configurations.get(config_id)
        if config is None:
            raise ValueError(f"Configuration {config_id} not found")

        # Start timer if measuring latency
        start_time = time.perf_counter() if measure_latency else None

        # Apply each component swap
        results = trace.vector_search_results.copy()
        metadata = {}

        for component_type, component_value in config.components.items():
            if component_type in self._component_handlers:
                handler = self._component_handlers[component_type]
                results, phase_metadata = handler(trace, component_value, results)
                metadata[component_type.value] = phase_metadata

        # Calculate metrics
        latency_ms = (time.perf_counter() - start_time) * 1000 if start_time else 0.0

        # Compute recall/precision at k
        recall_at_k = self._compute_recall_at_k(results)
        precision_at_k = self._compute_precision_at_k(results)
        ndcg = self._compute_ndcg(results)
        mrr = self._compute_mrr(results)

        # Compute improvement vs baseline
        improvement_pct = 0.0
        if self.baseline_result is not None:
            baseline_recall = self.baseline_result.recall_at_k.get(5, 0)
            current_recall = recall_at_k.get(5, 0)
            if baseline_recall > 0:
                improvement_pct = (current_recall - baseline_recall) / baseline_recall * 100

        result = ReplayResult(
            config_id=config_id,
            latency_ms=latency_ms,
            results=results,
            recall_at_k=recall_at_k,
            precision_at_k=precision_at_k,
            ndcg=ndcg,
            mrr=mrr,
            improvement_pct=improvement_pct,
            metadata=metadata,
        )

        self.results[config_id] = result

        # Set as baseline if this is the first replay
        if self.baseline_result is None:
            self.baseline_result = result

        return result

    def compare_configurations(
        self, config_id_1: str, config_id_2: str
    ) -> Optional[ReplayComparison]:
        """Compare two replay configurations.

        Args:
            config_id_1: First configuration ID
            config_id_2: Second configuration ID

        Returns:
            ReplayComparison or None if results don't exist
        """
        result1 = self.results.get(config_id_1)
        result2 = self.results.get(config_id_2)

        if result1 is None or result2 is None:
            return None

        latency_diff = result2.latency_ms - result1.latency_ms
        latency_diff_pct = (
            (latency_diff / result1.latency_ms * 100) if result1.latency_ms > 0 else 0
        )

        recall1 = result1.recall_at_k.get(5, 0)
        recall2 = result2.recall_at_k.get(5, 0)
        recall_improvement = (
            (recall2 - recall1) / max(recall1, 0.01) * 100 if recall1 > 0 else 0
        )

        precision1 = result1.precision_at_k.get(5, 0)
        precision2 = result2.precision_at_k.get(5, 0)
        precision_improvement = (
            (precision2 - precision1) / max(precision1, 0.01) * 100
            if precision1 > 0
            else 0
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(
            result1, result2, latency_diff_pct, recall_improvement
        )

        return ReplayComparison(
            baseline_config_id=config_id_1,
            test_config_id=config_id_2,
            baseline_result=result1,
            test_result=result2,
            latency_diff_ms=latency_diff,
            latency_diff_pct=latency_diff_pct,
            recall_improvement_pct=recall_improvement,
            precision_improvement_pct=precision_improvement,
            recommendation=recommendation,
        )

    def get_result(self, config_id: str) -> Optional[ReplayResult]:
        """Get replay result for a configuration.

        Args:
            config_id: Configuration ID

        Returns:
            ReplayResult or None
        """
        return self.results.get(config_id)

    def get_all_results(self) -> List[ReplayResult]:
        """Get all replay results.

        Returns:
            List of ReplayResult objects
        """
        return list(self.results.values())

    def rank_configurations_by_recall(self) -> List[ReplayResult]:
        """Rank configurations by recall@5.

        Returns:
            Sorted list of results (highest recall first)
        """
        return sorted(
            self.results.values(),
            key=lambda r: r.recall_at_k.get(5, 0),
            reverse=True,
        )

    def rank_configurations_by_latency(self) -> List[ReplayResult]:
        """Rank configurations by latency.

        Returns:
            Sorted list of results (lowest latency first)
        """
        return sorted(self.results.values(), key=lambda r: r.latency_ms)

    def rank_configurations_by_efficiency(self) -> List[ReplayResult]:
        """Rank configurations by efficiency (recall per millisecond).

        Returns:
            Sorted list of results (highest efficiency first)
        """
        def efficiency_score(result: ReplayResult) -> float:
            recall = result.recall_at_k.get(5, 0)
            latency = max(result.latency_ms, 1.0)
            return recall / latency

        return sorted(
            self.results.values(), key=efficiency_score, reverse=True
        )

    def get_configuration_report(self) -> Dict[str, Any]:
        """Get summary report of all replays.

        Returns:
            Dictionary with comparison data
        """
        if not self.results:
            return {}

        best_by_recall = self.rank_configurations_by_recall()[0]
        best_by_latency = self.rank_configurations_by_latency()[0]
        best_by_efficiency = self.rank_configurations_by_efficiency()[0]

        avg_latency = np.mean([r.latency_ms for r in self.results.values()])
        avg_recall = np.mean(
            [r.recall_at_k.get(5, 0) for r in self.results.values()]
        )

        return {
            "num_configurations_tested": len(self.results),
            "best_by_recall": {
                "config_id": best_by_recall.config_id,
                "recall_at_5": best_by_recall.recall_at_k.get(5, 0),
            },
            "best_by_latency": {
                "config_id": best_by_latency.config_id,
                "latency_ms": best_by_latency.latency_ms,
            },
            "best_by_efficiency": {
                "config_id": best_by_efficiency.config_id,
                "efficiency": best_by_efficiency.recall_at_k.get(5, 0) / max(best_by_efficiency.latency_ms, 1.0),
            },
            "average_latency_ms": avg_latency,
            "average_recall_at_5": avg_recall,
        }

    def _compute_recall_at_k(self, results: List[Any], k: int = 5) -> Dict[int, float]:
        """Compute recall@k metrics.

        Args:
            results: List of results
            k: Value of k

        Returns:
            Dict with recall@k metrics
        """
        recall_dict = {}
        for threshold in [1, 5, 10]:
            relevant = sum(
                1 for r in results[:threshold] if getattr(r, "is_relevant", False)
            )
            recall_dict[threshold] = relevant / threshold if threshold > 0 else 0

        return recall_dict

    def _compute_precision_at_k(
        self, results: List[Any], k: int = 5
    ) -> Dict[int, float]:
        """Compute precision@k metrics.

        Args:
            results: List of results
            k: Value of k

        Returns:
            Dict with precision@k metrics
        """
        precision_dict = {}
        for threshold in [1, 5, 10]:
            relevant = sum(
                1 for r in results[:threshold] if getattr(r, "is_relevant", False)
            )
            total_relevant = sum(1 for r in results if getattr(r, "is_relevant", False))
            precision_dict[threshold] = (
                relevant / total_relevant if total_relevant > 0 else 0
            )

        return precision_dict

    def _compute_ndcg(self, results: List[Any]) -> float:
        """Compute NDCG (Normalized Discounted Cumulative Gain).

        Args:
            results: List of results

        Returns:
            NDCG score (0-1)
        """
        dcg = sum(
            (1 if getattr(r, "is_relevant", False) else 0) / np.log2(i + 2)
            for i, r in enumerate(results[:10])
        )

        ideal_dcg = sum(1 / np.log2(i + 2) for i in range(min(10, len(results))))

        return dcg / ideal_dcg if ideal_dcg > 0 else 0

    def _compute_mrr(self, results: List[Any]) -> float:
        """Compute Mean Reciprocal Rank.

        Args:
            results: List of results

        Returns:
            MRR score (0-1)
        """
        for i, result in enumerate(results, 1):
            if getattr(result, "is_relevant", False):
                return 1 / i

        return 0.0

    def _generate_recommendation(
        self,
        result1: ReplayResult,
        result2: ReplayResult,
        latency_diff_pct: float,
        recall_improvement: float,
    ) -> str:
        """Generate recommendation based on comparison.

        Args:
            result1: Baseline result
            result2: Test result
            latency_diff_pct: Latency difference percentage
            recall_improvement: Recall improvement percentage

        Returns:
            Recommendation string
        """
        if recall_improvement > 10 and latency_diff_pct < 20:
            return "Recommended: Significant recall improvement with acceptable latency increase"
        elif recall_improvement > 5 and latency_diff_pct < 10:
            return "Recommended: Good recall improvement with minimal latency impact"
        elif recall_improvement < -5:
            return "Not recommended: Recall degradation"
        elif latency_diff_pct > 50:
            return "Not recommended: Unacceptable latency increase"
        else:
            return "Neutral: Marginal trade-offs"
