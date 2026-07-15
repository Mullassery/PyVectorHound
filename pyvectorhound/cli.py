"""CLI for pyvectorhound - retrieval debugger workflow integration."""

import json
import sys
from typing import Optional, List

from .hound import Hound
from .comparison import ModelComparison


class CLIInterface:
    """Command-line interface for pyvectorhound workflow integration."""

    def __init__(self):
        self.hounds = {}
        self.diagnostics = {}

    def create_hound(
        self,
        hound_id: str,
        db: str,
        endpoint: str,
        index_name: str = "documents",
        api_key: Optional[str] = None,
    ) -> dict:
        """Create a Hound instance for a vector database.

        Args:
            hound_id: Unique identifier for this hound instance
            db: Vector database type (qdrant, chroma, milvus, weaviate, postgres)
            endpoint: Database endpoint URL
            index_name: Index/collection name (default: documents)
            api_key: Optional API key

        Returns:
            JSON response with hound creation details
        """
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
                "message": f"Hound '{hound_id}' created for {db} at {endpoint}",
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
    ) -> dict:
        """Diagnose why retrieval is failing for a query.

        Args:
            hound_id: Hound instance ID
            query: Search query to diagnose
            top_k: Number of results to analyze (default: 5)
            expected_docs: Optional ground truth documents (JSON string)

        Returns:
            JSON response with diagnosis results
        """
        if hound_id not in self.hounds:
            return {
                "status": "error",
                "message": f"Hound '{hound_id}' not found",
            }

        try:
            hound = self.hounds[hound_id]
            expected = None
            if expected_docs:
                try:
                    expected = json.loads(expected_docs)
                except json.JSONDecodeError:
                    expected = expected_docs.split(",")

            diagnosis = hound.diagnose(
                query=query,
                top_k=top_k,
                expected_docs=expected,
            )

            return {
                "status": "success",
                "query": query,
                "hound_id": hound_id,
                "top_k": top_k,
                "findings": diagnosis.hunt() if hasattr(diagnosis, 'hunt') else "Analysis complete",
                "metrics": diagnosis.metrics() if hasattr(diagnosis, 'metrics') else {},
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
    ) -> dict:
        """Get actionable recommendations to fix retrieval.

        Args:
            hound_id: Hound instance ID
            query: Search query
            top_k: Number of results to analyze (default: 5)

        Returns:
            JSON response with recommendations
        """
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

    def list_hounds(self) -> dict:
        """List all active Hound instances.

        Returns:
            JSON response with hound list
        """
        hounds_info = []
        for hound_id, hound in self.hounds.items():
            hounds_info.append({
                "id": hound_id,
                "db": hound.db,
                "endpoint": hound.endpoint,
                "index_name": hound.index_name,
            })

        return {
            "status": "success",
            "hounds": hounds_info,
            "count": len(hounds_info),
        }


def main():
    """Main CLI entry point."""
    cli = CLIInterface()

    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "create-hound":
            if len(sys.argv) < 5:
                print(json.dumps({
                    "error": "Missing hound_id, db, or endpoint"
                }))
                sys.exit(1)

            hound_id = sys.argv[2]
            db = sys.argv[3]
            endpoint = sys.argv[4]
            index_name = sys.argv[5] if len(sys.argv) > 5 else "documents"
            api_key = sys.argv[6] if len(sys.argv) > 6 else None

            result = cli.create_hound(
                hound_id, db, endpoint, index_name, api_key
            )
            print(json.dumps(result))

        elif command == "diagnose":
            if len(sys.argv) < 4:
                print(json.dumps({
                    "error": "Missing hound_id or query"
                }))
                sys.exit(1)

            hound_id = sys.argv[2]
            query = sys.argv[3]
            top_k = int(sys.argv[4]) if len(sys.argv) > 4 else 5
            expected_docs = sys.argv[5] if len(sys.argv) > 5 else None

            result = cli.diagnose_query(
                hound_id, query, top_k, expected_docs
            )
            print(json.dumps(result))

        elif command == "recommendations":
            if len(sys.argv) < 4:
                print(json.dumps({
                    "error": "Missing hound_id or query"
                }))
                sys.exit(1)

            hound_id = sys.argv[2]
            query = sys.argv[3]
            top_k = int(sys.argv[4]) if len(sys.argv) > 4 else 5

            result = cli.get_recommendations(hound_id, query, top_k)
            print(json.dumps(result))

        elif command == "list":
            result = cli.list_hounds()
            print(json.dumps(result))

        elif command == "help":
            print_help()

        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}))
        sys.exit(1)


def print_help():
    """Print help message."""
    help_text = """
pyvectorhound CLI - Retrieval Debugger Workflow Integration

USAGE:
    pyvectorhound <command> [options]

COMMANDS:
    create-hound <hound_id> <db> <endpoint> [index_name] [api_key]
        Create a Hound instance for vector database diagnostics
        - hound_id: Unique identifier (required)
        - db: Database type (required) - qdrant, chroma, milvus, weaviate, postgres
        - endpoint: Database URL (required) - e.g., localhost:6333
        - index_name: Index/collection name (default: documents)
        - api_key: Optional API key (for some databases)

        Example:
            pyvectorhound create-hound hound1 qdrant localhost:6333
            pyvectorhound create-hound hound2 chroma http://localhost:8000

    diagnose <hound_id> <query> [top_k] [expected_docs]
        Diagnose why retrieval is failing
        - hound_id: Hound instance ID (required)
        - query: Search query to analyze (required)
        - top_k: Number of results to analyze (default: 5)
        - expected_docs: Ground truth doc IDs, comma-separated (optional)

        Example:
            pyvectorhound diagnose hound1 "quantum computing" 10
            pyvectorhound diagnose hound1 "machine learning" 5 doc1,doc2,doc3

    recommendations <hound_id> <query> [top_k]
        Get actionable recommendations to fix retrieval
        - hound_id: Hound instance ID (required)
        - query: Search query (required)
        - top_k: Number of results to analyze (default: 5)

        Example:
            pyvectorhound recommendations hound1 "neural networks" 5

    list
        List all active Hound instances

        Example:
            pyvectorhound list

    help
        Show this help message

OUTPUT FORMAT:
    All commands return JSON output
"""
    print(help_text)


if __name__ == "__main__":
    main()
