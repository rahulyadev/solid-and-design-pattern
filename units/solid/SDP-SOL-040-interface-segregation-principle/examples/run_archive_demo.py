"""Run from the repository root using the command in the practice guide."""

from archive_roles import (
    ArchiveReader,
    ArchiveWriter,
    duplicate,
    preview_text,
    purge_keys,
    save_report,
)
from archive_storage import MemoryArchive, PublishedBundle, UploadInbox


def main() -> None:
    archive = MemoryArchive({"welcome": b"hello", "obsolete": b"old"})
    bundle = PublishedBundle({"welcome": b"hello"})
    inbox = UploadInbox()

    print(f"bundle preview: {preview_text(bundle, 'welcome')}")
    save_report(inbox, "daily", "ready")
    print(f"inbox receipt: {inbox.receipts}")
    duplicate(archive, "welcome", "copy")
    print(f"copied preview: {preview_text(archive, 'copy')}")
    print(f"removed: {purge_keys(archive, ('obsolete', 'obsolete', 'missing'))}")

    reader: ArchiveReader = archive
    writer: ArchiveWriter = archive
    print(f"same object through two roles: {reader is archive and writer is archive}")
    save_report(writer, "welcome", "updated")
    print(f"reader sees later write: {preview_text(reader, 'welcome')}")
    print(f"runtime object still has remove: {hasattr(reader, 'remove')}")


if __name__ == "__main__":
    main()
