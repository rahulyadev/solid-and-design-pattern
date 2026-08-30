"""Characterize the intentional violation; passing tests do not endorse that provider."""

import pytest
from shape_probe import Maximum, observe, preserving_maximum, sorting_maximum


@pytest.mark.parametrize("provider", [preserving_maximum, sorting_maximum])
def test_result_only_check_misses_the_violation(provider: Maximum) -> None:
    assert observe(provider, [30, 10, 20]).maximum == 30


def test_alias_reveals_the_changed_acquisition_order() -> None:
    safe = observe(preserving_maximum, [30, 10, 20])
    unsafe = observe(sorting_maximum, [30, 10, 20])
    assert safe.before == safe.after == (30, 10, 20)
    assert safe.latest == 20
    assert unsafe.before == (30, 10, 20)
    assert unsafe.after == (10, 20, 30)
    assert unsafe.latest == 30


def test_sorted_fixture_can_hide_the_mutation() -> None:
    result = observe(sorting_maximum, [10, 20, 30])
    assert result.before == result.after


@pytest.mark.parametrize("provider", [preserving_maximum, sorting_maximum])
def test_empty_input_has_a_shared_error_contract(provider: Maximum) -> None:
    values: list[int] = []
    with pytest.raises(ValueError, match="empty"):
        provider(values)
    assert values == []


def test_probe_uses_fresh_input_for_each_run() -> None:
    values = [30, 10, 20]
    observe(sorting_maximum, values)
    assert values == [30, 10, 20]
