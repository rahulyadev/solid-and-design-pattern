"""Characterize only the starter. Passing does not solve the new requirements."""

import pytest
from packing_lab import pack, target_complete


@pytest.mark.parametrize(
    ("sizes", "capacity", "expected"),
    [
        ((), 10, ()),
        ((6, 6, 4, 4), 10, ((6,), (6, 4), (4,))),
        ((10, 10), 10, ((10,), (10,))),
        ((1, 2, 3), 6, ((1, 2, 3),)),
        ((1,) * 40, 20, ((1,) * 20, (1,) * 20)),
    ],
)
def test_starter(
    sizes: tuple[int, ...], capacity: int, expected: tuple[tuple[int, ...], ...]
) -> None:
    assert pack(sizes, capacity) == expected


@pytest.mark.parametrize(
    ("sizes", "capacity"),
    [((), 0), ((), 21), ((0,), 10), ((11,), 10), ((True,), 10), ((1,) * 41, 20)],
)
def test_invalid_input(sizes: tuple[int, ...], capacity: int) -> None:
    with pytest.raises(ValueError):
        pack(sizes, capacity)


def test_exercise_is_unsolved() -> None:
    assert target_complete() is False
