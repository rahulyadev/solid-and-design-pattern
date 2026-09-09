# Follow the references — SDP-CRE-040

Open [the self-contained explorer](copy-graph-explorer.html) in a browser that permits the local
artifact. It contains no network dependencies. It compares assignment, shallow copy, deep copy,
dataclass replacement, and independent deep copying of each child. A toggle appends one tag through
result edge 0 so you can see the effect on the source and the second child.

## How to read this visual

R and C identify original root/child objects; primes identify copied ones. Both original root edges
reach C, and C has a back edge to R. Follow the labeled edges before toggling the mutation. Identical
node names mean the same conceptual object. Distinct names mean distinct objects. Color is not
required to understand identity.

## Key insight

A fresh root is insufficient for isolation. Deep copying the whole graph preserves its internal
aliases; separate child traversals create different subgraphs and change that collaboration.

## Simplification or limitation

The visual embeds observations from the Python probe; it does not execute Python. List containers
are collapsed into edges, and split-copy subgraphs are represented by named hidden roots. It is not
CPython memory layout, a performance measurement, an authorization check, or a concurrent snapshot.
Native controls support keyboard access, a live region announces changes, and CSS stacks the two
graphs on narrow screens. Those features have static checks; they are not evidence of browser QA.

The in-app browser rejected the direct local `file:` URL under URL security policy during authoring.
No alternate browser, local server, indirect navigation, or other workaround was attempted. Actual
rendering, layout, and assistive-technology behavior remain unverified here. Static contracts and
JavaScript syntax are recorded separately in [validation](../VALIDATION.md).

The [Python experiment](../experiments/EXP-01-copy-graph/README.md) defines the observations. Its tests
compare every embedded field, scenario order, control option, and required structural feature.
