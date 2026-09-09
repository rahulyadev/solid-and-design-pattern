# Practice — SDP-BEH-020 State

| Field | Value |
|---|---|
| Unit note | [SDP-BEH-020](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-beh-020) |
| Evidence target | E+I+D+T; connect the separate X observation to the failure discussion |
| Attempt required before solution | Yes |
| Test command | `python -m pytest -q -p no:cacheprovider` |
| Status | Not attempted |

## Learning question

Can a reading station preserve ownership while its allowed actions change, without repeating a
growing status switch in every operation?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

[reservation_lab.py](reservation_lab.py) is a working direct baseline. Its four
[baseline tests](test_reservation_lab.py) do not implement or test the new requirements. There is
no reference solution, hidden finished implementation, or hint sequence in this folder.

## Problem and change pressure

The baseline has FREE, HELD and OCCUPIED. Reserve, enter and leave require a valid lifecycle and
exact owner match. Preserve those observations while adding these requirements:

- The holder may cancel a HELD station, freeing it; cancellation while OCCUPIED is forbidden.
- The occupant may pause, producing PAUSED while retaining ownership. PAUSED cannot be reserved,
  entered, or cancelled. Only the same owner may resume to OCCUPIED or leave to FREE.
- Every rejection leaves both status and owner unchanged. FREE has no owner; all other statuses
  have the current nonblank owner. Inputs are typed strings, and owner matching is exact.
- Existing public observations remain available, but callers must not be able to use normal public
  assignment to bypass the new invariants. Explain any necessary API migration.

Start with a transition matrix and invariants. Decide whether an enum/table or State objects fit
best; justify the decision with the new behavior. Do not mechanically copy the packet's classes:
this station cycles back to FREE and must preserve a caller's ownership across intermediate phases.

## Required edge cases

Check each new operation in every status, wrong owners, repeated pause/resume/cancel, empty names,
a reservation after leaving, and two independent stations. Demonstrate that a stale owner cannot
leave a station that has since been reserved by somebody else. Keep tests about observable behavior,
not the number of classes or exact private attribute names.

## Commands

Use the complete `/tmp` cache controls in [VALIDATION.md](../VALIDATION.md), then from this folder:

```bash
python reservation_lab.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-beh-020/pytest/practice
```

Create the basetemp parent first. The baseline prints `free, owner=None` and
`target_complete=False`; the second line is a reminder, not a result of a solution checker.
Record your own actual output. The author's validation is not your attempt.

## Predict before running

Write your expected states/owners for reserve → enter → wrong-owner leave → correct-owner leave.
Then predict the first failing behavior if a new PAUSED label is added without changing operations.
Explain where lifecycle and ownership rules would be duplicated.

## Rahul’s attempt

No attempt or reasoning supplied yet. Preserve the original code and explanation before editing
an attempted solution. Add actual commands, output, rejected alternative and first incorrect
assumption only when Rahul supplies evidence.

## Observe and explain

After running the baseline, identify which operation changes owner, which changes only status,
and why every rejected action must preserve both. After your change, choose the smallest case that
would expose a forgotten ownership guard. Explain why passing only baseline tests is insufficient.

## Refactor

Characterize the behavior before moving it. Introduce one coherent responsibility boundary, then
move one operation/phase at a time. Keep normal public APIs from installing impossible states.
Compare the resulting change cost with one simple table-based implementation sketch in prose.
Do not add factories, registries or persistence unless a requirement needs them.

## Vary and production transfer

After the first implementation, consider an explicit EXPIRE action allowed only for HELD
reservations. Supply the expiration decision as input; do not read a wall clock in unit tests.
Decide who is authorized to expire and what happens when EXPIRE races with entry in a backend.
Explain the missing storage/serialization boundary; no network service is required.

## Progressive hints, review and closure

No hints have been released. Ask for one hint at a time after recording your first attempt. Review
must identify the exact missing reasoning step before replacement code. Keep this lab Not attempted
until actual learner evidence exists; add closure and any comparison solution only after Rahul
closes the exercise.

## Troubleshooting

Run this directory in its own pytest process to avoid collisions with other educational modules.
If an operation rejects unexpectedly, record status and owner before the call and the specific guard
that failed. Do not fix a guard failure by directly assigning a new status.
