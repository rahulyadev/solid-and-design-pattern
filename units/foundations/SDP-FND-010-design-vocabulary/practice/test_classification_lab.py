"""Harness checks for the unsolved SDP-FND-010 starter."""

from classification_lab import CLAIMS, DesignClaim, DesignLevel, build_report, classify


def test_report_preserves_each_claim_exactly_once() -> None:
    report = build_report(CLAIMS)

    assert len(report) == len(CLAIMS)
    assert {row.partition(":")[0] for row in report} == {claim.name for claim in CLAIMS}


def test_starter_can_render_every_available_label() -> None:
    report = build_report(CLAIMS)

    for level in DesignLevel:
        assert any(row.endswith(level.value) for row in report)


def test_unknown_wording_is_not_forced_into_a_known_level() -> None:
    claim = DesignClaim("unknown", "This design is clean and scalable.")

    assert classify(claim) is DesignLevel.UNCLASSIFIED
