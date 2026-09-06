"""Keep the public worked demo deterministic."""

from __future__ import annotations

from run_mechanism_demo import main


def test_demo_reports_the_bounded_decision(capsys: object) -> None:
    main()
    output = capsys.readouterr().out.splitlines()  # type: ignore[attr-defined]

    assert output == [
        "endpoint=catalog:8080",
        "health=/ready@30s",
        "rule=standard; schema=1; quote=600",
        "decision=descriptor earned; subclass hook bounded; metaclass rejected",
    ]
