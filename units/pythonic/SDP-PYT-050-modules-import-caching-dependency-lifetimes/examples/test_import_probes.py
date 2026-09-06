"""Tests for the two runtime experiments."""

from __future__ import annotations

from import_cache_probe import observe_import_cache
from process_scope_probe import observe_process_scope


def test_import_cache_reload_and_alias_observations() -> None:
    assert observe_import_cache() == {
        "first_execution_count": 1,
        "repeat_returns_same_module": True,
        "execution_count_after_repeat": 1,
        "reload_reuses_module": True,
        "execution_count_after_reload": 2,
        "imported_alias_stays_old": True,
        "cache_deletion_creates_new_module": True,
        "new_module_execution_count": 1,
    }


def test_two_processes_have_separate_import_caches() -> None:
    assert observe_process_scope() == {
        "child_processes": 2,
        "distinct_processes": True,
        "each_process_executes_target_once": True,
        "each_process_reuses_its_own_module": True,
    }
