# EXP-02 — History through aliases

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-030](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-030) |
| Precise question | Can an added subtype method break a reader's history promise without overriding any existing method? |
| Classification | Python language behaviour: shared identity and mutation |
| Status | Run and interpreted by maintainer; learner prediction not recorded |

## Why observation is necessary

Looking only at individual results shows legal nonnegative numbers. Following two references
to the same object reveals the broken promise across calls. No concurrency is needed.
Predict the readings yourself before continuing to the observed result.

## Hypothesis and predicted result

The reader and writer should denote the same object. An advance followed by reset should
produce `(0, 3, 0)`: nonnegative at every observation but not monotone. A restricted interface
does not stop another reference from calling an extra method on that object.
This is the maintainer's hypothesis, not a learner prediction.

## Environment

```text
Date: 2026-08-30
Operating system / architecture: Linux / x86_64
Python: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation.name: cpython
sys.implementation.cache_tag: cpython-314
Dependencies: standard library; pytest 8.4.2 and Hypothesis 6.165.2 for checks
Flags: PYTHONDONTWRITEBYTECODE=1; pytest cache disabled; external Hypothesis storage
```

## Controls and variables

- Controlled: one object, sequential calls, nonnegative advances, and public reads.
- Changed: a candidate subtype adds `reset()` to the grow-only implementation.
- Measured: reference identity, readings, a per-state invariant, and a history predicate.
- Positive control: generated nonnegative advances on `GrowingCount` never decrease its value.

## Reproduction commands

Apply the external-environment exports in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/experiments/EXP-02-history-through-aliases/alias_history.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/experiments/EXP-02-history-through-aliases
```

## Observed result

Actual canonical-interpreter output:

```text
same object: True
readings: (0, 3, 0)
nonnegative states: True
never decreases: False
```

## Visual interpretation

```text
reader: CountReader ──┐
                     ├──→ one ResettableCount object
writer ──────────────┘

writer's action       construct     advance(3)     reset()
reader's observation      0             3             0
state is nonnegative     yes           yes           yes
history never falls      —             yes           NO
```

### How to read this visual

The top arrows mean two references to one object, not copying. The lower rows align actions
with later observations. Read left to right; compare adjacent values in the last row.

### Key insight

Valid individual states do not establish a valid history. An added method can matter to a
client that never calls that method itself.

### Simplification or limitation

This is a conceptual reference diagram and literal sequential observation trace, not CPython
memory layout. It shows neither threads nor a transaction protocol.

## Interpretation and design conclusion

The run directly shows that mutation through `writer` changes `reader`'s later observation.
Python's identity/mutability model explains why; an annotation does not copy an object.
[Python data model](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

Our `CountReader` prose explicitly promises never to decrease. Under that contract the resettable
candidate is invalid. If a different boundary promised only nonnegative readings, this reset
would not violate that specific promise. A read-only property is not synonymous with a stable
or immutable object; structural protocol member access is a separate concern.
[Typing specification, protocols](https://typing.python.org/en/latest/spec/protocol.html).

Choose an honest capability and lifecycle contract rather than relying on the absence of
overrides. The original behavioural-subtyping source is discussed in the [unit note](../../README.md#3-history-and-formal-definition).

## Limitations and sources

Cooperative callers use public methods. Direct mutation of private attributes is not modeled.
The property-based tests sample sequences; they are not a proof over all programs. No reference
counts, addresses, garbage-collection behaviour, or interpreter-specific details are inferred.

- [Python 3.14: objects, values and types](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).
- [Executable positive controls and counterexample](test_alias_history.py).
