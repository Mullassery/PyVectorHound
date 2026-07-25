"""Advanced analytics for retrieval system optimization.

Provides cross-database comparison, cost analysis, and performance forecasting
to help optimize infrastructure choices and configurations.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from enum import Enum
import numpy as np


class CostModel(Enum):
    """Cost models for different databases."""

    QDRANT_CLOUD = "qdrant_cloud"
    PINECONE = "pinecone"
    WEAVIATE_CLOUD = "weaviate_cloud"
    MILVUS_SELF_HOSTED = "milvus_self_hosted"
    PGVECTOR_RDS = "pgvector_rds"


@dataclass
class DatabaseCost:
    """Database infrastructure cost analysis."""

    database_name: str
    query_cost_per_million: float  # Cost per 1M queries
    storage_cost_per_gb_month: float  # $/GB/month
    compute_cost_per_hour: float  # $/hour for compute
    total_monthly_estimate: float  # Estimated monthly cost


@dataclass
class PerformanceCharacteristics:
    """Performance characteristics of a database."""

    database_name: str
    avg_query_latency_ms: float
    p95_query_latency_ms: float
    p99_query_latency_ms: float
    throughput_qps: float  # Queries per second
    recall_avg: float
    scalability_score: float  # 0-100


@dataclass
class OptimizationRecommendation:
    """Recommendation for database/configuration optimization."""

    current_database: str
    recommended_database: Optional[str]
    improvement_type: str  # latency, cost, recall, throughput
    expected_improvement_pct: float
    estimated_cost_savings_monthly: float
    implementation_effort: str  # low, medium, high
    risk_level: str  # low, medium, high
    rationale: str
    migration_steps: List[str]


class AdvancedAnalytics:
    """Advanced analytics engine for retrieval optimization.

    Provides cross-database comparison, cost analysis, and recommendations
    for optimizing retrieval system infrastructure.
    """

    def __init__(self):
        """Initialize analytics engine."""
        self._cost_models = self._initialize_cost_models()
        self._performance_data: Dict[str, PerformanceCharacteristics] = {}

    def _initialize_cost_models(self) -> Dict[CostModel, DatabaseCost]:
        """Initialize cost models for different databases.

        Returns:
            Dictionary of cost models
        """
        return {
            CostModel.QDRANT_CLOUD: DatabaseCost(
                database_name="Qdrant Cloud",
                query_cost_per_million=0.0,  # Free tier available
                storage_cost_per_gb_month=0.5,
                compute_cost_per_hour=0.0,  # Included in storage
                total_monthly_estimate=0.0,  # Based on usage
            ),
            CostModel.PINECONE: DatabaseCost(
                database_name="Pinecone",
                query_cost_per_million=0.0,
                storage_cost_per_gb_month=1.0,
                compute_cost_per_hour=0.0,
                total_monthly_estimate=0.0,
            ),
            CostModel.WEAVIATE_CLOUD: DatabaseCost(
                database_name="Weaviate Cloud",
                query_cost_per_million=0.0,
                storage_cost_per_gb_month=0.75,
                compute_cost_per_hour=0.0,
                total_monthly_estimate=0.0,
            ),
            CostModel.MILVUS_SELF_HOSTED: DatabaseCost(
                database_name="Milvus (Self-Hosted)",
                query_cost_per_million=0.0,
                storage_cost_per_gb_month=0.1,  # EC2 storage
                compute_cost_per_hour=0.5,  # EC2 compute
                total_monthly_estimate=500.0,  # Rough estimate
            ),
            CostModel.PGVECTOR_RDS: DatabaseCost(
                database_name="PostgreSQL with pgvector (RDS)",
                query_cost_per_million=0.0,
                storage_cost_per_gb_month=0.2,
                compute_cost_per_hour=1.0,
                total_monthly_estimate=750.0,
            ),
        }

    def register_performance_data(
        self,
        database_name: str,
        avg_latency_ms: float,
        p95_latency_ms: float,
        p99_latency_ms: float,
        throughput_qps: float,
        recall_avg: float,
        scalability_score: float = 50.0,
    ) -> None:
        """Register performance data for a database.

        Args:
            database_name: Database name
            avg_latency_ms: Average query latency
            p95_latency_ms: P95 latency
            p99_latency_ms: P99 latency
            throughput_qps: Queries per second
            recall_avg: Average recall
            scalability_score: Scalability score (0-100)
        """
        self._performance_data[database_name] = PerformanceCharacteristics(
            database_name=database_name,
            avg_query_latency_ms=avg_latency_ms,
            p95_query_latency_ms=p95_latency_ms,
            p99_query_latency_ms=p99_latency_ms,
            throughput_qps=throughput_qps,
            recall_avg=recall_avg,
            scalability_score=scalability_score,
        )

    def compare_databases(
        self,
        database_names: List[str],
        optimization_goal: str = "balanced",  # latency, cost, recall, throughput, balanced
    ) -> Dict[str, Any]:
        """Compare multiple databases.

        Args:
            database_names: List of database names to compare
            optimization_goal: Goal for optimization

        Returns:
            Comparison dictionary
        """
        comparison = {
            "optimization_goal": optimization_goal,
            "databases": [],
            "best_by_latency": None,
            "best_by_cost": None,
            "best_by_recall": None,
            "best_by_throughput": None,
        }

        latencies = []
        costs = []
        recalls = []
        throughputs = []

        for db_name in database_names:
            if db_name not in self._performance_data:
                continue

            perf = self._performance_data[db_name]
            cost_model = self._find_cost_model(db_name)
            cost = cost_model.total_monthly_estimate if cost_model else 0.0

            db_info = {
                "name": db_name,
                "avg_latency_ms": perf.avg_query_latency_ms,
                "p95_latency_ms": perf.p95_query_latency_ms,
                "p99_latency_ms": perf.p99_query_latency_ms,
                "throughput_qps": perf.throughput_qps,
                "recall_avg": perf.recall_avg,
                "monthly_cost": cost,
                "efficiency_score": self._calculate_efficiency_score(
                    perf, cost, optimization_goal
                ),
            }

            comparison["databases"].append(db_info)
            latencies.append((db_name, perf.avg_query_latency_ms))
            costs.append((db_name, cost))
            recalls.append((db_name, perf.recall_avg))
            throughputs.append((db_name, perf.throughput_qps))

        # Find best in each category
        if latencies:
            comparison["best_by_latency"] = min(latencies, key=lambda x: x[1])[0]
        if costs:
            comparison["best_by_cost"] = min(costs, key=lambda x: x[1])[0]
        if recalls:
            comparison["best_by_recall"] = max(recalls, key=lambda x: x[1])[0]
        if throughputs:
            comparison["best_by_throughput"] = max(throughputs, key=lambda x: x[1])[0]

        return comparison

    def estimate_monthly_cost(
        self,
        database_name: str,
        num_documents: int = 1_000_000,
        queries_per_day: int = 100_000,
        storage_gb: Optional[float] = None,
    ) -> Dict[str, float]:
        """Estimate monthly cost for a database configuration.

        Args:
            database_name: Database name
            num_documents: Number of documents stored
            queries_per_day: Daily query volume
            storage_gb: Optional storage in GB (estimated if None)

        Returns:
            Cost breakdown dictionary
        """
        cost_model = self._find_cost_model(database_name)
        if not cost_model:
            return {}

        # Estimate storage if not provided
        if storage_gb is None:
            # Assume ~1KB per vector (768D float32 + metadata)
            storage_gb = (num_documents * 1024) / (1024**3)

        # Calculate monthly costs
        queries_per_month = queries_per_day * 30
        query_cost = (queries_per_month / 1_000_000) * cost_model.query_cost_per_million
        storage_cost = storage_gb * cost_model.storage_cost_per_gb_month
        compute_cost = 730 * cost_model.compute_cost_per_hour  # 730 hours/month

        total_cost = query_cost + storage_cost + compute_cost

        return {
            "query_cost": query_cost,
            "storage_cost": storage_cost,
            "compute_cost": compute_cost,
            "total_monthly": total_cost,
            "cost_per_query": total_cost / max(queries_per_month, 1),
            "cost_per_document": total_cost / max(num_documents, 1),
        }

    def forecast_performance(
        self,
        database_name: str,
        growth_factor: float = 2.0,  # Expected growth (e.g., 2x in 6 months)
    ) -> Dict[str, Any]:
        """Forecast performance under load growth.

        Args:
            database_name: Database name
            growth_factor: Expected load growth factor

        Returns:
            Forecast dictionary
        """
        if database_name not in self._performance_data:
            return {}

        perf = self._performance_data[database_name]
        cost_model = self._find_cost_model(database_name)

        # Assume linear scaling with growth
        forecast_latency = perf.avg_query_latency_ms * (growth_factor ** 0.5)
        forecast_throughput = perf.throughput_qps / growth_factor
        forecast_storage_cost = (
            cost_model.storage_cost_per_gb_month * growth_factor if cost_model else 0.0
        )

        return {
            "current_latency_ms": perf.avg_query_latency_ms,
            "forecast_latency_ms": forecast_latency,
            "latency_increase_pct": (
                (forecast_latency - perf.avg_query_latency_ms) / perf.avg_query_latency_ms * 100
            ),
            "current_throughput_qps": perf.throughput_qps,
            "forecast_throughput_qps": forecast_throughput,
            "throughput_decrease_pct": (
                (1 - forecast_throughput / perf.throughput_qps) * 100
            ),
            "estimated_storage_cost_monthly": forecast_storage_cost,
        }

    def get_optimization_recommendations(
        self,
        current_database: str,
        current_performance: PerformanceCharacteristics,
        constraints: Optional[Dict[str, float]] = None,
    ) -> List[OptimizationRecommendation]:
        """Get optimization recommendations.

        Args:
            current_database: Current database name
            current_performance: Current performance metrics
            constraints: Optional constraints (max_latency_ms, max_monthly_cost, min_recall, etc)

        Returns:
            List of recommendations
        """
        recommendations = []
        constraints = constraints or {}

        # Check if latency is a problem
        max_latency = constraints.get("max_latency_ms", 100)
        if current_performance.avg_query_latency_ms > max_latency:
            # Recommend lower-latency options
            for db_name, perf in self._performance_data.items():
                if db_name == current_database:
                    continue
                if perf.avg_query_latency_ms < current_performance.avg_query_latency_ms:
                    improvement_pct = (
                        (current_performance.avg_query_latency_ms - perf.avg_query_latency_ms)
                        / current_performance.avg_query_latency_ms * 100
                    )

                    recommendations.append(
                        OptimizationRecommendation(
                            current_database=current_database,
                            recommended_database=db_name,
                            improvement_type="latency",
                            expected_improvement_pct=improvement_pct,
                            estimated_cost_savings_monthly=0.0,
                            implementation_effort="medium",
                            risk_level="medium",
                            rationale=f"Reduce latency from {current_performance.avg_query_latency_ms:.1f}ms to {perf.avg_query_latency_ms:.1f}ms",
                            migration_steps=[
                                "Set up new database instance",
                                "Re-index documents",
                                "Run parallel testing",
                                "Cutover to new database",
                            ],
                        )
                    )

        # Check if cost is a problem
        max_cost = constraints.get("max_monthly_cost", float("inf"))
        current_cost_model = self._find_cost_model(current_database)
        current_cost = current_cost_model.total_monthly_estimate if current_cost_model else 0.0

        if current_cost > max_cost:
            # Recommend lower-cost options
            for db_name, perf in self._performance_data.items():
                if db_name == current_database:
                    continue

                cost_model = self._find_cost_model(db_name)
                if cost_model and cost_model.total_monthly_estimate < current_cost:
                    cost_savings = current_cost - cost_model.total_monthly_estimate
                    savings_pct = cost_savings / current_cost * 100

                    recommendations.append(
                        OptimizationRecommendation(
                            current_database=current_database,
                            recommended_database=db_name,
                            improvement_type="cost",
                            expected_improvement_pct=savings_pct,
                            estimated_cost_savings_monthly=cost_savings,
                            implementation_effort="medium",
                            risk_level="low",
                            rationale=f"Reduce monthly costs by ${cost_savings:.0f}",
                            migration_steps=[
                                "Estimate data transfer costs",
                                "Set up new database",
                                "Plan gradual migration",
                                "Monitor performance",
                            ],
                        )
                    )

        return recommendations

    def _find_cost_model(self, database_name: str) -> Optional[DatabaseCost]:
        """Find cost model for a database.

        Args:
            database_name: Database name

        Returns:
            DatabaseCost or None
        """
        name_lower = database_name.lower()
        for model in self._cost_models.values():
            if name_lower in model.database_name.lower():
                return model
        return None

    def _calculate_efficiency_score(
        self,
        perf: PerformanceCharacteristics,
        cost: float,
        optimization_goal: str,
    ) -> float:
        """Calculate efficiency score based on goal.

        Args:
            perf: Performance characteristics
            cost: Monthly cost
            optimization_goal: Optimization goal

        Returns:
            Efficiency score (0-100)
        """
        if optimization_goal == "latency":
            # Lower latency is better
            return max(0, 100 - perf.avg_query_latency_ms)
        elif optimization_goal == "cost":
            # Lower cost is better
            return max(0, 100 - (cost / 1000.0 * 10))
        elif optimization_goal == "recall":
            # Higher recall is better
            return perf.recall_avg * 100
        elif optimization_goal == "throughput":
            # Higher throughput is better
            return min(100, perf.throughput_qps / 10.0)
        else:  # balanced
            # Weighted combination
            return (
                (100 - perf.avg_query_latency_ms) * 0.25
                + max(0, 100 - (cost / 1000.0 * 10)) * 0.25
                + perf.recall_avg * 100 * 0.25
                + min(100, perf.throughput_qps / 10.0) * 0.25
            )
