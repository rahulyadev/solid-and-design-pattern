# Visuals — SDP-SOL-040 Interface Segregation Principle

[Unit note](../README.md) · [Interactive capability map](capability-map.html)

Open the HTML file in a browser; it is self-contained and makes no network requests.
The controls compare four clients, two parameter contracts, and three providers from the
[archive example](../examples/archive_roles.py). It does not run Python in the browser.

## How to read this visual

Read the client, required contract, and actual provider from left to right, or top to bottom
on a narrow screen. The table distinguishes operations called from operations required.

1. Keep Preview and Published bundle selected. The shared manager requires unused operations.
2. Switch only the parameter contract to Client capability. The same provider now fits.
3. Select Duplicate. Its real read-and-write requirement still rejects a reading-only bundle.
4. Select Full memory archive. One object can support all four roles.

## Key insight

Narrowing a dependency can remove irrelevant obligations without splitting or wrapping the
provider. Several operations may form one useful capability.

## Simplification or limitation

This is a conceptual structural-typing model. It assumes the compatible signatures in the
example and models only read, write, and remove. An accepted shape is not proof of behaviour.
Receipt inspection and other extra provider members are outside the diagram. No permission,
resource ownership, data copying, transaction, or concurrency guarantee follows from a type.

The client call path does not change when only the annotation changes. The separate
[dependency experiment](../experiments/EXP-01-client-dependency/README.md) checks that claim
with actual Python and mypy. The diagram arrows are dependency relationships, not objects
allocated by Protocol or a literal runtime call stack.

## Static companion

| Client | read | write | remove |
|---|---|---|---|
| Preview | Required | — | — |
| Report upload | — | Required | — |
| Cleanup | — | — | Required |
| Duplicate within one archive | Required | Required | — |

Read each row as one client's contract. The key insight is that the Duplicate row legitimately
has two requirements. The limitation is that this matrix cannot express their same-archive
relationship or failure semantics; those belong in the written contract and tests.
