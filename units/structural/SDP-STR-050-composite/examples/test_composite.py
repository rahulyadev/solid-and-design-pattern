from collections.abc import Iterator
from dataclasses import FrozenInstanceError, replace
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st
from occurrence_probe import Observation, expansion_limit, observations
from work_plan import (
    MAX_HEIGHT,
    MAX_OCCURRENCES,
    Estimable,
    Estimate,
    Group,
    Task,
    Work,
    describe,
    walk_tasks,
)


@pytest.mark.parametrize("minutes", [0, 1, 12, 10**30])
def test_leaf_estimate(minutes: int) -> None:
    task = Task("cut", minutes)
    assert task.estimate() == Estimate(minutes, 1)
    assert describe(task) == f"{minutes} min / 1 tasks"


def test_empty_group_is_identity_not_a_task() -> None:
    empty = Group("empty")
    assert empty.estimate() == Estimate(0, 0)
    assert empty.height == 0
    assert empty.occurrences == 1
    assert list(walk_tasks(empty)) == []


def test_nested_aggregation_and_paths() -> None:
    plan = Group("day", (Task("setup", 5), Group("kit", (Task("cut", 12), Task("tag", 3)))))
    assert plan.estimate() == Estimate(20, 3)
    assert [(o.path, o.task.name) for o in walk_tasks(plan)] == [
        ((0,), "setup"),
        ((1, 0), "cut"),
        ((1, 1), "tag"),
    ]
    assert plan.height == 2
    assert plan.occurrences == 5


def test_single_root_path() -> None:
    leaf = Task("cut", 12)
    (occurrence,) = walk_tasks(leaf)
    assert occurrence.path == ()
    assert occurrence.task is leaf


def test_same_leaf_is_counted_per_edge() -> None:
    leaf = Task("cut", 12)
    pair = Group("pair", (leaf, leaf))
    visits = tuple(walk_tasks(pair))
    assert visits[0].task is visits[1].task
    assert visits[0].path != visits[1].path
    assert pair.estimate() == Estimate(24, 2)


def test_diamond_has_occurrence_semantics() -> None:
    shared = Group("kit", (Task("cut", 12), Task("tag", 3)))
    root = Group("root", (Group("left", (shared,)), Group("right", (shared,))))
    assert root.estimate() == Estimate(30, 4)
    assert root.occurrences == 9
    assert len({id(o.task) for o in walk_tasks(root)}) == 2


def test_equal_values_are_not_unique_business_entities() -> None:
    first, second = Task("cut", 12), Task("cut", 12)
    assert first == second
    assert first is not second
    assert Group("pair", (first, second)).estimate() == Estimate(24, 2)


def test_rebuild_does_not_mutate_original_aliases() -> None:
    leaf = Task("cut", 12)
    group = Group("kit", (leaf,))
    old = Group("old", (group, group))
    changed = replace(group, children=(replace(leaf, minutes=8),))
    new = replace(old, children=(changed, group))
    assert old.estimate() == Estimate(24, 2)
    assert new.estimate() == Estimate(20, 2)
    assert new.children[1] is group
    assert old.children == (group, group)


def test_repeated_queries_and_interleaved_traversals_are_independent() -> None:
    root = Group("root", (Task("a", 1), Task("b", 2)))
    first, second = walk_tasks(root), walk_tasks(root)
    assert next(first).task.name == "a"
    assert [o.task.name for o in second] == ["a", "b"]
    assert [o.task.name for o in first] == ["b"]
    assert root.estimate() == root.estimate() == Estimate(3, 2)


@pytest.mark.parametrize("name", ["", " ", "\t\n"])
def test_blank_names_rejected(name: str) -> None:
    with pytest.raises(ValueError, match="blank"):
        Task(name, 1)
    with pytest.raises(ValueError, match="blank"):
        Group(name)


@pytest.mark.parametrize("name", [None, 9])
def test_non_string_names_rejected(name: object) -> None:
    with pytest.raises(TypeError, match="string"):
        Task(cast(str, name), 1)
    with pytest.raises(TypeError, match="string"):
        Group(cast(str, name))


@pytest.mark.parametrize("minutes", [True, False, 1.0, "12", None])
def test_non_integer_minutes_rejected(minutes: object) -> None:
    with pytest.raises(TypeError, match="whole integer"):
        Task("cut", cast(int, minutes))


@pytest.mark.parametrize("minutes", [-1, -100])
def test_negative_minutes_rejected(minutes: int) -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        Task("cut", minutes)


@pytest.mark.parametrize("children", [[], [Task("cut", 12)], {Task("cut", 12)}, None])
def test_non_tuple_children_rejected(children: object) -> None:
    with pytest.raises(TypeError, match="tuple"):
        Group("kit", cast(tuple[Work, ...], children))


def test_generator_rejected_without_consuming_it() -> None:
    calls: list[str] = []

    def source() -> Iterator[Task]:
        calls.append("consumed")
        yield Task("cut", 1)

    with pytest.raises(TypeError, match="tuple"):
        Group("kit", cast(tuple[Work, ...], source()))
    assert calls == []


class ExternalEstimate:
    def estimate(self) -> Estimate:
        return Estimate(7, 1)


def test_open_client_and_closed_structure() -> None:
    external: Estimable = ExternalEstimate()
    assert describe(external) == "7 min / 1 tasks"
    with pytest.raises(TypeError, match="exact Task or Group"):
        Group("kit", (cast(Work, external),))


@pytest.mark.parametrize("child", [1, "cut", (), None])
def test_invalid_children_rejected(child: object) -> None:
    with pytest.raises(TypeError, match="exact Task or Group"):
        Group("kit", (cast(Work, child),))


def test_runtime_subclass_cannot_enter_structure() -> None:
    # @final is static. Deliberately bypass it to verify the runtime admission policy.
    derived = type("DerivedTask", (Task,), {})
    with pytest.raises(TypeError, match="exact Task or Group"):
        Group("kit", (derived("cut", 12),))


@pytest.mark.parametrize("field,value", [("name", "changed"), ("minutes", 8)])
def test_task_is_frozen(field: str, value: object) -> None:
    task = Task("cut", 12)
    with pytest.raises(FrozenInstanceError):
        setattr(task, field, value)


def test_group_cannot_be_rewired_to_itself() -> None:
    group = Group("kit")
    with pytest.raises(FrozenInstanceError):
        setattr(group, "children", (group,))  # noqa: B010 -- deliberate runtime freeze check
    assert group.children == ()


def test_exact_height_boundary() -> None:
    node: Work = Task("cut", 1)
    for level in range(1, MAX_HEIGHT + 1):
        node = Group(f"level {level}", (node,))
    assert isinstance(node, Group)
    assert node.height == MAX_HEIGHT
    assert node.estimate() == Estimate(1, 1)
    assert len(next(walk_tasks(node)).path) == MAX_HEIGHT
    with pytest.raises(ValueError, match="height"):
        Group("too deep", (node,))


def test_exact_occurrence_boundary() -> None:
    leaf = Task("cut", 1)
    root = Group("wide", (leaf,) * (MAX_OCCURRENCES - 1))
    assert root.occurrences == MAX_OCCURRENCES
    assert root.estimate() == Estimate(MAX_OCCURRENCES - 1, MAX_OCCURRENCES - 1)
    with pytest.raises(ValueError, match="occurrence"):
        Group("too wide", (leaf,) * MAX_OCCURRENCES)
    with pytest.raises(ValueError, match="occurrence"):
        Group("one more parent", (root,))


def test_empty_groups_also_consume_the_bound() -> None:
    empty = Group("empty")
    root = Group("wide", (empty,) * (MAX_OCCURRENCES - 1))
    assert root.estimate() == Estimate(0, 0)
    with pytest.raises(ValueError, match="occurrence"):
        Group("one more parent", (root,))


def test_failed_rebuild_leaves_existing_value_usable() -> None:
    root = Group("kit", (Task("cut", 12),))
    with pytest.raises(TypeError):
        replace(root, children=cast(tuple[Work, ...], []))
    assert root.estimate() == Estimate(12, 1)


def test_probe_rows_and_expansion_limit() -> None:
    assert observations() == (
        Observation("leaf", 1, 1, 12, ((),)),
        Observation("empty", 0, 0, 0, ()),
        Observation("distinct equal", 2, 2, 24, ((0,), (1,))),
        Observation("same leaf twice", 1, 2, 24, ((0,), (1,))),
        Observation("same group twice", 2, 4, 30, ((0, 0), (0, 1), (1, 0), (1, 1))),
    )
    assert expansion_limit() == (13, 8191)


@given(st.lists(st.integers(min_value=0, max_value=1000), max_size=30))
def test_aggregation_agrees_with_independent_flat_values(minutes: list[int]) -> None:
    leaves = tuple(Task(f"task {i}", value) for i, value in enumerate(minutes))
    midpoint = len(leaves) // 2
    root = Group("root", (Group("left", leaves[:midpoint]), Group("right", leaves[midpoint:])))
    assert root.estimate() == Estimate(sum(minutes), len(minutes))
    assert [o.task.minutes for o in walk_tasks(root)] == minutes


def test_actual_delegation_order_counts_alias_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    original = Task.estimate

    def traced(task: Task) -> Estimate:
        calls.append(task.name)
        return original(task)

    kit = Group("kit", (Task("cut", 12), Task("tag", 3)))
    root = Group("root", (Task("setup", 5), kit, kit))
    # Instrumentation exposes actual delegation; it is not a supported plugin/mutation API.
    monkeypatch.setattr(Task, "estimate", traced)
    assert root.estimate() == Estimate(35, 5)
    assert calls == ["setup", "cut", "tag", "cut", "tag"]


def test_query_failure_propagates_without_later_visits(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    failure = RuntimeError("synthetic query failure")
    original = Task.estimate

    def failing(task: Task) -> Estimate:
        calls.append(task.name)
        if task.name == "broken":
            raise failure
        return original(task)

    root = Group("root", (Task("first", 1), Group("inner", (Task("broken", 2),)), Task("last", 3)))
    with monkeypatch.context() as patch:
        patch.setattr(Task, "estimate", failing)
        with pytest.raises(RuntimeError) as caught:
            root.estimate()
        assert caught.value is failure
    assert calls == ["first", "broken"]
    assert root.estimate() == Estimate(6, 3)


@pytest.mark.parametrize("field", ["height", "occurrences"])
def test_derived_bounds_cannot_be_rebound_normally(field: str) -> None:
    root = Group("root", (Task("cut", 1),))
    with pytest.raises(FrozenInstanceError):
        setattr(root, field, 0)
    assert root.height == 1
    assert root.occurrences == 2


def test_converted_input_list_is_not_a_live_child_collection() -> None:
    source: list[Work] = [Task("cut", 12)]
    root = Group("root", tuple(source))
    source.append(Task("tag", 3))
    assert root.estimate() == Estimate(12, 1)
    assert len(root.children) == 1


def test_reorder_changes_paths_without_changing_sum_or_previous_root() -> None:
    first, second = Task("a", 1), Task("b", 2)
    old = Group("root", (first, second))
    new = replace(old, children=(second, first))
    assert new.estimate() == old.estimate() == Estimate(3, 2)
    assert next(walk_tasks(old)).task is first
    assert next(walk_tasks(new)).task is second
    assert next(walk_tasks(old)).path == next(walk_tasks(new)).path == (0,)


def test_static_capability_does_not_enforce_business_meaning() -> None:
    class DishonestEstimator:
        def estimate(self) -> Estimate:
            return Estimate(-5, -1)

    component: Estimable = DishonestEstimator()
    # A client trusts its semantic contract; accepting this shape cannot prove that contract.
    assert describe(component) == "-5 min / -1 tasks"
