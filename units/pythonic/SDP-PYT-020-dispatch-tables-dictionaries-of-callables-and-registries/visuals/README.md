# Visuals — SDP-PYT-020

[Unit note](../README.md) · [Dispatch boundary explorer](dispatch-boundary.html)

Open the HTML file in a browser. It is self-contained, works offline, and makes no external
requests. GitHub may display the source rather than execute it; open the local file instead.

## How to read this visual

Begin with **Known key** and follow request → lookup → selected handler → outcome. Then compare
**Unknown key** with **Handler raises `KeyError`**. The red boundary around lookup marks the only
operation whose `KeyError` is translated to `UnknownEventType`.

In **Registry lifecycle**, advance through Empty → Register → Seal → After seal. The registered
names appear in insertion order. Publication locks the name bindings; it does not freeze state
inside a stored callable.

## Key insight

Selection and execution are separate events. A registry adds policies around the mapping—who may
register, when publication happens, how duplicates and misses behave—not a new way to call a
function.

## Simplification or limitation

The flow is conceptual and driven by fixed observations from
[dispatch_tools.py](../examples/dispatch_tools.py); it does not execute Python in the browser.
Arrows are call and selection relationships, not CPython object layout. The lifecycle view omits
threads, processes, plugin discovery, external effects, retries, and handler resource lifetimes.

## Reproduce and verify

Use the [practice environment and commands](../practice/README.md#commands). A test compares the
HTML's complete data block with `visual_observations()` from Python. Maintainer execution and
visual checks are recorded in [VALIDATION.md](../VALIDATION.md).

The full observations remain readable in the unit and experiment notes if interactive HTML is not
available. The visual contains no practice solution.
