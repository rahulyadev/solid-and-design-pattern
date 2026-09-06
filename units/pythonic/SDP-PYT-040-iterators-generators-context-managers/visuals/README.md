# Visual — SDP-PYT-040 protocol lifecycle explorer

Open [protocol-lifecycle.html](protocol-lifecycle.html) in a browser. It is a self-contained,
responsive visual with no external script, font, analytics, network call, or production data.

## How to read this visual

Start with the left panel. Move from creation to first request, exhaustion, and a second pass; then
contrast that one-shot generator with the container state. In the right panel, compare normal
exit, a propagating body exception, selective suppression, and failed entry. Follow the numbered
boxes before reading the exact observation under each flow.

The colors mean:

- teal: a requested or completed step;
- amber: the current suspension point or body;
- plum: exhaustion, exit policy, or cleanup.

## Key insight

The iteration protocol standardizes request-driven traversal. The context management protocol
standardizes entry and exit around a block. They remove much handwritten pattern machinery, but
they solve different lifecycle questions.

## Simplification or limitation

This is a conceptual synchronous view, not literal stack frames, bytecode, object layout, garbage
collection, async scheduling, or a transactional guarantee. The embedded JSON contains fixed
observations from tested Python probes; the page itself does not execute Python. Tests compare the
entire JSON block with those probes.

## Controls and accessibility

Every scenario is a native button with a visible focus state and `aria-pressed`. The page supports
light and dark appearance, narrow viewports, and reduced-motion preferences. Meaning is repeated
in text rather than encoded only by color.
