"""Prevent the published visual from drifting away from the Python observation."""

import json
from html.parser import HTMLParser
from pathlib import Path

from binding_probe import observations


class ObservationData(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.inside_data = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script" and dict(attrs).get("id") == "observations":
            self.inside_data = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self.inside_data = False

    def handle_data(self, data: str) -> None:
        if self.inside_data:
            self.parts.append(data)


def test_visual_data_matches_reproduced_python_observations() -> None:
    visual = Path(__file__).resolve().parents[1] / "visuals" / "callable-state.html"
    parser = ObservationData()
    parser.feed(visual.read_text())
    assert parser.parts, "The visual must contain its offline observation data."
    assert json.loads("".join(parser.parts)) == observations()
