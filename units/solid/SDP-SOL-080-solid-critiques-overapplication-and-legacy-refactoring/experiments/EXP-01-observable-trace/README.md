# EXP-01 — Same outcome, different observable behaviour

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-080](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-080) |
| Precise question | Does moving all formatting before all writes preserve the exporter's observable behaviour? |
| Classification | Python language execution plus an explicit synthetic application contract |
| Status | Interpreted by maintainer; no learner attempt recorded |

## Why observation is necessary

A successful fixture can hide when input was consumed and what was already written when
a later operation failed. The old function and an eager rewrite can return the same count
or raise the same error while interacting differently with their collaborators.

The [probe](../../examples/trace_probe.py) uses the actual worked implementations in
[name_export.py](../../examples/name_export.py). It lives beside them so both the script
and tests can use ordinary imports without path manipulation.
[Counterexample tests](../../examples/test_trace_probe.py) check the important differences.

## Hypothesis

> Extracting one formatting helper will preserve the observed sequence. Buffering the
> formatted lines will move source reads ahead of writes, changing failure effects or
> input consumption even when the final outcome matches.

This is the maintainer's experiment hypothesis. Rahul should record his own prediction
before running it as a learning exercise.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Canonical sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
Compatibility sys.version: 3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]
sys.implementation.name: cpython on both
sys.implementation.cache_tag: cpython-314 / cpython-311
Runtime dependencies: standard library only
Test tool: pytest 8.4.2 from the repository lock
Relevant flags: -B or PYTHONDONTWRITEBYTECODE=1; no optimization flag
```

## Controls and variables

- Controlled: the formatting rule, source values, sink operation, and observation fields.
- Changed: legacy, extracted, or eager implementation; one of five controlled scenarios.
- Measured: returned count or exception, values yielded, write attempts, saved lines, event order.
- Each observation gets a fresh source and recorder. No state is shared between candidates.
- “Read” means a value yielded to the consumer; the probe does not count failed `next` calls.

## Reproduction command

Use the external-environment setup in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring/examples/trace_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-080-solid-critiques-overapplication-and-legacy-refactoring/examples/test_trace_probe.py
```

Use `--json` on the probe to obtain all recorded fields, including the full trace. The
interactive visual embeds that JSON as static teaching data. It does not execute Python.
Repeat with the guide's separate Python 3.11 environment and `uv run --locked --python 3.11`.

## Predicted result

All successful versions save the same three lines. The extraction matches the original
on every selected observation. Eager formatting loses prefix writes on validation or
source failure and reads an extra name before a writer failure.

## Observed result

Both CPython 3.14.7 and 3.11.16 produced the following output:

```text
success
  legacy: return 3; read=3; attempted=3; saved=['[MIRA]', '[OMAR]', '[ASHA]']
  extracted: return 3; read=3; attempted=3; saved=['[MIRA]', '[OMAR]', '[ASHA]']
  eager: return 3; read=3; attempted=3; saved=['[MIRA]', '[OMAR]', '[ASHA]']
empty-name
  legacy: ValueError: empty name; read=2; attempted=1; saved=['[MIRA]']
  extracted: ValueError: empty name; read=2; attempted=1; saved=['[MIRA]']
  eager: ValueError: empty name; read=2; attempted=0; saved=[]
source-failure
  legacy: RuntimeError: source unavailable; read=1; attempted=1; saved=['[MIRA]']
  extracted: RuntimeError: source unavailable; read=1; attempted=1; saved=['[MIRA]']
  eager: RuntimeError: source unavailable; read=1; attempted=0; saved=[]
sink-before
  legacy: OSError: writer unavailable; read=2; attempted=2; saved=['[MIRA]']
  extracted: OSError: writer unavailable; read=2; attempted=2; saved=['[MIRA]']
  eager: OSError: writer unavailable; read=3; attempted=2; saved=['[MIRA]']
sink-after
  legacy: OSError: acknowledgement lost; read=2; attempted=2; saved=['[MIRA]', '[OMAR]']
  extracted: OSError: acknowledgement lost; read=2; attempted=2; saved=['[MIRA]', '[OMAR]']
  eager: OSError: acknowledgement lost; read=3; attempted=2; saved=['[MIRA]', '[OMAR]']
```

## Interpretation

1. Final outcomes match within every scenario, including errors. Those checks alone miss
   incompatible interactions.
2. The successful eager trace starts with three reads. The original reads, calls, and saves
   the first line before reading the second. The summary counts do not show this ordering.
3. On a late empty name or source failure, eager formatting has not called the sink at all.
4. Both writer-failure cases leave the third name unread in the original and consumed in
   the eager version. A source read may itself be meaningful work.
5. The sink-after case saves the second line and raises. That observation disproves the
   assumption “exception means no side effect,” but does not model a real network protocol.
6. Matching these observations is evidence for the extraction on these cases, not proof
   over all inputs. Separate fixed expected-value tests reduce reliance on the old code alone.

## Visual interpretation

```text
original: read Mira -> call -> save -> read Omar -> call -> save -> error
eager:    read Mira -> read Omar -> read Asha -> call -> save -> call -> save -> error
```

### How to read this visual

Read each row left to right for the sink-after case. The second call saves its line and
then raises. Arrows indicate sequence, not duration.

### Key insight

An equivalent final exception can conceal different source consumption.

### Simplification or limitation

This is a condensed literal trace from synchronous in-memory code. It omits line arguments,
uses no actual device, and measures neither latency nor distributed delivery guarantees.

## Design conclusion

Extract the rule while leaving its execution at the same point in the operation. Choose
buffering only after explicitly deciding its input, memory, and failure contract. Separating
responsibilities on paper does not justify changing effects under the name “refactoring.”

## Limitations

- The input is finite; no real stream, database, network, thread, or transaction was used.
- Unicode property tests broaden successful inputs but are not an exhaustive equivalence proof.
- The eager version is an intentional counterexample. Its differences are asserted by passing
  tests, not hidden behind skipped tests or expected-failure markers.
- The observation boundary is explicit. Another caller may permit read-ahead; that would be
  a different contract, not evidence that this trace is wrong.

## Sources

1. [Python language reference: for statement](https://docs.python.org/3.14/reference/compound_stmts.html#the-for-statement) — item retrieval and loop body execution.
2. [Fowler: definition of refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) — preservation of observable behaviour.
