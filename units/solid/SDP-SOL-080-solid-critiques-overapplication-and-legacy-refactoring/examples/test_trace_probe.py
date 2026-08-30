"""Fixed counterexamples for the deliberately unsafe eager transformation."""

import pytest
from name_export import export_eager, export_legacy, export_refactored
from trace_probe import SCENARIOS, Scenario, observe


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_extraction_preserves_each_observed_boundary(scenario: Scenario) -> None:
    assert observe(export_refactored, scenario) == observe(export_legacy, scenario)


def test_equal_success_values_hide_different_read_write_order() -> None:
    before = observe(export_legacy, "success")
    eager = observe(export_eager, "success")
    assert before.result == eager.result == 3
    assert before.saved == eager.saved == ("[MIRA]", "[OMAR]", "[ASHA]")
    assert before.trace[:3] == ("read 'Mira'", "call '[MIRA]'", "save '[MIRA]'")
    assert eager.trace[:3] == ("read 'Mira'", "read 'Omar'", "read 'Asha'")


@pytest.mark.parametrize("scenario", ("empty-name", "source-failure"))
def test_equal_errors_hide_lost_prefix_effects(scenario: Scenario) -> None:
    before = observe(export_legacy, scenario)
    eager = observe(export_eager, scenario)
    assert before.result is eager.result is None
    assert before.error == eager.error
    assert before.saved == ("[MIRA]",)
    assert eager.saved == ()


@pytest.mark.parametrize("scenario", ("sink-before", "sink-after"))
def test_eager_reads_unneeded_tail_on_writer_failure(scenario: Scenario) -> None:
    before = observe(export_legacy, scenario)
    eager = observe(export_eager, scenario)
    assert before.error == eager.error
    assert before.consumed == ("Mira", "Omar")
    assert eager.consumed == ("Mira", "Omar", "Asha")


def test_exception_does_not_mean_nothing_was_saved() -> None:
    observation = observe(export_legacy, "sink-after")
    assert observation.result is None
    assert observation.error == "OSError: acknowledgement lost"
    assert observation.saved == ("[MIRA]", "[OMAR]")
