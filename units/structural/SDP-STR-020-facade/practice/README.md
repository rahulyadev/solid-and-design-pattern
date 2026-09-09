# Unsolved import preflight lab — SDP-STR-020

Two clients preview an import by inspecting files and reading available capacity. The baseline is
runnable but both clients own the same calculation. A new requirement makes preflight a shared task:
unsupported files must be reported, and “fits” alone no longer means “ready.”

This is a read-only planning exercise, with no archive writes, report generation, or network calls.
There is no solution file. `build_preflight` intentionally raises `NotImplementedError`; its `object`
return annotation is a temporary boundary for you to replace with your own result contract.

## Predict

Before running, write what each baseline client prints for the provided file. Predict the current
answer for an unsupported file that fits in capacity. Explain what that answer fails to tell a user.
Draw which clients know the inspection and capacity APIs.

## Run

From the repository root with an existing locked interpreter and cache exports from the unit note:

```bash
python units/structural/SDP-STR-020-facade/practice/import_lab.py
mkdir -p /tmp/sdp-str-020/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-020/pytest/lab units/structural/SDP-STR-020-facade/practice
```

## Observe

The demo prints a CLI summary, a dictionary, and `target_complete=False`. Baseline tests check current
behavior and confirm the target is unsolved. Passing them proves no exercise completion.

## Explain

Identify the repeated subsystem knowledge. Which changes belong to planning, and which belong to
presentation? Explain why a supported diagnostics caller may still inspect individual files directly.
Decide whether one function is enough or retained dependencies justify an object; state the force.

## Refactor — public target contract

Preserve your original attempt separately before changing it. Design and implement one common
preflight entry point. Its result must let both clients present the same facts:

- Total file count and total required bytes include **all** inspected files.
- Unsupported filenames are reported in inspection order; duplicate names remain separate entries.
- `fits` means total bytes are at most remaining capacity, including equality.
- `ready` means all files are supported and capacity suffices; an empty batch is ready when capacity
  is nonnegative. A zero-byte unsupported file still prevents readiness.
- Negative size or negative remaining capacity is invalid. Do not coerce malformed values into a
  plausible successful plan. Define where runtime validation belongs for these owned inputs.
- Preflight does not reserve capacity or import files. Repeated calls recompute observations, and a
  result does not promise capacity will still be available at import time.
- Unexpected collaborator exceptions remain visible; do not report readiness after a failed read.

Move both presentation clients to the common task result. Choose a concrete immutable result shape
and useful typed seams. Add your own behavior tests, including exact capacity, empty input, duplicates,
unsupported zero-byte input, negative inputs, repeated observations, and failure. Update the
“exercise starts unsolved” baseline test only after preserving the original attempt. Do not keep a
test that requires `NotImplementedError` once you deliberately implement the target.

## Vary

The capacity subsystem now also reports a revision token. Explain whether displaying that revision
makes the plan an atomic reservation. Then one client needs raw metadata diagnostics: design the
smallest supported access path without making the common facade mirror every inspector operation.
No reference implementation or progressive hints are included. Request one hint at a time after an
attempt; review should identify the first missing reasoning step before replacement code.

## Done means evidence

Provide your attempt, actual test results, one before/after dependency sketch, an explanation of
function versus object, and a changed-requirement critique. The lab's source being present is not
implementation evidence. Record learning state only after the repository's evidence thresholds are met.
