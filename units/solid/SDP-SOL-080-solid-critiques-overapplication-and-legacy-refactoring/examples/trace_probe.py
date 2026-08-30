"""Observe input reads, write attempts, saved values, and final outcome."""

import argparse
import json
from collections.abc import Callable, Iterable, Iterator
from dataclasses import asdict, dataclass
from typing import Literal

from name_export import export_eager, export_legacy, export_refactored

Exporter = Callable[[Iterable[str], Callable[[str], None]], int]
Scenario = Literal["success", "empty-name", "source-failure", "sink-before", "sink-after"]
SCENARIOS: tuple[Scenario, ...] = (
    "success",
    "empty-name",
    "source-failure",
    "sink-before",
    "sink-after",
)
IMPLEMENTATIONS: tuple[tuple[str, Exporter], ...] = (
    ("legacy", export_legacy),
    ("extracted", export_refactored),
    ("eager", export_eager),
)


@dataclass(frozen=True)
class Observation:
    result: int | None
    error: str | None
    consumed: tuple[str, ...]
    attempts: tuple[str, ...]
    saved: tuple[str, ...]
    trace: tuple[str, ...]


def observe(export: Exporter, scenario: Scenario) -> Observation:
    consumed: list[str] = []
    attempts: list[str] = []
    saved: list[str] = []
    trace: list[str] = []

    def source() -> Iterator[str]:
        values = ("Mira", "", "Asha") if scenario == "empty-name" else ("Mira", "Omar", "Asha")
        for index, value in enumerate(values):
            if scenario == "source-failure" and index == 1:
                raise RuntimeError("source unavailable")
            consumed.append(value)
            trace.append(f"read {value!r}")
            yield value

    def emit(line: str) -> None:
        attempts.append(line)
        trace.append(f"call {line!r}")
        if scenario == "sink-before" and len(attempts) == 2:
            raise OSError("writer unavailable")
        saved.append(line)
        trace.append(f"save {line!r}")
        if scenario == "sink-after" and len(attempts) == 2:
            raise OSError("acknowledgement lost")

    result: int | None = None
    error: str | None = None
    try:
        result = export(source(), emit)
    except (ValueError, RuntimeError, OSError) as failure:
        error = f"{type(failure).__name__}: {failure}"
        trace.append(error)
    else:
        trace.append(f"return {result}")
    return Observation(result, error, tuple(consumed), tuple(attempts), tuple(saved), tuple(trace))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit observations for the visual")
    args = parser.parse_args()
    observations = {
        scenario: {name: asdict(observe(export, scenario)) for name, export in IMPLEMENTATIONS}
        for scenario in SCENARIOS
    }
    if args.json:
        print(json.dumps(observations, ensure_ascii=False, indent=2))
        return
    for scenario in SCENARIOS:
        print(scenario)
        for name, export in IMPLEMENTATIONS:
            observation = observe(export, scenario)
            outcome = observation.error or f"return {observation.result}"
            print(
                f"  {name}: {outcome}; read={len(observation.consumed)}; "
                f"attempted={len(observation.attempts)}; saved={list(observation.saved)!r}"
            )


if __name__ == "__main__":
    main()
