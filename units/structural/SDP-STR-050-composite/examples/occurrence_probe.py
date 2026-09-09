"""Controlled counts, not a timing or memory benchmark."""

from dataclasses import dataclass

from work_plan import MAX_OCCURRENCES, Group, Task, Work, walk_tasks


@dataclass(frozen=True)
class Observation:
    case: str
    unique_tasks: int
    visits: int
    minutes: int
    paths: tuple[tuple[int, ...], ...]


def observe(case: str, root: Work) -> Observation:
    leaves = tuple(walk_tasks(root))  # Keeps references alive during identity counting.
    return Observation(
        case,
        len({id(item.task) for item in leaves}),
        len(leaves),
        root.estimate().minutes,
        tuple(item.path for item in leaves),
    )


def observations() -> tuple[Observation, ...]:
    leaf = Task("cut", 12)
    kit = Group("kit", (leaf, Task("label", 3)))
    return (
        observe("leaf", leaf),
        observe("empty", Group("empty")),
        observe("distinct equal", Group("pair", (Task("cut", 12), Task("cut", 12)))),
        observe("same leaf twice", Group("pair", (leaf, leaf))),
        observe("same group twice", Group("pair", (kit, kit))),
    )


def expansion_limit() -> tuple[int, int]:
    node: Work = Task("one", 1)
    for level in range(1, MAX_OCCURRENCES):
        try:
            node = Group(f"level {level}", (node, node))
        except ValueError:
            return level, node.occurrences if isinstance(node, Group) else 1
    raise AssertionError("expected the occurrence bound to reject repeated doubling")


def main() -> None:
    for row in observations():
        print(
            f"{row.case}: unique={row.unique_tasks}, visits={row.visits}, "
            f"minutes={row.minutes}, paths={row.paths}"
        )
    rejected_level, last_occurrences = expansion_limit()
    print(f"doubling: rejected_level={rejected_level}, last_occurrences={last_occurrences}")


if __name__ == "__main__":
    main()
