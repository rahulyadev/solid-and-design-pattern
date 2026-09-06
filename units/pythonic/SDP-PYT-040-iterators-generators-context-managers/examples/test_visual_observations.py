"""Keep the interactive visual's fixed claims tied to Python observations."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import visual_observations

VISUAL = Path(__file__).parents[1] / "visuals" / "protocol-lifecycle.html"


def test_embedded_visual_data_matches_python_observations() -> None:
    html = VISUAL.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="observations" type="application/json">\s*(.*?)\s*</script>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None

    embedded = json.loads(match.group(1))
    actual = json.loads(json.dumps(visual_observations()))
    assert embedded == actual


def test_visual_contains_reading_and_limitation_guidance() -> None:
    html = VISUAL.read_text(encoding="utf-8")

    assert "How to read" in html
    assert "Key insight" in html
    assert "Simplification or limitation" in html
    assert "Iterable and iterator" in html
    assert "Context manager" in html
