"""Instantiation, virtual membership, and business correctness are separate."""

from abc import ABC, abstractmethod
from collections.abc import Callable


class BufferBase(ABC):
    def __init__(self) -> None:
        self.records: list[bytes] = []

    @abstractmethod
    def append(self, payload: bytes) -> None:
        """Store exactly one payload in records, preserving its value."""
        raise NotImplementedError

    def count(self) -> int:
        return len(self.records)


class MissingBuffer(BufferBase):
    pass


class DroppingBuffer(BufferBase):
    def append(self, payload: bytes) -> None:
        pass


class MemoryBuffer(BufferBase):
    def append(self, payload: bytes) -> None:
        self.records.append(payload)


def creation_outcome(factory: Callable[[], object]) -> str:
    try:
        factory()
    except TypeError:
        return "blocked by TypeError"
    return "created"


def virtual_observation() -> tuple[bool, bool, bool]:
    class Unrelated:
        pass

    BufferBase.register(Unrelated)
    candidate = Unrelated()
    return (
        isinstance(candidate, BufferBase),
        hasattr(candidate, "append"),
        hasattr(candidate, "count"),
    )


def main() -> None:
    print("incomplete nominal subclass:", creation_outcome(MissingBuffer))
    member, has_append, has_count = virtual_observation()
    print(
        f"virtual subclass: membership={member}; append={has_append}; inherited count={has_count}"
    )
    implementations: tuple[BufferBase, ...] = (DroppingBuffer(), MemoryBuffer())
    for buffer in implementations:
        buffer.append(b"sample")
        print(f"{type(buffer).__name__}: stored={buffer.count()}")


if __name__ == "__main__":
    main()
