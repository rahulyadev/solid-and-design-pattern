"""Keep the interactive visual synchronized with executable lifecycle observations."""

from __future__ import annotations

import json
import re
from pathlib import Path

from visual_data import lifecycle_scenarios

VISUAL = Path(__file__).parents[1] / "visuals" / "plugin-lifecycle-explorer.html"


def embedded_scenarios() -> list[dict[str, object]]:
    html = VISUAL.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="lifecycle-scenarios" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("embedded lifecycle scenario data was not found")
    value = json.loads(match.group(1))
    assert isinstance(value, list)
    return value


def test_visual_embeds_exact_runtime_backed_scenarios() -> None:
    assert embedded_scenarios() == lifecycle_scenarios()


def test_visual_covers_every_lifecycle_stage_and_both_failure_policies() -> None:
    scenarios = embedded_scenarios()
    paths: list[object] = []
    for scenario in scenarios:
        path = scenario["path"]
        assert isinstance(path, list)
        paths.extend(path)
    combined_paths = " ".join(str(item) for item in paths)

    for stage in (
        "registration",
        "discovery",
        "load",
        "construction",
        "validation",
        "activation",
        "invocation",
    ):
        assert stage in combined_paths
    assert {str(scenario["policy"]) for scenario in scenarios} >= {
        "fail fast",
        "quarantine optional providers",
    }
