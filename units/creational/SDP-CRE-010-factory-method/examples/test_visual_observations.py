"""Keep the interactive construction visual synchronized with maintained data."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import construction_scenarios

VISUAL = Path(__file__).parents[1] / "visuals" / "construction-decision-explorer.html"


def embedded_scenarios() -> list[dict[str, str]]:
    html = VISUAL.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="construction-scenarios" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("embedded construction data was not found")
    value = json.loads(match.group(1))
    assert isinstance(value, list)
    return value


def test_visual_embeds_exact_maintained_decisions() -> None:
    assert embedded_scenarios() == construction_scenarios()


def test_visual_covers_the_full_selection_ladder() -> None:
    decisions = {scenario["decision"] for scenario in embedded_scenarios()}

    assert decisions == {
        "direct construction",
        "small conditional",
        "dictionary of callables",
        "injected factory callable",
        "GoF Factory Method",
        "alternate classmethod constructor",
        "dynamic registration boundary",
        "reject service locator",
    }


def test_visual_has_accessible_targets_and_responsive_rules() -> None:
    html = VISUAL.read_text(encoding="utf-8")

    for target in (
        'id="scenario-tabs"',
        'id="pressure"',
        'id="decision"',
        'id="boundary"',
        'id="reject"',
        'id="because"',
        'id="ladder"',
        'aria-live="polite"',
    ):
        assert target in html
    assert html.count("@media") >= 2
    assert html.count("{") == html.count("}")
