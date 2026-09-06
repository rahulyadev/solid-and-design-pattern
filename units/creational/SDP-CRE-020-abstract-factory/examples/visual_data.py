"""Maintained scenario contract mirrored by the Abstract Factory explorer."""

from __future__ import annotations

from typing import TypedDict


class FamilyScenario(TypedDict):
    id: str
    title: str
    selection: str
    products: list[str]
    coherence: str
    boundary: str
    outcome: str
    verdict: str


SCENARIOS: tuple[FamilyScenario, ...] = (
    {
        "id": "direct-one",
        "title": "One stable family",
        "selection": "Policy constructs JSON products directly",
        "products": ["JsonEncoder", "JsonChannel", "JsonAckDecoder"],
        "coherence": "Visible but hard-coded",
        "boundary": "Inside policy workflow",
        "outcome": "Works; change touches policy",
        "verdict": "Keep direct construction until family variation is real.",
    },
    {
        "id": "ready-bundle",
        "title": "One startup-selected bundle",
        "selection": "Composition root injects DeliveryBundle",
        "products": ["Encoder", "Channel context", "AckDecoder"],
        "coherence": "Validated once during assembly",
        "boundary": "Composition root",
        "outcome": "Policy stays concrete-free",
        "verdict": "Ordinary dependency injection is the smaller answer.",
    },
    {
        "id": "family-factory",
        "title": "Repeated per-job creation",
        "selection": "Composition root injects one family factory",
        "products": ["create_encoder", "open_channel", "create_ack_decoder"],
        "coherence": "One family identity spans every role",
        "boundary": "Factory plus runtime invariant gate",
        "outcome": "Fresh related products per job",
        "verdict": "Abstract Factory is earned by family-wide repeatable creation.",
    },
    {
        "id": "mixed-family",
        "title": "Accidental mixed products",
        "selection": "JSON encoder + PIPE channel + PIPE decoder",
        "products": ["JsonEncoder", "PipeChannel", "PipeAckDecoder"],
        "coherence": "Broken before use",
        "boundary": "Family validation gate",
        "outcome": "Reject before external write",
        "verdict": "Compatibility is the invariant, not matching method names.",
    },
    {
        "id": "one-factory-method",
        "title": "Only one product varies",
        "selection": "Creator overrides create_channel",
        "products": ["One Channel product"],
        "coherence": "No multi-product relationship",
        "boundary": "Creator method",
        "outcome": "Stable workflow, one creation decision",
        "verdict": "This is Factory Method, not Abstract Factory.",
    },
    {
        "id": "constructor-bag",
        "title": "Bag of unrelated constructors",
        "selection": "Object stores logger, clock, encoder factories",
        "products": ["make_logger", "make_clock", "make_encoder"],
        "coherence": "No shared compatibility rule",
        "boundary": "Generic dependency container",
        "outcome": "Names are grouped; semantics are not",
        "verdict": "A constructor bag is DI plumbing, not an Abstract Factory.",
    },
    {
        "id": "registry-root",
        "title": "Configuration registry at the root",
        "selection": "Exact allowed name resolves a factory builder",
        "products": ["JsonDeliveryFactory or PipeDeliveryFactory"],
        "coherence": "Alias checked against factory identity",
        "boundary": "Startup composition root",
        "outcome": "Unknown and disallowed remain distinct",
        "verdict": "Registry selection complements; it does not define the pattern.",
    },
    {
        "id": "dynamic-plugin",
        "title": "Independently shipped family",
        "selection": "Trusted entry point loads a provider",
        "products": ["Provider-supplied family factory"],
        "coherence": "Contract plus provider conformance tests",
        "boundary": "Package discovery and trust policy",
        "outcome": "New deployment can add families",
        "verdict": "Discovery is a separate lifecycle and security boundary.",
    },
)
