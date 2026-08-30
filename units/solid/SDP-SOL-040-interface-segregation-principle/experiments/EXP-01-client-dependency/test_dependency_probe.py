"""The rejected case is an observed negative control, not a skipped failing test."""

import pytest
from dependency_probe import Observation, run_probes


@pytest.fixture(scope="module")
def observations() -> tuple[Observation, ...]:
    return run_probes()


@pytest.mark.parametrize("index", [0, 1, 2])
def test_actual_preview_call_is_unchanged(
    observations: tuple[Observation, ...], index: int
) -> None:
    assert observations[index].runtime_result == "hello"


def test_original_small_shared_contract_accepts_reader(
    observations: tuple[Observation, ...],
) -> None:
    assert observations[0].static_accepted
    assert observations[0].error_codes == ()


def test_growth_rejects_reader_for_unused_operations(
    observations: tuple[Observation, ...],
) -> None:
    result = observations[1]
    assert not result.static_accepted
    assert result.error_codes == ("arg-type",)
    assert "write" in result.diagnostics
    assert "remove" in result.diagnostics


def test_client_boundary_survives_unrelated_contract_growth(
    observations: tuple[Observation, ...],
) -> None:
    assert observations[2].static_accepted
    assert observations[2].error_codes == ()
