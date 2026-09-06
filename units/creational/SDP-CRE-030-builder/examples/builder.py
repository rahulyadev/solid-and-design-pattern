"""Runnable Builder example for SDP-CRE-030.

The synthetic reporting domain separates mutable, staged configuration from an
immutable and fully validated ``ReportPlan`` snapshot.  A small Director also
shows one construction sequence producing two representations.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, Self, TypeVar


class ReportFormat(StrEnum):
    CSV = "csv"
    JSONL = "jsonl"


class Destination(StrEnum):
    INTERNAL_ARCHIVE = "internal-archive"
    EXTERNAL_TRANSFER = "external-transfer"


class Compression(StrEnum):
    NONE = "none"
    GZIP = "gzip"


class PlanError(ValueError):
    """Base class for safe, expected construction failures."""


class MissingStepError(PlanError):
    """One or more required construction steps have not supplied a value."""

    def __init__(self, missing: Sequence[str]) -> None:
        self.missing = tuple(missing)
        super().__init__(f"required construction steps are missing: {', '.join(self.missing)}")


class InvalidPlanError(PlanError):
    """The completed candidate violates a product invariant."""

    def __init__(self, code: str, field_name: str, message: str) -> None:
        self.code = code
        self.field_name = field_name
        super().__init__(message)


@dataclass(frozen=True, slots=True)
class EncryptionRef:
    """Reference to key material; the key itself never enters the plan."""

    value: str = field(repr=False)

    def __post_init__(self) -> None:
        if not self.value or self.value != self.value.strip():
            raise InvalidPlanError(
                "invalid_encryption_reference",
                "encryption",
                "encryption reference must be nonblank and already normalized",
            )


@dataclass(frozen=True, slots=True)
class Column:
    selector: str
    sensitive: bool = False

    def __post_init__(self) -> None:
        if not self.selector or self.selector != self.selector.strip():
            raise InvalidPlanError(
                "invalid_column",
                "columns",
                "column selectors must be nonblank and already normalized",
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportPlan:
    """Valid immutable snapshot consumed by the report execution layer."""

    name: str
    source: str
    columns: tuple[Column, ...]
    destination: Destination
    report_format: ReportFormat = ReportFormat.JSONL
    compression: Compression = Compression.NONE
    encryption: EncryptionRef | None = field(default=None, repr=False)
    max_rows: int | None = None
    labels: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.name, "name")
        _require_text(self.source, "source")

        if not self.columns:
            raise InvalidPlanError(
                "missing_columns", "columns", "a report plan needs at least one column"
            )

        selectors = tuple(column.selector for column in self.columns)
        if len(set(selectors)) != len(selectors):
            raise InvalidPlanError(
                "duplicate_columns", "columns", "column selectors must be unique"
            )

        if self.report_format is ReportFormat.CSV and any("." in item for item in selectors):
            raise InvalidPlanError(
                "nested_csv_column",
                "columns",
                "CSV plans cannot contain nested column selectors",
            )

        if self.destination is Destination.EXTERNAL_TRANSFER and self.encryption is None:
            raise InvalidPlanError(
                "external_requires_encryption",
                "encryption",
                "external transfers require an encryption reference",
            )

        if self.max_rows is not None and not 1 <= self.max_rows <= 1_000_000:
            raise InvalidPlanError(
                "invalid_row_limit",
                "max_rows",
                "max_rows must be between 1 and 1,000,000",
            )

        label_keys = tuple(key for key, _value in self.labels)
        if len(set(label_keys)) != len(label_keys):
            raise InvalidPlanError("duplicate_labels", "labels", "label keys must be unique")
        for key, value in self.labels:
            _require_text(key, "labels")
            _require_text(value, "labels")


@dataclass(frozen=True, slots=True)
class BuildObservation:
    """Allow-listed diagnostics that intentionally omit configuration values."""

    phase: str
    step: str
    column_count: int
    error_code: str | None = None


Observer = Callable[[BuildObservation], None]


def ignore_observation(observation: BuildObservation) -> None:
    """Default best-effort observation sink."""


class ReportPlanBuilder:
    """Mutable request-local Builder with explicit build and reset semantics.

    ``build`` returns an immutable snapshot and leaves the Builder configured.
    ``reset`` is the only operation that clears staged state.  The object is not
    thread-safe and should not be shared between concurrent construction flows.
    """

    def __init__(self, observe: Observer = ignore_observation) -> None:
        self._observe = observe
        self._name: str | None = None
        self._source: str | None = None
        self._columns: list[Column] = []
        self._destination: Destination | None = None
        self._report_format = ReportFormat.JSONL
        self._compression = Compression.NONE
        self._encryption: EncryptionRef | None = None
        self._max_rows: int | None = None
        self._labels: dict[str, str] = {}

    def reset(self) -> Self:
        self._name = None
        self._source = None
        self._columns.clear()
        self._destination = None
        self._report_format = ReportFormat.JSONL
        self._compression = Compression.NONE
        self._encryption = None
        self._max_rows = None
        self._labels.clear()
        self._emit("builder.reset")
        return self

    def named(self, name: str) -> Self:
        self._name = name
        self._emit("name.staged")
        return self

    def from_source(self, source: str) -> Self:
        self._source = source
        self._emit("source.staged")
        return self

    def include(self, selector: str, *, sensitive: bool = False) -> Self:
        self._columns.append(Column(selector, sensitive))
        self._emit("column.staged")
        return self

    def as_format(self, report_format: ReportFormat) -> Self:
        self._report_format = report_format
        self._emit("format.staged")
        return self

    def deliver_to(
        self,
        destination: Destination,
        *,
        encryption: EncryptionRef | None = None,
    ) -> Self:
        self._destination = destination
        self._encryption = encryption
        self._emit("destination.staged")
        return self

    def compress_with(self, compression: Compression) -> Self:
        self._compression = compression
        self._emit("compression.staged")
        return self

    def limit_rows(self, max_rows: int | None) -> Self:
        self._max_rows = max_rows
        self._emit("limit.staged")
        return self

    def label(self, key: str, value: str) -> Self:
        self._labels[key] = value
        self._emit("label.staged")
        return self

    def build(self) -> ReportPlan:
        missing = self._missing_steps()
        if missing:
            self._emit("build.rejected", error_code="missing_steps")
            raise MissingStepError(missing)

        name = self._name
        source = self._source
        destination = self._destination
        if name is None or source is None or destination is None:
            raise AssertionError("missing-step check and Builder state disagree")

        try:
            product = ReportPlan(
                name=name,
                source=source,
                columns=tuple(self._columns),
                destination=destination,
                report_format=self._report_format,
                compression=self._compression,
                encryption=self._encryption,
                max_rows=self._max_rows,
                labels=tuple(sorted(self._labels.items())),
            )
        except InvalidPlanError as exc:
            self._emit("build.rejected", error_code=exc.code)
            raise

        self._emit("build.succeeded")
        return product

    def _missing_steps(self) -> tuple[str, ...]:
        missing: list[str] = []
        if self._name is None:
            missing.append("name")
        if self._source is None:
            missing.append("source")
        if not self._columns:
            missing.append("columns")
        if self._destination is None:
            missing.append("destination")
        return tuple(missing)

    def _emit(self, step: str, *, error_code: str | None = None) -> None:
        observation = BuildObservation(
            phase="report-plan.build",
            step=step,
            column_count=len(self._columns),
            error_code=error_code,
        )
        try:
            self._observe(observation)
        except Exception:
            # This example chooses best-effort diagnostics for a pure construction path.
            # A real application must document a different policy if losing telemetry is fatal.
            return


@dataclass(frozen=True, slots=True)
class BuildManifest:
    """Second representation produced by the standard construction sequence."""

    steps: tuple[str, ...]


class ManifestBuilder:
    """Concrete Builder that records a safe structural manifest, not a ReportPlan."""

    def __init__(self) -> None:
        self._steps: list[str] = []

    def reset(self) -> Self:
        self._steps.clear()
        self._steps.append("reset")
        return self

    def named(self, name: str) -> Self:
        self._steps.append("name")
        return self

    def from_source(self, source: str) -> Self:
        self._steps.append("source")
        return self

    def include(self, selector: str, *, sensitive: bool = False) -> Self:
        suffix = ":sensitive" if sensitive else ""
        self._steps.append(f"column{suffix}")
        return self

    def as_format(self, report_format: ReportFormat) -> Self:
        self._steps.append("format")
        return self

    def deliver_to(
        self,
        destination: Destination,
        *,
        encryption: EncryptionRef | None = None,
    ) -> Self:
        self._steps.append("destination")
        return self

    def compress_with(self, compression: Compression) -> Self:
        self._steps.append("compression")
        return self

    def limit_rows(self, max_rows: int | None) -> Self:
        self._steps.append("limit")
        return self

    def label(self, key: str, value: str) -> Self:
        self._steps.append("label")
        return self

    def build(self) -> BuildManifest:
        return BuildManifest((*self._steps, "build"))


ProductT_co = TypeVar("ProductT_co", covariant=True)
ProductT = TypeVar("ProductT")


class StandardReportBuilder(Protocol[ProductT_co]):
    """Builder role used by the optional Director."""

    def reset(self) -> StandardReportBuilder[ProductT_co]: ...

    def named(self, name: str) -> StandardReportBuilder[ProductT_co]: ...

    def from_source(self, source: str) -> StandardReportBuilder[ProductT_co]: ...

    def include(
        self, selector: str, *, sensitive: bool = False
    ) -> StandardReportBuilder[ProductT_co]: ...

    def as_format(self, report_format: ReportFormat) -> StandardReportBuilder[ProductT_co]: ...

    def deliver_to(
        self,
        destination: Destination,
        *,
        encryption: EncryptionRef | None = None,
    ) -> StandardReportBuilder[ProductT_co]: ...

    def compress_with(self, compression: Compression) -> StandardReportBuilder[ProductT_co]: ...

    def limit_rows(self, max_rows: int | None) -> StandardReportBuilder[ProductT_co]: ...

    def label(self, key: str, value: str) -> StandardReportBuilder[ProductT_co]: ...

    def build(self) -> ProductT_co: ...


def construct_daily_activity(  # noqa: UP047 - PEP 695 syntax would break Python 3.11
    builder: StandardReportBuilder[ProductT],
) -> ProductT:
    """Optional Director: one recipe can produce more than one representation."""

    return (
        builder.reset()
        .named("daily-activity")
        .from_source("activity-v1")
        .include("event_id")
        .include("actor_id", sensitive=True)
        .as_format(ReportFormat.JSONL)
        .deliver_to(Destination.INTERNAL_ARCHIVE)
        .compress_with(Compression.GZIP)
        .limit_rows(250_000)
        .label("cadence", "daily")
        .build()
    )


def make_internal_report(
    *,
    name: str,
    source: str,
    columns: Sequence[Column],
    report_format: ReportFormat = ReportFormat.JSONL,
    labels: Mapping[str, str] | None = None,
) -> ReportPlan:
    """Focused factory: the smaller choice when no staged workflow remains."""

    return ReportPlan(
        name=name,
        source=source,
        columns=tuple(columns),
        destination=Destination.INTERNAL_ARCHIVE,
        report_format=report_format,
        labels=tuple(sorted((labels or {}).items())),
    )


def _require_text(value: str, field_name: str) -> None:
    if not value or value != value.strip():
        raise InvalidPlanError(
            f"invalid_{field_name}",
            field_name,
            f"{field_name} must be nonblank and already normalized",
        )
