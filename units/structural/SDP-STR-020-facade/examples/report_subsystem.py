"""Synthetic in-memory subsystem, deliberately sequential and non-idempotent."""

from report_contracts import LoadError, Receipt, RenderError, Snapshot, StoreError


class MemoryReports:
    def __init__(self, reports: dict[str, Snapshot], events: list[str]) -> None:
        self._reports = dict(reports)
        self._events = events

    def load(self, report_id: str) -> Snapshot:
        self._events.append("load")
        try:
            return self._reports[report_id]
        except KeyError as exc:
            raise LoadError("report not available") from exc


class TextRenderer:
    def __init__(self, events: list[str], *, fail: bool = False) -> None:
        self._events = events
        self._fail = fail

    def render(self, snapshot: Snapshot) -> bytes:
        self._events.append("render")
        if self._fail:
            raise RenderError("renderer unavailable")
        return ("REPORT\n" + "\n".join(snapshot.rows) + "\n").encode("utf-8")


class MemoryArchive:
    """Each successful write allocates a new key, even for the same report_id.

    fail_before_write and lose_ack select known fault scenarios for the probe.
    close is infallible here. This fake is neither durable nor thread-safe.
    """

    def __init__(
        self, events: list[str], *, fail_before_write: bool = False, lose_ack: bool = False
    ) -> None:
        self._events = events
        self._fail_before_write = fail_before_write
        self._lose_ack = lose_ack
        self._objects: dict[str, bytes] = {}
        self._closed = False
        self.close_count = 0

    def store(self, report_id: str, payload: bytes) -> Receipt:
        self._require_open()
        self._events.append("store")
        if self._fail_before_write:
            raise StoreError("storage unavailable")
        key = f"{report_id}/{len(self._objects) + 1}"
        self._objects[key] = payload
        if self._lose_ack:
            raise StoreError("acknowledgement lost")
        return Receipt(key, len(payload))

    def keys(self) -> tuple[str, ...]:
        """Lower-level maintenance capability, intentionally absent from the facade."""
        self._require_open()
        return tuple(self._objects)

    def read(self, key: str) -> bytes:
        self._require_open()
        return self._objects[key]

    def close(self) -> None:
        self.close_count += 1
        self._closed = True

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("archive is closed")
