"""Executable claims for the two focused runtime experiments."""

from entry_point_probe import observe_entry_point_boundary
from import_process_probe import observe_import_boundaries


def test_entry_point_discovery_does_not_import_but_load_does() -> None:
    observation = observe_entry_point_boundary()

    assert observation.name == "fixture"
    assert observation.group == "sdp.pyt090.fixture"
    assert observation.value == "sdp_pyt090_fixture_runtime:provide"
    assert observation.module == "sdp_pyt090_fixture_runtime"
    assert observation.attribute == "provide"
    assert observation.distribution == "Acme-Report-Plugin"
    assert observation.version == "2.4.0"
    assert observation.imported_during_discovery is False
    assert observation.import_executions_after_two_loads == 1
    assert observation.same_loaded_object is True
    assert observation.provider_result == "synthetic-provider-ready"


def test_import_cache_and_process_boundaries() -> None:
    observation = observe_import_boundaries()

    assert observation.same_module_in_process is True
    assert observation.same_token_in_process is True
    assert observation.executions_after_same_process_imports == 1
    assert observation.executions_after_two_child_processes == 3
    assert observation.cycle_error_type == "ImportError"
    assert observation.cycle_modules_cached_after_failure is False
