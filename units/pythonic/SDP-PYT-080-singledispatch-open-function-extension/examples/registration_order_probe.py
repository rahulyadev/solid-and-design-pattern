"""Show that importing registration modules configures one generic function."""

from __future__ import annotations

import importlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import registration_target


@dataclass(frozen=True, slots=True)
class RegistrationOutcome:
    order: tuple[str, str]
    result: str
    handler: str


def _run_child(order: tuple[str, str]) -> RegistrationOutcome:
    completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--child", *order],
        check=True,
        capture_output=True,
        text=True,
    )
    order_text, result, handler = completed.stdout.strip().split("|", maxsplit=2)
    observed_order = tuple(order_text.split(","))
    if len(observed_order) != 2:
        raise RuntimeError("child returned an invalid order")
    return RegistrationOutcome((observed_order[0], observed_order[1]), result, handler)


def observe_import_orders() -> tuple[RegistrationOutcome, RegistrationOutcome]:
    return _run_child(("alpha", "beta")), _run_child(("beta", "alpha"))


def _child(order: tuple[str, str]) -> None:
    for extension_name in order:
        importlib.import_module(f"extension_{extension_name}")

    value = registration_target.ExternalPayload("ext-9")
    handler = registration_target.summarize_external.dispatch(type(value))
    print(
        f"{','.join(order)}|{registration_target.summarize_external(value)}|"
        f"{handler.__module__}.{handler.__name__}"
    )


def main(arguments: list[str]) -> None:
    if arguments[:1] == ["--child"]:
        child_order = tuple(arguments[1:])
        if len(child_order) != 2 or set(child_order) != {"alpha", "beta"}:
            raise SystemExit("child order must contain alpha and beta exactly once")
        _child((child_order[0], child_order[1]))
        return

    for outcome in observe_import_orders():
        print(f"order={','.join(outcome.order)} result={outcome.result} handler={outcome.handler}")


if __name__ == "__main__":
    main(sys.argv[1:])
