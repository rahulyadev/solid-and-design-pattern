"""Unsolved Builder lab for SDP-CRE-030.

The baseline is deliberately a valid keyword-only construction API.  Do not
introduce a Builder until the staged requirements in the practice brief make it
the smallest justified design.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ArchiveMode(StrEnum):
    FULL = "full"
    INCREMENTAL = "incremental"


class ArchiveTarget(StrEnum):
    INTERNAL = "internal"
    PARTNER = "partner"


class InvalidArchiveJob(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


@dataclass(frozen=True, slots=True, kw_only=True)
class ArchiveJob:
    tenant_id: str
    datasets: tuple[str, ...]
    mode: ArchiveMode
    target: ArchiveTarget
    checkpoint: str | None = None
    encryption_ref: str | None = field(default=None, repr=False)
    retention_days: int = 30

    def __post_init__(self) -> None:
        if not self.tenant_id or self.tenant_id != self.tenant_id.strip():
            raise InvalidArchiveJob("invalid_tenant", "tenant_id must be normalized")
        if not self.datasets or len(set(self.datasets)) != len(self.datasets):
            raise InvalidArchiveJob("invalid_datasets", "datasets must be nonempty and unique")
        if any(not item or item != item.strip() for item in self.datasets):
            raise InvalidArchiveJob("invalid_datasets", "dataset names must be normalized")
        if self.mode is ArchiveMode.INCREMENTAL and self.checkpoint is None:
            raise InvalidArchiveJob(
                "checkpoint_required", "incremental archives require a checkpoint"
            )
        if self.mode is ArchiveMode.FULL and self.checkpoint is not None:
            raise InvalidArchiveJob("checkpoint_forbidden", "full archives reject checkpoints")
        if self.target is ArchiveTarget.PARTNER and self.encryption_ref is None:
            raise InvalidArchiveJob(
                "encryption_required", "partner archives require an encryption reference"
            )
        if not 1 <= self.retention_days <= 365:
            raise InvalidArchiveJob("invalid_retention", "retention_days must be from 1 to 365")


def prepare_archive_job(
    *,
    tenant_id: str,
    datasets: tuple[str, ...],
    mode: ArchiveMode,
    target: ArchiveTarget,
    checkpoint: str | None = None,
    encryption_ref: str | None = None,
    retention_days: int = 30,
) -> ArchiveJob:
    """Baseline focused factory; staged configuration is not separated yet."""

    return ArchiveJob(
        tenant_id=tenant_id,
        datasets=datasets,
        mode=mode,
        target=target,
        checkpoint=checkpoint,
        encryption_ref=encryption_ref,
        retention_days=retention_days,
    )


def summarize(job: ArchiveJob) -> str:
    """Stable consumer that must remain independent of construction mechanics."""

    return (
        f"{job.tenant_id}:{job.mode.value}:{job.target.value}:"
        f"{len(job.datasets)} datasets:{job.retention_days} days"
    )


TARGET_REFACTOR_COMPLETE = False


def main() -> None:
    job = prepare_archive_job(
        tenant_id="tenant-demo",
        datasets=("orders", "refunds"),
        mode=ArchiveMode.INCREMENTAL,
        target=ArchiveTarget.INTERNAL,
        checkpoint="cursor-042",
    )
    print(summarize(job))
    print(f"target_complete={TARGET_REFACTOR_COMPLETE}")


if __name__ == "__main__":
    main()
