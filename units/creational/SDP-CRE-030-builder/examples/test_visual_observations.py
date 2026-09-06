"""Keep the HTML Builder explorer aligned with maintained Python data."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import SCENARIOS

HTML_PATH = Path(__file__).parents[1] / "visuals" / "construction-pressure-explorer.html"


def _html() -> str:
    return HTML_PATH.read_text(encoding="utf-8")


def _embedded_scenarios() -> list[dict[str, object]]:
    match = re.search(r"const SCENARIOS = (\[.*?\]);", _html(), re.DOTALL)
    assert match is not None
    return json.loads(match.group(1))


def test_every_visual_field_matches_maintained_python_data() -> None:
    assert _embedded_scenarios() == list(SCENARIOS)


def test_visual_covers_simpler_builder_director_ordering_and_shared_state() -> None:
    assert {scenario["id"] for scenario in SCENARIOS} == {
        "keywords",
        "factory",
        "locals",
        "builder",
        "director",
        "fluent-only",
        "ordered",
        "shared",
    }


def test_visual_has_accessible_keyboard_and_responsive_contracts() -> None:
    html = _html()

    for marker in (
        'role="tablist"',
        'role="tabpanel"',
        'aria-live="polite"',
        'button.addEventListener("keydown"',
        "ArrowLeft",
        "ArrowRight",
        "@media (max-width: 920px)",
        "@media (prefers-reduced-motion: reduce)",
    ):
        assert marker in html
    assert html.count("{") == html.count("}")
