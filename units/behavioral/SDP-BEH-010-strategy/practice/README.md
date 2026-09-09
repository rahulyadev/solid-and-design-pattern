# Practice — SDP-BEH-010 Strategy

| Field | Value |
|---|---|
| Unit note | [SDP-BEH-010](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-beh-010) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Status | Not attempted |
| Test command | `python -m pytest -q -p no:cacheprovider units/behavioral/SDP-BEH-010-strategy/practice` |

## Learning question

Can you make a packing decision replaceable while preserving one input/output contract, and explain
when a plain function is sufficient? This is synthetic capacity arithmetic, not a real packaging
optimizer. Do not import or adapt the worked job-ordering implementation as the lab solution.

## Starter files

- [packing_lab.py](packing_lab.py): runnable consecutive-packing baseline.
- [test_packing_lab.py](test_packing_lab.py): baseline characterization only.

## Problem and change pressure

The starter accepts a typed tuple of integer item sizes and an integer capacity. Capacity is 1–20;
there are at most 40 items, each 1–capacity. Bool is rejected. It walks items in arrival order and
starts a new group when the next item will not fit the current one. Empty input returns no groups.

Add a selectable **first-fit** policy: visit items in input order, place each into the earliest
existing group with enough remaining capacity, and open a group only when none can accept it.
Preserve insertion order within each group and group creation order. For `(6, 6, 4, 4)` at capacity
10, consecutive packing yields `((6,), (6, 4), (4,))`; first-fit must yield `((6, 4), (6, 4))`.
Neither rule promises the minimum possible number of groups for every input.

The stable contract is a tuple of nonempty groups, each within capacity, containing every input
item occurrence exactly once. Repeated sizes represent separate items. Global flattened arrival
order is a property of consecutive packing, not a shared promise of both algorithms. Invalid
input must fail before running the chosen rule. Preserve `pack`'s existing two-argument behavior.
Do not prescribe public classes until you can defend why the new requirements need them.

## Lab cycle

1. **Predict:** Write the baseline result and trace the two responsibilities: contract handling
   and group choice. Predict which rule changes the number of groups in the given case.
2. **Run:** Execute the starter and its tests. Record your actual output before editing.
3. **Observe:** Explain why baseline tests pass while selectable first-fit is still absent. Write
   black-box tests for the new requirements; do not make tests depend on a proposed class structure.
4. **Explain:** State the common meaning of input, output and errors. Identify which ordering
   promise must not be imposed on every implementation. Compare a callable with an object contract.
5. **Refactor:** Preserve your initial attempt and reasoning before revising. Add the seam and
   selection boundary you chose; retain the old two-argument behavior and validate both policies.
6. **Vary:** A consumer adds “at most two items per group.” Specify whether this is common input,
   policy configuration or a different contract. Explain the change before writing more code.

## Edge cases and review targets

Cover empty input, one item, an exact-capacity item, repeated sizes, all items fitting together,
multiple groups, invalid capacity, invalid sizes, the 40-item boundary and a policy failure. Check
multiplicity, not just a set of sizes. An empty group is invalid even if all items are present.
State how unknown choices and malformed policy results behave; add tests for that decision.

For D evidence, identify the first failed assumption in your own attempt with the smallest exposing
case. A design can pass a happy-path example while confusing group order, item occurrence, validation
ownership or selection. Do not replace the original attempt with a polished answer.

For T evidence, a service wants a preview and a committed packing plan to use the same rule revision.
Explain where selection occurs, what configuration is recorded, who owns request state, and what
happens when a policy fails. This does not require building a server or database.

## Commands

From repository root with the locked development interpreter selected:

```bash
export PYTHONDONTWRITEBYTECODE=1
export MYPY_CACHE_DIR=/tmp/sdp-beh-010/mypy-lab
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-beh-010/hypothesis-lab
mkdir -p /tmp/sdp-beh-010/pytest
python units/behavioral/SDP-BEH-010-strategy/practice/packing_lab.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-beh-010/pytest/lab \
  units/behavioral/SDP-BEH-010-strategy/practice
```

## Attempt, hints and closure

No learner attempt, hints, review or solution exists yet. Record your prediction, code, rejected
alternative, actual test output and remaining question. Ask for one progressive hint after trying.
Do not toggle `target_complete()` to simulate learning or claim success from the baseline tests.

The review should ask one focused question about the first missing reasoning step. Only after Rahul
closes the exercise should a comparison solution or progress evidence be added. Keep generated
state under `/tmp`; run this pytest directory independently if unrelated units reuse module names.
