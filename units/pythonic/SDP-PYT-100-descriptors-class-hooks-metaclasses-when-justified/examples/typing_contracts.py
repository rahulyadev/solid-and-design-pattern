"""Small static-typing contract for the production-oriented descriptor example."""

from __future__ import annotations

from managed_fields import HealthCheck, ServiceEndpoint


def endpoint_label(endpoint: ServiceEndpoint) -> str:
    return endpoint.authority()


def next_interval(check: HealthCheck) -> int:
    return check.interval_seconds + 1
