# Practice — SDP-SOL-030 Liskov Substitution Principle and behavioural subtyping

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-030](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-030) |
| Evidence target | E+I+D+X+T |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/practice` |
| Status | Not attempted |

## Learning question

Can you evaluate a replacement from the caller's contract, including the state left after an
error, and reject an integration when its real capabilities cannot support that contract?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

The baseline implementation and its tests are intentionally green. The partner candidate needs
review; its repair and contract acceptance tests are not supplied. Nothing in a maintainer run
counts as Rahul's implementation, prediction, or design explanation.

## Starter files

- [seat_reservation_lab.py](seat_reservation_lab.py): baseline `SeatPool`, a candidate partner
  integration, and a small sequential runner.
- [test_seat_reservation_lab.py](test_seat_reservation_lab.py): public baseline behaviour only.
  No helper names, private storage choices, or final refactoring design are required by tests.

## Problem and change pressure

A workshop allocates distinct seats from a finite pool. Existing callers reserve a whole group
or handle a rejection. The new `PartnerSeatPool` is offered as a drop-in replacement.
It has the same method signature and inherits the baseline class. Decide whether that is enough.

Start from the public promises below, then inspect the candidate. Do not begin by making the
client branch on concrete class names, weakening the contract, or adding exception suppression.

## Expected observable behaviour

| Concern | Baseline contract to preserve |
|---|---|
| Construction | Distinct positive integer seat IDs, captured in supplied order |
| Count | Nonnegative integer; zero is valid and has no effect |
| Successful return | Tuple of exactly the requested number of available IDs |
| Order | Return the earliest remaining seats in original order |
| Identity | Once reserved, a seat is not returned again by this pool |
| Negative count | `ValueError`, with the pool unchanged |
| Insufficient seats | `NotEnoughSeats`, with the pool unchanged |
| Availability | Reflect completed successful reservations; never negative |
| Ownership | Later edits to the constructor's source list do not edit the pool |

Assume correctly typed callers; this is not a parser for untrusted external values. The model
has no threads, network, cancellations, seat expirations, or real customer records.

## Prediction before running

For each pool in the runner, predict the outcome and remaining count after requests `1`, `3`,
then `1`, starting with `[41, 43, 47]`. Also predict what mypy and the current tests will tell you.
Record which expectation comes from the public contract and which comes from reading the code.
No learner prediction has been recorded yet.

## Commands

Run from a clean repository Worktree. Keep tools and caches outside it because the repository's
hygiene validator examines ignored paths too. This setup chooses a fresh external directory:

```bash
SDP_SOL_030_TOOLS=$(mktemp -d /tmp/sdp-sol-030-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_SOL_030_TOOLS/venv"
export UV_CACHE_DIR="$SDP_SOL_030_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_SOL_030_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_SOL_030_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/practice/seat_reservation_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping
uv run --locked ruff check --no-cache units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping
uv run --locked mypy units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping
uv run --locked python scripts/validate_repo.py
```

The solved teaching example and experiments have separate runners:

```bash
uv run --locked python units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/examples/run_catalog_demo.py
uv run --locked python units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/experiments/EXP-01-shape-is-not-contract/shape_probe.py
uv run --locked python units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/experiments/EXP-02-history-through-aliases/alias_history.py
```

Record actual commands and results. A green baseline suite does not certify a replacement it
has never tested. The shape experiment's subprocess requires mypy from the locked dev group.

## Rahul's attempt

Not attempted. When beginning, preserve the starter commit and the original prediction. Record
the attempt's file/commit, first failing sequence, design explanation, rejected alternative,
acceptance tests, and actual results. Do not overwrite earlier reasoning after seeing a result.

## Observe and explain

After execution, identify the first promise that stops holding and the first observation that
reveals it. Distinguish an error's **type** from the state it leaves behind. Explain why static
acceptance and passing tests of only the baseline do not answer the substitution question.

## Refactor

1. Write a public-behaviour contract test that exposes the candidate's first violation.
2. Decide which implementations can honestly share this contract. Explain your choice before
   editing; neither inheritance nor composition is required as the answer.
3. Make the smallest justified change while preserving the baseline promises.
4. Apply the shared contract suite to every implementation you admit to that boundary.
5. Keep the failing-before/passing-after evidence and explain one tempting but invalid repair.

No repair, target architecture, hint, or completed partner acceptance suite is supplied.

## Required edge cases

Cover zero requests, no seats, a negative request, exact capacity, one over capacity, multiple
successful reservations, repeated failures, and a valid request after failure. Check remaining
seat identities and order, not only their count. Verify source-list independence. Use another
reference to the same pool when observing the aftermath of a rejected call.

For experiment evidence, predict both linked runtime probes, run them, and distinguish language
behaviour, standard-library checking, type-checker diagnostics, and your design conclusion.

## Vary: production transfer

Now suppose a remote partner can allocate a subset before responding and cannot guarantee
undo. Network timeouts may leave its allocation outcome unknown. Does the old all-or-nothing
operation still describe that provider honestly? Propose an explicit boundary and caller policy;
explain what you refuse to promise and why. Do not implement a distributed system for this lab.

A second optional interview variation: an approval-based provider returns a pending reference,
not assigned seat IDs. Decide whether it belongs under the same operation. Compare the impact
on callers instead of hiding the distinction behind `None` or unsupported-method exceptions.

## Progressive hints

No hints are included. Ask for one after an attempt; feedback should identify the first missing
reasoning step and offer one nudge at a time.

## Troubleshooting

- A deliberate defect remains in the partner candidate. Do not call the lab completed because
  the initial tests pass; those tests deliberately cover only the existing baseline.
- Run from the repository root with the locked tools. Keep caches external; do not delete
  pre-existing user files to make the hygiene validator pass.
- Existing units reuse some test-module names. For regression, run each unit in a separate
  pytest process instead of excluding old tests or editing unrelated units.
- The demo catches known errors only to display outcomes. It is not an error-recovery policy.

## Closure criteria

Close only after the original attempt is preserved, a real counterexample and repair/rejection
are explained, contract and edge-case tests pass for every admitted provider, and the changed
remote-provider requirement is evaluated without claiming guarantees it lacks. No final solution
or learner review exists yet. Update [PROGRESS.md](../../../../PROGRESS.md) only from actual evidence.
