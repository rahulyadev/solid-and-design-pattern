"""One operation can be supplied by a function, closure, or callable instance."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass


def plain_name(name: str) -> str:
    return name


def make_prefix(prefix: str) -> Callable[[str], str]:
    def render(name: str) -> str:
        return f"{prefix}{name}"

    return render


@dataclass(frozen=True)
class NamePrefix:
    prefix: str

    def __call__(self, name: str) -> str:
        return f"{self.prefix}{name}"


def render_names(names: Iterable[str], render: Callable[[str], str]) -> tuple[str, ...]:
    """Preserve encounter order and duplicates; propagate a renderer failure."""
    return tuple(render(name) for name in names)
