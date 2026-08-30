"""Synthetic vendor API for the unsolved lab; no network or private data."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass


class PlannerOffline(RuntimeError):
    """This vendor could not answer the request."""


@dataclass(frozen=True)
class VendorOpening:
    code: str
    free_seats_text: str


class PlanningClient:
    def __init__(
        self, days: Mapping[str, Sequence[tuple[str, int]]], *, offline: bool = False
    ) -> None:
        if any(seats < 0 for openings in days.values() for _, seats in openings):
            raise ValueError("seats must be nonnegative")
        self._days = {
            day: tuple(VendorOpening(code, str(seats)) for code, seats in openings)
            for day, openings in days.items()
        }
        self._offline = offline

    def list_openings(self, day: str) -> tuple[VendorOpening, ...]:
        if self._offline:
            raise PlannerOffline("vendor planner offline")
        return self._days.get(day, ())
