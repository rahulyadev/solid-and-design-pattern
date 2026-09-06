# Visual — SDP-PYT-100 mechanism decision explorer

Open [mechanism-decision-explorer.html](mechanism-decision-explorer.html) in a browser. Select a
change-pressure scenario, read the smallest fitting mechanism, and then inspect the next-more-
powerful mechanism that was deliberately rejected.

## How to read this visual

Read left to right. The scenario supplies a concrete force. The center card identifies when the
chosen mechanism runs and why it is sufficient. The right card shows the extra power and risk being
avoided. The vertical ladder is ordered by increasing implicitness and class-wide reach; it is a
decision aid, not a mandatory migration path.

## Key insight

Descriptors, subclass hooks, class decorators, and metaclasses are not interchangeable levels of
cleverness. Each intercepts a different event. Choose the least powerful event boundary that
matches the real change.

## Simplification or limitation

This is a conceptual mechanism chooser, not literal CPython control flow, a performance model, or a
framework recommendation. The eight embedded scenarios are compared with maintained Python data by
[test_visual_observations.py](../examples/test_visual_observations.py). The visual omits concurrency,
plugin discovery, annotation resolution, exotic metaclass callables, and framework-specific
contracts.
