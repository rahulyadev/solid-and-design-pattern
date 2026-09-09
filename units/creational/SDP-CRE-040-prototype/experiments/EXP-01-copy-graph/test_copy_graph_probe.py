"""Controlled semantic checks, including version and reconstruction boundaries."""

import copy
import sys
from dataclasses import InitVar, dataclass, field, replace
from typing import ClassVar

import pytest
from copy_graph_probe import Mode, probe


@pytest.mark.parametrize(
    "mode,fresh,shared,alias,cycle,source,second",
    [
        (Mode.ASSIGN, False, True, True, False, ("base", "edit"), ("base", "edit")),
        (Mode.SHALLOW, True, True, True, False, ("base", "edit"), ("base", "edit")),
        (Mode.DEEP, True, False, True, True, ("base",), ("base", "edit")),
        (Mode.REPLACE, True, True, True, False, ("base", "edit"), ("base", "edit")),
        (Mode.SPLIT, True, False, False, False, ("base",), ("base",)),
    ],
)
def test_topology(mode, fresh, shared, alias, cycle, source, second) -> None:
    result = probe(mode)
    assert (result.root_fresh, result.child_shared_with_source) == (fresh, shared)
    assert (result.internal_alias_preserved, result.cycle_rebased) == (alias, cycle)
    assert (result.source_tags_after, result.second_child_tags_after) == (source, second)


@dataclass
class Checked:
    value: int
    tags: list[str] = field(default_factory=list)
    doubled: int = field(init=False)
    calls: ClassVar[int] = 0

    def __post_init__(self) -> None:
        type(self).calls += 1
        if self.value < 0:
            raise ValueError("negative")
        self.doubled = self.value * 2


def test_replace_revalidates_and_recomputes_but_shares_unchanged_fields() -> None:
    source = Checked(2)
    source.doubled = 99
    before = Checked.calls
    changed = replace(source, value=3)
    assert Checked.calls == before + 1
    assert changed.doubled == 6 and changed.tags is source.tags
    assert source.doubled == 99
    with pytest.raises(ValueError, match="negative"):
        replace(source, value=-1)
    expected_error = {(3, 11): ValueError, (3, 14): TypeError}.get(
        sys.version_info[:2], (TypeError, ValueError)
    )
    with pytest.raises(expected_error):
        replace(source, doubled=100)
    with pytest.raises(TypeError):
        replace(source, unknown=1)


@pytest.mark.parametrize("operation", [copy.copy, copy.deepcopy])
def test_default_copy_does_not_rerun_post_init(operation) -> None:
    source = Checked(2)
    source.doubled = 99
    before = Checked.calls
    result = operation(source)
    assert Checked.calls == before and result.doubled == 99


def test_required_initvar_must_be_supplied_to_replace() -> None:
    @dataclass
    class Restricted:
        value: int
        approved: InitVar[bool]

        def __post_init__(self, approved: bool) -> None:
            if not approved:
                raise ValueError("approval_required")

    source = Restricted(2, True)
    expected_error = {(3, 11): ValueError, (3, 14): TypeError}.get(
        sys.version_info[:2], (TypeError, ValueError)
    )
    with pytest.raises(expected_error):
        replace(source, value=3)
    assert replace(source, value=3, approved=True).value == 3


def test_copy_replace_version_boundary() -> None:
    available = getattr(copy, "replace", None)
    assert (available is not None) == (sys.version_info >= (3, 13))
    if available is not None:
        source = Checked(2)
        result = available(source, value=4)
        assert result.doubled == 8 and result.tags is source.tags


def test_functions_are_shared_and_open_file_is_rejected(tmp_path) -> None:
    def constant() -> int:
        return 1

    assert copy.copy(constant) is constant and copy.deepcopy(constant) is constant
    with (tmp_path / "synthetic.txt").open("w") as handle:
        for operation in (copy.copy, copy.deepcopy):
            with pytest.raises(TypeError):
                operation(handle)


def test_copy_hook_can_share_even_under_deepcopy() -> None:
    class Shared:
        def __deepcopy__(self, memo):
            return self

    source = Shared()
    assert copy.deepcopy(source) is source


def test_list_subclass_container_copy_differs_from_generic_copy() -> None:
    class Labels(list):
        pass

    source = Labels(["x"])
    assert type(source.copy()) is list
    assert type(copy.copy(source)) is Labels
