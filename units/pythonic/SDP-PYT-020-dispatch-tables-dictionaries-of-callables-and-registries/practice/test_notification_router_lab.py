"""Phase-A characterization tests; these do not reveal the target refactoring."""

from collections.abc import Iterator

import pytest
from notification_router_lab import Notification, route_notifications


@pytest.mark.parametrize(
    ("channel", "expected"),
    [
        ("email", ("email:r@example.test:hello",)),
        ("sms", ("sms:r@example.test:hello",)),
    ],
)
def test_known_channels_keep_their_exact_receipt_shape(
    channel: str, expected: tuple[str, ...]
) -> None:
    assert route_notifications([Notification("r@example.test", "hello")], channel) == expected


@pytest.mark.parametrize("channel", ["push", "EMAIL", " email", "email ", ""])
def test_unknown_channel_is_exact_and_not_normalized(channel: str) -> None:
    with pytest.raises(ValueError, match=f"unsupported channel: {channel}"):
        route_notifications([], channel)


def test_unknown_channel_is_rejected_before_consuming_input() -> None:
    consumed: list[str] = []

    def source() -> Iterator[Notification]:
        consumed.append("started")
        yield Notification("r@example.test", "hello")

    with pytest.raises(ValueError, match="unsupported channel: push"):
        route_notifications(source(), "push")
    assert consumed == []


@pytest.mark.parametrize("channel", ["email", "sms"])
def test_empty_known_channel_returns_an_empty_tuple(channel: str) -> None:
    assert route_notifications([], channel) == ()


def test_order_duplicates_blank_text_and_unicode_are_preserved() -> None:
    notifications = [
        Notification("एक@example.test", ""),
        Notification("dup@example.test", "hello | world"),
        Notification("dup@example.test", "hello | world"),
    ]
    assert route_notifications(notifications, "email") == (
        "email:एक@example.test:",
        "email:dup@example.test:hello | world",
        "email:dup@example.test:hello | world",
    )
    assert notifications == [
        Notification("एक@example.test", ""),
        Notification("dup@example.test", "hello | world"),
        Notification("dup@example.test", "hello | world"),
    ]


def test_one_pass_input_is_supported() -> None:
    source = iter(
        [
            Notification("first@example.test", "one"),
            Notification("second@example.test", "two"),
        ]
    )
    assert route_notifications(source, "sms") == (
        "sms:first@example.test:one",
        "sms:second@example.test:two",
    )
    assert tuple(source) == ()
