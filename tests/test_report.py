"""HTML/JSON report rendering tests."""

from pyvectorhound.diagnosis import Diagnosis
from pyvectorhound.report import render_html, render_json


def _diagnosis():
    return Diagnosis(
        query="what is <script>alert(1)</script>",
        results=[{"id": "a", "score": 0.9}],
        expected_docs=["a"],
    )


def test_html_is_escaped_and_contains_metrics():
    html = render_html(_diagnosis())
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
    assert "PyVectorHound diagnosis" in html
    assert "VECTOR SEARCH" in html.upper()


def test_json_payload_has_metrics_and_recommendations():
    payload = render_json(_diagnosis())
    assert '"query"' in payload
    assert '"metrics"' in payload
    assert '"recommendations"' in payload


def test_to_html_writes_file(tmp_path):
    path = tmp_path / "report.html"
    written = _diagnosis().to_html(str(path))
    assert written == str(path)
    assert path.read_text().startswith("<!DOCTYPE html>")
