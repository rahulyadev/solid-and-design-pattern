"""Maintained decisions embedded in the SDP-PYT-100 mechanism explorer."""

from __future__ import annotations

Scenario = dict[str, str]


def mechanism_scenarios() -> list[Scenario]:
    return [
        {
            "id": "value-now",
            "title": "Validate one incoming value",
            "pressure": "One request field needs trimming and a range check.",
            "decision": "function + dataclass",
            "moment": "explicit call / object construction",
            "next": "property",
            "why": "The caller can see the operation; no attribute interception is needed.",
            "risk": "A hook would hide a simple data transformation.",
        },
        {
            "id": "one-owner",
            "title": "Manage one attribute on one class",
            "pressure": "One mutable class needs validation whenever its port changes.",
            "decision": "property",
            "moment": "instance attribute access",
            "next": "descriptor",
            "why": "A property keeps the policy beside its sole owner.",
            "risk": "A reusable protocol adds indirection before reuse exists.",
        },
        {
            "id": "repeated-field",
            "title": "Reuse managed-attribute semantics",
            "pressure": (
                "Several fields on several classes share get, set, delete, and naming rules."
            ),
            "decision": "data descriptor",
            "moment": "attribute lookup / assignment / deletion",
            "next": "__init_subclass__",
            "why": "The repeated unit is an attribute-access policy, not a class-family rule.",
            "risk": (
                "Lookup becomes implicit; slow I/O and surprising side effects are unacceptable."
            ),
        },
        {
            "id": "explicit-set",
            "title": "Select from an application-owned set",
            "pressure": "Five known handlers need deterministic lookup.",
            "decision": "explicit dictionary",
            "moment": "startup assembly / explicit lookup",
            "next": "__init_subclass__",
            "why": "The application can list its handlers without definition-time global mutation.",
            "risk": "Auto-registration would introduce import-order and test-isolation state.",
        },
        {
            "id": "future-subclasses",
            "title": "Govern an existing hierarchy",
            "pressure": "Every future subclass must declare validated metadata.",
            "decision": "__init_subclass__",
            "moment": "subclass creation",
            "next": "metaclass",
            "why": "Ordinary cooperative inheritance supplies a post-creation hook.",
            "risk": "Missing super() or keyword forwarding can silently break sibling hooks.",
        },
        {
            "id": "one-class",
            "title": "Transform one completed class explicitly",
            "pressure": "One class needs a visible marker independent of descendants.",
            "decision": "in-place class decorator",
            "moment": "after class creation, before name binding",
            "next": "replacement decorator",
            "why": "The opt-in is local and returning the same class preserves identity.",
            "risk": "Replacement can alter identity, MRO, typing, pickling, and tooling.",
        },
        {
            "id": "body-namespace",
            "title": "Control the class-body namespace",
            "pressure": "A framework must reject duplicate declarations while the body executes.",
            "decision": "metaclass __prepare__",
            "moment": "before and during class-body execution",
            "next": "more metaclass hooks",
            "why": "No post-creation hook can change the namespace used by the already-run body.",
            "risk": (
                "The framework owns metaclass composition, __classcell__, typing, and diagnostics."
            ),
        },
        {
            "id": "vague-framework",
            "title": "Add framework-like magic",
            "pressure": (
                "The proposal says a metaclass will make models cleaner but names no invariant."
            ),
            "decision": "do not add a mechanism",
            "moment": "none",
            "next": "explicit prototype first",
            "why": "Power is not a requirement; there is no evidenced change pressure.",
            "risk": (
                "Magic would create inheritance coupling and import-time failures without a payoff."
            ),
        },
    ]
