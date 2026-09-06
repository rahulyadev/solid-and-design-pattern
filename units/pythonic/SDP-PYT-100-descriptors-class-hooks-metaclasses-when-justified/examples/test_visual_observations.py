"""Keep the interactive decision visual synchronized with maintained data."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import mechanism_scenarios

VISUAL = Path(__file__).parents[1] / "visuals" / "mechanism-decision-explorer.html"


def embedded_scenarios() -> list[dict[str, str]]:
    html = VISUAL.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="mechanism-scenarios" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("embedded mechanism data was not found")
    value = json.loads(match.group(1))
    assert isinstance(value, list)
    return value


def test_visual_embeds_exact_maintained_decisions() -> None:
    assert embedded_scenarios() == mechanism_scenarios()


def test_visual_covers_the_decision_boundary_not_only_advanced_hooks() -> None:
    decisions = {scenario["decision"] for scenario in embedded_scenarios()}

    assert decisions >= {
        "function + dataclass",
        "property",
        "data descriptor",
        "explicit dictionary",
        "__init_subclass__",
        "in-place class decorator",
        "metaclass __prepare__",
        "do not add a mechanism",
    }


def test_visual_has_required_accessible_targets_and_responsive_rules() -> None:
    html = VISUAL.read_text(encoding="utf-8")

    for target in (
        'id="scenario-tabs"',
        'id="pressure"',
        'id="decision"',
        'id="moment"',
        'id="next-power"',
        'id="why"',
        'id="risk"',
        'id="ladder"',
        'aria-live="polite"',
    ):
        assert target in html
    assert html.count("@media") >= 2
    assert html.count("{") == html.count("}")
