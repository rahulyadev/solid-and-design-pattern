# Practice — SDP-PYT-010 Functions, closures, and callable objects as design tools

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-010](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-pyt-010) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-010-functions-closures-callable-objects/practice` |
| Status | Not attempted |

## Learning question

Can you make a review decision replaceable while preserving the existing workflow, then
give a limited review round the correct state lifetime?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

This is an activity sequence, not a runtime graph. Follow each step in order; passing
the baseline tests alone does not complete the refactoring or establish learning.

## Starter files

- [review_queue_lab.py](review_queue_lab.py): runnable legacy code, not a final design.
- [test_review_queue_lab.py](test_review_queue_lab.py): phase-A characterization tests.

The worked encoder examples use a different domain. There is no replacement review
implementation, hidden solution, released hint, or fabricated learner review.

## Problem and change pressure

A synthetic support tool selects tickets for two review lanes: urgent tickets, and tickets
at least fourteen days old. Closed tickets are excluded from both. The workflow currently
knows both policy names and rules. A third team wants to supply its own eligibility rule.

**Phase A — preserve behaviour.** Refactor so the stable traversal can accept a ticket
decision callable without knowing lane names. Preserve the public `Ticket` record and
`choose_reviews(tickets, lane)` entry point and its old observations. Existing lane selection
may remain at that compatibility boundary. Do not build a registry, plugin loader, class
hierarchy, or mode framework. Add a test using a new decision without editing the core
traversal. Explain which part chooses the rule and which part executes it.

For the new callable-facing boundary, closed tickets must be skipped before consulting
the decision. Consult it exactly once for each open ticket, in order. Propagate its first
exception unchanged and leave later source items unconsumed. This is a new documented
boundary; the supplied tests do not yet prove that you implemented it.

**Phase B — stateful change, after preserving phase A.** A newly configured review round
may accept at most two tickets that its base rule accepts. Closed or rejected tickets
do not use the allowance. Separate rounds have separate allowances, even when configured
with the same base rule. Within a round, aliases to its one decision share the allowance.
The capped decision still receives every open ticket through the phase-A traversal;
exhaustion is a false result, not permission to stop consuming the finite input.
Existing uncapped urgent/stale calls must keep their old behaviour.

Choose and justify the state owner and construction boundary. Add your own tests for
repeated, independent, and interleaved rounds. Do not use module-global state. No target
closure or class implementation is supplied.

## Expected observable behaviour in the original API

| Dimension | Urgent lane | Stale lane |
|---|---|---|
| Eligibility | `urgent` is true. | `age_days >= 14`. |
| Closed tickets | Excluded. | Excluded. |
| Order and duplicates | Preserved. | Preserved. |
| Result | Tuple of exact keys. | Tuple of exact keys. |
| Empty known lane | Empty tuple. | Empty tuple. |
| Unknown lane | `ValueError("unknown review lane")` before consuming input. | Same. |

The supported input is a finite `Iterable[Ticket]` with annotated field types. A one-pass
iterator works. Keys are not normalized or deduplicated. Negative ages are accepted:
they do not satisfy the stale rule but do not prohibit urgent review. These are compatibility
facts, not recommendations for validating real support data. Do not silently add sorting,
runtime type validation, escaping, or a new error policy during phase A.

## Required edge cases

- Empty input, all closed tickets, none eligible, and the exact fourteen-day threshold.
- Repeated keys, repeated objects, whitespace, blank keys, Unicode, negative and zero age.
- A one-pass iterator, an input list reused unchanged, and a source that raises.
- The new decision raises on the first or a later open ticket; closed tickets never reach it.
- A quota round with rejected tickets before accepted tickets; zero successful selections.
- More than two eligible tickets, two separate rounds, and interleaved aliases/owners.

Add a meaningful case of your own. Explain why each observation matters to a caller.

## Prediction before running

Record your prediction of the demo's two tuples and the unknown-lane case before running.
Identify which code chooses a policy and which code traverses input. No learner prediction
has been recorded by the maintainer.

## Commands

Run in a clean repository Worktree. The validator checks ignored directories too, so keep
environments and caches outside the repository. Use the unchanged dependency lock:

```bash
SDP_PYT_010_TOOLS=$(mktemp -d /tmp/sdp-pyt-010-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_PYT_010_TOOLS/venv"
export UV_PYTHON_INSTALL_DIR="$SDP_PYT_010_TOOLS/python"
export UV_CACHE_DIR="$SDP_PYT_010_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_PYT_010_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_PYT_010_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/pythonic/SDP-PYT-010-functions-closures-callable-objects/practice/review_queue_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-010-functions-closures-callable-objects
uv run --locked ruff check --no-cache units/pythonic/SDP-PYT-010-functions-closures-callable-objects
uv run --locked ruff format --check --no-cache units/pythonic/SDP-PYT-010-functions-closures-callable-objects
uv run --locked mypy units/pythonic/SDP-PYT-010-functions-closures-callable-objects
uv run --locked python scripts/validate_repo.py
```

Use the same environment for the independent worked example and observations:

```bash
uv run --locked python units/pythonic/SDP-PYT-010-functions-closures-callable-objects/examples/run_callable_demo.py
uv run --locked python units/pythonic/SDP-PYT-010-functions-closures-callable-objects/examples/binding_probe.py
uv run --locked python units/pythonic/SDP-PYT-010-functions-closures-callable-objects/examples/effects_probe.py
```

For Python 3.11, choose another external environment, synchronize it with
`uv sync --locked --group dev --python 3.11`, then use `uv run --locked --python 3.11`
and mypy's `--python-version 3.11`. Do not replace another task's environment. Record
the actual interpreter and results, not just the intended target.

## Rahul's attempt

Not attempted. Before editing, preserve your prediction, first implementation, design
reasoning, rejected alternative, and test output. Preserve phase A before phase B in Git
or a clearly named attempt file. Maintainer runs are not your prediction or solution.

## Observe and explain

After running, explain who chooses the policy, who calls it, who owns mutable state,
what happens on failure, and which tests protect the old API. Describe why green baseline
tests cannot prove the new decision boundary or correct quota lifetime.

## Refactor

Write a short decision record: change pressure, stable promises, proposed boundary,
state owner, rejected alternative, smallest safe step, and trigger to reconsider.
Do phase A without weakening its supplied characterization tests. Then implement phase B
with new tests and preserve the uncapped old callers.

## Progressive hints and review

No hints have been released and no learner review has occurred. After preserving your
attempt, ask for one hint if needed. Review should identify the first missing reasoning
step, show the smallest exposing case, and request a targeted revision before replacement code.

## Vary: production transfer

The review decision now depends on an external service, and selected reviews may run
tomorrow after a restart. Propose where timeout/error handling, stable operation data,
idempotency, and resource ownership belong. Explain why serializing a closure or capturing
a request-bound connection is not a complete design. No network call or broker implementation
is required. State which assumptions changed and which concerns deserve a separate unit.

## Interview checkpoint

Ask one question at a time, beginning: **“Why should two review rounds not share the
same mutable allowance, and where would you construct that allowance?”** Wait before
probing callable form, the old API, or failure semantics.

## Troubleshooting

- The starter is runnable and its tests should pass. The exercise is still unsolved.
- Hyphenated directories are not Python package names; use the documented file paths.
- Older units repeat some test-module names. Full regression uses a separate pytest process
  per unit; do not rename unrelated tests to make one combined collection work.
- The binding probe's one B023 suppression marks an intentional counterexample, not a
  recommended implementation. Do not copy the bug into the lab.
- A material approval or Git merge does not supply implementation or retrieval evidence.

## Closure requirements

Only after Rahul closes the exercise: record the preserved attempt, passing phase-A and
phase-B tests, edge-case reasoning, rejected design, transfer explanation, and actual review.
Then a comparison solution may be added. Until then, status stays **Not attempted** and
the learning tracker is unchanged.
