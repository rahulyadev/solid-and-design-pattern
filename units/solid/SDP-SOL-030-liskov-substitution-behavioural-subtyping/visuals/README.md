# Visual guide — SDP-SOL-030

Open [the contract explorer](contract-explorer.html) in a browser. It is a self-contained,
offline teaching visual; the [unit note](../README.md) and Python examples remain canonical.
No external fonts, scripts, services, tracking, or real user data are used.

## How to read this visual

Select a provider and use **Next call** or **Previous call** to replay five ordered lookups.
Read the client call, the actual versus expected outcome, then the remaining entries. The
history row marks each observed call; a prior violation stays visible even if a later call
happens to match. Selecting another provider restarts with the same initial catalog.

## Key insight

The same method signature can conceal an input restriction, wrong absence result, unexpected
exception, or destructive read. In the consuming case, the returned string can look correct
while the promise about future reads has already been broken.

## Simplification or limitation

This is an original, scripted conceptual model of the supplied Python providers, not a Python
interpreter or CPython memory diagram. The state panel exposes entries for teaching; the
actual client has only `lookup`, so a later read establishes the observable failure. Five
traces are witnesses, not exhaustive proof. No concurrency, latency, or backend I/O is modeled.

The layout supports narrow screens, native select/buttons, text-labelled outcomes, system
light/dark appearance, and a polite announcement of the current verdict. No animation is needed.

## Notebook reconstruction

Draw one valid client call, a box for the replacement, and three observations: return value,
error, and state available to the next call. Reconstruct one violation without copying the
screen. The separate alias-history visual is in the [second experiment](../experiments/EXP-02-history-through-aliases/README.md#visual-interpretation).
