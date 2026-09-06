"""Canonical data embedded in the SDP-PYT-050 lifetime visual."""

from __future__ import annotations

from typing import TypedDict


class LifetimeState(TypedDict):
    id: str
    label: str
    owner: str
    begins: str
    ends: str
    shared_with: str
    cleanup: str
    warning: str


def lifetime_states() -> list[LifetimeState]:
    return [
        {
            "id": "module",
            "label": "Module cache",
            "owner": "Import system, keyed by fully qualified module name",
            "begins": "First successful import in this interpreter",
            "ends": "Cache invalidation or interpreter end; references may survive deletion",
            "shared_with": "Importers that resolve the same key in this interpreter",
            "cleanup": "No application-resource cleanup contract",
            "warning": "Not one-per-machine, one-per-cluster, or necessarily one-per-app",
        },
        {
            "id": "application",
            "label": "Application scope",
            "owner": "Composition root or framework lifespan",
            "begins": "Successful application startup",
            "ends": "Defined application shutdown",
            "shared_with": "Requests handled by that application instance",
            "cleanup": "Explicit close or async close at shutdown",
            "warning": "Each worker or app instance may own a separate resource",
        },
        {
            "id": "request",
            "label": "Request scope",
            "owner": "Request boundary or yield dependency",
            "begins": "Request dependency acquisition",
            "ends": "Documented response/function exit point",
            "shared_with": "Collaborators inside one request dependency graph",
            "cleanup": "Explicit exit even when handling raises",
            "warning": "Do not retain a closed session in background work",
        },
        {
            "id": "operation",
            "label": "Transient operation",
            "owner": "Immediate caller",
            "begins": "Ordinary construction or function call",
            "ends": "Last useful reference or explicit close",
            "shared_with": "Only code receiving the object",
            "cleanup": "Usually none; explicit when the object owns a resource",
            "warning": "Construction cost may make a wider explicit scope worthwhile",
        },
        {
            "id": "singleton",
            "label": "Traditional Singleton",
            "owner": "Class-level construction gate",
            "begins": "First access or eager class/module initialization",
            "ends": "Often implicit or test-only reset",
            "shared_with": "Callers that reach the same class state in one runtime domain",
            "cleanup": "Frequently hidden or awkward",
            "warning": (
                "Uniqueness does not define ownership, isolation, or distributed coordination"
            ),
        },
    ]
