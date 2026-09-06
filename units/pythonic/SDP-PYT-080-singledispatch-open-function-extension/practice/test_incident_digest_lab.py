"""Behavior protection for the unsolved incident-digest starter."""

import pytest
from incident_digest_lab import (
    DeploymentNotice,
    DigestContext,
    ServiceAlert,
    UnsupportedIncidentError,
    digest_incident,
)


@pytest.fixture
def context() -> DigestContext:
    return DigestContext("req-lab-1", "on-call")


def test_service_alert_behavior(context: DigestContext) -> None:
    result = digest_incident(ServiceAlert("inc-7", "catalog", 3), context=context)

    assert result == "alert:inc-7:catalog:sev=3:audience=on-call:request=req-lab-1"


def test_deployment_notice_behavior(context: DigestContext) -> None:
    result = digest_incident(DeploymentNotice("inc-8", "checkout", "2026.09.1"), context=context)

    assert result == "deploy:inc-8:checkout:2026.09.1:audience=on-call:request=req-lab-1"


@pytest.mark.parametrize("value", ["maintenance", b"maintenance"])
def test_text_behavior(value: str | bytes, context: DigestContext) -> None:
    assert (
        digest_incident(value, context=context)
        == "message:maintenance:audience=on-call:request=req-lab-1"
    )


@pytest.mark.parametrize("severity", [0, 6])
def test_service_alert_rejects_out_of_range_severity(severity: int, context: DigestContext) -> None:
    with pytest.raises(ValueError, match="between 1 and 5"):
        digest_incident(ServiceAlert("inc-9", "billing", severity), context=context)


def test_validation_happens_before_formatting(context: DigestContext) -> None:
    with pytest.raises(ValueError, match="service"):
        digest_incident(ServiceAlert("inc-10", " billing", 2), context=context)


def test_unknown_type_fails_closed(context: DigestContext) -> None:
    with pytest.raises(UnsupportedIncidentError, match="dict"):
        digest_incident({"incident_id": "inc-11"}, context=context)


def test_second_argument_does_not_define_the_incident_type() -> None:
    value = ServiceAlert("inc-12", "search", 2)

    on_call = digest_incident(value, context=DigestContext("req-a", "on-call"))
    leadership = digest_incident(value, context=DigestContext("req-b", "leadership"))

    assert on_call.startswith("alert:inc-12:search")
    assert leadership.startswith("alert:inc-12:search")
    assert on_call != leadership
