import json
import re
from pathlib import Path

from visual_data import SCENARIOS

VISUAL = Path(__file__).parents[1] / "visuals" / "interface-mechanism-chooser.html"


def test_visual_embeds_the_maintained_semantic_model() -> None:
    html = VISUAL.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="scenario-data" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )

    assert match is not None
    assert json.loads(match.group(1)) == SCENARIOS


def test_visual_is_self_contained_and_has_required_guidance() -> None:
    html = VISUAL.read_text(encoding="utf-8")

    assert "https://" not in html
    assert "http://" not in html
    assert "How to read this visual" in html
    assert "Key insight" in html
    assert "Simplification or limitation" in html
