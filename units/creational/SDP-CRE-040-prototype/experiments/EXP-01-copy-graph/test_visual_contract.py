"""Static structure and all displayed data; this does not claim browser rendering."""

import json
import re
from pathlib import Path

from copy_graph_probe import observations

HTML = Path(__file__).resolve().parents[2] / "visuals/copy-graph-explorer.html"


def test_embedded_observations_match_actual_python_results() -> None:
    page = HTML.read_text()
    match = re.search(
        r'<script id="observations" type="application/json">(.*?)</script>', page, re.S
    )
    assert match is not None
    assert json.loads(match.group(1)) == observations()


def test_control_choices_match_all_observations_in_order() -> None:
    page = HTML.read_text()
    modes = re.findall(r'<option value="([^"]+)"', page)
    assert modes == [item["mode"] for item in observations()]
    assert 'value="deep" selected' in page


def test_required_accessibility_and_responsive_structure() -> None:
    page = HTML.read_text()
    ids = re.findall(r'\bid="([^"]+)"', page)
    assert len(ids) == len(set(ids))
    for target in re.findall(r'\b(?:for|aria-labelledby)="([^"]+)"', page):
        assert target in ids
    for target in re.findall(r'get\("([^"]+)"\)', page):
        assert target in ids
    assert 'aria-live="polite"' in page and 'aria-pressed="false"' in page
    assert "prefers-reduced-motion" in page and "max-width: 620px" in page
    assert "grid-template-columns: 1fr;" in page
    assert "fetch(" not in page and "XMLHttpRequest" not in page
    assert "How to read this visual" in page
    assert "Key insight" in page and "Simplification or limitation" in page
