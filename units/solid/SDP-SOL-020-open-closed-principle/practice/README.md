# Practice — SDP-SOL-020 Open/Closed Principle

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-020](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-020) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-020-open-closed-principle/practice` |
| Status | Not attempted |

## Learning question

Can you distinguish a new set of values from a genuinely new algorithm, preserve the queue's
existing contract, and protect only the workflow that needs to stay stable?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

The working starter and its characterization tests are intentionally green. The new requirements,
extension API, acceptance tests, and design explanation remain learner work. The reporting example
is solved teaching material in a different domain; do not mistake it for a completed queue lab.

## Starter files

- [support_queue_lab.py](support_queue_lab.py): validated ticket values, two conditional plans,
  queue assembly, and a synthetic runner.
- [test_support_queue_lab.py](test_support_queue_lab.py): existing public behavior only. Tests do
  not demand a particular helper, registry, superclass, or number of objects.

## Problem

A support queue displays how many minutes remain before each ticket's response budget expires.
Plans currently differ only in their urgent and ordinary allowances. A ticket also records how
many times it has been reopened, but the existing plans ignore that fact.

The current API is `remaining_minutes(ticket, plan)` and `queue_report(tickets, plan)`.
Keep those calls working for existing names. Any new public extension API is your design choice.

## Change pressure

Work through these checkpoints in order, preserving the original attempt and reasoning:

1. **Data variation:** a `partner` plan allows 45 minutes for urgent tickets and 180 for ordinary
   tickets. Decide whether this calls for new behavior or merely different values.
2. **Behavior variation:** a `recovery` plan allows 15 minutes for an urgent ticket. For an ordinary
   ticket, its allowance is 180 minus 20 times its reopen count, with a minimum allowance of 30.
   Elapsed age is subtracted afterward and the remaining budget cannot be negative.
3. **Extension boundary:** an application team must be able to supply a further compatible policy
   without editing the already-refactored queue assembly and remaining-budget workflow. Wiring
   edits are allowed. Explain what an extension must return and what it must never do.

Use the smallest design that handles the observed forces. Do not build plugin discovery, a rule
language, decorators for auto-registration, a web server, or a class hierarchy without a need.

## Expected observable behavior

| Concern | Existing contract to preserve |
|---|---|
| Typed input | Nonblank reference, nonnegative integer age and reopen count, boolean urgency |
| Standard allowances | 120 urgent; 480 ordinary |
| Priority allowances | 30 urgent; 120 ordinary |
| Remaining budget | Allowance minus age, clamped at zero |
| Reference | Preserve the supplied nonblank string, including surrounding whitespace |
| Report | Tuple of `(reference, remaining_minutes)` pairs in input order |
| Repeated reference | Preserve both entries; do not deduplicate or sort |
| Empty input | Empty tuple for a known plan; unknown plan still raises `ValueError` |
| Name matching | Exact and case-sensitive; no fallback or normalization |
| Effects | Do not mutate tickets, publish messages, or read the clock |

The starter assumes typed callers and validates the listed value constraints; it is not an
untrusted-input parser. Minutes are synthetic integer budgets, not business calendars, time
zones, guarantees to actual customers, or a scheduling system.

For future policies, decide and document how you reject an invalid returned allowance and how
you propagate a policy's own error. A broad fallback that hides a broken policy is not success.

## Required edge cases

Check one minute before, exactly at, and one minute after a deadline. Cover urgent and ordinary
tickets, zero age, large age, no tickets, repeated references, and unsupported names.

For `recovery`, include zero reopens, the minimum-allowance boundary and one step on either side,
then subtract age. Verify that urgency follows its own stated allowance. For a supplied policy,
record selection behavior, invalid allowance behavior, an implementation exception, and whether
input or external state changed.

## Prediction before running

Before executing the starter, record your predicted `standard` and `priority` reports for the
three sample tickets, which current functions know the plan names, and which behavior should
remain unchanged after each requirement. No learner prediction is recorded yet.

## Commands

Run from the repository root in a clean Worktree. Keep environments and caches outside the
repository because its hygiene validator scans the filesystem, including ignored paths:

```bash
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-sol-020-venv
export UV_CACHE_DIR=/tmp/sdp-sol-020-uv-cache
export PYTHONDONTWRITEBYTECODE=1
export MYPY_CACHE_DIR=/tmp/sdp-sol-020-mypy-cache
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-sol-020-hypothesis

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-020-open-closed-principle/practice/support_queue_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-020-open-closed-principle
uv run --locked ruff check --no-cache units/solid/SDP-SOL-020-open-closed-principle
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-020-open-closed-principle
uv run --locked mypy units/solid/SDP-SOL-020-open-closed-principle
uv run --locked python scripts/validate_repo.py
```

Teaching and experiment runners:

```bash
uv run --locked python units/solid/SDP-SOL-020-open-closed-principle/examples/run_summary_demo.py
uv run --locked python units/solid/SDP-SOL-020-open-closed-principle/experiments/EXP-01-registry-views/registry_views.py
```

Record actual commands and results with the attempt. Maintainer runs in `VALIDATION.md` do not
substitute for the learner's explanation or acceptance tests.

## Rahul's attempt

Not attempted. When work begins, preserve the baseline commit and create the learner's attempt
without replacing its earlier reasoning. Link the attempt, predictions, rejected alternative,
acceptance tests, and actual results here. Do not fabricate an attempt or review now.

## Observe and explain

After the baseline run, trace the plan decision, age subtraction, and report assembly. Identify
the first change that needs only data and the first that needs behavior. Explain which public
contract your proposed boundary protects and one limitation it intentionally retains.

## Refactor

Preserve baseline behavior first. Add the two requirements separately, recording each diff and
why each edited component needed to change. A reviewer should be able to identify the stable
consumer and the legitimate composition edit. Passing existing tests alone is insufficient.

## Vary

Supply a new compatible policy through your proposed boundary. Then evaluate a different request:
reports must return absolute calendar deadlines instead of remaining integer minutes. Explain
why that request may require a contract change rather than pretending all changes are extensions.
This is production-design transfer evidence only after the learner performs and explains it.

## Progressive hints

No hints or solutions are included. Ask for one hint after an attempt; feedback should identify
the earliest missing reasoning step and give one useful nudge at a time.

## Troubleshooting

- A green starter suite proves only its existing behavior. Add acceptance tests for your design.
- Run from the repository root. The supplied test layout resolves sibling imports with pytest's
  normal import mode; changing that mode may require packaging changes outside this exercise.
- Older units reuse some test module names. For complete regression, run each unit in a separate
  pytest process rather than silently excluding tests or modifying unrelated units.
- Keep an implementation exception distinct from an unknown configured name.
- Do not delete pre-existing local environments or caches to satisfy hygiene; use a clean Worktree.

## Closure criteria

Close only after the original attempt is preserved, new behavior and edge cases are tested, a
further policy is supplied without changing the protected workflow, and the learner explains a
simpler rejected option and the calendar-contract limitation. Add review evidence and any optional
comparison solution only then. No closure or learning-state advancement is recorded by initialization.
