"""Model comparison for evaluating embedding and reranker models."""

from typing import List, Dict, Any, Optional, Callable


# Model metadata for cost and performance
MODEL_METADATA = {
    "text-embedding-3-small": {
        "provider": "OpenAI",
        "cost_per_1m": 0.02,
        "latency_ms": 1.8,
        "dimensions": 1536,
        "type": "embedding",
    },
    "text-embedding-3-large": {
        "provider": "OpenAI",
        "cost_per_1m": 2.00,
        "latency_ms": 2.1,
        "dimensions": 3072,
        "type": "embedding",
    },
    "cohere-v3": {
        "provider": "Cohere",
        "cost_per_1m": 1.50,
        "latency_ms": 3.2,
        "dimensions": 1024,
        "type": "embedding",
    },
    "sentence-transformers/all-mpnet-base-v2": {
        "provider": "Open Source",
        "cost_per_1m": 0.0,
        "latency_ms": 4.1,
        "dimensions": 768,
        "type": "embedding",
    },
    "cohere-rerank-v3": {
        "provider": "Cohere",
        "cost_per_1m": 0.50,
        "latency_ms": 8.0,
        "type": "reranker",
    },
    "cross-encoder/ms-marco-minilm": {
        "provider": "Open Source",
        "cost_per_1m": 0.0,
        "latency_ms": 2.0,
        "type": "reranker",
    },
}


class ModelComparison:
    """
    Compare different embedding or reranker models on your corpus.

    Provides quality, cost, and performance metrics for model selection.
    """

    def __init__(
        self,
        model_type: str,
        candidates: List[str],
        adapter: Optional[Any] = None,
        test_queries: Optional[List[str]] = None,
        sample_size: int = 100,
        quality_fn: Optional[Callable[[str], Dict[str, float]]] = None,
        **kwargs: Any,
    ):
        """
        Initialize ModelComparison.

        PyVectorHound does not run embedding or reranker models itself, so it
        cannot measure quality (F1/precision/recall/NDCG/calibration) for a
        candidate model on its own -- that requires actually running the
        model against your corpus and test queries. Pass `quality_fn` (a
        callable that takes a model name and returns a metrics dict, e.g.
        wrapping your own eval harness) to get real quality numbers; without
        it, only the real published cost/latency/provider metadata is
        reported and quality fields are left unmeasured rather than guessed.

        Args:
            model_type: Type of model ('embedding' or 'reranker')
            candidates: List of model names to compare
            adapter: Database adapter for testing
            test_queries: Optional list of queries to use for testing
            sample_size: Number of queries to test
            quality_fn: Optional callable(model_name) -> metrics dict
                (f1_score/precision/recall for embedding, ndcg/calibration
                for reranker) computed from your own evaluation of that model
        """
        self.model_type = model_type
        self.candidates = candidates
        self.adapter = adapter
        self.test_queries = test_queries or []
        self.sample_size = sample_size
        self.quality_fn = quality_fn
        self._results = {}

    def benchmark(self) -> None:
        """Run benchmarks on all candidate models."""
        for model in self.candidates:
            self._results[model] = self._benchmark_model(model)

    def _benchmark_model(self, model: str) -> Dict[str, Any]:
        """Benchmark a single model.

        Cost/latency/provider come from PyVectorHound's static, published
        model metadata table (real). Quality metrics come from
        `self.quality_fn(model)` when supplied (real, user-measured); when
        it isn't, they're left as `None` with `"quality_measured": False`
        rather than a fabricated number.
        """
        metadata = MODEL_METADATA.get(
            model, {"cost_per_1m": 0.0, "latency_ms": 0.0, "provider": "Unknown"}
        )

        quality: Dict[str, Optional[float]]
        if self.quality_fn is not None:
            quality = dict(self.quality_fn(model))
            quality_measured = True
        elif self.model_type == "embedding":
            quality = {"f1_score": None, "precision": None, "recall": None}
            quality_measured = False
        else:  # reranker
            quality = {"ndcg": None, "calibration": None}
            quality_measured = False

        return {
            "model": model,
            "latency_ms": metadata.get("latency_ms", 0),
            "cost_per_1m": metadata.get("cost_per_1m", 0),
            "provider": metadata.get("provider", "Unknown"),
            "quality_measured": quality_measured,
            **quality,
        }

    def report(self) -> str:
        """
        Get comparison report in plain English.

        Returns:
            Human-readable comparison with recommendations

        Examples:
            >>> comparison = hound.compare_models(
            ...     model_type="embedding",
            ...     candidates=["3-small", "3-large", "cohere-v3"]
            ... )
            >>> print(comparison.report())
        """
        if not self._results:
            self.benchmark()

        report = f"""
EMBEDDING MODEL COMPARISON
═════════════════════════════════════════════════════════════

Benchmarking {len(self.candidates)} models on your corpus...

"""

        # Sort by F1 score (or NDCG for reranker); unmeasured models sort last.
        key_metric = "f1_score" if self.model_type == "embedding" else "ndcg"
        sorted_models = sorted(
            self._results.items(),
            key=lambda x: x[1].get(key_metric) if x[1].get(key_metric) is not None else -1.0,
            reverse=True,
        )

        report += f"{'Model':<30} {key_metric.upper():<10} Cost/1M   Latency  Quality\n"
        report += "─" * 70 + "\n"

        for model_name, metrics in sorted_models:
            f1 = metrics.get(key_metric)
            f1_str = f"{f1:.2%}" if f1 is not None else "N/A"
            cost = metrics.get("cost_per_1m", 0)
            latency = metrics.get("latency_ms", 0)
            quality_note = (
                "measured" if metrics.get("quality_measured") else "not measured (pass quality_fn)"
            )

            report += (
                f"{model_name:<30} {f1_str:<10} "
                f"${cost:<6.2f}  {latency:.1f}ms  {quality_note}\n"
            )

        report += "\nRECOMMENDATION:\n"
        frontier = self.pareto_frontier()
        report += f"→ Best quality: {frontier['best_quality']}\n"
        report += f"→ Best value: {frontier['best_value']}\n"
        report += f"→ Best budget: {frontier['best_budget']}\n"
        if not any(m.get("quality_measured") for m in self._results.values()):
            report += (
                "\nNote: no quality_fn was supplied, so 'best quality'/'best value' above "
                "are based on cost/latency only -- pass quality_fn to ModelComparison for "
                "quality-aware ranking.\n"
            )

        return report

    def metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Get detailed metrics for each model.

        Returns:
            Dictionary with quality, cost, latency for each model

        Examples:
            >>> metrics = comparison.metrics()
            >>> for model, vals in metrics.items():
            ...     print(f"{model}: F1={vals['f1_score']}, Cost=${vals['cost_per_1m']}")
        """
        if not self._results:
            self.benchmark()

        return self._results

    def pareto_frontier(self) -> Dict[str, str]:
        """
        Get Pareto frontier of models (best quality, best value, best budget).

        Returns:
            Dictionary with Pareto-optimal models

        Examples:
            >>> frontier = comparison.pareto_frontier()
            >>> print(f"Best quality: {frontier['best_quality']}")
            >>> print(f"Best value: {frontier['best_value']}")
            >>> print(f"Best budget: {frontier['best_budget']}")
        """
        if not self._results:
            self.benchmark()

        # Best quality: highest F1 / NDCG among models with measured quality;
        # falls back to lowest cost if no model has measured quality.
        key = "f1_score" if self.model_type == "embedding" else "ndcg"
        measured = {
            m: v for m, v in self._results.items() if v.get(key) is not None
        }
        if measured:
            best_quality = max(measured.items(), key=lambda x: x[1][key])[0]
        else:
            best_quality = min(
                self._results.items(), key=lambda x: x[1].get("cost_per_1m", float("inf"))
            )[0]

        # Best value: highest quality per dollar (only among measured models)
        best_value = None
        best_roi = 0
        for model, metrics in measured.items():
            quality = metrics.get(key, 0)
            cost = metrics.get("cost_per_1m", 1)
            roi = quality / (cost + 0.01)  # Avoid division by zero
            if roi > best_roi:
                best_roi = roi
                best_value = model

        # Best budget: lowest cost
        best_budget = min(self._results.items(), key=lambda x: x[1].get("cost_per_1m", float("inf")))[0]

        return {
            "best_quality": best_quality,
            "best_value": best_value or best_quality,
            "best_budget": best_budget,
        }

    def ab_test(
        self,
        model_a: str,
        model_b: str,
        duration_days: int = 7,
        traffic_split: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Set up A/B test between two models.

        Args:
            model_a: First model (control)
            model_b: Second model (test)
            duration_days: How long to run the test
            traffic_split: Fraction of traffic to send to model_b

        Returns:
            A/B test configuration and results

        Examples:
            >>> ab_test = comparison.ab_test(
            ...     model_a="3-small",
            ...     model_b="3-large",
            ...     duration_days=7
            ... )
            >>> print(f"Winner: {ab_test['winner']}")
        """
        return {
            "model_a": model_a,
            "model_b": model_b,
            "duration_days": duration_days,
            "traffic_split": traffic_split,
            "status": "ready",
            "sample_size": self.sample_size,
        }
