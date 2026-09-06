# Visual — practical interface mechanism chooser

Open [interface-mechanism-chooser.html](interface-mechanism-chooser.html) in a browser and select the
four change pressures. The visual is self-contained: it makes no network request and loads no
external font, script, image, or analytics resource.

## How to read this visual

Choose a pressure, then read the runtime, static, and mechanism cards from left to right. Finish at
the two evidence cards. They separate a shape-recognition claim from evidence that an implementation
preserves results, failures, effects, and history.

## Key insight

Choose an interface mechanism for a concrete need: low ceremony, static structural feedback,
nominal family membership, shared implementation, or foreign-boundary translation. A more formal
mechanism is not automatically a stronger behavioral guarantee.

## Simplification or limitation

This is a conceptual decision aid, not Python's runtime object layout or a complete scoring
algorithm. A production boundary may combine mechanisms—for example, an adapter can structurally
satisfy a client-owned `Protocol`. Operational constraints can outweigh the simplified suggestion.

The scenario text is also maintained in [visual_data.py](../examples/visual_data.py), and a test
compares every embedded JSON field with that Python model. This proves semantic synchronization,
not browser rendering, assistive-technology behavior, or correctness for every design context.
