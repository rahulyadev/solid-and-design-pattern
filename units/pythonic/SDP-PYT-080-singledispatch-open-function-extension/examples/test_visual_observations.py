"""Keep the interactive visual synchronized with executable observations."""

import json
import re
from pathlib import Path

from visual_data import visual_scenarios

VISUAL_PATH = Path(__file__).parents[1] / "visuals" / "dispatch-resolution-explorer.html"


def test_embedded_scenarios_match_runtime_observations() -> None:
    html = VISUAL_PATH.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="dispatch-scenarios" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )

    assert match is not None
    assert json.loads(match.group(1)) == visual_scenarios()


def test_visual_has_required_guidance_and_accessible_controls() -> None:
    html = VISUAL_PATH.read_text(encoding="utf-8")

    assert "How to read this visual" in html
    assert "Key insight" in html
    assert "Simplification or limitation" in html
    assert 'aria-live="polite"' in html
    assert 'button.type = "button"' in html
    assert "aria-pressed" in html
