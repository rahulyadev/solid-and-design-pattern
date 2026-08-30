# Practice — SDP-SOL-060 SOLID interactions, tensions, and trade-offs

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-060](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-060) |
| Evidence target | E+D+T |
| Attempt required before solution | Yes |
| Test command | See the external-environment commands below |
| Status | Not attempted |

## Learning question

Can you choose a small, honest boundary when a new provider changes both capabilities and
the meaning of completion?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

- [parcel_label_lab.py](parcel_label_lab.py): runnable synchronous baseline with synthetic data.
- [test_parcel_label_lab.py](test_parcel_label_lab.py): tests of existing observable behaviour.

No queued partner, final refactoring, prewritten hints, learner answer, or comparison solution
is included. The baseline tests should pass before the exercise is attempted.

## Problem and change pressure

`prepare_dispatch` validates a parcel, asks a `LocalLabelDesk` for a ready label, and returns
a dispatch note. The same desk also exposes voiding and daily totals, although dispatch
uses neither. An unavailable desk raises an error; it does not return a successful note.

A proposed partner behaves differently:

- `submit(parcel)` immediately returns a nonblank request reference.
- `status(reference)` later reports pending, ready with label text, or failed.
- The partner has no voiding operation and no daily-totals operation.
- Submission can time out; a timeout does not establish whether it accepted the request.

Product says: “Support this partner without making the dispatch screen claim a parcel is
ready before a label exists.” A teammate suggests renaming `submit` to `make_label`, returning
its request reference as the string, and filling unsupported methods with no-ops.

Your task is to review that proposal, explain the actual change pressure, and refactor only
what is justified. Decide the client-visible behaviour for pending and failure before writing
the new synthetic provider. No real label service, network request, or external account is needed.

## Expected observable behaviour

- Preserve the current synchronous path: a valid parcel gets a ready label and matching reference.
- Blank reference/destination and nonpositive integer weight fail before provider access.
- A known provider failure remains visible. It must not appear as a successful dispatch note.
- A queued request must never be displayed as a ready label just because its identifier is text.
- Define and test pending, ready, and failed behaviour for the new workflow explicitly.
- Do not require a provider to implement capabilities its client does not need.
- Preserve caller data and explain who owns provider state and any polling lifecycle.

The public workflow may need an explicit contract change. Identify which compatibility
promises remain and which callers must change; do not silently redefine “ready.”
No required class layout or number of interfaces is specified.

## Prediction before running

Record your prediction in your own attempt note before executing the starter:

- What will the supplied parcel print, and what state will the desk retain?
- What does a returned `DispatchNote` promise to its caller?
- What would the proposed partner substitution cause the dispatch screen to claim?
- Which principle is the primary diagnostic lens, and which is supporting?
- What evidence would justify retaining the current direct design?

No learner prediction has been recorded. Maintainer runs must not replace this step.

## Commands

Run from the repository root in a clean Worktree. Keep all tool environments and caches
outside it; the validator inspects ignored directories too.

```bash
SDP_SOL_060_TOOLS=$(mktemp -d /tmp/sdp-sol-060-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_SOL_060_TOOLS/venv"
export UV_CACHE_DIR="$SDP_SOL_060_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_SOL_060_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_SOL_060_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/practice/parcel_label_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs
uv run --locked ruff check --no-cache units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs
uv run --locked mypy units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs
uv run --locked python scripts/validate_repo.py
```

The independent teaching example and experiments are runnable with the same environment:

```bash
uv run --locked python units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/examples/run_alert_demo.py
uv run --locked python units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-01-compatible-shape/shape_probe.py
uv run --locked python units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-02-split-operation/split_probe.py
```

Record actual results. The worked example does not implement the dispatch exercise.

## Rahul's attempt

Not attempted. Preserve the baseline commit, first prediction, first implementation, design
reasoning, and one rejected alternative. Add a learner review only after an actual attempt.

## Observe and explain

Draw the client's promises separately from the methods a provider happens to offer. Explain
what types can check and what they cannot. Describe how a successful-looking string could
still represent the wrong event. Identify the smallest observable case that tests your claim.

## Refactor

Create a decision record with the real force, primary diagnosis, contract, selected boundary,
rejected alternative, cost, and trigger to reconsider. Make the implementation match that
record. Add acceptance tests for your new workflow without replacing the existing guarantees
with weaker assertions. If construction changes, preserve the behavioural assertions and
explain changed test setup.

Do not use `Any`, ignored type errors, no-op success, global service lookup, or a class-name
switch to hide an unresolved contract. Do not build a generic task platform for this exercise.
No hints have been released; request one progressive hint only after preserving your attempt.

## Required edge cases

Cover invalid input before access, existing synchronous success/failure, pending without a
label, eventual readiness, explicit failure, empty/malformed partner responses, an unknown
request reference, and duplicate calls. Decide how to surface an ambiguous submission timeout;
do not assume an automatic retry is safe.

The baseline issues another label on a repeated valid call, even if the string is identical.
That is characterization, not a desirable idempotency guarantee. If your changed workflow
adds idempotency, document that intentional behaviour change and test it separately.

## Vary: production transfer

After the first attempt, choose one new pressure:

- Product needs to cancel pending work. Decide which client owns that capability and what an
  unsupported cancellation means, without requiring every provider to pretend success.
- Two dispatch screens request the same parcel simultaneously. State which consistency or
  deduplication guarantee is needed and where it must be enforced.
- The partner returns a document reference that expires. Explain whether ready still means
  printable and how that changes the lifetime contract.

These prompts are unsolved. No new canonical unit or integration project is initialized.

## Interview checkpoint

Ask one question at a time. Start with: **“Which existing caller promise does the proposed
partner substitution put at risk, and what is the smallest test that would expose it?”**
Review the missing reasoning step before discussing implementation alternatives.

## Troubleshooting

- Run by the documented paths; hyphenated unit directories are not importable package names.
- Baseline tests do not test an unimplemented partner and should not be treated as exercise completion.
- Do not delete pre-existing caches or environments to satisfy the validator; use a clean Worktree.
- For full repository regression, run one pytest process per existing unit to avoid reused test names.
- Integers are the typed weight contract. Arbitrary external payload validation is separate work.

## Review and closure

Closure requires the preserved attempt, diagnosis, tested behaviour, edge-case reasoning,
one rejected alternative, and transfer to a changed requirement. Passing tests alone cannot
explain whether the chosen boundary is useful. Add a comparison solution only after Rahul
closes the exercise. Generated material does not advance the learning state.
