"""Static diagnostic reports (HTML) for sharing/CI artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, Optional


def _safe(value: Any) -> str:
    return html.escape(str(value))


def render_html(diagnosis: Any) -> str:
    """Render a Diagnosis as a self-contained, escaped HTML report."""
    metrics = diagnosis.metrics()
    recs = diagnosis.recommendations()
    rows = []
    for name, component in metrics.items():
        if not isinstance(component, dict):
            continue
        status = component.get("status", "UNKNOWN")
        explanation = component.get("explanation", "")
        rows.append(
            '<tr><td>%s</td><td class="%s">%s</td><td>%s</td></tr>'
            % (_safe(name), _safe(status.lower()), _safe(status), _safe(explanation))
        )

    rec_items = (
        "".join(
            "<li><strong>%s</strong> — %s (impact: %s, cost: %s)</li>"
            % (
                _safe(rec.get("priority", "")),
                _safe(rec.get("action", "")),
                _safe(rec.get("impact", "")),
                _safe(rec.get("cost", "")),
            )
            for rec in recs
        )
        or "<li>No recommendations.</li>"
    )

    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>PyVectorHound diagnosis</title>
<style>
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:2rem;color:#1f2933}
table{border-collapse:collapse;width:100%%;margin:1rem 0}
th,td{border:1px solid #d9e2ec;padding:.5rem;text-align:left;vertical-align:top}
th{background:#f0f4f8}.good{color:#0b7a3b}.moderate{color:#9a6700}.weak{color:#b42318}
pre{background:#f7f9fb;padding:1rem;white-space:pre-wrap}
</style></head><body>
<h1>PyVectorHound diagnosis</h1>
<p><strong>Query:</strong> %s</p>
<p><strong>Results retrieved:</strong> %s</p>
<h2>Components</h2>
<table><thead><tr><th>Component</th><th>Status</th><th>Explanation</th></tr></thead>
<tbody>%s</tbody></table>
<h2>Recommendations</h2><ul>%s</ul>
<h2>Plain-English report</h2><pre>%s</pre>
<p><small>Generated locally by PyVectorHound. Metrics with insufficient input are reported as UNKNOWN.</small></p>
</body></html>""" % (
        _safe(getattr(diagnosis, "query", "")),
        _safe(len(getattr(diagnosis, "results", []))),
        "".join(rows),
        rec_items,
        _safe(diagnosis.hunt()),
    )


def write_html(diagnosis: Any, path: str) -> str:
    output = Path(path)
    output.write_text(render_html(diagnosis), encoding="utf-8")
    return str(output)


def render_json(diagnosis: Any) -> str:
    payload: Dict[str, Any] = {
        "query": getattr(diagnosis, "query", ""),
        "results": getattr(diagnosis, "results", []),
        "metrics": diagnosis.metrics(),
        "recommendations": diagnosis.recommendations(),
    }
    return json.dumps(payload, indent=2, default=str)


def write_json(diagnosis: Any, path: Optional[str] = None) -> str:
    text = render_json(diagnosis)
    if path:
        Path(path).write_text(text, encoding="utf-8")
        return path
    return text
