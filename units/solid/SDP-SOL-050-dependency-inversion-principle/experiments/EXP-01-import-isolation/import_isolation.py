"""Run each policy import in a fresh process with sqlite3 deliberately unavailable."""

import subprocess
import sys
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"
PROBE = """
import sys

sys.path.insert(0, sys.argv[1])
sys.modules["sqlite3"] = None
if sys.argv[2] == "concrete":
    try:
        import coupled_replenishment
    except ModuleNotFoundError as error:
        if error.name != "sqlite3":
            raise
        print("concrete: import blocked (sqlite3)")
    else:
        raise AssertionError("the concrete dependency was expected to reach sqlite3")
else:
    from replenishment_policy import replenishment_plan

    class OfflineStock:
        def units_available(self, sku: str, /) -> int:
            print(f"runtime: policy -> fake.units_available({sku})")
            return 3

    print("inverted:", replenishment_plan({"BOLT": 8}, OfflineStock()))
    assert sys.modules["sqlite3"] is None
"""


def run_probe() -> tuple[str, str]:
    observations: list[str] = []
    for mode in ("concrete", "inverted"):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", PROBE, str(EXAMPLES), mode],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        observations.append(result.stdout.strip())
    return observations[0], observations[1]


def main() -> None:
    for observation in run_probe():
        print(observation)


if __name__ == "__main__":
    main()
