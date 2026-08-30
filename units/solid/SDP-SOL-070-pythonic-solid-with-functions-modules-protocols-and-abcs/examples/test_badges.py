import json
from collections.abc import Callable

import plain_badges
import pytest
from badge_layouts import JsonBadgeLayout
from badge_policy import BadgeDocument, BadgeLayout, BadgeRequest, prepare_badge
from callable_choices import NamePrefix, make_prefix, plain_name, render_names
from owned_layouts import StaffBadgeLayout, VisitorBadgeLayout


@pytest.mark.parametrize("renderer", [make_prefix("Guest: "), NamePrefix("Guest: ")])
def test_configured_callables_keep_order_and_duplicates(renderer: Callable[[str], str]) -> None:
    names = iter(("Mina", "Asha", "Mina"))
    assert render_names(names, renderer) == ("Guest: Mina", "Guest: Asha", "Guest: Mina")


def test_plain_function_and_empty_input() -> None:
    assert render_names(("Asha", "Mina"), plain_name) == ("Asha", "Mina")
    assert render_names((), plain_name) == ()


def test_closure_configuration_is_per_factory_call() -> None:
    guest = make_prefix("Guest: ")
    staff = make_prefix("Staff: ")
    assert (guest("Asha"), staff("Asha"), guest("Mina")) == (
        "Guest: Asha",
        "Staff: Asha",
        "Guest: Mina",
    )


def test_callable_failure_remains_visible() -> None:
    def unavailable(name: str) -> str:
        raise LookupError(name)

    with pytest.raises(LookupError, match="Asha"):
        render_names(("Asha",), unavailable)


@pytest.mark.parametrize(
    ("attendee", "event"),
    [("Asha", "Open Lab"), ("  Mina  ", "Evening"), ('Zoë "Z"', "研究会")],
)
def test_module_preserves_legacy_text(attendee: str, event: str) -> None:
    layout: BadgeLayout = plain_badges
    request = BadgeRequest(attendee, event)
    assert prepare_badge(request, layout) == BadgeDocument(
        "text/plain; charset=utf-8", f"{event}\n{attendee}"
    )
    assert request == BadgeRequest(attendee, event)


@pytest.mark.parametrize("indent", [None, 0, 2])
def test_json_keeps_values_and_advertises_the_matching_representation(indent: int | None) -> None:
    request = BadgeRequest('Zoë "Z"\nSecond line', "研究会")
    document = prepare_badge(request, JsonBadgeLayout(indent))
    assert document.content_type == "application/json"
    assert json.loads(document.body) == {"event": request.event, "attendee": request.attendee}


def test_negative_indent_is_rejected() -> None:
    with pytest.raises(ValueError, match="indent"):
        JsonBadgeLayout(-1)


@pytest.mark.parametrize(
    ("layout", "label"),
    [(StaffBadgeLayout(), "STAFF"), (VisitorBadgeLayout(), "VISITOR")],
)
def test_owned_family_shares_framing_without_changing_policy(
    layout: BadgeLayout, label: str
) -> None:
    assert prepare_badge(BadgeRequest("Asha", "Open Lab"), layout) == BadgeDocument(
        "text/plain; charset=utf-8", f"[Open Lab]\n{label}: Asha"
    )


class FailingLayout:
    content_type = "text/plain"

    def render(self, attendee: str, /, *, event: str) -> str:
        raise RuntimeError("layout unavailable")


@pytest.mark.parametrize(("attendee", "event"), [("", "Open Lab"), (" \t", "X"), ("Asha", "\n")])
def test_invalid_request_fails_before_rendering(attendee: str, event: str) -> None:
    with pytest.raises(ValueError, match="nonblank"):
        prepare_badge(BadgeRequest(attendee, event), FailingLayout())


def test_layout_failure_is_not_a_success_document() -> None:
    with pytest.raises(RuntimeError, match="layout unavailable"):
        prepare_badge(BadgeRequest("Asha", "Open Lab"), FailingLayout())


def test_blank_metadata_fails_before_rendering() -> None:
    layout = FailingLayout()
    layout.content_type = " "
    with pytest.raises(ValueError, match="content type"):
        prepare_badge(BadgeRequest("Asha", "Open Lab"), layout)


def test_blank_output_is_rejected() -> None:
    class BlankLayout:
        content_type = "text/plain"

        def render(self, attendee: str, /, *, event: str) -> str:
            return "\n"

    with pytest.raises(ValueError, match="body"):
        prepare_badge(BadgeRequest("Asha", "Open Lab"), BlankLayout())
