"""Deferral and state ownership do not supply transaction or replay semantics."""

import json
from collections.abc import Callable

from callable_tools import make_write_action, run_actions


def make_counter() -> Callable[[], int]:
    count = 0

    def next_count() -> int:
        nonlocal count
        count += 1
        return count

    return next_count


def observe_effects() -> dict[str, object]:
    first = make_counter()
    alias = first
    second = make_counter()
    counts = [first(), alias(), second(), first()]
    records: list[str] = []
    failure = OSError("synthetic writer failed after recording")

    def sink(payload: bytes, /, *, channel: str) -> None:
        message = payload.decode("ascii")
        records.append(f"{channel}:{message}")
        if payload == b"stop":
            raise failure

    first_action = make_write_action(b"ready", sink, channel="events")
    failed_action = make_write_action(b"stop", sink, channel="events")
    never_run = make_write_action(b"later", sink, channel="events")
    before = records.copy()
    same_error = False
    try:
        run_actions((first_action, failed_action, never_run))
    except OSError as error:
        same_error = error is failure
    after_failure = records.copy()
    first_action()
    return {
        "counter_calls_first_alias_second_first": counts,
        "before_execution": before,
        "after_failure": after_failure,
        "same_exception": same_error,
        "after_replay": records.copy(),
    }


if __name__ == "__main__":
    print(json.dumps(observe_effects(), indent=2))
