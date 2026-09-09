"""Unsolved starter: only consecutive packing exists. Keep the original attempt."""


def pack(sizes: tuple[int, ...], capacity: int) -> tuple[tuple[int, ...], ...]:
    """Keep arrival order; close a group when the next item would overflow it."""
    if type(capacity) is not int or not 1 <= capacity <= 20:
        raise ValueError("capacity must be an integer in 1..20")
    if len(sizes) > 40 or any(type(size) is not int or not 1 <= size <= capacity for size in sizes):
        raise ValueError("at most 40 integer items, each in 1..capacity")
    groups: list[tuple[int, ...]] = []
    current: list[int] = []
    for size in sizes:
        if sum(current) + size > capacity:
            groups.append(tuple(current))
            current = []
        current.append(size)
    if current:
        groups.append(tuple(current))
    return tuple(groups)


def target_complete() -> bool:
    return False


if __name__ == "__main__":
    print(pack((6, 6, 4, 4), 10))
    print(f"target_complete={target_complete()}")
