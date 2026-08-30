# EXP-01 — Separating functions does not undo completed effects

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-010](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-010) |
| Precise question | Does moving save and notify into separate functions automatically undo earlier effects when an exception occurs? |
| Classification | Python language; synthetic in-memory effects |
| Status | Interpreted — maintainer run; learner prediction not recorded |

## Why observation is necessary

A tidy collaboration diagram can conceal a partial outcome. This experiment makes completed
effects visible after control leaves a failing operation. It distinguishes responsibility
boundaries from failure recovery without depending on a database, network, or timing race.

The [script](effects_experiment.py) contains a mixed publication and a split publication. Both
save a pickup identifier, then deliver a notice. Faults can occur before saving, before delivery,
or just after delivery. Lists stand in for observable effects, not durable external systems.

## Hypothesis

Maintainer hypothesis, not a learner answer: both structures preserve effects completed before a
fault. A second attempt after delivery may repeat both effects unless additional retry semantics
exist. Extracting functions alone supplies no rollback operation.

Before inspecting the recorded result, Rahul should predict the saved count, delivered count,
and error signal for each fault point and explain the reasoning. No prediction is attributed to
Rahul by this file.

## Environment

```text
Date: 2026-08-30
Operating system: Linux-7.0.0-30-generic-x86_64-with-glibc2.43
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: namespace(name='cpython', cache_tag='cpython-314', version=sys.version_info(major=3, minor=14, micro=7, releaselevel='final', serial=0), hexversion=51251184, _multiarch='x86_64-linux-gnu', supports_isolated_interpreters=True)
Dependencies: standard library only; verification uses locked pytest 8.4.2
Relevant flags: optimize=0, dont_write_bytecode=1, isolated=0
Execution: synchronous, one process, no external I/O
```

## Controls and variables

- Controlled: one synthetic pickup ID, save-before-notify order, list-based effects, and fresh
  state for each fault case.
- Changed: mixed versus split implementation, and the injected fault point.
- Measured: saved entries, delivered entries, and whether an error reached the observing wrapper.
- Separate retry case: reuse the same state after an error occurring just after delivery, then
  make a second attempt with no injected failure. The wrapper catches only the expected
  `RuntimeError` for observation; production error handling is not being recommended.

## Reproduction command

From the repository root, after setting up the external environment described in the
[practice commands](../../practice/README.md#commands):

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --locked python \
  units/solid/SDP-SOL-010-single-responsibility-principle/experiments/EXP-01-effects-survive-errors/effects_experiment.py

PYTHONDONTWRITEBYTECODE=1 uv run --locked pytest -q -p no:cacheprovider \
  units/solid/SDP-SOL-010-single-responsibility-principle/experiments/EXP-01-effects-survive-errors
```

The recorded run used the same locked environment directly via
`/tmp/sdp-sol-010-venv/bin/python`, with `PYTHONDONTWRITEBYTECODE=1`, followed by the relative script
path above. The unit test run included this experiment's ten cases.

## Predicted result

For either structure: no fault leaves one save and one delivery; a save fault leaves neither;
a fault before notification leaves only the save; a fault after notification leaves both.
The explicit retry after the last case leaves two saves and two deliveries.

## Observed result

Actual stdout from the CPython 3.14.7 run, exit status 0:

```text
mixed fault=none saved=1 delivered=1 error=False
mixed fault=save saved=0 delivered=0 error=True
mixed fault=before_notify saved=1 delivered=0 error=True
mixed fault=after_notify saved=1 delivered=1 error=True
mixed retry-after-delivery saved=2 delivered=2 error=False
split fault=none saved=1 delivered=1 error=False
split fault=save saved=0 delivered=0 error=True
split fault=before_notify saved=1 delivered=0 error=True
split fault=after_notify saved=1 delivered=1 error=True
split retry-after-delivery saved=2 delivered=2 error=False
```

The script completes because the observation wrapper catches the injected errors. `error=False`
on the retry line refers to the second attempt; it does not erase the failure on the first attempt.

## Interpretation

1. Direct observation: the same saved and delivered entries remain in both implementations at
   every injected fault point. The explicit retry duplicates the already completed effects.
2. Reasonable inference for this design: changing function boundaries without adding recovery
   behaviour did not change its partial outcomes.
3. Not established: database transaction behaviour, real delivery acknowledgement, crash
   recovery, thread safety, exactly-once delivery, performance, or whether the split design is
   best for a particular organization.

Python's exception control flow skips remaining statements on the failed path and searches for
a matching handler. This script contains no compensating operation that removes prior entries.
[Source: Python tutorial, Handling Exceptions.](https://docs.python.org/3.14/tutorial/errors.html#handling-exceptions)

## Visual interpretation

```text
one publication attempt

save ──> saved entry ──> notify ──> delivered entry ──> normal return
  X                       X                 X
before save          before delivery   after delivery
saved=0              saved=1           saved=1
delivered=0          delivered=0       delivered=1

explicit retry after delivery error: saved=2, delivered=2
```

### How to read this visual

Move left to right through the synchronous operations. Each `X` is a different fault injection
point in a fresh run; the counts below it are the observed state after the error is caught.
The retry line is a separate two-attempt run that deliberately keeps the same state.

### Key insight

An error does not tell you that nothing happened. The caller needs a clear success and recovery
contract; function or class separation alone cannot supply one.

### Simplification or limitation

This is an execution timeline for deterministic list mutations, not a network acknowledgement
diagram or database transaction trace. The harness knows where its fault occurred; a real caller
may not know whether a remote operation completed.

## Design conclusion

Use SRP to assign policy and effect responsibilities clearly. Separately decide which component
owns publication success, retries, duplicate handling, and recovery. These concerns can justify a
workflow boundary without moving all detailed business rules into the coordinator.

## Limitations

- Synthetic callbacks and immediate list updates model no external durability.
- There is no concurrent execution, process crash, timeout, or transaction manager.
- The retry is deliberately unsafe demonstration code, not a recommended implementation.
- No timing or memory benchmark was run.
- A maintainer's execution is artifact verification, not Rahul's learning evidence.

## Sources

1. Python 3.14, [Handling Exceptions](https://docs.python.org/3.14/tutorial/errors.html#handling-exceptions),
   read 2026-08-30.
