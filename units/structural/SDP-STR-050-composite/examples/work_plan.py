"""Bounded value Composite for synthetic workshop estimates; no work is executed."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Protocol, TypeAlias, final

MAX_HEIGHT = 32  # Leaf and empty group have height zero; a parent adds one edge.
MAX_OCCURRENCES = 10_000  # Includes groups, even empty groups; aliases count each time.


@dataclass(frozen=True, slots=True)
class Estimate:
    minutes: int
    tasks: int


class Estimable(Protocol):
    """Pure, repeatable effort in whole minutes and task occurrences; no external work."""

    def estimate(self) -> Estimate: ...


def describe(component: Estimable) -> str:
    result = component.estimate()
    return f"{result.minutes} min / {result.tasks} tasks"


def _validate_name(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not name.strip():
        raise ValueError("name must not be blank")


@final
@dataclass(frozen=True, slots=True)
class Task:
    name: str
    minutes: int

    def __post_init__(self) -> None:
        _validate_name(self.name)
        if type(self.minutes) is not int:  # bool is an int subtype, but not a duration here.
            raise TypeError("minutes must be a whole integer, excluding bool")
        if self.minutes < 0:
            raise ValueError("minutes must be nonnegative")

    def estimate(self) -> Estimate:
        return Estimate(self.minutes, 1)


@final
@dataclass(frozen=True, slots=True)
class Group:
    name: str
    children: tuple[Task | Group, ...] = ()
    height: int = field(init=False, repr=False, compare=False)
    occurrences: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _validate_name(self.name)
        if type(self.children) is not tuple:
            raise TypeError("children must be a tuple of completed Task or Group values")
        if len(self.children) + 1 > MAX_OCCURRENCES:
            raise ValueError("expanded occurrence limit exceeded")
        height = 0
        occurrences = 1
        for child in self.children:
            # A client capability is open; this construction boundary is deliberately closed.
            if type(child) not in (Task, Group):
                raise TypeError("only exact Task or Group values may be children")
            child_height = child.height if isinstance(child, Group) else 0
            height = max(height, 1 + child_height)
            occurrences += child.occurrences if isinstance(child, Group) else 1
            if height > MAX_HEIGHT:
                raise ValueError("height limit exceeded")
            if occurrences > MAX_OCCURRENCES:
                raise ValueError("expanded occurrence limit exceeded")
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "occurrences", occurrences)

    def estimate(self) -> Estimate:
        minutes = tasks = 0
        for child in self.children:  # Left-to-right, depth-first, once per occurrence.
            result = child.estimate()
            minutes += result.minutes
            tasks += result.tasks
        return Estimate(minutes, tasks)


Work: TypeAlias = Task | Group


@dataclass(frozen=True, slots=True)
class Occurrence:
    path: tuple[int, ...]
    task: Task


def walk_tasks(root: Work) -> Iterator[Occurrence]:
    """Yield leaves in child order with paths local to this immutable root version."""
    stack: list[tuple[tuple[int, ...], Work]] = [((), root)]
    while stack:
        path, node = stack.pop()
        if isinstance(node, Task):
            yield Occurrence(path, node)
        else:
            for index in range(len(node.children) - 1, -1, -1):
                stack.append(((*path, index), node.children[index]))
