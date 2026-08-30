# Practice — SDP-SOL-080 SOLID critiques, overapplication, and legacy refactoring

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-080](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-080) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | See Commands below |
| Status | Not attempted |

## Learning question

Can you untangle two independently changing reports while distinguishing a safe
structural change from an intentional correction to existing behaviour?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

- [workshop_reports_lab.py](workshop_reports_lab.py): runnable legacy code, not the solution.
- [test_workshop_reports_lab.py](test_workshop_reports_lab.py): phase-A characterization tests.

There is no final replacement, phase-B implementation, released hint, or comparison solution.
Passing the supplied tests only confirms the starting behaviour.

## Problem and change pressure

A workshop has a staff board and a historical archive. A shared report engine accumulated
flags to serve both. The board team changes presentation rules; the archive consumer
depends on a fixed representation. The only supported report entry points for this exercise
are `board_report` and `archive_report`, plus the `RepairJob` input record. The engine,
options, and factory are internal and have no external subclasses or direct callers here.

Phase A: simplify the internal design without changing either public result. Do not merely
rename the flags or replace the factory with a service locator. Explain what shared knowledge
you kept and what independent decisions you separated. There is no target class count.

Phase B, only after recording a verified phase A: the board now distinguishes a known zero
minute estimate from an unknown estimate. Zero must display `0`; `None` must still display
`?`. The archive must retain its old spelling for both values until its consumer is migrated.
This is the exercise's explicitly requested behaviour change, not part of the refactoring.
Add new tests and update only the board expectation affected by that approved change; keep
the preserved phase-A attempt and its original checks available in Git or an attempt file.

## Expected observable behaviour during phase A

| Dimension | Staff board | Historical archive |
|---|---|---|
| Closed jobs | Omitted | Included |
| Title | Stripped and uppercase | Exact input spelling and whitespace |
| Identifier | Omitted | Exact identifier first |
| Field separator | ` / ` | `::` |
| Zero or unknown minutes | `?` | `unknown` |
| Result | Tuple of lines in input order | Tuple of lines in input order |

Both retain duplicates and preserve the caller's input. Empty input gives an empty tuple.
Blank titles, negative estimates, and delimiter or newline characters are currently accepted.
No escaping is performed. These facts are compatibility observations, not recommendations
for a new interchange format. Do not add validation, escaping, sorting, or deduplication
under the label “refactoring.”

The supported input is a finite `Sequence[RepairJob]` with the annotated field types.
General generator support, runtime type validation, and new persistence are out of scope.

## Prediction before running

Write your own prediction for the printed board and archive, then for zero versus `None`,
a closed job, repeated identifiers, and a title containing spaces. Name which consumer
would notice each change. No learner prediction has been recorded.

## Commands

Run from a clean repository Worktree. Keep environments and caches outside the repository;
the validator checks ignored directories too. These commands install the repository lock
without changing it:

```bash
SDP_SOL_080_TOOLS=$(mktemp -d /tmp/sdp-sol-080-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_SOL_080_TOOLS/venv"
export UV_PYTHON_INSTALL_DIR="$SDP_SOL_080_TOOLS/python"
export UV_CACHE_DIR="$SDP_SOL_080_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_SOL_080_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_SOL_080_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring/practice/workshop_reports_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring
uv run --locked ruff check --no-cache units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring
uv run --locked mypy units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring
uv run --locked python scripts/validate_repo.py
```

Run the independent worked example and experiment with the same environment:

```bash
uv run --locked python units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring/examples/run_export_demo.py
uv run --locked python units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring/examples/trace_probe.py
```

For Python 3.11, choose a separate external environment, run
`uv sync --locked --group dev --python 3.11`, and use `uv run --locked --python 3.11`
for its commands. Add `--python-version 3.11` to mypy. Do not overwrite another task's
environment. Record actual versions and output; maintainer runs do not replace your attempt.

## Rahul's attempt

Not attempted. Before editing, preserve your prediction, first design, reasoning, one
rejected alternative, and actual test results. Preserve phase A before starting phase B.
No formal learner review has occurred.

## Observe and explain

Explain why the baseline treats zero and `None` alike and why that does not authorize a
correction in both clients. Python's `or` returns one of its operands, and both zero and
`None` are falsy. [Python language reference: Boolean operations](https://docs.python.org/3.14/reference/expressions.html#boolean-operations).

Then identify which tests protect client promises and which assertions would unnecessarily
freeze internal structure. A test that the factory was called twice would not establish
the report contract.

## Refactor

Write a brief decision record: change pressure, stable promises, proposed boundary, rejected
alternative, cost, smallest step, and trigger to reconsider. Simplify only as far as the
observed need warrants. Each step must pass the unchanged phase-A tests.

No hints have been released. After preserving your attempt, ask for one progressive hint
if needed. A review should first identify the missing reasoning step, not replace your code.

## Required edge cases

Cover empty input, all-closed input, unknown and zero estimates, a negative estimate,
whitespace-only and empty titles, Unicode, duplicate jobs, repeated identifiers, separator
characters, embedded newlines, order, and input reuse without mutation. Add one meaningful
case of your own before phase B. Do not claim the synthetic archive is a safe general parser.

## Vary: production transfer

After phase B, an external partner asks for an escaped archive format. Propose a migration
that preserves the old consumer while introducing the new contract. Identify whether a
versioned entry point is justified, what you would compare, and how you would stop accidental
dual writes. No implementation or actual external publishing is required for this transfer.

Then change one assumption: the factory is part of a public package and third parties
subclass its engine. Explain why deleting it now has a different compatibility cost.

## Interview checkpoint

Ask one question at a time, beginning: **“Why must zero stay unchanged in phase A, and why
does phase B change only one consumer?”** Wait for the answer before probing the abstraction.

## Troubleshooting

- Green baseline tests are expected; the exercise is still unsolved.
- Hyphenated unit paths are not Python package names. Run the documented file paths.
- Run full repository regression in separate pytest processes per unit; older test-module
  names repeat across units.
- Preserve unrelated environments and learner work. Use a clean Worktree for hygiene checks.
- Changing a golden expectation needs an explicit behaviour decision, not merely a new output.

## Review and closure

Closure requires the original attempt, tested phase A, separately tested phase B, edge-case
reasoning, a rejected design, and transfer reasoning. Add a comparison solution only after
Rahul closes the exercise. Generated code and maintainer validation do not advance learning state.
