"""Check the experiment's workload contracts without asserting platform byte totals."""

import pytest
from memory_probe import Mode, build


@pytest.mark.parametrize("mode", ["fresh", "explicit", "pooled"])
@pytest.mark.parametrize("distinct", [1, 5, 12])
def test_workload_equivalence_and_object_count(mode: Mode, distinct: int) -> None:
    rows, owner = build(mode, 12, distinct)
    reference, _ = build("fresh", 12, distinct)
    assert rows == reference
    assert [row.tile.pixels for row in rows] == [row.tile.pixels for row in reference]
    assert [r.sample(1, 2) for r in rows] == [r.sample(1, 2) for r in reference]
    assert len({id(row.tile) for row in rows}) == (12 if mode == "fresh" else distinct)
    if owner is not None:
        owner.clear()
    assert rows == reference


@pytest.mark.parametrize("n,distinct", [(0, 0), (2, 3), (65537, 1)])
def test_invalid_probe_dimensions(n: int, distinct: int) -> None:
    with pytest.raises(ValueError):
        build("fresh", n, distinct)
