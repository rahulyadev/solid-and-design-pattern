# Practice — SDP-STR-060 Bridge

| Field | Value |
|---|---|
| Unit note | [SDP-STR-060](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-str-060) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Status | Not attempted |
| Test command | `python -m pytest -q -p no:cacheprovider units/structural/SDP-STR-060-bridge/practice` |

## Learning question

Can two trail-guide choices evolve separately, and when would plain functions be enough?
The [starter](trail_lab.py) is deliberately only a walking text guide. The [tests](test_trail_lab.py)
characterize existing behavior; their success does not mean the exercise is complete.

## Problem and change pressure

A fictional park now offers walking and step-free stop lists, each requested as text or JSON.
Walking keeps every stop. Step-free excludes stops marked `stairs=True`. Both preserve source
order and repeated names; this is a stop-list exercise, not a route-finding or accessibility claim.
The text contract joins retained names using ` -> `, with empty input producing an empty string.
The JSON contract is an array of retained names, including an empty array for no retained stops.
Parsing JSON must recover the names exactly, including quotes, newlines and Unicode.

No public class structure is prescribed. Preserve the current `WalkingTextGuide.render` behavior.
Do not import the worked inventory example. Choose and defend a design; do not merely rename it.

## Lab cycle

1. **Predict:** Before execution, write the current output and explain which responsibility owns
   stop selection and which owns text production. Predict where four subclasses would duplicate work.
2. **Run:** Use the commands below and record your own actual output.
3. **Observe:** Contrast the passing baseline with the missing three combinations. Passing old tests
   is not evidence of new behavior. Create black-box acceptance tests for the requirements above.
4. **Explain:** Sketch the dependencies, state the semantic contract and justify which variations
   are independent. Compare two ordinary functions with a Bridge using objects.
5. **Refactor:** Preserve your original attempt separately before revising. Implement your choice;
   cover empty input, all stairs, mixed stops, repeated names, ordering and special characters.
6. **Vary:** The park asks for a quiet-stop guide (using a new explicit attribute) and a new output
   requested by a consumer. Specify both contracts before coding. Show which existing code changes.

## Commands

From the repository root, after selecting the locked Python environment:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-060/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-060/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-060/hypothesis
mkdir -p /tmp/sdp-str-060/pytest
python units/structural/SDP-STR-060-bridge/practice/trail_lab.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-060/pytest/lab \
  units/structural/SDP-STR-060-bridge/practice
```

## Attempt and review boundary

No learner attempt, hints, review or solution exists yet. Ask for one progressive hint only after
an attempt. Record your prediction, code, rejected alternative, actual test output and remaining
question. Do not flip `target_complete()` just to make the status look complete.

A review first identifies the missing reasoning step: independence, semantic preservation,
configuration, or failure ownership. It then asks one focused follow-up. Do not replace the original
attempt. A senior transfer answer should discuss a consumer that needs a richer structure than a
list of names; explain whether the common contract survives instead of promising arbitrary formats.

## Troubleshooting and closure

Run this directory independently if other units have modules with the same test filename. Keep all
caches under `/tmp` and disable pytest's cache provider. Closure requires the implementation, edge
cases and design explanation from Rahul. Only then add evidence links and consider learning state.
