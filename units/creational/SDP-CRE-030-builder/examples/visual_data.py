"""Maintained scenario contract mirrored by the Builder decision explorer."""

from __future__ import annotations

from typing import TypedDict


class BuilderScenario(TypedDict):
    id: str
    title: str
    pressure: str
    inputs: list[str]
    sequence: str
    validation: str
    lifecycle: str
    verdict: str


SCENARIOS: tuple[BuilderScenario, ...] = (
    {
        "id": "keywords",
        "title": "All values available together",
        "pressure": "Six readable options, one call site",
        "inputs": ["required values known", "optional defaults stable"],
        "sequence": "No meaningful stages",
        "validation": "Product constructor",
        "lifecycle": "No mutable construction object",
        "verdict": "Use keyword-only construction; a Builder adds state without solving pressure.",
    },
    {
        "id": "factory",
        "title": "One named preset",
        "pressure": "Many callers need the same internal-report defaults",
        "inputs": ["name", "source", "columns"],
        "sequence": "One focused policy function",
        "validation": "Product constructor",
        "lifecycle": "Function-local values",
        "verdict": "Use a focused factory function; there is still no staged workflow.",
    },
    {
        "id": "locals",
        "title": "One local staged workflow",
        "pressure": "Inputs arrive from three nearby decisions",
        "inputs": ["identity", "columns", "destination"],
        "sequence": "Ordinary local variables then one final call",
        "validation": "Product constructor at the end",
        "lifecycle": "Local scope owns partial values",
        "verdict": "Keep incremental locals while one readable orchestration owns every stage.",
    },
    {
        "id": "builder",
        "title": "Repeated staged construction",
        "pressure": "Several flows gather required and optional parts over time",
        "inputs": ["required steps", "optional steps", "cross-field choices"],
        "sequence": "Concrete Builder accumulates private state",
        "validation": "build() plus Product invariants",
        "lifecycle": "Request-local Builder; immutable snapshot Product",
        "verdict": "Builder is justified; publish a Product only after explicit finalization.",
    },
    {
        "id": "director",
        "title": "One recipe, two representations",
        "pressure": "The daily sequence produces an executable plan and a safe manifest",
        "inputs": ["same ordered construction calls", "different Concrete Builders"],
        "sequence": "Optional Director drives the Builder role",
        "validation": "Each Concrete Builder finalizes its own Product",
        "lifecycle": "Director owns sequence, not Product state",
        "verdict": "Add a Director only because the sequence itself is named and reusable.",
    },
    {
        "id": "fluent-only",
        "title": "Fluent setters with no construction pressure",
        "pressure": "A chain looks readable but merely assigns three fields",
        "inputs": ["host", "port", "timeout"],
        "sequence": "Methods return self",
        "validation": "Unclear or absent",
        "lifecycle": "Mutable object can escape unfinished",
        "verdict": "Fluency alone is not GoF Builder; prefer a small value or function.",
    },
    {
        "id": "ordered",
        "title": "Illegal call order is a safety risk",
        "pressure": "Credentials must be bound only after an endpoint is verified",
        "inputs": ["endpoint stage", "verification stage", "credential stage"],
        "sequence": "Call order is part of the contract",
        "validation": "Runtime state machine or typed stage objects",
        "lifecycle": "Each stage exposes only legal next operations",
        "verdict": "A plain Self-returning Builder cannot prove order; use stronger stages.",
    },
    {
        "id": "shared",
        "title": "Shared mutable Builder",
        "pressure": "Two requests configure one module-global instance",
        "inputs": ["request A steps", "request B steps"],
        "sequence": "Interleaved writes contaminate state",
        "validation": "May validate the wrong combined candidate",
        "lifecycle": "Ownership is ambiguous and reset races",
        "verdict": "Create one Builder per flow or use immutable functional construction.",
    },
)
