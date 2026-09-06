"""Semantic source used to verify the interactive mechanism chooser."""

SCENARIOS = {
    "local": {
        "title": "Local, one-operation collaboration",
        "pressure": "One stable synchronous operation inside one small code path.",
        "mechanism": "Plain function or runtime duck typing",
        "static": "Optional callable annotation",
        "runtime": "Make the call and handle its documented failures",
        "evidence": "Focused examples plus behavior tests",
        "cost": "Lowest declaration and coupling cost",
    },
    "typed": {
        "title": "Independent implementations need static feedback",
        "pressure": "The client owns a small shape implemented across packages.",
        "mechanism": "Client-owned Protocol",
        "static": "Structural signature compatibility",
        "runtime": "Still an ordinary attribute lookup and call",
        "evidence": "Strict type checking plus shared contract tests",
        "cost": "Possible accidental matches and checker dependence",
    },
    "owned": {
        "title": "Owned family needs construction rules or shared behavior",
        "pressure": "Direct subclasses belong to one intentional extension family.",
        "mechanism": "ABC inheritance",
        "static": "Nominal relationship and annotated members",
        "runtime": "Incomplete direct subclasses cannot be instantiated",
        "evidence": "Subclass tests plus shared contract tests",
        "cost": "Inheritance, MRO, and stronger source coupling",
    },
    "foreign": {
        "title": "Foreign object must be recognized or translated",
        "pressure": "A third-party type cannot or should not inherit our base.",
        "mechanism": "Adapter; registration only for intentional recognition",
        "static": "Adapter can satisfy a Protocol explicitly or structurally",
        "runtime": "Registration changes isinstance, not methods or MRO",
        "evidence": "Adapter/registration probes plus behavior tests",
        "cost": "Registration is global trust and can overclaim compatibility",
    },
}
