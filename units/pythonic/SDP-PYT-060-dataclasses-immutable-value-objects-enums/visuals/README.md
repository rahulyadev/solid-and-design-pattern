# Visual — value boundary and immutable replacement

Open [value-object-boundary.html](value-object-boundary.html) in a browser and select the three
stages. The visual is self-contained: it makes no network request and loads no external font,
script, image, or analytics resource.

## How to read this visual

Start with the raw boundary record, move to the validated value graph, then move to the replacement
snapshot. Within each stage, read the cards left to right. The arrow label names the operation that
must cross the boundary.

## Key insight

The useful boundary is not “dictionary versus class.” It is untrusted, open-ended data versus a
validated graph whose states and mutation policy are explicit. A transition produces a new snapshot
rather than changing the old one invisibly.

## Simplification or limitation

This is a conceptual value-flow model, not CPython object layout, a database transaction diagram,
or a guarantee of deep immutability. The example uses tuples and frozen value fields, but the visual
omits persistence races, schema versioning, object allocation, garbage collection, and enum
deployment compatibility.

The stage text is also maintained in
[visual_data.py](../examples/visual_data.py), and a test compares all embedded JSON with that Python
model. That proves semantic synchronization, not browser rendering or accessibility conformance.
