"""Unsolved starter for the SDP-PYT-080 incident-digest exercise.

The current conditional is intentionally small and working.  Preserve its
behavior before deciding whether the new extension pressure earns refactoring.
"""

from __future__ import annotations

from dataclasses import dataclass


class UnsupportedIncidentError(TypeError):
    """Raised when the starter cannot digest an incident value."""


@dataclass(frozen=True, slots=True)
class ServiceAlert:
    incident_id: str
    service: str
    severity: int


@dataclass(frozen=True, slots=True)
class DeploymentNotice:
    incident_id: str
    service: str
    version: str


@dataclass(frozen=True, slots=True)
class DigestContext:
    request_id: str
    audience: str


def _require_text(field_name: str, value: str) -> None:
    if not value or value != value.strip():
        raise ValueError(f"{field_name} must be non-empty and trimmed")


def digest_incident(value: object, *, context: DigestContext) -> str:
    """Return the existing digest; this is the learner's refactoring target."""

    _require_text("request_id", context.request_id)
    _require_text("audience", context.audience)

    if isinstance(value, ServiceAlert):
        _require_text("incident_id", value.incident_id)
        _require_text("service", value.service)
        if not 1 <= value.severity <= 5:
            raise ValueError("severity must be between 1 and 5")
        return (
            f"alert:{value.incident_id}:{value.service}:sev={value.severity}:"
            f"audience={context.audience}:request={context.request_id}"
        )

    if isinstance(value, DeploymentNotice):
        _require_text("incident_id", value.incident_id)
        _require_text("service", value.service)
        _require_text("version", value.version)
        return (
            f"deploy:{value.incident_id}:{value.service}:{value.version}:"
            f"audience={context.audience}:request={context.request_id}"
        )

    if isinstance(value, (str, bytes)):
        text = value.decode("utf-8") if isinstance(value, bytes) else value
        _require_text("message", text)
        return f"message:{text}:audience={context.audience}:request={context.request_id}"

    raise UnsupportedIncidentError(f"unsupported incident type: {type(value).__qualname__}")


def main() -> None:
    context = DigestContext("req-lab-1", "on-call")
    print(digest_incident(ServiceAlert("inc-7", "catalog", 3), context=context))
    print(digest_incident(b"maintenance", context=context))


if __name__ == "__main__":
    main()
