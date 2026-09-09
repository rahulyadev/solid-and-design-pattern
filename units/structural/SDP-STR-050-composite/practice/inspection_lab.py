"""Unsolved starter: only an item or one flat batch can be inspected."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    label: str
    passed: bool


@dataclass(frozen=True)
class Batch:
    label: str
    checks: tuple[Check, ...]


def all_passed(subject: Check | Batch) -> bool:
    if isinstance(subject, Check):
        return subject.passed
    return all(check.passed for check in subject.checks)


def main() -> None:
    print("empty passes:", all_passed(Batch("empty", ())))
    print("mixed passes:", all_passed(Batch("gate", (Check("seal", True), Check("tag", False)))))
    print("target_complete=False")


if __name__ == "__main__":
    main()
