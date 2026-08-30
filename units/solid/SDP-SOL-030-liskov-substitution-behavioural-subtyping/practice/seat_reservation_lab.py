"""Unsolved reservation lab. The partner candidate needs a behavioral review.

Baseline public contract for typed callers:
- Construction accepts distinct positive integer seat IDs, preserving order.
- reserve(count) accepts any nonnegative integer count; zero is a no-op.
- Success returns exactly count distinct available IDs, in their original order.
- A negative count raises ValueError without effects.
- An insufficient count raises NotEnoughSeats without effects.
- Successful reservations cannot return the same seat again from this pool.

This is sequential synthetic in-memory allocation, not a production booking API.
"""

from collections.abc import Sequence


class NotEnoughSeats(Exception):
    """The pool cannot fulfill this reservation in full."""


class SeatPool:
    def __init__(self, seat_ids: Sequence[int]) -> None:
        if any(seat_id <= 0 for seat_id in seat_ids):
            raise ValueError("seat IDs must be positive")
        if len(set(seat_ids)) != len(seat_ids):
            raise ValueError("seat IDs must be distinct")
        self._available = list(seat_ids)

    @property
    def available_count(self) -> int:
        return len(self._available)

    def reserve(self, count: int) -> tuple[int, ...]:
        if count < 0:
            raise ValueError("count must be nonnegative")
        if count > self.available_count:
            raise NotEnoughSeats("reservation cannot be filled")
        reserved = tuple(self._available[:count])
        del self._available[:count]
        return reserved


class PartnerSeatPool(SeatPool):
    """Candidate integration. Do not assume inheritance establishes its contract."""

    def reserve(self, count: int) -> tuple[int, ...]:
        reserved = super().reserve(min(count, self.available_count))
        if len(reserved) != count:
            raise NotEnoughSeats("partner could not fill the reservation")
        return reserved


def describe_request(pool: SeatPool, count: int) -> str:
    """Runner only: report a result and observable state for a learner prediction."""
    before = pool.available_count
    try:
        result = repr(pool.reserve(count))
    except (ValueError, NotEnoughSeats) as error:
        result = type(error).__name__
    return f"request={count}; before={before}; outcome={result}; after={pool.available_count}"


def run_demo() -> tuple[str, ...]:
    lines: list[str] = []
    for pool in (SeatPool([41, 43, 47]), PartnerSeatPool([41, 43, 47])):
        lines.append(type(pool).__name__)
        for count in (1, 3, 1):
            lines.append(describe_request(pool, count))
    return tuple(lines)


if __name__ == "__main__":
    print("\n".join(run_demo()))
