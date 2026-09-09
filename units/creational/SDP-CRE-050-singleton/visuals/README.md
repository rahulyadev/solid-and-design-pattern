# Identity explorer — SDP-CRE-050

Open [identity-explorer.html](identity-explorer.html) in a permitted browser, or use the equivalent
[experiment table](../experiments/EXP-01-identity-and-lifetime/README.md). There are no external
assets, network requests, tracking scripts, or user data. Keyboard selection updates the graph,
count label, accessible description, and observation detail.

## How to read this visual

Select one of five measured scenarios. Left boxes represent successful access calls, or application
owners in the two-app scenario. Arrows point to returned objects. One right-hand box means shared
identity; two boxes mean distinct objects. The count label states allocations, factory calls,
factory attempts, or reader acquisitions as appropriate. The retry's failed call returns no object
and therefore has no object arrow.

## Key insight

Sameness alone does not prove once-only initialization, safe publication, or correct lifetime.
The two-app case deliberately uses two resources, with sharing inside each application.

## Simplification or limitation

The graph is conceptual and static per selected observation. It is neither Python memory layout
nor a simulation of every thread schedule. The counts are small controlled experiment results,
not performance measurements. Resource use and shutdown races are outside the diagram.

Contract tests compare every embedded data field to actual Python observations and check semantic
controls, element references, reading guidance, and script structure. Node syntax checks are separate
from browser rendering. The rendering status is recorded in [VALIDATION.md](../VALIDATION.md);
a blocked local URL must not be bypassed with a server, another browser, or indirect execution.
