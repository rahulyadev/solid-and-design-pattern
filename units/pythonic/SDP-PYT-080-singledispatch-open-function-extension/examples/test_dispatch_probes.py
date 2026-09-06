"""Tests for the two controlled runtime experiments."""

from dispatch_mechanics_probe import MechanicsObservation, observe_mechanics
from registration_order_probe import RegistrationOutcome, observe_import_orders


def test_resolution_and_ambiguity_probe() -> None:
    assert observe_mechanics() == MechanicsObservation(
        bool_before_exact_registration="int",
        bool_after_exact_registration="bool",
        selected_after_exact_registration="classify_bool",
        parameterized_registration_error="TypeError",
        ambiguous_abc_error="RuntimeError",
    )


def test_registration_import_order_probe_uses_fresh_processes() -> None:
    assert observe_import_orders() == (
        RegistrationOutcome(
            ("alpha", "beta"),
            "beta:ext-9",
            "extension_beta.summarize_external_beta",
        ),
        RegistrationOutcome(
            ("beta", "alpha"),
            "alpha:ext-9",
            "extension_alpha.summarize_external_alpha",
        ),
    )
