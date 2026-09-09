"""A typed function decorator and an executable three-phase ordering probe."""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def traced(events: list[str], name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """This teaching tracer assumes list.append succeeds; it is not Observed."""
    events.append(f"evaluate:{name}")

    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        events.append(f"apply:{name}")

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            events.append(f"enter:{name}")
            try:
                return function(*args, **kwargs)
            finally:
                events.append(f"exit:{name}")

        return wrapper

    return decorate


def order_probe() -> tuple[str, ...]:
    events: list[str] = []

    @traced(events, "outer")
    @traced(events, "inner")
    def text() -> str:
        events.append("body")
        return "ready"

    assert text() == "ready"
    return tuple(events)


if __name__ == "__main__":
    print(",".join(order_probe()))
