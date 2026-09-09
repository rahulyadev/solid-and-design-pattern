"""Compare reference topology, not printed memory addresses or timings."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field, replace
from enum import StrEnum


class Mode(StrEnum):
    ASSIGN = "assignment"
    SHALLOW = "shallow"
    DEEP = "deep"
    REPLACE = "replace"
    SPLIT = "split-memos"


@dataclass(eq=False)
class Node:
    label: str
    tags: list[str] = field(default_factory=list)
    edges: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Observation:
    mode: str
    root_fresh: bool
    child_shared_with_source: bool
    internal_alias_preserved: bool
    cycle_rebased: bool
    source_tags_after: tuple[str, ...]
    second_child_tags_after: tuple[str, ...]


def probe(mode: Mode) -> Observation:
    child = Node("filter", ["base"])
    source = Node("query", edges=[child, child])
    child.edges.append(source)
    if mode is Mode.ASSIGN:
        result = source
    elif mode is Mode.SHALLOW:
        result = copy.copy(source)
    elif mode is Mode.DEEP:
        result = copy.deepcopy(source)
    elif mode is Mode.REPLACE:
        result = replace(source, label="renamed")
    else:
        # Deliberate counterexample: each call starts its own memo.
        result = Node("query", edges=[copy.deepcopy(edge) for edge in source.edges])
    result.edges[0].tags.append("edit")
    return Observation(
        mode.value,
        result is not source,
        result.edges[0] is child,
        result.edges[0] is result.edges[1],
        result is not source and result.edges[0].edges[0] is result,
        tuple(child.tags),
        tuple(result.edges[1].tags),
    )


def observations() -> list[dict[str, object]]:
    return [
        {
            "mode": item.mode,
            "root_fresh": item.root_fresh,
            "child_shared_with_source": item.child_shared_with_source,
            "internal_alias_preserved": item.internal_alias_preserved,
            "cycle_rebased": item.cycle_rebased,
            "source_tags_after": list(item.source_tags_after),
            "second_child_tags_after": list(item.second_child_tags_after),
        }
        for item in (probe(mode) for mode in Mode)
    ]


if __name__ == "__main__":
    print(json.dumps(observations(), indent=2))
