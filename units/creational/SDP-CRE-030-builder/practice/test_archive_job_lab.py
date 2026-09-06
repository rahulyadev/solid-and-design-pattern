"""Baseline behavior tests that intentionally do not prescribe a Builder shape."""

from __future__ import annotations

import pytest
from archive_job_lab import (
    TARGET_REFACTOR_COMPLETE,
    ArchiveMode,
    ArchiveTarget,
    InvalidArchiveJob,
    prepare_archive_job,
    summarize,
)


def test_incremental_internal_baseline() -> None:
    job = prepare_archive_job(
        tenant_id="tenant-a",
        datasets=("orders", "refunds"),
        mode=ArchiveMode.INCREMENTAL,
        target=ArchiveTarget.INTERNAL,
        checkpoint="cursor-001",
    )

    assert summarize(job) == "tenant-a:incremental:internal:2 datasets:30 days"


def test_partner_job_requires_encryption_without_exposing_reference() -> None:
    job = prepare_archive_job(
        tenant_id="tenant-a",
        datasets=("orders",),
        mode=ArchiveMode.FULL,
        target=ArchiveTarget.PARTNER,
        encryption_ref="kms/archive/partner-a",
    )

    assert "kms/archive/partner-a" not in repr(job)


@pytest.mark.parametrize(
    ("mode", "checkpoint", "code"),
    [
        (ArchiveMode.INCREMENTAL, None, "checkpoint_required"),
        (ArchiveMode.FULL, "cursor-001", "checkpoint_forbidden"),
    ],
)
def test_checkpoint_cross_field_rules(mode: ArchiveMode, checkpoint: str | None, code: str) -> None:
    with pytest.raises(InvalidArchiveJob) as captured:
        prepare_archive_job(
            tenant_id="tenant-a",
            datasets=("orders",),
            mode=mode,
            target=ArchiveTarget.INTERNAL,
            checkpoint=checkpoint,
        )

    assert captured.value.code == code


def test_partner_without_encryption_is_rejected() -> None:
    with pytest.raises(InvalidArchiveJob) as captured:
        prepare_archive_job(
            tenant_id="tenant-a",
            datasets=("orders",),
            mode=ArchiveMode.FULL,
            target=ArchiveTarget.PARTNER,
        )

    assert captured.value.code == "encryption_required"


@pytest.mark.parametrize("retention_days", [0, 366])
def test_retention_bounds(retention_days: int) -> None:
    with pytest.raises(InvalidArchiveJob) as captured:
        prepare_archive_job(
            tenant_id="tenant-a",
            datasets=("orders",),
            mode=ArchiveMode.FULL,
            target=ArchiveTarget.INTERNAL,
            retention_days=retention_days,
        )

    assert captured.value.code == "invalid_retention"


def test_starter_remains_unsolved() -> None:
    assert TARGET_REFACTOR_COMPLETE is False
