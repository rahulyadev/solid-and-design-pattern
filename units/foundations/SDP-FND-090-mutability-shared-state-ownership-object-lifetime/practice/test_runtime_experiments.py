"""Reproducibility checks for the SDP-FND-090 runtime experiments."""

from __future__ import annotations

from copy_depth_experiment import observe_copy_depth
from default_argument_experiment import observe_default_argument
from lost_update_experiment import observe_lost_update
from weakref_lifetime_experiment import observe_weak_reference


def test_default_argument_experiment_exposes_one_reused_object() -> None:
    assert observe_default_argument() == {
        "first_value_before_second_call": ("first",),
        "same_result_object": True,
        "default_is_result_object": True,
        "value_after_second_call": ("first", "second"),
    }


def test_copy_depth_experiment_separates_outer_and_nested_identity() -> None:
    assert observe_copy_depth() == {
        "assignment_is_original": True,
        "shallow_is_original": False,
        "shallow_first_step_is_original": True,
        "deep_first_step_is_original": False,
        "original_first_step": ("pick", "scan"),
        "shallow_first_step": ("pick", "scan"),
        "deep_first_step": ("pick",),
    }


def test_weak_reference_experiment_separates_observation_from_ownership() -> None:
    assert observe_weak_reference() == {
        "alive_while_strongly_registered": True,
        "dead_after_strong_owner_releases": True,
    }


def test_lost_update_experiment_forces_and_then_protects_the_transition() -> None:
    assert observe_lost_update() == {
        "unsafe_expected_if_both_counted": 2,
        "unsafe_observed": 1,
        "locked_observed": 2,
    }
