"""Original teaching implementations; the eager variant is deliberately incompatible."""

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable


def export_legacy(names: Iterable[str], emit: Callable[[str], None]) -> int:
    """Preserved baseline: validate, format, and emit one name at a time."""
    count = 0
    for name in names:
        if name == "":
            raise ValueError("empty name")
        emit(f"[{name.upper()}]")
        count += 1
    return count


def format_name(name: str) -> str:
    """The existing representation rule, including its whitespace behaviour."""
    if name == "":
        raise ValueError("empty name")
    return f"[{name.upper()}]"


def export_refactored(names: Iterable[str], emit: Callable[[str], None]) -> int:
    """Extract the representation rule without moving its execution in time."""
    count = 0
    for name in names:
        emit(format_name(name))
        count += 1
    return count


def preview_names(names: Iterable[str]) -> tuple[str, ...]:
    """A separate new feature: materialize a finite preview without emitting."""
    return tuple(format_name(name) for name in names)


def export_eager(names: Iterable[str], emit: Callable[[str], None]) -> int:
    """Counterexample: buffering changes input consumption and failure effects."""
    lines = tuple(format_name(name) for name in names)
    for line in lines:
        emit(line)
    return len(lines)


class NameRule(ABC):
    """Speculative hierarchy: no caller currently needs another rule."""

    @abstractmethod
    def render(self, name: str) -> str:
        raise NotImplementedError


class UpperNameRule(NameRule):
    def render(self, name: str) -> str:
        return format_name(name)


class RuleFactory:
    def create(self) -> NameRule:
        return UpperNameRule()


class ExportService:
    def __init__(self, rule: NameRule, emit: Callable[[str], None]) -> None:
        self.rule = rule
        self.emit = emit

    def publish(self, names: Iterable[str]) -> int:
        count = 0
        for name in names:
            self.emit(self.rule.render(name))
            count += 1
        return count


def export_overbuilt(names: Iterable[str], emit: Callable[[str], None]) -> int:
    """Correct output alone does not justify these extra construction decisions."""
    return ExportService(RuleFactory().create(), emit).publish(names)
