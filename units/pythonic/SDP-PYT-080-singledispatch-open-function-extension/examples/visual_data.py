"""Tested observations embedded in the interactive dispatch visual."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypedDict

from open_rendering import (
    PrivilegedUserRegistered,
    RenderContext,
    UnsupportedPayloadError,
    UserRegistered,
    render_payload,
)
from registration_order_probe import observe_import_orders


class VisualScenario(TypedDict):
    id: str
    title: str
    phase: str
    value: str
    runtime_type: str
    candidate_path: list[str]
    selected: str
    outcome: str
    principle: str
    owner: str
    warning: str


def visual_scenarios() -> list[VisualScenario]:
    context = RenderContext("req-viz", "operations")
    exact = UserRegistered("evt-1", "rahul", "example.test")
    inherited = PrivilegedUserRegistered("evt-2", "sam", "example.test", "admin")
    mapping_value = {"count": 2, "state": "ready"}
    binary = b"ready"

    try:
        render_payload(("unknown",), context=context)
    except UnsupportedPayloadError as error:
        fallback_outcome = type(error).__name__
    else:  # pragma: no cover - incompatible with the maintained default
        fallback_outcome = "no-error"

    alpha_then_beta, beta_then_alpha = observe_import_orders()

    return [
        {
            "id": "exact",
            "title": "Exact type",
            "phase": "request dispatch",
            "value": "UserRegistered(evt-1)",
            "runtime_type": type(exact).__name__,
            "candidate_path": ["UserRegistered", "AuditEvent", "object"],
            "selected": render_payload.dispatch(type(exact)).__name__,
            "outcome": render_payload(exact, context=context).body,
            "principle": "An exact registered runtime type is the most specific candidate.",
            "owner": "open_rendering.render_payload",
            "warning": "Later arguments affect the body, not handler selection.",
        },
        {
            "id": "inheritance",
            "title": "Inherited match",
            "phase": "request dispatch",
            "value": "PrivilegedUserRegistered(evt-2)",
            "runtime_type": type(inherited).__name__,
            "candidate_path": [
                "PrivilegedUserRegistered (unregistered)",
                "UserRegistered",
                "AuditEvent",
                "object",
            ],
            "selected": render_payload.dispatch(type(inherited)).__name__,
            "outcome": render_payload(inherited, context=context).body,
            "principle": "MRO finds the nearest registered base implementation.",
            "owner": "open_rendering.render_payload",
            "warning": "The selected base handler does not automatically use subclass-only fields.",
        },
        {
            "id": "abc",
            "title": "ABC match",
            "phase": "request dispatch",
            "value": "dict(count=2, state=ready)",
            "runtime_type": type(mapping_value).__name__,
            "candidate_path": ["dict", "Mapping (registered ABC)", "object"],
            "selected": render_payload.dispatch(type(mapping_value)).__name__,
            "outcome": render_payload(mapping_value, context=context).body,
            "principle": "A registered ABC can serve its virtual subclasses.",
            "owner": "open_rendering.render_payload",
            "warning": (
                f"Registry key is {Mapping.__module__}.{Mapping.__qualname__}; dict is not a key."
            ),
        },
        {
            "id": "union",
            "title": "Union registration",
            "phase": "request dispatch",
            "value": "bytes: b'ready'",
            "runtime_type": type(binary).__name__,
            "candidate_path": ["bytes", "object"],
            "selected": render_payload.dispatch(type(binary)).__name__,
            "outcome": render_payload(binary, context=context).body,
            "principle": "One union annotation installed the same handler for str and bytes.",
            "owner": "open_rendering.render_payload",
            "warning": (
                "Union registration is supported from Python 3.11; it is still single dispatch."
            ),
        },
        {
            "id": "fallback",
            "title": "Default fallback",
            "phase": "request dispatch",
            "value": "tuple('unknown')",
            "runtime_type": "tuple",
            "candidate_path": ["tuple (unregistered)", "object (base/default)"],
            "selected": render_payload.dispatch(tuple).__name__,
            "outcome": fallback_outcome,
            "principle": "The original decorated function is the object fallback.",
            "owner": "open_rendering.render_payload",
            "warning": (
                "A fail-closed default is a domain decision, not a singledispatch requirement."
            ),
        },
        {
            "id": "imports",
            "title": "Competing imports",
            "phase": "startup configuration",
            "value": "ExternalPayload(ext-9)",
            "runtime_type": "ExternalPayload",
            "candidate_path": [
                "import extension_alpha",
                "import extension_beta",
                "dispatch ExternalPayload",
            ],
            "selected": alpha_then_beta.handler,
            "outcome": (
                f"alpha,beta -> {alpha_then_beta.result}; beta,alpha -> {beta_then_alpha.result}"
            ),
            "principle": "Registrations configure one generic function during module execution.",
            "owner": "registration_target.summarize_external",
            "warning": (
                "A production owner should reject duplicates instead of accepting order dependence."
            ),
        },
    ]
