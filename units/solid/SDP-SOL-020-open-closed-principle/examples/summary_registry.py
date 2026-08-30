"""Optional name selection, separate from rendering and publication."""

from collections.abc import Iterable, Mapping
from types import MappingProxyType

from summary_core import Renderer


class UnknownRenderer(LookupError):
    """The configured renderer name is not present."""


def build_renderers(entries: Iterable[tuple[str, Renderer]]) -> Mapping[str, Renderer]:
    """Reject ambiguous registration, then expose a private mapping through a read-only view."""
    renderers: dict[str, Renderer] = {}
    for name, render in entries:
        if not name or name != name.strip():
            raise ValueError("renderer names must be nonblank with no surrounding whitespace")
        if name in renderers:
            raise ValueError(f"duplicate renderer: {name}")
        renderers[name] = render
    return MappingProxyType(renderers)


def select_renderer(name: str, renderers: Mapping[str, Renderer]) -> Renderer:
    """Translate a missing name only; renderer execution happens outside this handler."""
    try:
        return renderers[name]
    except KeyError:
        raise UnknownRenderer(f"unsupported renderer: {name}") from None
