"""Small task facade. Ports are trusted implementations of the documented contract."""

import re

from report_contracts import (
    Archive,
    LoadError,
    PacketUnavailable,
    Receipt,
    Renderer,
    RenderError,
    SnapshotReader,
    Stage,
    StoreError,
    WriteOutcome,
)


def build_packet(
    report_id: str, *, reader: SnapshotReader, renderer: Renderer, archive: Archive
) -> Receipt:
    """Load, render, store once; never retry or close borrowed collaborators."""
    if re.fullmatch(r"[A-Z0-9-]{1,24}", report_id) is None:
        raise ValueError("report_id must contain 1-24 uppercase ASCII letters, digits or hyphens")
    try:
        snapshot = reader.load(report_id)
    except LoadError as exc:
        raise PacketUnavailable(Stage.LOAD, WriteOutcome.NOT_ATTEMPTED) from exc
    try:
        payload = renderer.render(snapshot)
    except RenderError as exc:
        raise PacketUnavailable(Stage.RENDER, WriteOutcome.NOT_ATTEMPTED) from exc
    try:
        return archive.store(report_id, payload)
    except StoreError as exc:
        raise PacketUnavailable(Stage.STORE, WriteOutcome.UNKNOWN) from exc


class ReportFacade:
    """Retain borrowed dependencies for clients that repeatedly request report packets."""

    def __init__(self, reader: SnapshotReader, renderer: Renderer, archive: Archive) -> None:
        self._reader = reader
        self._renderer = renderer
        self._archive = archive

    def build(self, report_id: str) -> Receipt:
        return build_packet(
            report_id, reader=self._reader, renderer=self._renderer, archive=self._archive
        )
