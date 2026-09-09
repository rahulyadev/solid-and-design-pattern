# Practice — SDP-STR-050 Composite

| Field | Value |
|---|---|
| Unit note | [SDP-STR-050](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-str-050) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | `python -m pytest -q -p no:cacheprovider units/structural/SDP-STR-050-composite/practice` |
| Status | Not attempted |

## Learning question

Can one inspection operation handle a check or a nested batch without confusing “nothing failed”
with “something was actually inspected”?

## Problem and change pressure

The [starter](inspection_lab.py) supports one check or one flat batch. It returns a Boolean; an empty
batch currently passes. A release-desk preview now needs nested batches and a meaningful explanation.
This domain is independent of the note's additive workshop estimate. Copying its numeric reducer
would not meet this target.

Design a common inspection operation with these observable requirements:

- Inspect an individual check or any valid nested batch through the same client capability.
- Report an overall status and the labels/occurrence paths of failed checks in left-to-right order.
- All actual checks are inspected; collecting diagnostics must not stop at the first failure.
- Zero inspected checks means **not inspected**, distinct from pass or fail.
- An empty nested batch contributes no inspected checks; it must not turn successful nonempty
  siblings into failure or manufacture a successful check.
- A repeated check reference is inspected once per occurrence, and both failure paths are retained.
- Choose an explicit immutable value construction policy or a controlled mutable exclusive tree.
  Explain the choice, reject cycles/invalid combinations under its supported API, and define size
  and depth bounds. Do not claim support for arbitrary cyclic graphs.
- Keep child management off the common client capability unless every component can honor it.

Specify the status/result contract before choosing classes, functions, enums or dataclasses. The
result must let a client distinguish no evidence from positive evidence without inspecting concrete
component classes. Do not add actual release actions, databases, network services or credentials.

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

**Read the cycle:** make a prediction before observing the starter, then change one design decision.
**Key insight:** passing the old tests characterizes the old semantics; it does not prove the new
contract. **Limitation:** this is an exercise workflow, not a concurrency or request-flow diagram.

## Starter files

- [inspection_lab.py](inspection_lab.py): executable flat baseline, intentionally unsolved.
- [test_inspection_lab.py](test_inspection_lab.py): four characterization cases, not target tests.

Preserve these files as the original attempt boundary. Write your implementation in a new attempt
file and target tests in a separate file. Do not silently rewrite characterization tests to imply
the new requirement was always satisfied.

## Commands

From the repository root, select an existing locked environment with pytest installed. Route state
outside the repository:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-050/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-050/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-050/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-str-050/ruff
export UV_CACHE_DIR=/tmp/sdp-str-050/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-050/venv
export COVERAGE_FILE=/tmp/sdp-str-050/coverage
mkdir -p /tmp/sdp-str-050/pytest
python units/structural/SDP-STR-050-composite/practice/inspection_lab.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-050/pytest/practice \
  units/structural/SDP-STR-050-composite/practice
```

## Predict, run, observe, explain

Before running, record the predicted answers for a passing check, a mixed flat batch, an empty batch,
and two failing occurrences of the same check. State which answers the Boolean starter cannot
express. Then run the commands and record actual output. Explain the smallest case that exposes
the gap; avoid guessing about library internals.

## Required edge cases and refactor checkpoint

Test a single pass, single fail, all-pass nested batch, mixed nested failures, root empty batch,
several nested empty batches, empties mixed with real checks, duplicate labels at different paths,
a shared failed check in two branches, an invalid child kind, the first rejected depth/size, and an
attempted cycle through your supported construction/editing API. Explain how failure paths remain
unambiguous despite duplicate labels.

Demonstrate that the common client uses your operation on a check and a batch. Show that all failures
are collected in order and a later check is visited even after an earlier failure. Explain the
identity/alias policy and one intentionally unsupported input. Passing target tests plus that
reasoning, after a real attempt, may support I/D evidence.

## Vary

After the first attempt and review, consider a new requirement: some checks depend on a remote
inspector that can time out. Decide how unknown results differ from fail and not inspected, how
partial diagnostics are represented, and whether this still belongs in the same pure component
model. Justify a boundary; do not build the remote integration.

## Rahul's attempt and progressive hints

No attempt or prediction has been supplied. No solution, review result or weakness is fabricated.
Ask for one hint when needed; the mentor should provide only the next useful nudge after identifying
the current reasoning gap. Hints and a final solution are intentionally absent.

For review, bring the attempt file, chosen contract, rejected alternative, edge cases and actual
command results. A mentor should preserve the attempt and identify the first missing reasoning
step. Closure and PROGRESS.md evidence links are added only after Rahul completes the exercise.

## Troubleshooting

Run from the repository root and give pytest the explicit practice directory. The baseline tests
must pass unchanged. An import error is an environment/path issue, not evidence for changing the
business contract. Use `/tmp` for caches and the configured environment; do not commit generated
output or build an environment inside this unit.
