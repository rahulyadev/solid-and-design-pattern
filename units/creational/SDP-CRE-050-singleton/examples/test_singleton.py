import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from copy import copy, deepcopy
from pathlib import Path
from pickle import dumps, loads

import pytest
from singleton import ProcessMarker


def test_constructor_identity() -> None:
    assert ProcessMarker() is ProcessMarker()


def test_threads_share_marker() -> None:
    with ThreadPoolExecutor(max_workers=4) as executor:
        values = list(executor.map(lambda _: ProcessMarker(), range(12)))
    assert all(value is values[0] for value in values)


@pytest.mark.parametrize("operation", [copy, deepcopy, lambda value: loads(dumps(value))])
def test_explicit_copy_and_pickle_policy(operation) -> None:
    marker = ProcessMarker()
    assert operation(marker) is marker


def test_runtime_subclass_policy() -> None:
    with pytest.raises(TypeError, match="subclasses"):
        type("ChildMarker", (ProcessMarker,), {})


def test_direct_allocation_is_outside_cooperative_contract() -> None:
    assert object.__new__(ProcessMarker) is not ProcessMarker()


def test_marker_has_no_instance_state() -> None:
    with pytest.raises(AttributeError):
        ProcessMarker().label = "mutable"


def test_fresh_process_reconstructs_its_own_marker() -> None:
    import singleton

    # The parent-only binding must not appear in a newly started interpreter.
    singleton.parent_only = True
    try:
        source = (
            "import json, os, singleton; "
            "from pickle import dumps, loads; "
            "m = singleton.ProcessMarker(); "
            "print(json.dumps([os.getpid(), hasattr(singleton, 'parent_only'), "
            "m is loads(dumps(m))]))"
        )
        child = subprocess.run(
            [sys.executable, "-c", source],
            cwd=Path(__file__).parent,
            check=True,
            text=True,
            capture_output=True,
            timeout=10,
        )
        pid, inherited, identity = json.loads(child.stdout)
        assert pid != os.getpid()
        assert inherited is False
        assert identity is True
    finally:
        delattr(singleton, "parent_only")


def test_loading_same_file_under_two_names_creates_two_classes() -> None:
    source = """
import importlib.util
import singleton
spec = importlib.util.spec_from_file_location('second_marker', singleton.__file__)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert singleton.ProcessMarker is not module.ProcessMarker
assert singleton.ProcessMarker() is not module.ProcessMarker()
print('two class objects, two markers')
"""
    result = subprocess.run(
        [sys.executable, "-c", source],
        cwd=Path(__file__).parent,
        check=True,
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.stdout.strip() == "two class objects, two markers"
