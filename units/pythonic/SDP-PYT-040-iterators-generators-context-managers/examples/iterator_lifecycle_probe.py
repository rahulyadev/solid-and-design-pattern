"""Deterministic iterable, iterator, and generator observations for SDP-PYT-040."""

from __future__ import annotations

import json
from typing import Any

from streaming_reports import parse_alerts


def iterator_observations() -> dict[str, Any]:
    """Return observations without relying on implementation-specific repr output."""

    trace: list[str] = []
    lines = [
        "a-1|2|queued",
        "a-2|5|worker unavailable",
    ]
    pipeline = parse_alerts(lines, trace=trace.append)

    before_first_next = tuple(trace)
    first = next(pipeline)
    after_first_next = tuple(trace)
    remaining_ids = tuple(alert.alert_id for alert in pipeline)
    after_exhaustion = tuple(trace)

    try:
        next(pipeline)
    except StopIteration:
        exhausted_again = "StopIteration"
    else:  # pragma: no cover - an iterator that resumes would violate the contract
        exhausted_again = "unexpected value"

    reusable = (10, 20)
    reusable_first = iter(reusable)
    reusable_second = iter(reusable)

    return {
        "before_first_next": before_first_next,
        "first_id": first.alert_id,
        "after_first_next": after_first_next,
        "remaining_ids": remaining_ids,
        "after_exhaustion": after_exhaustion,
        "generator_iter_is_self": iter(pipeline) is pipeline,
        "second_pass": tuple(pipeline),
        "next_after_exhaustion": exhausted_again,
        "container_iterators_are_distinct": reusable_first is not reusable_second,
        "container_passes": (tuple(reusable_first), tuple(reusable_second)),
    }


def main() -> None:
    print(json.dumps(iterator_observations(), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
