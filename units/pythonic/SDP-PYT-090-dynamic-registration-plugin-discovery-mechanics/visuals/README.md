# Visual — SDP-PYT-090 plugin lifecycle explorer

Open [plugin-lifecycle-explorer.html](plugin-lifecycle-explorer.html) in a browser. Choose a
successful path or failure scenario, then follow the candidate through the stage rail. The page is
self-contained and uses no network resource.

## How to read this visual

Read the selected scenario from top to bottom: metadata candidates and host policy first, then each
stage event, the published registry, and the final outcome. Green stages completed, red stages own a
failure, and a missing later stage means processing stopped or the candidate was quarantined.

## Key insight

A plugin is not one thing moving through one magical loader. Metadata is discovered; an object is
loaded; a provider constructs an offer; the host validates it; a complete set is activated; only
then does request-time invocation begin. Each boundary owns different policy and failure evidence.

## Simplification or limitation

This is a conceptual lifecycle and policy visual, not CPython import internals, a security boundary,
or a deployment topology. The six embedded scenarios are compared with maintained Python
observations by [test_visual_observations.py](../examples/test_visual_observations.py). The visual
omits cancellation, native extensions, subinterpreters, signature verification, process managers,
rolling restarts, and handler-internal work.
