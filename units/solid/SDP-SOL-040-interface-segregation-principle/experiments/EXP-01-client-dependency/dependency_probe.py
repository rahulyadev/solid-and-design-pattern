"""Observe contract growth with one unchanged reader and one unchanged call body."""

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

SOURCE = """from typing import Protocol

class ArchiveReader(Protocol):
    def read(self, key: str, /) -> bytes: ...

class SharedArchive(ArchiveReader, Protocol):
ADMIN_OPERATIONS

class Bundle:
    def read(self, key: str, /) -> bytes:
        return b"hello"

def preview(archive: BOUNDARY) -> str:
    return archive.read("welcome").decode("utf-8")

result = preview(Bundle())
"""

ADMIN_OPERATIONS = """    def write(self, key: str, payload: bytes, /) -> None: ...
    def remove(self, key: str, /) -> bool: ..."""


@dataclass(frozen=True)
class Scenario:
    name: str
    admin_added: bool
    boundary: str


SCENARIOS = (
    Scenario("shared contract before growth", False, "SharedArchive"),
    Scenario("shared contract after growth", True, "SharedArchive"),
    Scenario("client contract after growth", True, "ArchiveReader"),
)


@dataclass(frozen=True)
class Observation:
    name: str
    static_accepted: bool
    error_codes: tuple[str, ...]
    runtime_result: str
    diagnostics: str


def observe(scenario: Scenario) -> Observation:
    source = SOURCE.replace(
        "ADMIN_OPERATIONS", ADMIN_OPERATIONS if scenario.admin_added else "    pass"
    ).replace("BOUNDARY", scenario.boundary)
    with TemporaryDirectory(prefix="sdp-sol-040-probe-") as temporary:
        directory = Path(temporary)
        candidate = directory / "candidate.py"
        candidate.write_text(source, encoding="utf-8")
        configuration = directory / "mypy.ini"
        configuration.write_text("[mypy]\nstrict = True\n", encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--config-file",
                str(configuration),
                "--cache-dir",
                str(directory / "cache"),
                "--no-incremental",
                "--show-error-codes",
                "--no-error-summary",
                "--python-version",
                f"{sys.version_info.major}.{sys.version_info.minor}",
                str(candidate),
            ],
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
            timeout=45,
        )
        if completed.returncode not in (0, 1) or completed.stderr:
            raise RuntimeError(f"mypy did not complete normally: {completed.stderr}")
        namespace: dict[str, object] = {}
        # This is a fixed, local teaching probe, never untrusted/user-supplied code.
        exec(compile(source, str(candidate), "exec"), namespace)
        runtime_result = namespace["result"]
        if not isinstance(runtime_result, str):
            raise TypeError("probe returned a non-string result")
        return Observation(
            scenario.name,
            completed.returncode == 0,
            tuple(re.findall(r"error:.*\[([a-z-]+)\]", completed.stdout)),
            runtime_result,
            completed.stdout,
        )


def run_probes() -> tuple[Observation, ...]:
    return tuple(observe(scenario) for scenario in SCENARIOS)


def main() -> None:
    for result in run_probes():
        verdict = "accepted" if result.static_accepted else "rejected"
        codes = ",".join(result.error_codes) or "none"
        print(f"{result.name}: static={verdict}; errors={codes}; runtime={result.runtime_result!r}")


if __name__ == "__main__":
    main()
