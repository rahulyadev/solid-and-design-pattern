"""Reproducibility checks for the SDP-FND-100 import experiments."""

from __future__ import annotations

from cycle_timing_experiment import observe_cycle_timing
from dependency_graph_experiment import observe_dependency_graph
from execution_context_experiment import observe_execution_context
from module_cache_experiment import observe_module_cache
from package_init_experiment import observe_package_initializer


def test_dependency_graph_finds_the_checkout_service_adapter_cycle() -> None:
    observation = observe_dependency_graph()

    assert observation["module_count"] == 5
    assert observation["cycle"] == (
        "checkout_lab.service",
        "checkout_lab.email_adapter",
        "checkout_lab.service",
    )


def test_module_cache_experiment_separates_import_reload_and_reimport() -> None:
    assert observe_module_cache() == {
        "same_object_after_second_import": True,
        "executions_after_second_import": 1,
        "same_object_after_reload": True,
        "executions_after_reload": 2,
        "token_replaced_by_reload": True,
        "new_object_after_cache_deletion": True,
        "fresh_executions_after_cache_deletion": 1,
    }


def test_cycle_timing_experiment_exposes_partial_initialization() -> None:
    assert observe_cycle_timing() == {
        "from_cycle_failed": True,
        "from_cycle_error_is_import_error": True,
        "from_cycle_mentions_partial_initialization": True,
        "module_cycle_loaded": True,
        "alpha_ready_visible_during_beta_load": False,
        "delayed_lookup_result": "beta-ready",
    }


def test_execution_context_experiment_preserves_package_metadata_with_m() -> None:
    assert observe_execution_context() == {
        "direct_file_failed": True,
        "direct_file_relative_import_error": True,
        "module_execution_succeeded": True,
        "module_name": "__main__",
        "package": "execution_probe",
        "spec_name": "execution_probe.report",
        "message": "package-context-preserved",
    }


def test_package_initializer_experiment_exposes_eager_transitive_import() -> None:
    assert observe_package_initializer() == {
        "requested_leaf_value": "leaf-value",
        "public_module_loaded_transitively": True,
        "execution_trace": ("package-init", "public-api", "leaf"),
    }
