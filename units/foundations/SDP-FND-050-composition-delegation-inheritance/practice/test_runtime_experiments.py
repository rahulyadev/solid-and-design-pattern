"""Deterministic checks for the SDP-FND-050 runtime observation scripts."""

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


def test_special_method_delegation_observation() -> None:
    assert run_script("special_method_delegation_experiment.py") == [
        "explicit_append=(10, 20, 30)",
        "explicit_count=1",
        "implicit_len=TypeError",
        "implicit_getitem=TypeError",
    ]


def test_cooperative_mro_observation() -> None:
    assert run_script("cooperative_mro_experiment.py") == [
        "mro=CombinedHandler -> AuditLayer -> RetryLayer -> TerminalHandler -> object",
        (
            "trace=AuditLayer.before -> RetryLayer.before -> TerminalHandler -> "
            "RetryLayer.after -> AuditLayer.after"
        ),
    ]
