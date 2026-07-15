"""REST API server for pyvectorhound - retrieval debugger workflow integration."""

from typing import Dict, Any, Optional, List

from .hound import Hound


class PyvectorhoundServer:
    """REST API server for retrieval diagnostics."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8006):
        """Initialize server."""
        self.host = host
        self.port = port
        self.hounds: Dict[str, Hound] = {}

    def create_hound(
        self,
        hound_id: str,
        db: str,
        endpoint: str,
        index_name: str = "documents",
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a Hound instance."""
        try:
            hound = Hound(
                db=db,
                endpoint=endpoint,
                index_name=index_name,
                api_key=api_key,
            )
            self.hounds[hound_id] = hound
            return {
                "status": "success",
                "hound_id": hound_id,
                "db": db,
                "endpoint": endpoint,
                "index_name": index_name,
                "message": f"Hound '{hound_id}' created for {db}",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "hound_id": hound_id,
            }

    def diagnose_query(
        self,
        hound_id: str,
        query: str,
        top_k: int = 5,
        expected_docs: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Diagnose query retrieval."""
        if hound_id not in self.hounds:
            return {
                "status": "error",
                "message": f"Hound '{hound_id}' not found",
            }

        try:
            hound = self.hounds[hound_id]
            diagnosis = hound.diagnose(
                query=query,
                top_k=top_k,
                expected_docs=expected_docs,
            )

            return {
                "status": "success",
                "query": query,
                "hound_id": hound_id,
                "top_k": top_k,
                "findings": (
                    diagnosis.hunt() if hasattr(diagnosis, 'hunt') else ""
                ),
                "metrics": (
                    diagnosis.metrics() if hasattr(diagnosis, 'metrics') else {}
                ),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "hound_id": hound_id,
                "query": query,
            }

    def get_recommendations(
        self,
        hound_id: str,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Get recommendations."""
        if hound_id not in self.hounds:
            return {
                "status": "error",
                "message": f"Hound '{hound_id}' not found",
            }

        try:
            hound = self.hounds[hound_id]
            diagnosis = hound.diagnose(query=query, top_k=top_k)

            return {
                "status": "success",
                "query": query,
                "hound_id": hound_id,
                "recommendations": (
                    diagnosis.recommendations()
                    if hasattr(diagnosis, 'recommendations')
                    else []
                ),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "hound_id": hound_id,
            }

    def list_hounds(self) -> Dict[str, Any]:
        """List hounds."""
        hounds_info = [
            {
                "id": hound_id,
                "db": hound.db,
                "endpoint": hound.endpoint,
                "index_name": hound.index_name,
            }
            for hound_id, hound in self.hounds.items()
        ]

        return {
            "status": "success",
            "hounds": hounds_info,
            "count": len(hounds_info),
        }

    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "pyvectorhound",
            "version": "0.1.0",
            "hounds_active": len(self.hounds),
        }


def create_flask_app(server: Optional[PyvectorhoundServer] = None):
    """Create Flask app for REST API."""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        raise ImportError(
            "Flask is required for REST API. Install with: pip install flask"
        )

    app = Flask(__name__)
    srv = server or PyvectorhoundServer()

    @app.route("/health", methods=["GET"])
    def health():
        """Health check."""
        return jsonify(srv.health_check())

    @app.route("/hounds", methods=["POST"])
    def create_hound():
        """Create hound."""
        data = request.get_json()
        hound_id = data.get("hound_id")
        db = data.get("db")
        endpoint = data.get("endpoint")
        index_name = data.get("index_name", "documents")
        api_key = data.get("api_key")

        if not hound_id or not db or not endpoint:
            return (
                jsonify({
                    "status": "error",
                    "message": "hound_id, db, endpoint required"
                }),
                400,
            )

        return jsonify(
            srv.create_hound(hound_id, db, endpoint, index_name, api_key)
        )

    @app.route("/hounds", methods=["GET"])
    def list_hounds():
        """List hounds."""
        return jsonify(srv.list_hounds())

    @app.route("/hounds/<hound_id>/diagnose", methods=["POST"])
    def diagnose(hound_id):
        """Diagnose query."""
        data = request.get_json() or {}
        query = data.get("query")
        top_k = data.get("top_k", 5)
        expected_docs = data.get("expected_docs")

        if not query:
            return (
                jsonify({"status": "error", "message": "query required"}),
                400,
            )

        return jsonify(
            srv.diagnose_query(hound_id, query, top_k, expected_docs)
        )

    @app.route("/hounds/<hound_id>/recommendations", methods=["POST"])
    def recommendations(hound_id):
        """Get recommendations."""
        data = request.get_json() or {}
        query = data.get("query")
        top_k = data.get("top_k", 5)

        if not query:
            return (
                jsonify({"status": "error", "message": "query required"}),
                400,
            )

        return jsonify(srv.get_recommendations(hound_id, query, top_k))

    return app


def run_server(host: str = "0.0.0.0", port: int = 8006):
    """Run the REST API server."""
    app = create_flask_app()
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    run_server()
