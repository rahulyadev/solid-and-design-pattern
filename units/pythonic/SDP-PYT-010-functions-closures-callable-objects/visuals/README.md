# Visuals — SDP-PYT-010

[Unit note](../README.md) · [Callable state explorer](callable-state.html)

Open the HTML file in a browser. It is self-contained, works offline, and makes no external
requests. GitHub may display its source rather than execute it; open the local file instead.

## How to read this visual

In **Mutation and rebinding**, move through Create → Mutate → Rebind. The top shows the
outer name and the original list reference. Each row traces what a callable retains and
shows the tuple it returns after that operation. A shaded result changed since the preceding
step. Predict the change before selecting a step.

Then select **Callbacks created in a loop**. The three readers are constructed with settings
2, 5, and 8 and called only after the loop ends. Compare one shared binding with separate
default arguments and separate factory-call bindings. Results are shown in creation order.

## Key insight

Changing an object differs from rebinding a name. Retaining a reference does not copy a
value, and allocating several function objects does not require separate enclosing bindings.

## Simplification or limitation

The displayed observations come from [binding_probe.py](../examples/binding_probe.py),
not a Python interpreter in the browser. List A and List B are conceptual object labels,
not addresses or a CPython layout. Selecting a step displays a recorded observation;
selecting steps out of order does not execute a different experiment.

The probe returns tuples and converts them to JSON arrays for storage. The first view
reconstructs tuple notation; the loop view displays a list of individual integer results.
The snapshot contains integers only, not nested mutable objects. Defaults can be explicitly
overridden by arguments, which this fixed experiment does not exercise. No scheduling,
garbage collection, thread safety, security boundary, or performance is simulated.

## Reproduce and verify

Use the [experiment's command and environment](../experiments/EXP-01-binding-and-aliases/README.md).
Its JSON must equal the HTML's `observations` data block. The maintainer checked this against
actual Python output; see [VALIDATION.md](../VALIDATION.md) for the recorded verification.

The complete numerical observations and textual interpretation remain available in the
experiment note if the interactive view is unavailable. This visual contains no lab solution.
