"""Observe class and instance creation without presenting a metaclass recipe."""

from __future__ import annotations

from class_hooks import EVENTS, AuditedJob


def observe_creation() -> list[str]:
    existing = [f"{event.stage}:{event.target}:{event.detail}" for event in EVENTS]
    job = AuditedJob("nightly")
    created = [f"{event.stage}:{event.target}:{event.detail}" for event in EVENTS]
    return [*existing, *created[len(existing) :], f"result:{job.describe()}"]


def main() -> None:
    for item in observe_creation():
        print(item)


if __name__ == "__main__":
    main()
