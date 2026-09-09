# Unsolved sensor lab — SDP-CRE-050

A sampling tool opens a synthetic sensor for each reading and closes it immediately. That baseline
works. New requirements introduce sharing during a sampling window, independent stations, failed
startup, and cancellation. Decide the identity and lifetime contract before choosing a pattern.

The worked report examples are not a target implementation for this exercise. No target API,
constructor layout, provider recipe, solution file, or implementation-oriented target fixtures are
supplied. Preserve `sensor_lab.py` and baseline tests; put your first attempt and original predictions
in separate files. Later corrections must not erase your original reasoning.

## Predict → run → observe → explain → refactor → vary

1. **Predict:** Draw creation/use/close for two calls to `sample`. Identify which objects can be
   shared now. Predict what a global cached Sensor would change after the first call closes it.
2. **Run:** Execute the unchanged starter and baseline tests using the commands below.
3. **Observe:** Record actual output, acquisition counts, closed-state behavior, and the environment.
   Preserve any disagreement with your original prediction.
4. **Explain:** State the required scope, who owns shutdown, and what a global Singleton would hide.
   State why the baseline tests passing does not fulfill the new requirements.
5. **Refactor:** Choose an interface and implement the target behavior below in your own attempt.
   Write black-box tests for ownership, failures, identity where meaningful, and isolation.
6. **Vary:** Choose one changed requirement after review. Revise the contract before changing code.

## Target behavior

- During one sampling window, two consumers can reuse one usable sensor for a station.
- Two windows for different stations can coexist in one interpreter without stale configuration or
  interference. Make an explicit decision about two concurrent windows for the same station.
- The owner rejects an invalid station before publishing a usable capability.
- Acquisition failure publishes no partial sensor; retry semantics are stated and tested.
- Consumers cannot close another active window's sensor. Work finishes before its sensor is closed.
- After shutdown, retained consumer references cannot silently continue successful readings.
- Temporary failures must not make unrelated stations fail or inherit another station's identity.
- Record a synthetic lifecycle trace without exposing credentials or user-specific data.

Choose construction, explicit dependencies, provider, module, or a reasoned combination. A class
Singleton is not a grading requirement. Include a rejected alternative and the invariant it violates.
Baseline tests only check today's `sample` and `Sensor` behavior; design your own target tests.

## Commands

From the repository root, use a locked development interpreter as `python` and the all-cache-to-`/tmp`
exports in the [unit commands](../README.md#20-run-and-study). Then run:

```bash
python units/creational/SDP-CRE-050-singleton/practice/sensor_lab.py
python -m pytest -p no:cacheprovider units/creational/SDP-CRE-050-singleton/practice
```

The starter prints `north:ready` and `target_complete=False`. No learning state changes follow from
running it. Ask for one progressive hint at a time only after making a prediction or attempt.

## Later variations and review

Choose one at a time: sensor acquisition becomes async and can be cancelled halfway through;
readings arrive from two OS threads; the external provider imposes a process-local handle limit;
configuration rotates while a window is active; cleanup itself fails; four worker processes start.

Before implementation review, explain the first ownership edge that changes. A review should name
the exact missing step (for example, who cleans up a resource before acquisition returns), then ask
one focused follow-up. Completion needs your preserved attempt, applicable tests, edge cases, and
explanation. Delayed recall and independent transfer are separate evidence.
