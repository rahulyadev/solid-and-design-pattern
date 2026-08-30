"""A runtime Protocol check is not a signature or behavioural check."""

from typing import Protocol, runtime_checkable


class StaticMaker(Protocol):
    def make(self, title: str, /, *, prefix: str) -> str: ...


@runtime_checkable
class RuntimeMaker(Protocol):
    def make(self, title: str, /, *, prefix: str) -> str: ...


class GoodMaker:
    def make(self, title: str, /, *, prefix: str) -> str:
        return f"{prefix}{title}"


class WrongSignature:
    def make(self) -> int:
        return 7


class IgnoresTitle:
    def make(self, title: str, /, *, prefix: str) -> str:
        return prefix


def membership(candidate: object, interface: type[object]) -> bool:
    return isinstance(candidate, interface)


def observe(candidate: object) -> tuple[bool, str]:
    if not isinstance(candidate, RuntimeMaker):
        return False, "missing member"
    try:
        result = candidate.make("Luna", prefix="Hi: ")
    except TypeError:
        return True, "TypeError"
    return True, "contract kept" if result == "Hi: Luna" else "contract broken"


def main() -> None:
    try:
        membership(GoodMaker(), StaticMaker)
    except TypeError:
        print("ordinary Protocol isinstance: TypeError")
    candidates = (GoodMaker(), WrongSignature(), IgnoresTitle(), object())
    for candidate in candidates:
        matched, outcome = observe(candidate)
        print(f"{type(candidate).__name__}: member check={matched}; call={outcome}")


if __name__ == "__main__":
    main()
