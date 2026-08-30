"""Protect the teaching example's observable contract across the refactoring."""

from collections.abc import Callable

import pytest
from parcel_labels import (
    HandlingCode,
    HandlingDecision,
    Parcel,
    StoreLabel,
    mixed_label,
    publish_label,
)


@pytest.mark.parametrize("publish", [mixed_label, publish_label])
@pytest.mark.parametrize(
    ("weight", "fragile", "expected"),
    [
        (1, False, "standard"),
        (2000, False, "standard"),
        (2001, False, "manual"),
        (1, True, "manual"),
        (2000, True, "manual"),
    ],
)
def test_label_contract(
    publish: Callable[[Parcel, StoreLabel], HandlingDecision],
    weight: int,
    fragile: bool,
    expected: HandlingCode,
) -> None:
    stored: dict[str, str] = {}
    decision = publish(Parcel("P-17", weight, fragile), stored.__setitem__)
    assert decision == HandlingDecision("P-17", expected)
    assert stored == {"P-17": f"P-17 | handling={expected}"}


@pytest.mark.parametrize(("parcel_id", "weight"), [("", 1), ("  ", 1), ("P-17", 0), ("P-17", -1)])
def test_invalid_parcel(parcel_id: str, weight: int) -> None:
    with pytest.raises(ValueError):
        Parcel(parcel_id, weight)


def test_storage_failure_is_visible_to_the_caller() -> None:
    def unavailable_store(parcel_id: str, text: str) -> None:
        raise OSError("synthetic storage failure")

    with pytest.raises(OSError, match="synthetic storage failure"):
        publish_label(Parcel("P-17", 2000), unavailable_store)
