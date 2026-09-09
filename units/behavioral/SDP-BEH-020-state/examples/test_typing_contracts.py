"""Positive and exact negative static clients; negative programs never execute."""

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

POSITIVE = """from state import Editing, Event, Packet, PacketState, ReleaseGate, Snapshot
state: PacketState = Editing(2)
next_state: PacketState = state.handle(Event.SEAL, 0)
def broad_gate(proposal: object) -> None:
    pass
gate: ReleaseGate = broad_gate
result: Snapshot = Packet(gate).handle(Event.ADD, 2)
class Independent:
    phase = state.phase
    pages = 2
    def handle(self, action: Event, count: int, /) -> PacketState:
        return self
independent: PacketState = Independent()
"""

NEGATIVE = """from state import Event, Packet, PacketState, Phase, ReleaseGate, Snapshot
class WrongOutput:
    phase = Phase.EDITING
    pages = 0
    def handle(self, event: Event, pages: int, /) -> str:
        return "bad"
class WrongInput:
    phase = Phase.EDITING
    pages = 0
    def handle(self, event: str, pages: int, /) -> PacketState:
        raise RuntimeError
class KeywordOnly:
    phase = Phase.EDITING
    pages = 0
    def handle(self, *, event: Event, pages: int) -> PacketState:
        raise RuntimeError
def wrong_gate(proposal: str) -> None:
    pass
def non_none(proposal: Snapshot) -> int:
    return 1
async def asynchronous(proposal: Snapshot) -> None:
    pass
a: PacketState = WrongOutput()  # E:assignment
b: PacketState = WrongInput()  # E:assignment
c: PacketState = KeywordOnly()  # E:assignment
d: ReleaseGate = wrong_gate  # E:assignment
e: ReleaseGate = non_none  # E:assignment
f: ReleaseGate = asynchronous  # E:assignment
Packet().handle("seal")  # E:arg-type
Packet().handle(Event.ADD, "2")  # E:arg-type
Packet().snapshot.pages = 9  # E:misc
wrong: str = Packet().handle(Event.CANCEL)  # E:assignment
"""


@pytest.mark.parametrize("version", ["3.11", "3.14"])
def test_static_clients(tmp_path: Path, version: str) -> None:
    expected = {
        number: line.split("# E:")[1]
        for number, line in enumerate(NEGATIVE.splitlines(), start=1)
        if "# E:" in line
    }
    assert len(expected) == 10
    env = dict(
        os.environ,
        MYPYPATH=str(Path(__file__).resolve().parent),
        MYPY_CACHE_DIR=str(tmp_path / "mypy"),
    )
    for name, source in (("positive", POSITIVE), ("negative", NEGATIVE)):
        path = tmp_path / f"{name}.py"
        path.write_text(source)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--strict",
                "--python-version",
                version,
                "--show-error-codes",
                "--no-error-summary",
                str(path),
            ],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        output = result.stdout + result.stderr
        if name == "positive":
            assert result.returncode == 0, output
        else:
            assert result.returncode == 1, output
            diagnostics = re.findall(r":(\d+): error: .*\[([\w-]+)\]", result.stdout)
            assert len(diagnostics) == len(expected), output
            assert {int(line): code for line, code in diagnostics} == expected, output
