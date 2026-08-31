"""Fixed observations make the runtime claims falsifiable."""

from binding_probe import capture_trace, loop_observation
from effects_probe import make_counter, observe_effects


def test_mutation_reaches_reference_holders_but_not_the_integer_snapshot() -> None:
    before, mutated, _ = capture_trace()
    assert before["closure"] == before["default"] == before["partial"] == [2]
    assert mutated["current"] == mutated["original"] == [2, 5]
    assert mutated["closure"] == mutated["default"] == mutated["partial"] == [2, 5]
    assert mutated["snapshot"] == [2]
    assert before["current"] == [2]  # Observations themselves were copied.


def test_rebinding_changes_only_the_reader_of_the_outer_binding() -> None:
    rebound = capture_trace()[-1]
    assert rebound["current"] == rebound["closure"] == [8]
    assert rebound["original"] == rebound["default"] == rebound["partial"] == [2, 5]
    assert rebound["snapshot"] == [2]


def test_loop_calls_after_construction_show_shared_vs_distinct_bindings() -> None:
    result = loop_observation()
    assert result["configured"] == [2, 5, 8]
    assert result["late"] == [8, 8, 8]
    assert result["default"] == result["factory"] == [2, 5, 8]
    assert result["shared_cell"] is True
    assert result["separate_cells"] is True


def test_counter_alias_is_same_state_and_factory_calls_are_independent() -> None:
    first = make_counter()
    alias = first
    second = make_counter()
    assert [first(), alias(), second(), first()] == [1, 2, 1, 3]


def test_deferred_effects_are_not_transactional_or_automatically_idempotent() -> None:
    result = observe_effects()
    assert result["before_execution"] == []
    assert result["after_failure"] == ["events:ready", "events:stop"]
    assert result["same_exception"] is True
    assert result["after_replay"] == ["events:ready", "events:stop", "events:ready"]
