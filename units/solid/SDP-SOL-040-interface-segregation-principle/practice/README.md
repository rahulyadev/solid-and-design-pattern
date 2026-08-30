# Practice — SDP-SOL-040 Interface Segregation Principle

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-040](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-040) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | See the isolated-environment commands below |
| Status | Not attempted |

## Learning question

How can two clients accept the capabilities they actually need while preserving meaningful
relationships between operations?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

- [station_console_lab.py](station_console_lab.py): working lab console, reporting, and configuration.
- [test_station_console_lab.py](test_station_console_lab.py): current behaviour only.
- [Separate solved archive example](../examples/run_archive_demo.py): teaching material, not a station solution.

## Problem and change pressure

The reporting client and a configuration workflow both accept the broad `StationConsole`.
The report uses measurements; the configuration workflow changes a sampling interval and
then restarts the same station through the same console.

A partner now provides a temperature feed. It can supply `reading(station_id)`, returning
integer Celsius, but cannot configure or restart devices. Integrate this partner without
inventing unsupported operations or weakening the checked contract. Preserve the existing
configuration workflow and explain whether its operations should be separated or kept together.

Add the partner provider and meaningful acceptance tests yourself. No partner solution,
target type hierarchy, hidden fix, or completed acceptance suite is supplied.

## Expected observable behaviour

- Reports preserve requested order and duplicates; zero and negative Celsius values are valid.
- An empty request yields an empty report; an unknown station raises `KeyError`.
- Reporting does not modify measurements, configuration, or restart counts.
- A valid interval is an integer from 1 through 3600 seconds, inclusive.
- A successful configuration changes only the selected station and restarts it once.
- Rejected intervals leave configuration and restart count unchanged.
- Successful configuration calls happen before restart, using the same provider.
- Current in-memory input mappings and old snapshots remain independent of later changes.

Assume correctly typed callers. This is not an external-data parser; boolean-versus-integer
validation, threads, transport, authentication, and persistent hardware state are out of scope.

## Prediction before running

Record your own answers before execution:

1. Which operations does each client use, and which does its annotation require?
2. Would a partner object with only `reading` work in the report at runtime? What would mypy say?
3. What would happen if you changed only the parameter annotation?
4. What should remain true after applying interval 120 and then rejecting interval 0?

No learner prediction has been recorded.

## Commands

Run from a clean repository Worktree. The validator inspects ignored directories too, so keep
environments and caches outside it. These exports create a fresh task-specific location:

```bash
SDP_SOL_040_TOOLS=$(mktemp -d /tmp/sdp-sol-040-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_SOL_040_TOOLS/venv"
export UV_CACHE_DIR="$SDP_SOL_040_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_SOL_040_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_SOL_040_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-040-interface-segregation-principle/practice/station_console_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-040-interface-segregation-principle
uv run --locked ruff check --no-cache units/solid/SDP-SOL-040-interface-segregation-principle
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-040-interface-segregation-principle
uv run --locked mypy units/solid/SDP-SOL-040-interface-segregation-principle
uv run --locked python scripts/validate_repo.py
```

The separate teaching example and mechanism experiment are runnable:

```bash
uv run --locked python units/solid/SDP-SOL-040-interface-segregation-principle/examples/run_archive_demo.py
uv run --locked python units/solid/SDP-SOL-040-interface-segregation-principle/experiments/EXP-01-client-dependency/dependency_probe.py
```

The experiment launches the locked mypy in subprocesses. Record actual output, including
failures. Passing the starter tests proves baseline behaviour only, not the new integration.

## Rahul's attempt

Not attempted. Preserve the starting commit, original prediction, and first attempt. After
working, record the changed files/commit, design explanation, rejected alternative, actual
commands, and results. Do not rewrite earlier reasoning to match an observed result.

## Observe and explain

Identify the first unnecessary obligation and its actual consequence. Explain the difference
between narrowing a dependency, deleting a provider method, and creating a wrapper. State
which guarantees require tests beyond a static type checker.

## Refactor

Keep the existing baseline green. Add your new provider and acceptance tests; show that the
report can use it without unsupported stubs, `Any`, ignored type errors, or runtime type
branches in the report. Explain the chosen boundary and at least one design you rejected.

No hints have been released. Ask for one hint when needed; keep each attempt before revising.

## Required edge cases

Cover empty requests, duplicate IDs, zero/negative readings, unknown IDs, interval endpoints,
invalid intervals, repeated reconfiguration, report non-mutation, and input-map independence.
Show that the partner can be used where appropriate and is not admitted to unsupported
workflows. Test the configuration/restart ordering using observable calls, without requiring
the implementation to adopt a particular class hierarchy.

## Vary: production transfer

After your first attempt, choose one variation at a time:

- Configuration succeeds remotely but restart times out. Define what the caller can know
  and whether retry is safe; splitting methods cannot create rollback.
- A partner renames its measurement operation and returns a documented structured value.
  Decide where translation belongs without changing the report's stable behaviour.
- An administrative client now needs firmware installation. Explain which clients should
  absorb the new requirement and which should remain unaffected.

## Interview checkpoint

Ask one question at a time. Start with: **“Which dependency is unnecessarily broad here,
and what evidence supports that conclusion?”** Review the missing reasoning step before
offering code. A green test count alone is not a successful answer.

## Troubleshooting

- Run the supplied entry-point paths from the repository root; do not import hyphenated unit folders.
- If mypy is missing, complete the locked dev synchronization before running the experiment.
- If the repository validator finds ignored caches, use a clean Worktree and external caches;
  do not delete an existing environment or weaken the validator.
- Existing units reuse some test-module names. Run repository regression one unit per pytest
  process, as documented in the maintainer validation record.

## Review and closure

No learner review or completed solution exists. Add a learner-specific `REVIEW.md` only at
the first actual review. Closure requires preserved attempt evidence, applicable acceptance
tests, explanation of edge cases, a rejected alternative, and a new-scenario judgment.
Do not create a comparison solution before Rahul closes the exercise.
