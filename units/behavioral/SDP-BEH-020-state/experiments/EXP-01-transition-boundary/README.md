# EXP-01 — Transition boundary

| Field | Value |
|---|---|
| Owning unit | [SDP-BEH-020](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-beh-020) |
| Precise question | What survives when a release gate returns, raises before/after an effect, or attempts a nested event? |
| Classification | Design-level local commit policy, explained by Python language exception behavior |
| Status | Reproduced |

## Why observation is necessary

A diagram can hide the moment at which a proposed state becomes current. It also hides callbacks
that change something else before throwing. Inspect both the context snapshot and a synthetic
external list to distinguish local preservation from rollback of all work. This is a controlled
behavioral observation, not a performance benchmark or CPython-internals claim.

## Hypothesis

A normal gate return installs the proposed RELEASED snapshot. A gate exception preserves the same
SEALED snapshot and revision. Appending before that exception still changes the separate list.
An uncaught same-context nested event is rejected and aborts the outer transition before commit.

## Environment

Observed on 2026-09-10, Linux 7.0.0-31-generic, x86_64, glibc 2.43:

```text
CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation.name: cpython; cache_tag: cpython-314
CPython 3.11.16
sys.version: 3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]
sys.implementation.name: cpython; cache_tag: cpython-311
Dependencies: standard library only for this experiment
Flags: PYTHONDONTWRITEBYTECODE=1; no async, threads or network
```

The focused verification uses pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1 and Hypothesis 6.165.2 on both
runtimes. Full environment and cache controls are in [VALIDATION.md](../../VALIDATION.md).

## Controls and variables

- Controlled: fresh Packet per case, ADD(2), SEAL, one RELEASE request, identical event order,
  page count, starting revision 2, and the same observation code.
- Changed: gate behavior only—return, raise before append, append then raise, or reenter CANCEL.
- Measured: old phase seen by gate, proposed phase, effect list, escaping exception class, final
  phase/revision, and whether final snapshot is the identical saved object.

The callback appends proposed revision 3 as a synthetic effect. It is not a real message, payment,
file write, or durable audit record. The `seen` list is measurement instrumentation.

## Reproduction command

From repository root, select either verified interpreter as `python`:

```bash
PYTHONDONTWRITEBYTECODE=1 python units/behavioral/SDP-BEH-020-state/examples/observe_boundary.py
```

The executable is [observe_boundary.py](../../examples/observe_boundary.py); its output contract is
checked by [test_state.py](../../examples/test_state.py). No wall clock, random seed or benchmark
warm-up affects the four cases.

## Predicted result

Success moves from sealed revision 2 to released revision 3. Both gate failures and uncaught
reentrancy retain revision 2 and snapshot identity. Only success and fail-after retain an effect.

## Observed result

Both runtimes produced the same four lines:

```text
success: seen=['sealed->released'], effects=[3], error=none, state=released, rev=3, same_snapshot=False
fail_before: seen=['sealed->released'], effects=[], error=GateFailure, state=sealed, rev=2, same_snapshot=True
fail_after: seen=['sealed->released'], effects=[3], error=GateFailure, state=sealed, rev=2, same_snapshot=True
reenter: seen=['sealed->released'], effects=[], error=ReentrantEvent, state=sealed, rev=2, same_snapshot=True
```

## Interpretation

1. Every gate sees the context still SEALED while receiving a RELEASED proposal. Preparation and
   installation are distinct moments.
2. The fail-after row directly disproves “unchanged local state means no side effects.” The effect
   list retains an entry despite the identical context snapshot.
3. The reenter row shows the chosen same-context nesting policy. It does not prove locking or
   protection against simultaneous threads. A gate that catches the nesting error can still return
   normally; focused tests cover that separate case.
4. No automatic retry runs. Focused tests show the guard clears after failure and a caller can make
   a new request. Retrying a real effect still requires a separate idempotency/recovery decision.

## Visual interpretation

```text
SEALED rev2 --prepare--> proposal RELEASED rev3
              gate sees current SEALED
              append effect 3
              raise GateFailure
SEALED rev2 remains; effect 3 remains too
```

### How to read this visual

Read downward through the fail-after case. “Prepare” creates a value, not a current-state change.
The final line describes two independently owned objects after exception propagation.

### Key insight

Preserving the context's current reference is weaker than reversing every effect made during a call.

### Simplification or limitation

This is a conceptual call timeline; it contains no concurrent interleaving, database, crash or
remote uncertainty. It makes no speed or resource-use claim. No browser rendering is performed.

## Design conclusion and limitations

Keep this gate side-effect-free when possible. When effects are essential, specify where durable
state and outgoing work are committed and how uncertainty is reconciled. The State pattern alone
does not supply that protocol. A process crash or asynchronous interruption around commit may leave
a caller unsure whether a local transition occurred; ordinary pre-commit exception tests do not
establish crash atomicity. Python `finally` clears the local busy flag; it does not roll back lists.

Author observation is not learner evidence. Rahul must first predict, then reproduce and explain
these results to satisfy the unit's X learning evidence.

## Sources

- [Python language reference: finally](https://docs.python.org/3.14/reference/compound_stmts.html#finally-clause), for cleanup and propagation semantics.
- [Python threading documentation](https://docs.python.org/3.14/library/threading.html), for the distinction between synchronization and this local reentrancy flag.
- [Original implementation](../../examples/state.py), for the policy actually observed.
