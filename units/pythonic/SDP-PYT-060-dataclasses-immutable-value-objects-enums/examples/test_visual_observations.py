"""Keep the visual's embedded model aligned with maintained Python data."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import VISUAL_STATES

VISUAL = Path(__file__).parents[1] / "visuals" / "value-object-boundary.html"


def test_embedded_visual_model_matches_maintained_states() -> None:
    html = VISUAL.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="model-data" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )

    assert match is not None
    assert json.loads(match.group(1)) == VISUAL_STATES


def test_visual_has_native_controls_and_required_reading_guidance() -> None:
    html = VISUAL.read_text(encoding="utf-8")

    assert html.count('class="stage-button"') == len(VISUAL_STATES)
    assert "<button" in html
    assert "How to read this visual" in html
    assert "Key insight" in html
    assert "Simplification or limitation" in html
