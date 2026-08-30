"""Runtime presence checks and static signatures leave a semantic gap."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ByteCounter(Protocol):
    """Return the length of text.encode('utf-8') for encodable strings."""

    def count(self, text: str) -> int: ...


class UTF8Counter:
    def count(self, text: str) -> int:
        return len(text.encode("utf-8"))


class ZeroCounter:
    def count(self, text: str) -> int:
        return 0


class WrongArityCounter:
    def count(self) -> int:
        return 0


STATIC_SEMANTIC_GAP = """\
from typing import Protocol
class ByteCounter(Protocol):
    def count(self, text: str) -> int: ...
class ZeroCounter:
    def count(self, text: str) -> int:
        return 0
counter: ByteCounter = ZeroCounter()
"""

STATIC_SIGNATURE_MISMATCH = """\
from typing import Protocol
class ByteCounter(Protocol):
    def count(self, text: str) -> int: ...
class WrongArityCounter:
    def count(self) -> int:
        return 0
counter: ByteCounter = WrongArityCounter()
"""


def observe(candidate: object) -> str:
    if not isinstance(candidate, ByteCounter):
        return f"{type(candidate).__name__}: runtime=False; not called"
    try:
        result = str(candidate.count("ñ"))
    except TypeError:
        result = "TypeError"
    return f"{type(candidate).__name__}: runtime=True; count('ñ')={result}"


def run_probe() -> tuple[str, ...]:
    return tuple(
        observe(candidate) for candidate in (UTF8Counter(), ZeroCounter(), WrongArityCounter())
    )


if __name__ == "__main__":
    print("\n".join(run_probe()))
