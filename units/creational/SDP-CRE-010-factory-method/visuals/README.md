# Visual — SDP-CRE-010 construction decision explorer

Open [construction-decision-explorer.html](construction-decision-explorer.html) in a browser. Choose
a change-pressure scenario, then compare the smallest construction boundary with the mechanism it
deliberately rejects.

## How to read this visual

Read from the selected scenario to **Pressure**, then across **Smallest decision**, **Boundary**, and
**Rejected next move**. The vertical ladder orders common options by increasing indirection; it is
a reasoning aid, not a mandatory refactoring path.

## Key insight

Factory Method is one specific point on a wider construction-decision ladder. A stable workflow
plus meaningful Creator subclasses may earn it; ordinary Python code often stops earlier at a
function or injected callable.

## Simplification or limitation

This is a conceptual design chooser, not a literal runtime object graph, benchmark, or universal
ranking. The embedded scenarios are checked against maintained Python data by
[test_visual_observations.py](../examples/test_visual_observations.py). It omits framework-specific
containers, asynchronous cleanup, provider trust, and distributed configuration rollout.
