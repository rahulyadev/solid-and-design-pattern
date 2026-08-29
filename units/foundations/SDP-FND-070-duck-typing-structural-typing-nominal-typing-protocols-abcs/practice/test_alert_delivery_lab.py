"""Characterization tests for the unsolved SDP-FND-070 alert boundary."""

from __future__ import annotations

from abc import ABC
from dataclasses import FrozenInstanceError

import pytest
from alert_delivery_lab import (
    Alert,
    AlertChannel,
    DeliveryReceipt,
    EmailChannel,
    LegacyPager,
    PartnerWebhookChannel,
    SmsChannel,
    deliver_alert,
    deliver_batch,
)


def test_current_nominal_channels_deliver_in_input_order() -> None:
    alert = Alert("evt-42", "Payment queue is delayed", "critical")

    receipts = deliver_batch(alert, (EmailChannel(), SmsChannel()))

    assert receipts == (
        DeliveryReceipt("email", True, "email:evt-42"),
        DeliveryReceipt("sms", True, "sms:evt-42"),
    )


def test_sms_represents_normal_info_suppression_as_non_delivery() -> None:
    alert = Alert("evt-info", "Daily digest is ready", "info")

    receipt = deliver_alert(alert, SmsChannel())

    assert receipt == DeliveryReceipt(
        "sms",
        False,
        None,
        "SMS is reserved for warning and critical alerts",
    )


def test_structurally_compatible_partner_works_directly() -> None:
    alert = Alert("evt-42", "Payment queue is delayed", "critical")

    receipt = PartnerWebhookChannel().deliver(alert)

    assert receipt == DeliveryReceipt("partner-webhook", True, "webhook:evt-42")


def test_nominal_client_gate_rejects_the_compatible_partner() -> None:
    alert = Alert("evt-42", "Payment queue is delayed", "critical")
    partner = PartnerWebhookChannel()

    with pytest.raises(TypeError, match="unsupported alert channel: PartnerWebhookChannel"):
        deliver_alert(alert, partner)  # type: ignore[arg-type]


def test_current_runtime_recognition_is_nominal() -> None:
    assert isinstance(EmailChannel(), AlertChannel)
    assert isinstance(SmsChannel(), AlertChannel)
    assert not isinstance(PartnerWebhookChannel(), AlertChannel)
    assert AlertChannel in EmailChannel.__mro__
    assert AlertChannel not in PartnerWebhookChannel.__mro__


def test_incomplete_nominal_subclass_cannot_be_instantiated() -> None:
    class IncompleteChannel(AlertChannel):
        pass

    assert issubclass(IncompleteChannel, ABC)
    with pytest.raises(TypeError, match=r"abstract method.*deliver"):
        IncompleteChannel()  # type: ignore[abstract]


def test_incompatible_legacy_pager_has_a_different_operation() -> None:
    pager = LegacyPager()

    assert pager.push("critical alert", priority=1) == "pager:1:14"
    assert not hasattr(pager, "deliver")


def test_alert_is_not_mutated_by_delivery() -> None:
    alert = Alert("evt-42", "Payment queue is delayed", "critical")
    before = alert

    deliver_batch(alert, (EmailChannel(), SmsChannel()))

    assert alert == before
    with pytest.raises(FrozenInstanceError):
        alert.severity = "info"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {"event_id": "", "message": "message", "severity": "info"},
            "event_id must not be blank",
        ),
        (
            {"event_id": "evt-1", "message": " ", "severity": "info"},
            "message must not be blank",
        ),
        (
            {"event_id": "evt-1", "message": "message", "severity": "urgent"},
            "unsupported severity: urgent",
        ),
    ],
)
def test_invalid_alerts_are_rejected_before_boundary_selection(
    kwargs: dict[str, str],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        Alert(**kwargs)


@pytest.mark.parametrize(
    "receipt",
    [
        DeliveryReceipt("email", True, "ref-1"),
        DeliveryReceipt("sms", False, None, "suppressed by policy"),
    ],
)
def test_receipt_accepts_only_coherent_examples(receipt: DeliveryReceipt) -> None:
    assert receipt.channel_code


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (("", True, "ref", None), "channel_code must not be blank"),
        (("email", True, None, None), "a delivered receipt needs a provider reference"),
        (("email", True, " ", None), "a delivered receipt needs a provider reference"),
        (("email", True, "ref", "why"), "a delivered receipt must not contain a reason"),
        (
            ("email", False, "ref", "why"),
            "a non-delivery must not contain a provider reference",
        ),
        (("email", False, None, None), "a non-delivery needs a reason"),
        (("email", False, None, " "), "a non-delivery needs a reason"),
    ],
)
def test_receipt_rejects_incoherent_states(
    args: tuple[str, bool, str | None, str | None],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        DeliveryReceipt(*args)


def test_empty_batch_is_a_valid_no_work_request() -> None:
    alert = Alert("evt-42", "Payment queue is delayed", "critical")

    assert deliver_batch(alert, ()) == ()
