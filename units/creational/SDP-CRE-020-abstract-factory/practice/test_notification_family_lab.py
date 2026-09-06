"""Behavior tests for the unsolved Abstract Factory practice baseline."""

from __future__ import annotations

import json

import pytest
from notification_family_lab import (
    TARGET_REFACTOR_COMPLETE,
    IncompatibleNotificationProductError,
    InternalRenderer,
    Notice,
    PartnerSender,
    UnknownNotificationFamilyError,
    publish_notice,
)


def test_internal_baseline() -> None:
    output: list[bytes] = []

    receipt = publish_notice(Notice("NOTICE-1", "ready"), "internal", output)

    assert receipt.receipt_id == "internal:NOTICE-1"
    assert output == [b"NOTICE-1|ready"]


def test_partner_baseline_is_deterministic() -> None:
    output: list[bytes] = []

    receipt = publish_notice(Notice("NOTICE-2", "caf\u00e9 ready"), "partner-v1", output)

    assert receipt.receipt_id == "partner:NOTICE-2"
    assert json.loads(output[0]) == {"body": "caf\u00e9 ready", "id": "NOTICE-2"}
    assert output[0] == b'{"body":"caf\xc3\xa9 ready","id":"NOTICE-2"}'


@pytest.mark.parametrize(
    ("notice_id", "body"),
    [("", "ok"), ("\u00e9", "ok"), ("bad|id", "ok"), ("NOTICE-3", "")],
)
def test_invalid_notices(notice_id: str, body: str) -> None:
    with pytest.raises(ValueError):
        Notice(notice_id, body)


def test_unknown_family_fails_before_write() -> None:
    output: list[bytes] = []

    with pytest.raises(UnknownNotificationFamilyError, match="missing"):
        publish_notice(Notice("NOTICE-4", "ready"), "missing", output)

    assert output == []


def test_mixed_products_fail_before_write() -> None:
    output: list[bytes] = []
    rendered = InternalRenderer().render(Notice("NOTICE-5", "ready"))

    with pytest.raises(IncompatibleNotificationProductError):
        PartnerSender(output).send(rendered)

    assert output == []


def test_target_design_work_remains_unsolved() -> None:
    assert TARGET_REFACTOR_COMPLETE is False
