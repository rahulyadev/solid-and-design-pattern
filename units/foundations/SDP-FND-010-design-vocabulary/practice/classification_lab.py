"""Unsolved SDP-FND-010 starter: expose the limits of keyword classification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DesignLevel(StrEnum):
    """Labels used by the deliberately naive starter."""

    PRINCIPLE = "principle"
    PATTERN = "pattern"
    IDIOM = "idiom"
    FRAMEWORK = "framework"
    ARCHITECTURE = "architecture"
    UNCLASSIFIED = "unclassified"


@dataclass(frozen=True)
class DesignClaim:
    """A claim whose wording may or may not contain useful design evidence."""

    name: str
    statement: str


CLAIMS = (
    DesignClaim(
        "guidance",
        "Prefer an explicit dependency when hidden lookup obscures a decision.",
    ),
    DesignClaim(
        "recurrence",
        "A recurring provider mismatch is handled by a stable translation boundary.",
    ),
    DesignClaim("language", "Python callables are stored in a mapping and selected by a key."),
    DesignClaim("runtime", "Reusable host code calls an application hook during request dispatch."),
    DesignClaim("system", "A system note renames one private helper inside a module."),
    DesignClaim(
        "overlap",
        "A framework callback uses a Python callable to select a recurring behaviour.",
    ),
    DesignClaim("unknown", "This design is clean and scalable."),
)


def classify(claim: DesignClaim) -> DesignLevel:
    """Guess from words; this is the behaviour the learner must diagnose and replace."""

    statement = claim.statement.casefold()
    if "system" in statement:
        return DesignLevel.ARCHITECTURE
    if "framework" in statement or "host code" in statement or "calls" in statement:
        return DesignLevel.FRAMEWORK
    if "python" in statement:
        return DesignLevel.IDIOM
    if "recurring" in statement:
        return DesignLevel.PATTERN
    if "prefer" in statement:
        return DesignLevel.PRINCIPLE
    return DesignLevel.UNCLASSIFIED


def build_report(claims: tuple[DesignClaim, ...]) -> tuple[str, ...]:
    """Render one report row per claim without deciding whether the guess is sound."""

    return tuple(f"{claim.name}: {classify(claim).value}" for claim in claims)


def main() -> None:
    """Print the starter guesses for prediction and review."""

    for row in build_report(CLAIMS):
        print(row)


if __name__ == "__main__":
    main()
