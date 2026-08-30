"""Composition is explicit here; importing the policy selects no provider."""

import plain_badges
from badge_layouts import JsonBadgeLayout
from badge_policy import BadgeLayout, BadgeRequest, prepare_badge
from callable_choices import NamePrefix, make_prefix, plain_name, render_names
from owned_layouts import StaffBadgeLayout, VisitorBadgeLayout


def main() -> None:
    names = ("Asha", "Mina", "Asha")
    print("function:", render_names(names, plain_name))
    print("closure:", render_names(names, make_prefix("Guest: ")))
    print("callable object:", render_names(names, NamePrefix("Guest: ")))

    request = BadgeRequest("Asha", "Open Lab")
    layouts: tuple[tuple[str, BadgeLayout], ...] = (
        ("module", plain_badges),
        ("configured object", JsonBadgeLayout()),
        ("owned ABC / staff", StaffBadgeLayout()),
        ("owned ABC / visitor", VisitorBadgeLayout()),
    )
    for label, layout in layouts:
        document = prepare_badge(request, layout)
        print(f"{label} [{document.content_type}]: {document.body!r}")


if __name__ == "__main__":
    main()
