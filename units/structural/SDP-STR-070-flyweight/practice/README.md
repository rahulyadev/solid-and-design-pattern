# Practice — SDP-STR-070 Flyweight

| Field | Value |
|---|---|
| Unit note | [SDP-STR-070](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-str-070) |
| Evidence target | E+I+D+X+T |
| Attempt required before solution | Yes |
| Test command | `python -m pytest -q -p no:cacheprovider` from this directory |
| Status | Not attempted |

## Learning question

Can a report batch reuse repeated legend content without coupling row edits or retaining all
previous reports indefinitely? Decide whether a factory is justified before building one.

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

[legend_lab.py](legend_lab.py) is runnable. [test_legend_lab.py](test_legend_lab.py) characterizes
current behavior only; its passing result does not prove the requested redesign.

## Problem and change pressure

The starter creates independent mutable legend dictionaries. A new feed includes thousands of
rows whose legends repeat by language and publication revision. A row has its own text, ID and
highlight state. The repeated legend content must remain stable during a report. A subsequent report
may load a new revision without changing rows already issued by an earlier report.

Design the smallest representation and ownership rules you can defend. The worked grid code is
background only; this exercise has different text, update and report-lifetime requirements. No
particular class names, dictionary layout or factory algorithm is required.

## Expected observable behavior

- Keep row IDs, order and exact text, including empty and Unicode text.
- Editing one row's text or highlight does not change another row's observations.
- Rows rendered from an old report continue showing their original legend after a later revision.
- Equal legend inputs within the chosen sharing scope can reuse stable content where justified.
- Reject invalid inputs with a stated error policy; state how each report releases its ownership.

## Required edge cases

Empty batch, one row, all distinct legends, equal legends in different languages, revision changes,
repeated values after a report ends, conflicting content for the same purported identity, and a
caller trying to alter nested content. Define whether equality of displayed text is enough to share.

## Prediction before running

Write predicted outputs, which objects own each value, one suspected aliasing hazard, and why the
baseline may pass while the target requirement is unmet. Preserve this prediction with the attempt.

## Commands

Use the `/tmp` environment settings in [validation](../VALIDATION.md) before running. From this
directory, with the selected Python runtime:

```bash
python legend_lab.py
python -m pytest -q -p no:cacheprovider
```

Record actual output. The starter deliberately reports `target_complete=False`. Its independent
mutable-legends test is a characterization of the old design, not an instruction to keep per-row
copies in the redesign. Preserve the original module and reasoning before modifying a separate
attempt file. Do not set the marker to true merely to make a status test pass.

## Observe and explain

Which values currently repeat? Which mutations are isolated now? What breaks if someone merely
reuses the mutable dictionary? Which observations must stay stable during refactoring? State the
first missing reasoning step before requesting a hint.

## Refactor

Implement your proposed contract in a separate attempt, add behavioral edge-case tests, and justify
key equivalence and lifetime. Choose and reject at least one simpler alternative. Tests should
assert promised behavior rather than prescribe the internal storage.

## Vary and transfer

After the first attempt, consider report cancellation and an input where nearly every legend differs.
Predict how the chosen design behaves. Reproduce the worked controlled allocation experiment and
explain which measurements would need to change for your text workload. Do not copy its byte results
into a claim about the lab.

## Rahul's attempt and review

No attempt, result, hint or reviewer conclusion has been supplied. Hints are given one at a time
only when requested. Closure and optional comparison solution are added only after Rahul closes
the exercise. The tracker remains Not started until the appropriate evidence exists.
