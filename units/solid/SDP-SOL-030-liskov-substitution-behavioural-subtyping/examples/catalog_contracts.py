"""Original teaching example: an exact, stable catalog lookup contract.

Typed callers may supply any str, including empty and whitespace-only codes.
A present code returns its exact str value; an absent code raises UnknownCode.
Construction captures the supplied mapping. Lookups never change its observable
contents, so another caller can repeat a lookup. No I/O or concurrency is modeled.
The four explicitly named counterexamples deliberately violate this contract.
"""

from collections.abc import Mapping
from typing import Protocol


class UnknownCode(LookupError):
    """The requested code is absent from this catalog."""


class Catalog(Protocol):
    """The signature is only the shape; the module docstring owns the behavior."""

    def lookup(self, code: str) -> str: ...


class DictCatalog:
    """Own a snapshot; translate only the dictionary's missing-key operation."""

    def __init__(self, entries: Mapping[str, str]) -> None:
        self._entries = dict(entries)

    def lookup(self, code: str) -> str:
        try:
            return self._entries[code]
        except KeyError as error:
            raise UnknownCode(code) from error


class TupleCatalog:
    """A different representation, with the same externally visible promises."""

    def __init__(self, entries: Mapping[str, str]) -> None:
        self._entries = tuple(entries.items())

    def lookup(self, code: str) -> str:
        for candidate, value in self._entries:
            if candidate == code:
                return value
        raise UnknownCode(code)


class RestrictedCatalog(DictCatalog):
    """Counterexample: a compatible signature hides a narrower input domain."""

    def lookup(self, code: str) -> str:
        if len(code) < 3:
            raise ValueError("codes must have at least three characters")
        return super().lookup(code)


class BlankOnMissingCatalog(DictCatalog):
    """Counterexample: an error is replaced with a plausible success value."""

    def lookup(self, code: str) -> str:
        return self._entries.get(code, "")


class ConsumingCatalog(DictCatalog):
    """Counterexample: the first correct return value hides a state change."""

    def lookup(self, code: str) -> str:
        try:
            return self._entries.pop(code)
        except KeyError as error:
            raise UnknownCode(code) from error


class LeakyErrorCatalog(DictCatalog):
    """Counterexample: storage-specific failure escapes the catalog boundary."""

    def lookup(self, code: str) -> str:
        return self._entries[code]


def lookup_twice(catalog: Catalog, code: str) -> tuple[str, str]:
    """This client relies on stable repeated reads, not a concrete class name."""
    return catalog.lookup(code), catalog.lookup(code)


def label_or_unlisted(catalog: Catalog, code: str) -> str:
    """Only the documented absence outcome is converted to a display label."""
    try:
        return catalog.lookup(code)
    except UnknownCode:
        return "unlisted"
