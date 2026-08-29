"""Deterministic checks for the SDP-FND-070 controlled experiments."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_script(filename: str) -> list[str]:
    """Run one neighboring experiment in a fresh interpreter."""

    script = Path(__file__).with_name(filename)
    completed = subprocess.run(
        [sys.executable, str(script)],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip().splitlines()


def test_protocol_runtime_observation() -> None:
    dynamic_result = "False" if sys.version_info >= (3, 12) else "True"
    assert run_script("protocol_runtime_experiment.py") == [
        "compatible_call=ok:5",
        "compatible_runtime_protocol=True",
        "wrong_runtime_protocol=True",
        "wrong_actual_call=TypeError",
        "dynamic_hasattr=True",
        "dynamic_call=dynamic:5",
        f"dynamic_runtime_protocol={dynamic_result}",
    ]


def test_abc_virtual_subclass_observation() -> None:
    assert run_script("abc_virtual_subclass_experiment.py") == [
        "nominal_isinstance=True",
        "nominal_in_mro=True",
        "nominal_default=sends-text",
        "registered_isinstance=True",
        "registered_in_mro=False",
        "registered_has_default=False",
        "registered_call=registered:5",
        "incomplete_isinstance=True",
        "incomplete_actual_call=AttributeError",
    ]


def test_protocol_static_observation() -> None:
    assert run_script("protocol_static_experiment.py") == [
        "compatible: returncode=0 errors=0 codes=-",
        "wrong_signature: returncode=1 errors=1 codes=arg-type",
    ]
