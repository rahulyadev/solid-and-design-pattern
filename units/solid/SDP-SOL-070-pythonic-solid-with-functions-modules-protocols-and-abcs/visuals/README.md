# Visuals — SDP-SOL-070

[Unit note](../README.md) · [Interactive comparison](mechanism-chooser.html)

The comparison is self-contained and works offline in a browser. It uses original HTML,
CSS, and JavaScript; no remote scripts, fonts, analytics, or API calls are required.

## How to read this visual

Choose one concrete change pressure. Follow the caller to its supplied operation.
On narrow screens the flow stacks from top to bottom. Read the contract, why the shape
fits, its smaller alternative, and the remaining risk. The text under the flow provides
the relationship without relying on arrows or colour.

## Key insight

A function, closure, callable instance, module, Protocol, and ABC solve different needs.
The named Protocol can accept independent objects or modules. The ABC is an optional
implementation family, not a condition imposed on every provider.

## Simplification or limitation

The arrows represent conceptual call flow. They are not source imports, subclass arrows,
timing, network requests, or CPython memory layout. The result text is fixed illustration
of runnable examples, not live Python execution or a benchmark. Cases are alternatives,
not a universal decision algorithm or increasing levels of design quality.

The [unit note](../README.md#6-collaboration-and-execution-flow) separately shows actual
source imports and the condensed runtime flow. Both diagrams include their own reading
directions and limitations.
