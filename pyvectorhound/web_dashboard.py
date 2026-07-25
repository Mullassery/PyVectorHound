"""Web Dashboard for PyVectorHound.

FastAPI-based dashboard for visualizing traces, replays, trends,
recommendations, and analytics in real-time.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json


@dataclass
class DashboardConfig:
    """Dashboard configuration."""

    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    title: str = "PyVectorHound Dashboard"
    theme: str = "dark"  # dark or light
    update_interval_seconds: int = 5
    max_traces_displayed: int = 100
    max_metrics_displayed: int = 1000


class DashboardMetrics:
    """Real-time metrics for dashboard display."""

    def __init__(self):
        """Initialize dashboard metrics."""
        self.traces: List[Dict[str, Any]] = []
        self.replay_results: List[Dict[str, Any]] = []
        self.recommendations: List[Dict[str, Any]] = []
        self.trends: List[Dict[str, Any]] = []
        self.analytics_reports: List[Dict[str, Any]] = []
        self.timestamps: List[datetime] = []

    def add_trace_metric(self, trace_data: Dict[str, Any]) -> None:
        """Add trace data to metrics.

        Args:
            trace_data: Trace data dictionary
        """
        self.traces.append({
            **trace_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def add_replay_result(self, result_data: Dict[str, Any]) -> None:
        """Add replay result to metrics.

        Args:
            result_data: Replay result dictionary
        """
        self.replay_results.append({
            **result_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def add_recommendation(self, rec_data: Dict[str, Any]) -> None:
        """Add recommendation to metrics.

        Args:
            rec_data: Recommendation dictionary
        """
        self.recommendations.append({
            **rec_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def add_trend_data(self, trend_data: Dict[str, Any]) -> None:
        """Add trend data to metrics.

        Args:
            trend_data: Trend data dictionary
        """
        self.trends.append({
            **trend_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def add_analytics_report(self, report_data: Dict[str, Any]) -> None:
        """Add analytics report to metrics.

        Args:
            report_data: Analytics report dictionary
        """
        self.analytics_reports.append({
            **report_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def get_summary(self) -> Dict[str, Any]:
        """Get dashboard summary.

        Returns:
            Summary dictionary
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "num_traces": len(self.traces),
            "num_replays": len(self.replay_results),
            "num_recommendations": len(self.recommendations),
            "latest_trace": self.traces[-1] if self.traces else None,
            "latest_replay": self.replay_results[-1] if self.replay_results else None,
            "latest_recommendation": self.recommendations[-1] if self.recommendations else None,
            "avg_latency_ms": self._calculate_avg_latency(),
            "avg_recall": self._calculate_avg_recall(),
        }

    def get_performance_chart_data(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance chart data for time period.

        Args:
            hours: Number of hours to look back

        Returns:
            Chart data dictionary
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_traces = [
            t for t in self.traces
            if datetime.fromisoformat(t["timestamp"]) > cutoff
        ]

        latencies = [t.get("latency_ms", 0) for t in recent_traces]
        recalls = [t.get("recall", 0) for t in recent_traces]

        return {
            "timestamps": [t["timestamp"] for t in recent_traces],
            "latencies_ms": latencies,
            "recalls": recalls,
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "avg_recall": sum(recalls) / len(recalls) if recalls else 0,
        }

    def get_database_comparison_data(self) -> Dict[str, Any]:
        """Get database comparison data.

        Returns:
            Comparison data dictionary
        """
        db_stats = {}
        for replay in self.replay_results:
            db_name = replay.get("database", "unknown")
            if db_name not in db_stats:
                db_stats[db_name] = {
                    "count": 0,
                    "total_latency": 0,
                    "total_recall": 0,
                }

            db_stats[db_name]["count"] += 1
            db_stats[db_name]["total_latency"] += replay.get("latency_ms", 0)
            db_stats[db_name]["total_recall"] += replay.get("recall_at_5", 0)

        # Calculate averages
        for db_name in db_stats:
            count = db_stats[db_name]["count"]
            db_stats[db_name]["avg_latency_ms"] = db_stats[db_name]["total_latency"] / count if count > 0 else 0
            db_stats[db_name]["avg_recall"] = db_stats[db_name]["total_recall"] / count if count > 0 else 0

        return db_stats

    def get_recommendations_summary(self) -> Dict[str, Any]:
        """Get recommendations summary.

        Returns:
            Recommendations summary
        """
        if not self.recommendations:
            return {}

        categories = {}
        for rec in self.recommendations:
            category = rec.get("category", "unknown")
            if category not in categories:
                categories[category] = {"count": 0, "avg_roi": 0, "total_roi": 0}

            categories[category]["count"] += 1
            categories[category]["total_roi"] += rec.get("roi_pct", 0)

        for category in categories:
            count = categories[category]["count"]
            categories[category]["avg_roi"] = categories[category]["total_roi"] / count if count > 0 else 0

        return categories

    def _calculate_avg_latency(self) -> float:
        """Calculate average latency from traces.

        Returns:
            Average latency in ms
        """
        if not self.traces:
            return 0.0

        latencies = [t.get("latency_ms", 0) for t in self.traces]
        return sum(latencies) / len(latencies) if latencies else 0.0

    def _calculate_avg_recall(self) -> float:
        """Calculate average recall from traces.

        Returns:
            Average recall
        """
        if not self.traces:
            return 0.0

        recalls = [t.get("recall", 0) for t in self.traces]
        return sum(recalls) / len(recalls) if recalls else 0.0

    def clear_old_data(self, max_age_hours: int = 24) -> None:
        """Clear data older than specified hours.

        Args:
            max_age_hours: Maximum age in hours
        """
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)

        def is_recent(item: Dict[str, Any]) -> bool:
            ts = datetime.fromisoformat(item.get("timestamp", ""))
            return ts > cutoff

        self.traces = [t for t in self.traces if is_recent(t)]
        self.replay_results = [r for r in self.replay_results if is_recent(r)]
        self.recommendations = [r for r in self.recommendations if is_recent(r)]
        self.trends = [t for t in self.trends if is_recent(t)]
        self.analytics_reports = [r for r in self.analytics_reports if is_recent(r)]


class Dashboard:
    """PyVectorHound Web Dashboard.

    Provides real-time visualization of retrieval diagnostics, performance,
    and optimization recommendations.
    """

    def __init__(self, config: Optional[DashboardConfig] = None, hound: Optional[Any] = None):
        """Initialize dashboard.

        Args:
            config: Dashboard configuration
            hound: PyVectorHound Hound instance
        """
        self.config = config or DashboardConfig()
        self.hound = hound
        self.metrics = DashboardMetrics()
        self._app = None

    def create_app(self):
        """Create FastAPI app (requires fastapi installed).

        Returns:
            FastAPI app instance
        """
        try:
            from fastapi import FastAPI
            from fastapi.responses import HTMLResponse, JSONResponse
            from fastapi.staticfiles import StaticFiles
        except ImportError:
            raise ImportError(
                "FastAPI not installed. Install with: pip install fastapi uvicorn"
            )

        app = FastAPI(title=self.config.title)

        # API Endpoints
        @app.get("/api/summary")
        async def get_summary():
            """Get dashboard summary."""
            return self.metrics.get_summary()

        @app.get("/api/performance")
        async def get_performance(hours: int = 24):
            """Get performance metrics."""
            return self.metrics.get_performance_chart_data(hours)

        @app.get("/api/database-comparison")
        async def get_db_comparison():
            """Get database comparison."""
            return self.metrics.get_database_comparison_data()

        @app.get("/api/recommendations")
        async def get_recommendations():
            """Get recommendations summary."""
            return self.metrics.get_recommendations_summary()

        @app.get("/api/traces")
        async def get_traces(limit: int = 100):
            """Get recent traces."""
            return {"traces": self.metrics.traces[-limit:]}

        @app.get("/api/replays")
        async def get_replays(limit: int = 50):
            """Get recent replay results."""
            return {"replays": self.metrics.replay_results[-limit:]}

        @app.get("/")
        async def root():
            """Serve dashboard HTML."""
            return self._get_dashboard_html()

        @app.get("/health")
        async def health():
            """Health check endpoint."""
            return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

        self._app = app
        return app

    def _get_dashboard_html(self) -> str:
        """Get dashboard HTML.

        Returns:
            HTML string
        """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.config.title}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    background: {"#1e1e1e" if self.config.theme == "dark" else "#f5f5f5"};
                    color: {"#e0e0e0" if self.config.theme == "dark" else "#333"};
                    padding: 20px;
                }}
                header {{
                    max-width: 1400px;
                    margin: 0 auto 30px;
                }}
                h1 {{
                    font-size: 32px;
                    margin-bottom: 10px;
                }}
                .subtitle {{
                    opacity: 0.7;
                    font-size: 14px;
                }}
                .grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    max-width: 1400px;
                    margin: 0 auto 30px;
                }}
                .card {{
                    background: {"#2d2d2d" if self.config.theme == "dark" else "white"};
                    border-radius: 8px;
                    padding: 20px;
                    border: 1px solid {"#3d3d3d" if self.config.theme == "dark" else "#ddd"};
                }}
                .metric-value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #4CAF50;
                    margin: 10px 0;
                }}
                .metric-label {{
                    font-size: 12px;
                    opacity: 0.7;
                    text-transform: uppercase;
                }}
                .section {{
                    max-width: 1400px;
                    margin: 0 auto 30px;
                }}
                .section-title {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #4CAF50;
                }}
                .chart {{
                    width: 100%;
                    height: 300px;
                    background: {"#2d2d2d" if self.config.theme == "dark" else "#fafafa"};
                    border-radius: 8px;
                    border: 1px solid {"#3d3d3d" if self.config.theme == "dark" else "#ddd"};
                    padding: 20px;
                }}
                footer {{
                    text-align: center;
                    opacity: 0.5;
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 1px solid {"#3d3d3d" if self.config.theme == "dark" else "#ddd"};
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>🔍 PyVectorHound Dashboard</h1>
                <p class="subtitle">Real-time retrieval diagnostics and optimization</p>
            </header>

            <div class="grid" id="summary"></div>

            <div class="section">
                <h2 class="section-title">Performance Metrics</h2>
                <div class="chart" id="performance-chart">
                    <p>Loading performance data...</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Database Comparison</h2>
                <div class="grid" id="database-comparison"></div>
            </div>

            <div class="section">
                <h2 class="section-title">Recommendations</h2>
                <div class="grid" id="recommendations"></div>
            </div>

            <footer>
                <p>PyVectorHound v1.0 | Powered by FastAPI</p>
                <p id="last-update"></p>
            </footer>

            <script>
                async function updateDashboard() {{
                    try {{
                        const summary = await fetch('/api/summary').then(r => r.json());
                        const performance = await fetch('/api/performance').then(r => r.json());
                        const dbComparison = await fetch('/api/database-comparison').then(r => r.json());
                        const recommendations = await fetch('/api/recommendations').then(r => r.json());

                        // Update summary cards
                        const summaryDiv = document.getElementById('summary');
                        if (summary) {{
                            summaryDiv.innerHTML = `
                                <div class="card">
                                    <div class="metric-label">Total Traces</div>
                                    <div class="metric-value">${{summary.num_traces || 0}}</div>
                                </div>
                                <div class="card">
                                    <div class="metric-label">Avg Latency</div>
                                    <div class="metric-value">${{(summary.avg_latency_ms || 0).toFixed(1)}}ms</div>
                                </div>
                                <div class="card">
                                    <div class="metric-label">Avg Recall</div>
                                    <div class="metric-value">${{{(summary.avg_recall || 0).toFixed(2)}}}</div>
                                </div>
                                <div class="card">
                                    <div class="metric-label">Recommendations</div>
                                    <div class="metric-value">${{summary.num_recommendations || 0}}</div>
                                </div>
                            `;
                        }}

                        document.getElementById('last-update').textContent =
                            'Last updated: ' + new Date().toLocaleTimeString();
                    }} catch (error) {{
                        console.error('Error updating dashboard:', error);
                    }}
                }}

                // Update immediately and then every {self.config.update_interval_seconds} seconds
                updateDashboard();
                setInterval(updateDashboard, {self.config.update_interval_seconds * 1000});
            </script>
        </body>
        </html>
        """

    def run(self):
        """Run the dashboard server."""
        try:
            import uvicorn
        except ImportError:
            raise ImportError(
                "Uvicorn not installed. Install with: pip install uvicorn"
            )

        if self._app is None:
            self.create_app()

        uvicorn.run(
            self._app,
            host=self.config.host,
            port=self.config.port,
            reload=self.config.reload,
        )

    def get_app(self):
        """Get FastAPI app instance.

        Returns:
            FastAPI app
        """
        if self._app is None:
            self.create_app()
        return self._app
