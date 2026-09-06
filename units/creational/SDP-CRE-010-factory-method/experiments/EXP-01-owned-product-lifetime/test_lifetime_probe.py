"""Protect the observed lifetime trace."""

from __future__ import annotations

import pytest
from lifetime_probe import ProbeProduct, observe_lifetimes, run_failure, run_once


def test_success_closes_after_use() -> None:
    assert run_once(fail=False) == ("construct", "use", "close")


def test_failure_still_closes() -> None:
    trace: list[str] = []
    product = ProbeProduct(trace, fail=True)

    with pytest.raises(RuntimeError, match="synthetic"):
        try:
            product.use()
        finally:
            product.close()

    assert trace == ["construct", "use", "close"]


def test_recorded_probe_is_deterministic() -> None:
    result = observe_lifetimes()

    assert result.success_trace == ("construct", "use", "close")
    assert result.failure_trace == (
        "construct",
        "use",
        "close",
        "caught:RuntimeError",
    )


def test_failure_probe_preserves_actual_event_order() -> None:
    assert run_failure() == ("construct", "use", "close", "caught:RuntimeError")
