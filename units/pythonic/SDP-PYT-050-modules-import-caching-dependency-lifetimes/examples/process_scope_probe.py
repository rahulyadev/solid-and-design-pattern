"""Reproducible process-scope observations for SDP-PYT-050."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import TypedDict, cast


class ChildObservation(TypedDict):
    execution_count: int
    module_reused: bool
    pid: int


def _parse_child(stdout: str) -> ChildObservation:
    raw = json.loads(stdout)
    if not isinstance(raw, dict):
        raise RuntimeError("child did not return a JSON object")
    if not isinstance(raw.get("execution_count"), int):
        raise RuntimeError("child returned an invalid execution count")
    if not isinstance(raw.get("module_reused"), bool):
        raise RuntimeError("child returned an invalid reuse observation")
    if not isinstance(raw.get("pid"), int):
        raise RuntimeError("child returned an invalid process id")
    return cast(ChildObservation, raw)


def observe_process_scope(
    python_executable: str = sys.executable,
) -> dict[str, bool | int]:
    """Start two overlapping interpreters and normalize their observations."""

    child_path = Path(__file__).with_name("process_scope_child.py")
    processes: list[subprocess.Popen[str]] = [
        subprocess.Popen(
            [python_executable, str(child_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for _ in range(2)
    ]
    observations: list[ChildObservation] = []
    for process in processes:
        stdout, stderr = process.communicate(timeout=10)
        if process.returncode != 0:
            raise RuntimeError(f"child failed with {process.returncode}: {stderr.strip()}")
        observations.append(_parse_child(stdout))

    return {
        "child_processes": len(observations),
        "distinct_processes": len({item["pid"] for item in observations}) == 2,
        "each_process_executes_target_once": all(
            item["execution_count"] == 1 for item in observations
        ),
        "each_process_reuses_its_own_module": all(item["module_reused"] for item in observations),
    }


def main() -> None:
    print(json.dumps(observe_process_scope(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
