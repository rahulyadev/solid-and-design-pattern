# Practice — SDP-PYT-060 dataclasses, immutable value objects, and enums

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-060](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-pyt-060) |
| Evidence target | `E+I+D+T` |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-060-dataclasses-immutable-value-objects-enums/practice` |
| Status | Not attempted |

## Learning question

Can you turn a mutable, stringly typed shipment record into validated values and immutable snapshots
without breaking its wire format or smuggling mutation through nested containers?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Complete the stages in order. The starter tests pass because they characterize the legacy behavior;
green does not mean the target design already exists.

## Starter files

- [shipment_lab.py](shipment_lab.py) is a runnable legacy model with public mutation and string
  states.
- [test_shipment_lab.py](test_shipment_lab.py) records its current observable contract.

The worked pricing example uses another synthetic domain. This directory contains no target
implementation, comparison solution, hidden fixture, released hint, learner attempt, or fabricated
evidence.

## Problem and change pressure

`ShipmentDraft` began as a small request-shaped bag of fields. `apply_scan(...)` mutates that object
in place, accepts a status string, appends to a public list, and returns the same identity.

Now shipment snapshots will cross an event boundary and live in caches. Callers need to compare two
snapshots by value, reject unknown states before business logic, use a snapshot safely as a mapping
key when justified, and retain an old revision while calculating a new revision. The JSON-like wire
record must stay exactly as documented.

All shipments, identifiers, checkpoints, and events are synthetic. The starter performs no network,
database, filesystem, framework, or clock access.

## Legacy observable contract

| Dimension | Required observation |
|---|---|
| Record keys | `tracking_id`, `status`, `checkpoints`, and `revision`. |
| Initial values | Status `created`, empty checkpoints, revision `1`. |
| Valid scan | Append exactly one checkpoint, set the supplied known status, increment once. |
| Text | Preserve Unicode, colons, and literal pipes; reject empty or surrounding whitespace. |
| Unknown state | Raise `ValueError` before mutation. |
| Terminal state | A delivered shipment rejects every later scan without partial mutation. |
| Serialization | Returned record has its own checkpoint list. |
| Current identity | The legacy function returns the same object; the target may deliberately change this. |

The last row is an observed smell, not a permanent requirement. If the refactoring returns a new
snapshot, update that assertion only after explaining the API change and preserving the old value.

## Predict before running

Without executing the code, record:

1. Which object identity changes after `apply_scan(...)`?
2. Which aliases observe the mutation?
3. Does `@dataclass` validate the `status: str` annotation at runtime?
4. Why do two new drafts not share the default checkpoint list?
5. Could the current draft be a `dict` key, and should it be?
6. If the dataclass became frozen but kept a list, what mutation would remain possible?
7. Which existing test must change if a scan returns a replacement snapshot?

No learner prediction has been recorded by the maintainer.

## Run and observe

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-060-dataclasses-immutable-value-objects-enums/practice/shipment_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-060-dataclasses-immutable-value-objects-enums/practice
```

Record the exact commands, runtime, and output. Then add one small probe that keeps two references
to the same shipment and observes both after a scan. Do not treat these starter results as learner
evidence.

## Phase A — establish the value boundary

Preserve the record keys and error behavior. Parse or construct only valid tracking identifiers and
checkpoints. Replace the open-ended status string with a finite named state whose wire value stays
compatible.

Add focused tests proving:

- invalid tracking identifiers fail during value construction rather than during an unrelated scan;
- unknown wire states fail at the parser boundary;
- plain `Enum` members from different classes stay distinct even when wire values match; if you
  choose `StrEnum`, explain its intentional string-substitution trade-off;
- every valid wire state round-trips explicitly; and
- annotation presence alone is not claimed as runtime validation.

Do not introduce a validation framework, descriptor hierarchy, abstract factory, or base “value
object” class unless a concrete second requirement proves it useful.

## Phase B — make snapshots immutable by design

Choose immutable nested field types, then make a scan produce a valid next snapshot while the old
one stays unchanged. Decide which fields participate in equality and hashing; do not reach for
`unsafe_hash=True` as a shortcut.

Add focused tests proving:

- equal snapshots compare equal and, if intentionally hashable, have equal hashes;
- the previous revision is unchanged after success and failure;
- no nested checkpoint collection can be mutated through an alias;
- one valid scan increments exactly once;
- a terminal snapshot cannot transition; and
- concurrent readers of one snapshot cannot observe a partial in-place transition.

Changing from mutation to replacement is an API decision. Make it visible in the function name,
return type, tests, and caller flow.

## Phase C — keep transport outside the domain model

Add explicit inbound and outbound adapter functions. Keep list/string wire types at the boundary and
tuple/enum/value types inside. Reject invalid data once, then let the core operate on trusted values.

Test malformed records, empty collections, duplicate checkpoints if your policy forbids them,
Unicode, punctuation, unknown states, and round-trip behavior. Do not assume `dataclasses.asdict()`
is a complete API-versioning or enum-serialization policy.

## Phase D — transfer the judgment

Sketch one of these without implementing every variation:

- two workers race to persist different next revisions;
- a new `returned` state is deployed while an older consumer still reads records;
- checkpoints become structured values with a timestamp and facility code; or
- an ORM entity must remain mutable while the domain snapshot does not.

Explain which invariant belongs in the value, which belongs at the persistence boundary, and which
requires coordination beyond a frozen object.

## Required edge cases

- Empty, surrounding-space, Unicode, colon-containing, and pipe-containing text.
- Every supported state plus an unknown wire value.
- Zero, one, and several checkpoints.
- Equal snapshots created independently.
- One snapshot reached through two aliases.
- Success, invalid transition, and exception before replacement.
- A mutable object nested inside an otherwise frozen dataclass, as a deliberate failing probe only.
- Serialization that returns a detached list rather than the internal immutable sequence.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Design explanation: —
- Rejected alternative: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain

After the refactoring, explain:

1. Which equality semantics were generated and which were chosen explicitly?
2. Why is the new snapshot only as immutable as its reachable fields?
3. Where does string-to-enum parsing happen?
4. What proves an old revision cannot change through an alias?
5. What does `frozen=True` not solve about concurrent database updates?
6. Which abstraction could still be removed?

## Refactor checkpoint

The target is not “use every dataclass option.” It is one validated construction boundary, finite
state vocabulary, value-based equality where meaningful, replacement instead of hidden mutation,
and explicit transport conversion.

## Vary

Choose one change pressure:

- API clients require a deprecated state alias;
- checkpoint order becomes irrelevant;
- revisions must use optimistic concurrency in storage;
- one state carries a reason value; or
- an internal snapshot must be exposed through a public versioned schema.

State whether an enum, dataclass field, value invariant, adapter, or persistence contract changes.

## Troubleshooting

- Run from the repository root so pytest resolves the sibling starter module.
- If frozen assignment fails but `snapshot.checkpoints.append(...)` succeeds, the nested value is
  still mutable.
- If an enum prints acceptably but JSON serialization fails, choose a wire value explicitly.
- If a hash changes after mutation, remove hashability until the complete value graph is stable.
- If changing one call requires a generic base class, try one concrete frozen dataclass first.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution: —
- Optional comparison solution: —
- Trade-offs: —
- Remaining weakness: —
- Evidence link for `PROGRESS.md`: —
