"""Keep the interactive visual's embedded model aligned with Python data."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import lifetime_states


def test_visual_embeds_every_canonical_lifetime_state() -> None:
    visual = Path(__file__).parents[1] / "visuals" / "lifetime-map.html"
    html = visual.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="lifetime-data" type="application/json">\s*(.*?)\s*</script>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None
    assert json.loads(match.group(1)) == lifetime_states()
