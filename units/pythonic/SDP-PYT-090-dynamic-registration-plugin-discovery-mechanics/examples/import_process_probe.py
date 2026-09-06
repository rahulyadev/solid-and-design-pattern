"""Observe import caching, process-local execution, and a circular import failure."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

CACHE_MODULE = "sdp_pyt090_cache_target"
CYCLE_ALPHA = "sdp_pyt090_cycle_alpha"
CYCLE_BETA = "sdp_pyt090_cycle_beta"


@dataclass(frozen=True, slots=True)
class ImportObservation:
    same_module_in_process: bool
    same_token_in_process: bool
    executions_after_same_process_imports: int
    executions_after_two_child_processes: int
    cycle_error_type: str
    cycle_modules_cached_after_failure: bool


def _write_modules(root: Path, marker: Path) -> None:
    (root / f"{CACHE_MODULE}.py").write_text(
        f"""from pathlib import Path

_MARKER = Path({str(marker)!r})
with _MARKER.open("a", encoding="utf-8") as stream:
    stream.write("executed\\n")

TOKEN = object()
""",
        encoding="utf-8",
    )
    (root / f"{CYCLE_ALPHA}.py").write_text(
        f"from {CYCLE_BETA} import VALUE_B\nVALUE_A = 'alpha'\n",
        encoding="utf-8",
    )
    (root / f"{CYCLE_BETA}.py").write_text(
        f"from {CYCLE_ALPHA} import VALUE_A\nVALUE_B = 'beta'\n",
        encoding="utf-8",
    )


def _child_environment(root: Path) -> dict[str, str]:
    environment = dict(os.environ)
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = str(root) if not existing else f"{root}{os.pathsep}{existing}"
    return environment


def observe_import_boundaries() -> ImportObservation:
    with TemporaryDirectory(prefix="sdp-pyt090-import-") as temporary:
        root = Path(temporary)
        marker = root / "execution-marker.txt"
        _write_modules(root, marker)
        sys.path.insert(0, str(root))
        importlib.invalidate_caches()
        try:
            first = importlib.import_module(CACHE_MODULE)
            second = importlib.import_module(CACHE_MODULE)
            same_process_executions = marker.read_text(encoding="utf-8").count("executed\n")

            child_command = (sys.executable, "-c", f"import {CACHE_MODULE}")
            for _ in range(2):
                subprocess.run(
                    child_command,
                    check=True,
                    capture_output=True,
                    text=True,
                    env=_child_environment(root),
                )
            all_executions = marker.read_text(encoding="utf-8").count("executed\n")

            try:
                importlib.import_module(CYCLE_ALPHA)
            except Exception as error:
                cycle_error_type = type(error).__name__
            else:
                cycle_error_type = "none"

            return ImportObservation(
                same_module_in_process=first is second,
                same_token_in_process=first.TOKEN is second.TOKEN,
                executions_after_same_process_imports=same_process_executions,
                executions_after_two_child_processes=all_executions,
                cycle_error_type=cycle_error_type,
                cycle_modules_cached_after_failure=(
                    CYCLE_ALPHA in sys.modules or CYCLE_BETA in sys.modules
                ),
            )
        finally:
            sys.path.remove(str(root))
            for module_name in (CACHE_MODULE, CYCLE_ALPHA, CYCLE_BETA):
                sys.modules.pop(module_name, None)
            importlib.invalidate_caches()


def main() -> None:
    for key, value in asdict(observe_import_boundaries()).items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
