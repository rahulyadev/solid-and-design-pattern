"""Positive and exact negative static clients; negative programs never execute."""

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

POSITIVE = """from strategy import Job, Jobs, Order, OrderPolicy, Plan, SmallJobsFirst, plan
from strategy import small_jobs_first
from object_strategy import ObjectPlanner, Ordering, SmallFirstOrdering
jobs = (Job(1, 2),)
configured: OrderPolicy = SmallJobsFirst(5)
closure: OrderPolicy = small_jobs_first(5)
result: Plan = plan(jobs, configured)
method: Ordering = SmallFirstOrdering(SmallJobsFirst(5))
object_result: Plan = ObjectPlanner(method).plan(jobs)
class Renamed:
    def order(self, batch: Jobs, /) -> Order:
        return tuple(j.job_id for j in batch)
renamed: Ordering = Renamed()
def broad_input(value: object) -> Order:
    return ()
broad: OrderPolicy = broad_input
"""

NEGATIVE = """from strategy import Job, Jobs, Order, OrderPolicy, SmallJobsFirst, plan
from object_strategy import ObjectPlanner, Ordering
def wrong_input(jobs: tuple[str, ...]) -> Order:
    return ()
def wrong_output(jobs: Jobs) -> list[int]:
    return []
def keyword_only(*, jobs: Jobs) -> Order:
    return ()
def extra_argument(jobs: Jobs, required: int) -> Order:
    return ()
async def asynchronous(jobs: Jobs) -> Order:
    return ()
a: OrderPolicy = wrong_input  # E:assignment
b: OrderPolicy = wrong_output  # E:assignment
c: OrderPolicy = keyword_only  # E:assignment
d: OrderPolicy = extra_argument  # E:assignment
e: OrderPolicy = asynchronous  # E:assignment
plan([Job(1, 2)], SmallJobsFirst(5))  # E:arg-type
ObjectPlanner(SmallJobsFirst(5))  # E:arg-type
class WrongMethod:
    def order(self, jobs: Jobs) -> str:
        return "wrong"
method: Ordering = WrongMethod()  # E:assignment
SmallJobsFirst(5).cutoff = 10  # E:misc
wrong: str = plan((), SmallJobsFirst(5))  # E:assignment
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
