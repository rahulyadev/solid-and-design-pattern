# EXP-01 — Laziness, iterator identity, and exhaustion

| Field | Value |
|---|---|
| Unit | [SDP-PYT-040](../../README.md) |
| Evidence role | Required experiment (`X`) |
| Probe | [iterator_lifecycle_probe.py](../../examples/iterator_lifecycle_probe.py) |
| Last run | 2026-09-06 |
| Runtime | CPython 3.14.7 |
| Status | Reproduced by maintainer; not learner evidence |

## Question

When does a generator-backed pipeline touch its source, what does `iter(generator)` return, what
happens after exhaustion, and how does that differ from two passes over a container?

## Hypothesis recorded before the run

Creating the generator will not read a source line. The first `next()` will read only the first
line and yield its alert. The same generator object will be returned from `iter(...)`; after the
remaining line is consumed, a second pass will be empty and every later `next()` will raise
`StopIteration`. A tuple will create two distinct iterators that each see both values.

## Exact environment

| Item | Observed value |
|---|---|
| OS | Linux x86_64 |
| Runtime | CPython 3.14.7 |
| Dependency use | Standard library and the unit example only |
| Input | Two fixed in-memory synthetic alert strings |
| Network/files | None |
| Bytecode | Disabled with `PYTHONDONTWRITEBYTECODE=1` |

## Command

From the repository root, using the locked external environment documented in the practice guide:

```bash
python units/pythonic/SDP-PYT-040-iterators-generators-context-managers/examples/iterator_lifecycle_probe.py
```

## Actual output

```json
{"after_exhaustion": ["read:a-1|2|queued", "read:a-2|5|worker unavailable"], "after_first_next": ["read:a-1|2|queued"], "before_first_next": [], "container_iterators_are_distinct": true, "container_passes": [[10, 20], [10, 20]], "first_id": "a-1", "generator_iter_is_self": true, "next_after_exhaustion": "StopIteration", "remaining_ids": ["a-2"], "second_pass": []}
```

The automated contract test also passed in the canonical environment.

## Interpretation

The observations matched the hypothesis:

1. no trace existed before first demand;
2. first demand caused exactly one source read;
3. the generator was its own iterator;
4. exhaustion was permanent for that iterator;
5. a second traversal over the same generator produced nothing; and
6. the reusable tuple produced two independent full passes.

This is the design-relevant distinction: a function can create a new generator object per call,
but one generator object holds one traversal state. Repeatability also depends on whether the
upstream source can be traversed again.

## Limitations

- The probe has two in-memory values; it does not measure latency or memory.
- It observes synchronous iteration, not async generators or concurrent consumers.
- Trace calls are deliberate application observations, not CPython frame inspection.
- It proves behavior for these fixed inputs and protocol contracts, not that every lazy stage is
  bounded or side-effect free.
- Maintainer reproduction does not count as Rahul’s prediction, practice, recall, or transfer.

## Transfer prompt

If the source were a database cursor, where would cursor ownership live, and what API would make a
one-shot result impossible to mistake for a reusable collection?
