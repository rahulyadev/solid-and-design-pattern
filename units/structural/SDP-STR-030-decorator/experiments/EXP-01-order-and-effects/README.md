# EXP-01 — Wrapper order and observation scope

## Question and hypothesis

Does changing wrapper position alter output, measurement, and failure visibility even when every
object satisfies the same signature? Prediction: formatting order changes where the label appears;
observation inside formatting measures the base result, outside measures the final result; ordinary
observer failure is optional under the explicit Observed policy, while source failure remains visible.
This controlled experiment supports E and D without changing SDP-STR-030's E+I+D+T profile.

## Environment and command

Initial run: CPython 3.14.7, Linux, 2026-09-09. The example is standard-library only; all generated
state is routed to `/tmp/sdp-str-030`. The final cross-version record is in
[VALIDATION.md](../../VALIDATION.md). From the repository root:

```bash
python units/structural/SDP-STR-030-decorator/examples/order_effects_probe.py
python units/structural/SDP-STR-030-decorator/examples/function_wrappers.py
```

## Actual initial output

```text
label_outside | note: [ready]
bracket_outside | [note: ready]
observe_inside | [note: ready] | 5
observe_outside | [note: ready] | 13
observer_failure | ready | dropped=1
source_failure | KeyError | error
lifetime | calls=6 | closes=1
```

The separate function probe prints:

```text
evaluate:outer,evaluate:inner,apply:inner,apply:outer,enter:outer,enter:inner,body,exit:inner,exit:outer
```

## Observation table

| Controlled change | Observed result | Interpretation |
|---|---|---|
| Label outside bracket | `note: [ready]` | Prefix is added after the inner bracket result |
| Bracket outside label | `[note: ready]` | Brackets enclose the labeled result |
| Observer immediately around base | Final display unchanged, count 5 | That layer sees only source characters |
| Observer outside formatting | Final display unchanged, count 13 | That layer sees final presentation characters |
| Observer raises OSError | Source text returned, dropped=1 | Explicit best-effort diagnostics policy |
| Source key missing | KeyError with error observation | No fabricated success and no automatic retry |
| Root closes after six requests | Calls=6, closes=1 | Every source attempt counts, including the missing key |

### How to read this visual

Each row changes one placement or fault relative to the synthetic base. Counts are Unicode code
points at the observation layer, not bytes or durations. The function trace separates expression
evaluation, decorator application, and invocation; it is not the object-construction trace.

### Key insight

A compatible method signature permits composition, but only an explicit contract tells you whether
the output, effects, failure policy, and measured scope are correct for that client.

### Simplification or limitation

These are deterministic text observations, not a browser rendering or a performance experiment.
The leaf is an in-memory snapshot with infallible close. There is no live service, mandatory audit,
concurrent execution, async cancellation, retry engine, or durability model. BaseException paths are
covered separately by tests; this table does not claim an observer can never interrupt control flow.

## Reconstruction prompt

Before changing code, predict one new order and draw the return path. Then explain which contract
would fail if Observed rendered twice. Record your own prediction and result separately; the
maintainer's output above is not learner evidence or a solution to the quote lab.
