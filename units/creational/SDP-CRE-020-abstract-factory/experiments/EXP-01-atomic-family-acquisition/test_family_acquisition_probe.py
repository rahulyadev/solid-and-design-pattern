"""Contract tests for the family-acquisition lifetime probe."""

from __future__ import annotations

from family_acquisition_probe import observe


def test_success_closes_in_reverse_order() -> None:
    assert observe(False) == [
        "primary.open",
        "secondary.open",
        "use:primary+secondary",
        "secondary.close",
        "primary.close",
    ]


def test_partial_failure_closes_already_open_product() -> None:
    assert observe(True) == [
        "primary.open",
        "secondary.open",
        "primary.close",
        "caught:RuntimeError",
    ]
