"""Run controlled mypy cases for implicit structural Protocol compatibility."""

from __future__ import annotations

import re
import subprocess
import sys
from textwrap import dedent

VALID_SOURCE = dedent(
    """
    from typing import Protocol

    class SendsText(Protocol):
        def send(self, message: str) -> str: ...

    class UnrelatedButCompatible:
        def send(self, message: str) -> str:
            return f"ok:{len(message)}"

    def notify(sender: SendsText) -> str:
        return sender.send("alert")

    result: str = notify(UnrelatedButCompatible())
    """
).strip()

INVALID_SOURCE = dedent(
    """
    from typing import Protocol

    class SendsText(Protocol):
        def send(self, message: str) -> str: ...

    class WrongSignature:
        def send(self) -> int:
            return 7

    def notify(sender: SendsText) -> str:
        return sender.send("alert")

    result: str = notify(WrongSignature())
    """
).strip()


def check_source(source: str) -> tuple[int, int, str]:
    """Type-check one isolated source and summarize stable evidence."""

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--strict",
            "--no-incremental",
            "--no-error-summary",
            "--show-error-codes",
            "-c",
            source,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    error_count = sum("error:" in line for line in completed.stdout.splitlines())
    codes = sorted(set(re.findall(r"\[([a-z-]+)\]", completed.stdout)))
    return completed.returncode, error_count, ",".join(codes) or "-"


def main() -> None:
    """Show that static compatibility considers signatures, not inheritance."""

    for label, source in (("compatible", VALID_SOURCE), ("wrong_signature", INVALID_SOURCE)):
        returncode, error_count, codes = check_source(source)
        print(f"{label}: returncode={returncode} errors={error_count} codes={codes}")


if __name__ == "__main__":
    main()
