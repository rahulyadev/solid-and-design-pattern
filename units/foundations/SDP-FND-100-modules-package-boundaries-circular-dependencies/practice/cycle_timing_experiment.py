"""Compare immediate from-binding with delayed module attribute lookup in a cycle."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

PRACTICE_DIR = Path(__file__).resolve().parent
FROM_PREFIX = "cycle_examples.from_cycle"
MODULE_PREFIX = "cycle_examples.module_cycle"


def _clear_modules(prefix: str) -> None:
    for name in tuple(sys.modules):
        if name == prefix or name.startswith(f"{prefix}."):
            sys.modules.pop(name, None)


def observe_cycle_timing() -> dict[str, object]:
    """Return stable facts from one failing and one completing source cycle."""

    failing = subprocess.run(
        [sys.executable, "-c", f"import {FROM_PREFIX}.alpha"],
        cwd=PRACTICE_DIR,
        check=False,
        capture_output=True,
        text=True,
    )

    _clear_modules(MODULE_PREFIX)
    alpha = importlib.import_module(f"{MODULE_PREFIX}.alpha")
    beta = importlib.import_module(f"{MODULE_PREFIX}.beta")
    observation = {
        "from_cycle_failed": failing.returncode != 0,
        "from_cycle_error_is_import_error": "ImportError" in failing.stderr,
        "from_cycle_mentions_partial_initialization": (
            "partially initialized module" in failing.stderr
        ),
        "module_cycle_loaded": True,
        "alpha_ready_visible_during_beta_load": beta.ALPHA_READY_VISIBLE_DURING_BETA_LOAD,
        "delayed_lookup_result": alpha.read_beta(),
    }
    _clear_modules(MODULE_PREFIX)
    return observation


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_cycle_timing().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
