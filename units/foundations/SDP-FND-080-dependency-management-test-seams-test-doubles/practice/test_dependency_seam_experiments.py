"""Reproducibility checks for the completed SDP-FND-080 experiments."""

from __future__ import annotations

from fake_contract_experiment import observe_fake_contract
from mock_strictness_experiment import observe_mock_strictness
from patch_lookup_experiment import observe_patch_lookup


def test_patch_lookup_experiment_separates_definition_and_use_site_names() -> None:
    assert observe_patch_lookup() == {
        "definition_patch_changed_imported_alias": False,
        "definition_patch_changed_module_lookup": True,
        "use_site_patch_changed_imported_alias": True,
    }


def test_mock_strictness_experiment_exposes_loose_and_strict_behavior() -> None:
    assert observe_mock_strictness() == {
        "loose_created_typo_attribute": True,
        "strict_rejected_typo": True,
        "strict_rejected_wrong_signature": True,
        "stubbed_value": "pay-42",
        "recorded_valid_calls": 1,
    }


def test_fake_contract_experiment_exposes_semantic_drift() -> None:
    assert observe_fake_contract() == {
        "sqlite_adapter": True,
        "naive_fake": False,
        "contract_faithful_fake": True,
    }
