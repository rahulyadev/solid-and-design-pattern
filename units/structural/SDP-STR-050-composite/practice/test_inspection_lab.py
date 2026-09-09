"""Characterization of the starter only; these tests do not solve the target."""

import pytest
from inspection_lab import Batch, Check, all_passed


@pytest.mark.parametrize("passed", [False, True])
def test_single_check(passed: bool) -> None:
    assert all_passed(Check("seal", passed)) is passed


def test_flat_batch() -> None:
    assert all_passed(Batch("gate", (Check("seal", True), Check("tag", True))))
    assert not all_passed(Batch("gate", (Check("seal", True), Check("tag", False))))


def test_empty_starter_is_vacuously_true() -> None:
    assert all_passed(Batch("empty", ()))
