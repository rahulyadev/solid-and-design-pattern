"""Baseline characterization only; passing these does not solve the extension."""

from trail_lab import Stop, WalkingTextGuide


def test_original_walking_order() -> None:
    assert WalkingTextGuide().render((Stop("Pond", False), Stop("Tower", True))) == "Pond -> Tower"


def test_original_empty() -> None:
    assert WalkingTextGuide().render(()) == ""


def test_original_duplicate_names_are_preserved() -> None:
    assert WalkingTextGuide().render((Stop("Pond", False), Stop("Pond", False))) == "Pond -> Pond"
