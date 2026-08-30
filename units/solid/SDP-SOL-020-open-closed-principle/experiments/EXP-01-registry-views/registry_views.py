"""Observe live mapping views, copied bindings, and shared callable state."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType


def plain(value: int) -> str:
    return f"plain:{value}"


def loud(value: int) -> str:
    return f"LOUD:{value}"


def binding_observations() -> tuple[str, ...]:
    source: dict[str, Callable[[int], str]] = {"display": plain}
    live: Mapping[str, Callable[[int], str]] = MappingProxyType(source)
    snapshot: Mapping[str, Callable[[int], str]] = MappingProxyType(dict(source))
    before = f"before: live={live['display'](7)}; snapshot={snapshot['display'](7)}"
    source["display"] = loud
    source["extra"] = plain
    return (
        before,
        f"after replacement: live={live['display'](7)}; snapshot={snapshot['display'](7)}",
        f"names: live={tuple(live)}; snapshot={tuple(snapshot)}",
    )


@dataclass
class PrefixRenderer:
    prefix: str

    def __call__(self, value: int) -> str:
        return f"{self.prefix}:{value}"


def state_observations() -> tuple[str, str]:
    renderer = PrefixRenderer("first")
    source = {"display": renderer}
    snapshot = MappingProxyType(dict(source))
    before = f"callable state before: {snapshot['display'](7)}"
    renderer.prefix = "second"
    after = f"callable state after: {snapshot['display'](7)}"
    return before, after


def main() -> None:
    for line in (*binding_observations(), *state_observations()):
        print(line)


if __name__ == "__main__":
    main()
