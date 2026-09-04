"""Keep the interactive visual's data synchronized with Python observations."""

import json
import re
from pathlib import Path

from dispatch_tools import visual_observations


def test_visual_embeds_the_observed_python_data() -> None:
    visual = Path(__file__).parents[1] / "visuals" / "dispatch-boundary.html"
    source = visual.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="observations" type="application/json">\s*(.*?)\s*</script>',
        source,
        flags=re.DOTALL,
    )
    assert match is not None
    assert json.loads(match.group(1)) == visual_observations()
