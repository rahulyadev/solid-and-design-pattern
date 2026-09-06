"""Maintained decisions embedded in the SDP-CRE-010 construction explorer."""

from __future__ import annotations

Scenario = dict[str, str]


def construction_scenarios() -> list[Scenario]:
    return [
        {
            "id": "one-product",
            "title": "One stable product",
            "pressure": "The service always constructs one local formatter.",
            "decision": "direct construction",
            "boundary": "constructor call",
            "reject": "factory function",
            "because": "There is no variable creation decision to hide.",
        },
        {
            "id": "two-known",
            "title": "Two fixed choices",
            "pressure": "One application selects between two known transports at startup.",
            "decision": "small conditional",
            "boundary": "composition root",
            "reject": "class hierarchy",
            "because": "A visible branch is cheaper than a polymorphic family.",
        },
        {
            "id": "named-set",
            "title": "Several application-owned choices",
            "pressure": "Validated names select one of several explicit constructors.",
            "decision": "dictionary of callables",
            "boundary": "validated lookup",
            "reject": "dynamic registration",
            "because": "The application already owns and can list the complete set.",
        },
        {
            "id": "vary-construction",
            "title": "One workflow, injected construction",
            "pressure": "Tests and deployments supply different product construction.",
            "decision": "injected factory callable",
            "boundary": "function parameter",
            "reject": "Creator subclasses",
            "because": "Only construction varies; the workflow has no subclass identity.",
        },
        {
            "id": "creator-family",
            "title": "Existing Creator family",
            "pressure": "Each workflow subtype owns a stable product-creation policy.",
            "decision": "GoF Factory Method",
            "boundary": "overridable method",
            "reject": "simple factory function",
            "because": "Subclass polymorphism is already meaningful and controls creation.",
        },
        {
            "id": "same-type",
            "title": "Parse another representation",
            "pressure": "A class needs construction from a mapping as well as normal arguments.",
            "decision": "alternate classmethod constructor",
            "boundary": "class namespace",
            "reject": "Factory Method label",
            "because": "The method builds the same conceptual type, not a variable Product role.",
        },
        {
            "id": "independent-provider",
            "title": "Independent providers",
            "pressure": "Separately shipped packages contribute factories after discovery.",
            "decision": "dynamic registration boundary",
            "boundary": "startup discovery",
            "reject": "hard-coded dictionary",
            "because": "The application no longer owns the complete provider set.",
        },
        {
            "id": "global-lookup",
            "title": "Hidden global access",
            "pressure": "Code asks a global locator for whatever service happens to be registered.",
            "decision": "reject service locator",
            "boundary": "explicit dependency injection",
            "reject": "global factory singleton",
            "because": "Construction should not hide runtime dependencies from callers and tests.",
        },
    ]
