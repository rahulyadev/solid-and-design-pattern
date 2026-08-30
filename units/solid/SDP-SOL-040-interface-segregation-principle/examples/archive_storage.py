"""Synthetic in-memory providers. None inherits or imports the client protocols."""

from collections.abc import Mapping


class MemoryArchive:
    def __init__(self, entries: Mapping[str, bytes]) -> None:
        self._entries = dict(entries)

    def read(self, key: str, /) -> bytes:
        return self._entries[key]

    def write(self, key: str, payload: bytes, /) -> None:
        self._entries[key] = payload

    def remove(self, key: str, /) -> bool:
        if key not in self._entries:
            return False
        del self._entries[key]
        return True


class PublishedBundle:
    """A copied snapshot offering only reading through its ordinary public API."""

    def __init__(self, entries: Mapping[str, bytes]) -> None:
        self._entries = dict(entries)

    def read(self, key: str, /) -> bytes:
        return self._entries[key]


class UploadInbox:
    """Write capability with a receipt log for the synthetic demo."""

    def __init__(self) -> None:
        self._entries: dict[str, bytes] = {}
        self._receipts: list[tuple[str, bytes]] = []

    def write(self, key: str, payload: bytes, /) -> None:
        self._entries[key] = payload
        self._receipts.append((key, payload))

    @property
    def receipts(self) -> tuple[tuple[str, bytes], ...]:
        return tuple(self._receipts)
