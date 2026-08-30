# EXP-01 — Compatible shape, incompatible state effects

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-060](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-060) |
| Precise question | Can two implementations satisfy one callable Protocol but disagree on a caller's non-mutation promise? |
| Classification | Python language, standard-library behaviour, and design-level interpretation |
| Status | Interpreted by the maintainer; learner prediction not recorded |

## Why observation is necessary

Looking only at the returned maximum hides a change to the acquisition timeline. The probe
keeps an alias to the same list, so a later observation can reveal what the first call changed.
Static type compatibility does not express the promised preservation of that order.

## Hypothesis

Teaching prediction: both implementations return the same maximum, but only one preserves
the order the caller uses to interpret “latest.” This is not Rahul's prediction or a learner attempt.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython; cache_tag=cpython-314; version=3.14.7 final
Dependencies: probe uses standard library only; pytest 8.4.2 and mypy 1.20.2 for checks
Relevant flags: PYTHONDONTWRITEBYTECODE=1; pytest cache disabled; tool caches outside Worktree
```

## Controls and variables

- Controlled: fresh `[30, 10, 20]` input for each provider; same declared callable contract.
- Changed: maximum calculation using `max` versus sorting the supplied list first.
- Measured: result, before/after values, and last value seen through the alias.
- Not measured: execution time, memory use, concurrency, or all possible implementations.

## Reproduction command

From the repository root, apply the [practice environment exports](../../practice/README.md#commands):

```bash
uv run --locked python units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-01-compatible-shape/shape_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-01-compatible-shape
uv run --locked mypy units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-01-compatible-shape
```

## Predicted result

Both maximum values should be 30. The preserving implementation should leave the latest
reading at 20; the sorting implementation should make the alias report 30 as latest.

## Observed result

Executed by the maintainer on the canonical runtime:

```text
preserving: maximum=30; before=(30, 10, 20); after=(30, 10, 20); latest=20
sorting: maximum=30; before=(30, 10, 20); after=(10, 20, 30); latest=30
```

## Interpretation

1. Equal scalar results did not imply equal state effects.
2. The caller-visible timeline changed because the alias still referred to the same list.
3. Relative to the declared non-mutation promise, the sorting implementation is not a valid
   behavioural replacement. A compatible Protocol signature cannot establish that promise.
4. A sorted fixture would hide the problem; a single successful test is weak evidence.

## Visual interpretation

```text
readings ──┐                          readings ──┐
           ├──> [30, 10, 20]  sort               ├──> [10, 20, 30]
timeline ──┘                          timeline ──┘
              latest = 20                           latest = 30
```

### How to read this visual

Arrows mean two names referring to one list. The right-hand picture is the state after
in-place sorting, not a second list allocated by the sort.

### Key insight

An extension can change another consumer's observation without changing its return type.

### Simplification or limitation

Conceptual object-reference picture, not CPython memory layout. It shows only one shared list
and one specific promised use of order. Sorting is legitimate when a caller permits it.

## Design conclusion

State the shared semantic contract before treating collaborators as interchangeable.
Test state preservation and later observations as well as the immediate result. The worked
report uses a tuple of simple frozen records to avoid this particular collection mutation;
that still does not prove every formatter is correct.

## Limitations

- The probe copies the outer list before each run to isolate providers; integer elements need no deep copy.
- This is a deliberate counterexample, not a claim that `sort` is generally bad.
- A docstring is not executable enforcement. The tests characterize the violation on purpose.
- No runtime `isinstance` claim, inheritance requirement, or performance result is involved.
- The same code uses Python 3.11-compatible syntax; compatibility results belong in the final validation record.

## Sources

1. [Python Sorting HOWTO: sorting basics](https://docs.python.org/3.14/howto/sorting.html#sorting-basics): in-place `sort` and new-list `sorted` semantics.
2. [Typing specification: protocols](https://typing.python.org/en/latest/spec/protocol.html): structural compatibility.
3. [Liskov and Wing: introduction](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf): behavioural properties beyond signatures.
