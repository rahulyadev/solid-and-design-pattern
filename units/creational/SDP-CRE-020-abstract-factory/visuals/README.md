# Visual — SDP-CRE-020 product-family decision explorer

Open [product-family-explorer.html](product-family-explorer.html) in a browser. Choose a scenario
with the buttons or arrow keys and follow the five numbered lanes from selection to verdict.

## How to read it

1. **Pressure** says what must vary.
2. **Selection** shows who makes the family choice.
3. **Products** lists what that choice supplies.
4. **Coherence gate** states the compatibility invariant and failure point.
5. **Verdict** names the smallest justified design.

Arrows mean “passes control or products to,” not class inheritance. Red styling means the family
invariant is broken; amber means a simpler or adjacent design should be considered.

## Key insight

Several factory-shaped methods do not make an Abstract Factory. One decision must create related
product roles whose compatibility matters to the client.

## Simplification or limitation

The explorer is a maintained decision model, not an object diagram, benchmark, or runtime trace.
It omits constructor arguments, asynchronous cancellation, cleanup failures, distributed rollout,
and business-domain behavior. The executable example and lifetime experiment cover some of those
omissions separately.

## Source contract

The eight embedded scenarios are mirrored in
[`examples/visual_data.py`](../examples/visual_data.py). Tests compare every maintained field,
scenario order, accessibility target, keyboard hook, and structural marker so prose and the visual
cannot silently drift.
