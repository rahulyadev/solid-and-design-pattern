"""Baseline behavior only; target requirements remain a learner task."""

import pytest
from dispatch_lab import TARGET_REFACTOR_COMPLETE, prepare_dispatch


@pytest.mark.parametrize("channel", ["internal", "partner"])
def test_baseline_channels(channel: str) -> None:
    source = ["queue-a"]
    result = prepare_dispatch(channel=channel, destinations=source)
    source.append("queue-b")
    assert result.destinations == ["queue-a"] and result.attempts == []


@pytest.mark.parametrize("channel,targets", [("unknown", ["q"]), ("internal", [])])
def test_baseline_validation(channel: str, targets: list[str]) -> None:
    with pytest.raises(ValueError):
        prepare_dispatch(channel=channel, destinations=targets)


def test_exercise_is_still_unsolved() -> None:
    assert TARGET_REFACTOR_COMPLETE is False
