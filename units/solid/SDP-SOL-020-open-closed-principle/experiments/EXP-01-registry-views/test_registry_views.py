"""Keep the experiment's observations reproducible without depending on object addresses."""

from registry_views import binding_observations, state_observations


def test_rebinding_is_visible_through_live_view_but_not_copied_bindings() -> None:
    before, after, _ = binding_observations()
    assert before == "before: live=plain:7; snapshot=plain:7"
    assert after == "after replacement: live=LOUD:7; snapshot=plain:7"


def test_adding_a_name_does_not_add_it_to_the_snapshot() -> None:
    assert binding_observations()[2] == "names: live=('display', 'extra'); snapshot=('display',)"


def test_snapshot_does_not_freeze_the_state_of_its_callable_values() -> None:
    assert state_observations() == (
        "callable state before: first:7",
        "callable state after: second:7",
    )
