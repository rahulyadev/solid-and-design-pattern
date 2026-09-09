"""Small trusted-code capability; signatures alone do not encode access or freshness."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Key:
    tenant: str
    document: str


@dataclass(frozen=True)
class Document:
    key: Key
    revision: int
    lines: tuple[str, ...]


class Closed(RuntimeError):
    """The owner has ended this capability's lifetime."""


class ContractError(RuntimeError):
    """A collaborator returned a document for a different key."""


class Catalog(Protocol):
    def read(self, key: Key, /) -> Document:
        """Read a snapshot; access, freshness, errors and lifetime need separate policy."""
        ...


class OwnedCatalog(Catalog, Protocol):
    def close(self) -> None:
        """Release owned resources; successful close is idempotent."""
        ...


def headline(catalog: Catalog, key: Key) -> str:
    """Client depends on the shared operation, not the proxy's administration API."""
    document = catalog.read(key)
    return document.lines[0] if document.lines else "(empty)"
