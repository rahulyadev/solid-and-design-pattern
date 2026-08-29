"""Compare direct internal-file execution with Python's -m module execution."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PRACTICE_DIR = Path(__file__).resolve().parent


def observe_execution_context() -> dict[str, object]:
    """Return stable context facts from two fresh interpreter processes."""

    direct = subprocess.run(
        [sys.executable, "execution_probe/report.py"],
        cwd=PRACTICE_DIR,
        check=False,
        capture_output=True,
        text=True,
    )
    as_module = subprocess.run(
        [sys.executable, "-m", "execution_probe.report"],
        cwd=PRACTICE_DIR,
        check=False,
        capture_output=True,
        text=True,
    )
    output = dict(
        line.split("=", maxsplit=1) for line in as_module.stdout.splitlines() if "=" in line
    )
    return {
        "direct_file_failed": direct.returncode != 0,
        "direct_file_relative_import_error": (
            "attempted relative import with no known parent package" in direct.stderr
        ),
        "module_execution_succeeded": as_module.returncode == 0,
        "module_name": output.get("module_name"),
        "package": output.get("package"),
        "spec_name": output.get("spec_name"),
        "message": output.get("message"),
    }


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_execution_context().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
