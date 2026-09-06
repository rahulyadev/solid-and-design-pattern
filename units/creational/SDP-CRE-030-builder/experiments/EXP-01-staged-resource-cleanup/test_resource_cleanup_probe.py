"""Contract tests for staged resource ownership and cleanup."""

from __future__ import annotations

import pytest
from resource_cleanup_probe import AcquisitionError, prepare_resources, run_probe


def test_success_transfers_ownership_and_closes_in_reverse_order() -> None:
    success, _failure = run_probe()

    assert success == ["open:schema", "open:sink", "prepared", "use", "close:sink", "close:schema"]


def test_later_acquisition_failure_closes_earlier_resource() -> None:
    _success, failure = run_probe()

    assert failure == ["open:schema", "open-failed:sink", "close:schema", "rejected"]


def test_final_owner_close_is_idempotent() -> None:
    events: list[str] = []
    owner = prepare_resources(("schema", "sink"), events)

    owner.close()
    owner.close()

    assert events == ["open:schema", "open:sink", "prepared", "close:sink", "close:schema"]


def test_failed_acquisition_does_not_return_partial_product() -> None:
    events: list[str] = []

    with pytest.raises(AcquisitionError):
        prepare_resources(("schema", "sink"), events, fail_on="sink")

    assert events == ["open:schema", "open-failed:sink", "close:schema"]
