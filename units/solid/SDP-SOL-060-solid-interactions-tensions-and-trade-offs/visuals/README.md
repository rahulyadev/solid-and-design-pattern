# Visual guide — SDP-SOL-060

Open [the interactive trade-off map](trade-off-map.html) in a browser. It is a standalone,
offline teaching asset with no external libraries, analytics, network calls, or saved state.
GitHub displays its source rather than running it; open a local copy for interaction.

## How to read this visual

Choose one change pressure. Compare the current design with the smallest proposed response.
Read each row left to right on a wide screen, top to bottom on a phone. Arrows describe
conceptual collaboration, not imports or inheritance. Then read the promise, proposed change,
and cost below the map.

The five states cover a stable function, recurring formats, a semantically incompatible
replacement, a split invariant, and speculative framework machinery. The tinted middle
node locates the responsibility being considered; the labels carry meaning without colour.

## Key insight

More interfaces do not guarantee better isolation, correct behaviour, or safer state changes.
The useful boundary depends on the actual pressure and the promises the caller needs.

## Simplification or limitation

These are authored comparisons, not measured quality scores, an automatic design advisor,
or executed Python traces. The [shape experiment](../experiments/EXP-01-compatible-shape/README.md)
and [split-operation experiment](../experiments/EXP-02-split-operation/README.md) establish the
bounded observations described in their own run records. The split-operation visual does
not promise thread safety or distributed correctness.

The note also contains a compact notebook sketch and a call-sequence diagram, each with
its own reading directions and limits. No image-generation model or copied diagram is used.

## Local preview

From the repository root:

```bash
python -m http.server 8766 --bind 127.0.0.1
```

Open the [local visual](http://127.0.0.1:8766/units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/visuals/trade-off-map.html).
Stop the server after use. It binds only to the local machine. The HTML also works when opened
directly, though Markdown links may be downloaded or shown as text depending on the browser.

## Accessibility and fallback

The selector has a visible label and native keyboard behaviour. A polite live region names
the selected scenario. Rows stack on small screens, colours follow system appearance, and
all essential meaning is present as text. No animation or hover-only interaction is required.
With JavaScript disabled, the default format comparison and navigation remain visible.

Browser verification is recorded in the final maintainer validation record. It is not a full
screen-reader, accessibility, or cross-browser certification.
