"""Behaviour and capability tests for the solved teaching example."""

from collections.abc import Callable

import pytest
from archive_roles import duplicate, preview_text, purge_keys, save_report
from archive_storage import MemoryArchive, PublishedBundle, UploadInbox


@pytest.mark.parametrize("factory", [MemoryArchive, PublishedBundle])
@pytest.mark.parametrize("text", ["", "hello", "नमस्ते"])
def test_preview_accepts_readers_and_preserves_the_document(
    factory: Callable[[dict[str, bytes]], MemoryArchive | PublishedBundle], text: str
) -> None:
    source = factory({"document": text.encode("utf-8")})
    assert preview_text(source, "document") == text
    assert preview_text(source, "document") == text


@pytest.mark.parametrize("factory", [MemoryArchive, PublishedBundle])
def test_reader_distinguishes_empty_content_from_absence(
    factory: Callable[[dict[str, bytes]], MemoryArchive | PublishedBundle],
) -> None:
    source = factory({"empty": b""})
    assert preview_text(source, "empty") == ""
    with pytest.raises(KeyError):
        preview_text(source, "absent")


@pytest.mark.parametrize("factory", [MemoryArchive, PublishedBundle])
def test_provider_copies_initial_mapping(
    factory: Callable[[dict[str, bytes]], MemoryArchive | PublishedBundle],
) -> None:
    entries = {"document": b"original"}
    source = factory(entries)
    entries["document"] = b"changed"
    assert preview_text(source, "document") == "original"


def test_decoding_failure_does_not_consume_content() -> None:
    source = MemoryArchive({"binary": b"\xff"})
    with pytest.raises(UnicodeDecodeError):
        preview_text(source, "binary")
    assert source.read("binary") == b"\xff"


def test_writer_only_provider_can_receive_a_report() -> None:
    destination = UploadInbox()
    save_report(destination, "daily", "ready ✓")
    assert destination.receipts == (("daily", "ready ✓".encode()),)


def test_write_replaces_value_without_a_read_requirement() -> None:
    archive = MemoryArchive({"daily": b"old"})
    save_report(archive, "daily", "")
    assert archive.read("daily") == b""


def test_copy_retains_source_and_overwrites_destination() -> None:
    archive = MemoryArchive({"source": b"new", "destination": b"old"})
    duplicate(archive, "source", "destination")
    assert archive.read("source") == b"new"
    assert archive.read("destination") == b"new"


def test_copy_to_same_key_preserves_content() -> None:
    archive = MemoryArchive({"source": b"unchanged"})
    duplicate(archive, "source", "source")
    assert archive.read("source") == b"unchanged"


def test_missing_source_never_overwrites_destination() -> None:
    archive = MemoryArchive({"destination": b"keep"})
    with pytest.raises(KeyError):
        duplicate(archive, "missing", "destination")
    assert archive.read("destination") == b"keep"


def test_copy_propagates_write_failure_without_retrying() -> None:
    class FailingDestination:
        attempts = 0

        def read(self, key: str, /) -> bytes:
            return b"payload"

        def write(self, key: str, payload: bytes, /) -> None:
            self.attempts += 1
            raise OSError("write outcome unknown")

    archive = FailingDestination()
    with pytest.raises(OSError, match="outcome unknown"):
        duplicate(archive, "source", "destination")
    assert archive.attempts == 1


@pytest.mark.parametrize(
    ("keys", "expected"),
    [((), 0), (("missing",), 0), (("old", "old", "missing"), 1), (("old", "other"), 2)],
)
def test_purge_counts_actual_removals(keys: tuple[str, ...], expected: int) -> None:
    archive = MemoryArchive({"old": b"one", "other": b"two", "keep": b"three"})
    assert purge_keys(archive, iter(keys)) == expected
    assert archive.read("keep") == b"three"


def test_purge_can_use_a_provider_with_only_remove() -> None:
    class RemoveOnly:
        def __init__(self) -> None:
            self.keys = {"old"}

        def remove(self, key: str, /) -> bool:
            if key not in self.keys:
                return False
            self.keys.remove(key)
            return True

    assert purge_keys(RemoveOnly(), ("old", "old")) == 1


def test_purge_failure_does_not_imply_rollback() -> None:
    class FailingRemover:
        def __init__(self) -> None:
            self.removed: list[str] = []

        def remove(self, key: str, /) -> bool:
            if key == "blocked":
                raise PermissionError("retained document")
            self.removed.append(key)
            return True

    archive = FailingRemover()
    with pytest.raises(PermissionError, match="retained"):
        purge_keys(archive, ("first", "blocked", "last"))
    assert archive.removed == ["first"]
