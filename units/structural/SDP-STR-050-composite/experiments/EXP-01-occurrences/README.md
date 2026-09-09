# EXP-01 — Count occurrences or identities?

| Field | Value |
|---|---|
| Owning unit | [SDP-STR-050](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-str-050) |
| Precise question | Does an aliased recipe contribute once per object or once per occurrence, and can a small DAG expand into too much work? |
| Classification | Design-level policy observed with Python identity and value objects |
| Status | Reproduced |

## Why observe this?

A diagram drawn as a tree can hide shared references. Numerically identical totals can come from
two distinct equal tasks or two references to the same task. Observing both visits and identities
makes that ambiguity visible without pretending identity alone defines the business meaning.

## Hypothesis and controls

A leaf contributes once for each occurrence. Empty groups contribute no leaves. Reusing a group
expands all its leaves for each inclusion. The supplied occurrence bound should reject repeated
binary doubling before the height limit is reached.

Controlled: the same Task/Group implementation, pure integer estimates, child order, and fixed
inputs. Changed: leaf/group structure, identity sharing, and doubling level. Measured: unique live
task identities, leaf visits, minutes, occurrence paths, first rejected level and last admitted
expanded-node count. No elapsed time, allocation, construction cost or external action is measured.

## Environment and reproduction

Observed on 2026-09-09, Linux 7.0.0-31-generic, x86_64, glibc 2.43:

```text
CPython 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
CPython 3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]
```

The probe uses the standard library only. Executables:
`/home/parry/projects/solid-and-design-pattern/.venv/bin/python` and
`/tmp/sdp-cre-040/venv311/bin/python`. No environment was modified. Both produced the same output.

From the repository root with the chosen Python and all cache settings from
[VALIDATION.md](../../VALIDATION.md):

```bash
python units/structural/SDP-STR-050-composite/examples/occurrence_probe.py
```

## Actual output

```text
leaf: unique=1, visits=1, minutes=12, paths=((),)
empty: unique=0, visits=0, minutes=0, paths=()
distinct equal: unique=2, visits=2, minutes=24, paths=((0,), (1,))
same leaf twice: unique=1, visits=2, minutes=24, paths=((0,), (1,))
same group twice: unique=2, visits=4, minutes=30, paths=((0, 0), (0, 1), (1, 0), (1, 1))
doubling: rejected_level=13, last_occurrences=8191
```

## Visual interpretation

| Structure | Unique task objects | Task occurrences | Estimate in minutes |
|---|---|---|---|
| Leaf | 1 | 1 | 12 |
| Empty group | 0 | 0 | 0 |
| Distinct equal leaves | 2 | 2 | 24 |
| Same leaf twice | 1 | 2 | 24 |
| Same two-task group twice | 2 | 4 | 30 |

**How to read:** compare the two middle columns before reading the total. “Unique” counts live
identities; “occurrences” counts paths to leaves. **Key insight:** same total does not imply same
identity structure. **Limitation:** this is a controlled observation table, inspected as text and
asserted by tests; it is not browser-rendered, a graph visualization or a benchmark.

At doubling level k, expanded nodes follow N(k) = 1 + 2 × N(k−1), with N(0) = 1. Level 12 has
8,191 occurrences, although construction retains only 13 distinct nodes along that sharing chain.
Level 13 would require 16,383 occurrences and is rejected by the 10,000 bound. Height would be only
13; a depth limit alone would not control expanded work. This recurrence is analysis of the code.

## Design conclusion and limits

The observations agree with the chosen occurrence policy. A global deduplication set would answer
a different question, so it is not a correctness optimization for this model. A production system
for unique real tasks would need its own entity rules, IDs and aggregation contract.

The identity set keeps references alive during counting. No numeric identity values are exported.
The probe covers constructed acyclic values only; it does not validate arbitrary graphs, mutate
nodes, measure recursion exhaustion, prove thread safety or acquire resources. These observations
support explanation/debugging and do not alter the canonical E+I+D+T profile or learner progress.

## Sources and implementation

- [Python object identity and container references](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types): identity is distinct from value; integer identity values are not business IDs.
- [occurrence_probe.py](../../examples/occurrence_probe.py) and [test_composite.py](../../examples/test_composite.py): original controls, recurrence limit and assertions for every documented observation.
