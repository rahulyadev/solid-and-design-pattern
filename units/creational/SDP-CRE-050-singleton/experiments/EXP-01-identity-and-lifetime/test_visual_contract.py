import json
import re
from dataclasses import asdict
from html.parser import HTMLParser
from pathlib import Path

from identity_probe import observe

HTML = Path(__file__).resolve().parents[2] / "visuals" / "identity-explorer.html"


class Inventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.options: list[str] = []
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append((tag, values))
        if values.get("id") is not None:
            self.ids.append(str(values["id"]))
        if tag == "option":
            self.options.append(str(values["value"]))


def test_visual_matches_every_measured_field() -> None:
    text = HTML.read_text()
    matched = re.search(
        r'<script id="observations" type="application/json">(.*?)</script>', text, re.DOTALL
    )
    assert matched is not None
    assert json.loads(matched.group(1)) == [asdict(row) for row in observe()]


def test_accessible_structure_and_element_references() -> None:
    text = HTML.read_text()
    inventory = Inventory()
    inventory.feed(text)
    assert len(inventory.ids) == len(set(inventory.ids))
    assert inventory.options == [
        "repeated-init",
        "cache-race",
        "locked-provider",
        "retry",
        "two-apps",
    ]
    assert set(re.findall(r"getElementById\('([^']+)'\)", text)) <= set(inventory.ids)
    assert any(tag == "label" and attrs.get("for") == "scenario" for tag, attrs in inventory.tags)
    assert any(attrs.get("aria-live") == "polite" for _, attrs in inventory.tags)
    assert 'name="viewport"' in text
    assert "prefers-color-scheme:dark" in text
    assert "@media(max-width:420px)" in text
    assert "addEventListener('change',render)" in text
    assert "render();" in text
    for heading in ("How to read this visual", "Key insight", "Simplification or limitation"):
        assert heading in text
    assert "fetch(" not in text and "http" not in text
