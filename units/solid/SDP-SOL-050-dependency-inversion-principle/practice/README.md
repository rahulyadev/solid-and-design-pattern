# Practice — SDP-SOL-050 Dependency Inversion Principle

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-050](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-050) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | See the external-environment commands below |
| Status | Not attempted |

## Learning question

Can you protect a workshop-reporting policy from a provider change while keeping data and
failure meanings clear?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

- [workshop_vendor.py](workshop_vendor.py): a synthetic provider with its own record vocabulary.
- [workshop_report_lab.py](workshop_report_lab.py): a working but provider-dependent report.
- [test_workshop_report_lab.py](test_workshop_report_lab.py): baseline behavioural tests only.

The starter is intentionally not the requested final design. No second-provider implementation,
refactoring solution, prewritten hints, or learner answers are supplied.

## Problem and change pressure

The current report receives a `PlanningClient`, selects openings large enough for a group,
and returns sorted human-readable rows. The client is already passed in, yet the report
imports vendor definitions, parses the vendor's string capacity, and catches a vendor error.

A new planning partner exposes `openings(day)` as a sequence of `(slot_id, seats)` pairs,
with integer seats, and signals unavailability with `TimeoutError`. The report's selection
rule and output format must remain useful with either provider. Create only a synthetic
local partner for the exercise; do not connect to a real service.

After refactoring, policy must be importable and testable without importing `workshop_vendor`
or the new partner module. Keep concrete selection outside the policy. Decide the boundary
and error vocabulary yourself, and explain why they match this consumer's needs.

## Expected observable behaviour

- Group size is a typed positive integer; invalid sizes fail before provider access.
- Select openings with capacity greater than or equal to the group size.
- Return a tuple of rows in Python's ordinary string sort order, formatted as `ID: N seats`.
- Empty/unknown days produce an empty tuple; unavailable data produces a visible failure,
  not an empty day. Keep the public failure message `planning unavailable`.
- The supplied synthetic provider snapshots its inputs. Repeated reports do not change them.
- Duplicate rows remain duplicated. Deduplication is not part of the current policy.
- Provider details do not appear in the policy's imports, annotations, data parsing, or catches.

The last requirement needs code review and an import-boundary check; green baseline tests
alone cannot establish it. You may adjust test setup if construction changes, but preserve
the observable assertions and record why the setup changed.

## Prediction before running

Write your own prediction before executing the starter:

- Which rows should be produced for the supplied Monday schedule and group size five?
- Which file imports the vendor, and which object is actually called?
- Would injecting a different object remove the source dependency already present?
- What should happen if the provider fails before answering?

No prediction has been recorded. Do not replace your first prediction with the observed result.

## Commands

Run from a clean Worktree. The validator also inspects ignored directories, so keep tool
environments and caches outside the repository. These exports select a fresh location:

```bash
SDP_SOL_050_TOOLS=$(mktemp -d /tmp/sdp-sol-050-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_SOL_050_TOOLS/venv"
export UV_CACHE_DIR="$SDP_SOL_050_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_SOL_050_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_SOL_050_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-050-dependency-inversion-principle/practice/workshop_report_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-050-dependency-inversion-principle
uv run --locked ruff check --no-cache units/solid/SDP-SOL-050-dependency-inversion-principle
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-050-dependency-inversion-principle
uv run --locked mypy units/solid/SDP-SOL-050-dependency-inversion-principle
uv run --locked python scripts/validate_repo.py
```

The separate teaching example and import experiment are also runnable:

```bash
uv run --locked python units/solid/SDP-SOL-050-dependency-inversion-principle/examples/run_replenishment_demo.py
uv run --locked python units/solid/SDP-SOL-050-dependency-inversion-principle/experiments/EXP-01-import-isolation/import_isolation.py
```

Record actual commands and results. Maintainer execution validates the material; it does
not count as your attempt. The SQLite demonstration uses a disposable in-memory database.

## Rahul's attempt

Not attempted. Preserve the starting commit, original prediction, first code attempt, design
explanation, and rejected alternative. No learner review or completed solution exists.

## Observe and explain

After running, explain the difference between passing the client and removing dependence
on its definitions. Draw source references separately from runtime calls. Identify the
vendor's vocabulary that crossed into the policy and the failure that must not become data.

## Refactor

Keep baseline behaviour, support the second provider, and verify that the policy can load
without either provider module. Add meaningful acceptance tests for your chosen boundary
and errors. Do not use `Any`, ignored type errors, runtime branches on provider classes,
or a global registry to conceal the unresolved dependency.

No hints have been released. Ask for one progressive hint when needed, preserving each attempt.

## Required edge cases

Cover empty/unknown days, exact capacity, zero seats, invalid group sizes, Unicode IDs,
duplicate rows, repeated reports, source-input independence, both providers, and outages.
For malformed partner data, define and test an explicit failure contract; do not silently
accept negative capacity or coerce arbitrary values into valid business information.

Check import isolation in a fresh process so an already-loaded provider cannot hide the
dependency. Treat that check as one piece of evidence, not proof of all dependency semantics.

## Vary: production transfer

Choose one variation only after the initial attempt:

- The partner adds a result timestamp. The business now requires freshness. Decide whether
  this changes the policy contract or belongs solely in translation, and justify the choice.
- A report must work offline from a saved snapshot. State what changes about freshness and
  resource lifetime even if the same method shape can be used.
- The report becomes a seat-booking workflow. Explain why the existing read contract cannot
  promise atomic reservation, and identify what new guarantees need explicit design.

## Interview checkpoint

Ask one question at a time. Start with: **“What concrete dependency remains after this client
has been injected, and how would you demonstrate it?”** Review the first missing reasoning
step before suggesting an implementation.

## Troubleshooting

- Use the entry-point paths from the repository root; hyphenated unit folders are not Python package names.
- If SQLite setup fails, distinguish a missing driver/schema from a business-level unknown SKU.
- Keep caches external; do not delete a pre-existing environment or weaken the validator.
- Existing units reuse some test-module names. For full regression, run one unit per pytest process.
- The starter tests are expected to pass before refactoring. They do not certify the unsolved requirement.

## Review and closure

Add a learner-specific review only when an actual attempt exists. Closure requires the
preserved attempt, passing applicable tests, edge-case reasoning, source-dependency evidence,
one rejected alternative, and a new-scenario judgment. A comparison solution belongs only
after Rahul closes the exercise. No learning-state advance is justified by these starter files.
