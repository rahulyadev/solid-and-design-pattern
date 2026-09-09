"""A deliberately narrow class Singleton: one stateless identity marker per class object."""

from __future__ import annotations

from threading import RLock
from typing import ClassVar, final


@final
class ProcessMarker:
    """Cooperative API guarantee; deliberately no configuration, I/O, reset, or inheritance."""

    __slots__ = ()
    _instance: ClassVar[ProcessMarker | None] = None
    _lock: ClassVar[RLock] = RLock()

    def __new__(cls) -> ProcessMarker:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init_subclass__(cls) -> None:
        raise TypeError("ProcessMarker does not support subclasses")

    def __copy__(self) -> ProcessMarker:
        return self

    def __deepcopy__(self, memo: dict[int, object]) -> ProcessMarker:
        memo[id(self)] = self
        return self

    def __reduce__(self) -> tuple[object, tuple[()]]:
        return (process_marker, ())


def process_marker() -> ProcessMarker:
    """Top-level pickle reconstruction callable; resolves in the receiving interpreter."""
    return ProcessMarker()
