"""Unsolved SDP-CRE-020 predict-run-refactor practice baseline.

Keep this file unchanged as the original attempt, or copy it before refactoring.
The current conditional works; the family boundary remains for the learner.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol


class UnknownNotificationFamilyError(LookupError):
    """The baseline has no renderer/sender pair for the configured name."""


class IncompatibleNotificationProductError(RuntimeError):
    """A sender received content rendered for another family."""


@dataclass(frozen=True, slots=True)
class Notice:
    notice_id: str
    body: str

    def __post_init__(self) -> None:
        if not self.notice_id or not self.notice_id.isascii() or "|" in self.notice_id:
            raise ValueError("notice_id must be nonblank ASCII without '|'")
        if not self.body:
            raise ValueError("body must be nonblank")


@dataclass(frozen=True, slots=True)
class RenderedNotice:
    content_type: str
    body: bytes


@dataclass(frozen=True, slots=True)
class DeliveryReceipt:
    receipt_id: str
    accepted: bool


class NoticeRenderer(Protocol):
    def render(self, notice: Notice) -> RenderedNotice: ...


class NoticeSender(Protocol):
    def send(self, rendered: RenderedNotice) -> DeliveryReceipt: ...


@dataclass(frozen=True, slots=True)
class InternalRenderer:
    def render(self, notice: Notice) -> RenderedNotice:
        body = f"{notice.notice_id}|{notice.body}".encode()
        return RenderedNotice("text/x-internal-notice", body)


@dataclass(slots=True)
class InternalSender:
    output: list[bytes]

    def send(self, rendered: RenderedNotice) -> DeliveryReceipt:
        if rendered.content_type != "text/x-internal-notice":
            raise IncompatibleNotificationProductError("internal sender content type mismatch")
        self.output.append(rendered.body)
        notice_id, _separator, _body = rendered.body.partition(b"|")
        return DeliveryReceipt(f"internal:{notice_id.decode('ascii')}", True)


@dataclass(frozen=True, slots=True)
class PartnerRenderer:
    def render(self, notice: Notice) -> RenderedNotice:
        body = json.dumps(
            {"body": notice.body, "id": notice.notice_id},
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return RenderedNotice("application/vnd.partner.notice+json;v=1", body)


@dataclass(slots=True)
class PartnerSender:
    output: list[bytes]

    def send(self, rendered: RenderedNotice) -> DeliveryReceipt:
        if rendered.content_type != "application/vnd.partner.notice+json;v=1":
            raise IncompatibleNotificationProductError("partner sender content type mismatch")
        self.output.append(rendered.body)
        notice_id = str(json.loads(rendered.body)["id"])
        return DeliveryReceipt(f"partner:{notice_id}", True)


def prepare_delivery(
    family_name: str,
    output: list[bytes],
) -> tuple[NoticeRenderer, NoticeSender]:
    """Working selection baseline that policy code still calls directly."""

    if family_name == "internal":
        return InternalRenderer(), InternalSender(output)
    if family_name == "partner-v1":
        return PartnerRenderer(), PartnerSender(output)
    raise UnknownNotificationFamilyError(f"unknown notification family: {family_name!r}")


def publish_notice(notice: Notice, family_name: str, output: list[bytes]) -> DeliveryReceipt:
    """Stable desired workflow: render once, send once, return the receipt."""

    renderer, sender = prepare_delivery(family_name, output)
    return sender.send(renderer.render(notice))


TARGET_REFACTOR_COMPLETE = False


def main() -> None:
    output: list[bytes] = []
    receipt = publish_notice(Notice("NOTICE-7", "backup complete"), "internal", output)
    print(f"receipt={receipt.receipt_id}; writes={len(output)}")
    print(f"target_complete={TARGET_REFACTOR_COMPLETE}")


if __name__ == "__main__":
    main()
