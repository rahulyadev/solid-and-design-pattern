"""Task values and borrowed subsystem ports; no concrete subsystem imports."""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


@dataclass(frozen=True)
class Snapshot:
    rows: tuple[str, ...]


@dataclass(frozen=True)
class Receipt:
    key: str
    byte_count: int


class Stage(Enum):
    LOAD = "load"
    RENDER = "render"
    STORE = "store"


class WriteOutcome(Enum):
    NOT_ATTEMPTED = "not_attempted"
    UNKNOWN = "unknown"


class LoadError(Exception):
    """Known snapshot retrieval failure; no archive write."""


class RenderError(Exception):
    """Known formatting failure; no archive write."""


class StoreError(Exception):
    """No receipt; the write might already have happened."""


class PacketUnavailable(Exception):
    def __init__(self, stage: Stage, write_outcome: WriteOutcome) -> None:
        self.stage = stage
        self.write_outcome = write_outcome
        super().__init__(f"packet unavailable: {stage.value}; write={write_outcome.value}")


class SnapshotReader(Protocol):
    def load(self, report_id: str) -> Snapshot: ...


class Renderer(Protocol):
    def render(self, snapshot: Snapshot) -> bytes: ...


class Archive(Protocol):
    def store(self, report_id: str, payload: bytes) -> Receipt: ...


class PacketBuilder(Protocol):
    def build(self, report_id: str) -> Receipt: ...
