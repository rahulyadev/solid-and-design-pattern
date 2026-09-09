# EXP-01 — Shape and meaning at the Adapter boundary

This controlled teaching experiment supports SDP-STR-010 without changing its canonical E+I+D+T
evidence profile. It is maintainer evidence, not a learner attempt or performance benchmark.

## Question and hypothesis

Can a reader satisfy a static signature yet return the wrong unit? Can runtime protocol presence
accept a method whose required arguments make the intended call fail? Predict both before execution.

The fixed synthetic warehouse has two cases of six bolts, and demand is ten individual bolts.
`WarehouseAdapter` translates this correctly. `CountsCases` returns two with the same annotated
signature. `WrongSignature` has a `read` attribute but requires an extra argument.

## Command and environment

From the repository root using the `/tmp` exports in the unit README:

```bash
python units/structural/SDP-STR-010-adapter/examples/boundary_probe.py
```

Actual runtime versions, output, type-check results, and execution dates are recorded in the
[validation record](../../VALIDATION.md) after execution. The five fields below are predictions
until matched against that record.

```text
converted_units=12
converted_decision=enough
signature_only_decision=short
runtime_shape_accepts_wrong_signature=True
actual_call_raises_type_error=True
```

## How to read this visual

Read the first three rows as a comparison at the same demand. Read the last two as successive
runtime steps: attribute presence succeeds, then the actual call fails.

## Key insight

Static signatures, runtime presence, and semantic compatibility are distinct evidence layers.

## Simplification or limitation

This is a conceptual observation table for deterministic local objects. It does not establish that
all protocol checks behave identically across Python versions; lookup changed in 3.12. It does not
simulate a network, races, throughput, authorization, or SDK compatibility. The canonical note cites
the language/library/specification sources and discusses where behavior tests are still required.
