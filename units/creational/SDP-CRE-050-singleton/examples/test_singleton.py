import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from copy import copy, deepcopy
from pathlib import Path
from pickle import HIGHEST_PROTOCOL, dumps, loads

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


def test_cold_first_construction_under_concurrent_access() -> None:
    source = """
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from singleton import ProcessMarker
start = Barrier(4, timeout=5)
def get():
    start.wait()
    return ProcessMarker()
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(get) for _ in range(4)]
    markers = [future.result(timeout=10) for future in futures]
assert all(marker is markers[0] for marker in markers)
print('cold concurrent identity preserved')
"""
    child = subprocess.run(
        [sys.executable, "-c", source],
        cwd=Path(__file__).parent,
        check=True,
        text=True,
        capture_output=True,
        timeout=15,
    )
    assert child.stdout.strip() == "cold concurrent identity preserved"


@pytest.mark.parametrize("protocol", range(HIGHEST_PROTOCOL + 1))
def test_all_supported_pickle_protocols_preserve_marker(protocol: int) -> None:
    marker = ProcessMarker()
    assert loads(dumps(marker, protocol=protocol)) is marker


def test_deep_copy_of_repeated_marker_references() -> None:
    marker = ProcessMarker()
    original = [marker, marker]
    copied = deepcopy(original)
    assert copied is not original
    assert copied[0] is copied[1] is marker
