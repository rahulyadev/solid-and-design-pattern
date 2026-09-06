# Visual — SDP-PYT-080 dispatch resolution explorer

Open [dispatch-resolution-explorer.html](dispatch-resolution-explorer.html) in a browser. Choose a
scenario to trace the first argument from runtime type through registered candidates to the selected
handler and observable outcome.

## How to read this visual

Read the active scenario left to right: value → runtime type → candidate path → selected handler →
outcome. The owner line names the generic function whose registry is being consulted. “Competing
imports” is a startup-configuration trace; the other scenarios are request-dispatch traces.

## Key insight

The first argument's runtime type chooses the implementation. Registration configures the generic
function before that choice; later argument values and container item annotations do not become
extra dispatch dimensions.

## Simplification or limitation

The candidate path is a conceptual teaching trace, not CPython's private cache, memory layout, or a
complete rendering of its ABC linearization algorithm. The selected handler and outcomes are checked
against public `dispatch()` behavior by [test_visual_observations.py](../examples/test_visual_observations.py).
The import-order scenario intentionally demonstrates a policy failure; it is not a recommended
plugin loader.
