"""Client contracts and workflows; no storage implementation or vendor imports."""

from collections.abc import Iterable
from typing import Protocol


class ArchiveReader(Protocol):
    def read(self, key: str, /) -> bytes:
        """Return stored bytes, or raise KeyError without changing stored data."""
        ...


class ArchiveWriter(Protocol):
    def write(self, key: str, payload: bytes, /) -> None:
        """Store the exact bytes, replacing an existing value at this key."""
        ...


class ArchiveRemover(Protocol):
    def remove(self, key: str, /) -> bool:
        """Remove an existing key; return False when the key is already absent."""
        ...


class ReadWriteArchive(ArchiveReader, ArchiveWriter, Protocol):
    """Both operations address the same archive; no atomic-copy promise."""


class ArchiveManager(ArchiveReader, ArchiveWriter, ArchiveRemover, Protocol):
    """A deliberately broad comparison boundary, not the default client dependency."""


def preview_text(source: ArchiveReader, key: str) -> str:
    """Decode one stored UTF-8 document; absence and decoding errors propagate."""
    return source.read(key).decode("utf-8")


def save_report(destination: ArchiveWriter, key: str, text: str) -> None:
    destination.write(key, text.encode("utf-8"))


def purge_keys(archive: ArchiveRemover, keys: Iterable[str]) -> int:
    """Count actual removals. Earlier removals remain if a later operation fails."""
    return sum(archive.remove(key) for key in keys)


def duplicate(archive: ReadWriteArchive, source_key: str, destination_key: str) -> None:
    """Read before writing; overwrite destination; keep source; not a transaction."""
    payload = archive.read(source_key)
    archive.write(destination_key, payload)
