"""Verify observable outcomes of the fault injection, not function boundaries."""

import pytest
from effects_experiment import Failure, Style, observe, retry_after_error


@pytest.mark.parametrize("style", ["mixed", "split"])
@pytest.mark.parametrize(
    ("failure", "saved", "delivered", "error"),
    [
        ("none", 1, 1, False),
        ("save", 0, 0, True),
        ("before_notify", 1, 0, True),
        ("after_notify", 1, 1, True),
    ],
)
def test_effects_visible_after_each_outcome(
    style: Style,
    failure: Failure,
    saved: int,
    delivered: int,
    error: bool,
) -> None:
    observed = observe(style, failure)
    assert observed.saved == ("PICKUP-17",) * saved
    assert observed.delivered == ("PICKUP-17",) * delivered
    assert observed.error is error


@pytest.mark.parametrize("style", ["mixed", "split"])
def test_retry_can_duplicate_an_already_completed_effect(style: Style) -> None:
    observed = retry_after_error(style)
    assert observed.saved == ("PICKUP-17", "PICKUP-17")
    assert observed.delivered == ("PICKUP-17", "PICKUP-17")
    assert observed.error is False
