# EXP-01 — Copy graph topology

## Question and hypothesis

Can a result be independent from the source while still sharing a child internally? What changes
when each child is copied separately? Hypothesis: one deep traversal isolates the source while
preserving repeated edges and rebasing the cycle; separate traversals break the internal alias.

## Controlled input

An original synthetic query root has two edges to one filter node. That child has tags `[base]` and
one back edge to the root. Each scenario gets a fresh input graph. The only mutation after creation
appends `edit` through result edge 0. No random inputs, external services, timings, memory addresses,
or global memo are involved.

## Predict first

Before running, draw the five results: assignment, shallow, deep, replacement of the root label,
and separate deep copies of the two children. Record whether the second child's tags change and
whether the source changes. Preserve this prediction even if wrong. These maintainer observations
are not a substitute for your own experiment evidence.

## Environment and commands

Maintainer execution date: 2026-09-09. The probe ran on CPython 3.14.7 and CPython 3.11.16
with identical observations. Complete quality-check results are recorded in [VALIDATION.md](../../VALIDATION.md).
Use a locked development interpreter; select Python 3.11 and 3.14 separately when reproducing.

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-cre-040-experiment/bytecode
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-cre-040-experiment/hypothesis
export MYPY_CACHE_DIR=/tmp/sdp-cre-040-experiment/mypy
export RUFF_CACHE_DIR=/tmp/sdp-cre-040-experiment/ruff
export UV_CACHE_DIR=/tmp/sdp-cre-040-experiment/uv
export COVERAGE_FILE=/tmp/sdp-cre-040-experiment/coverage
python units/creational/SDP-CRE-040-prototype/experiments/EXP-01-copy-graph/copy_graph_probe.py
python -m pytest -p no:cacheprovider units/creational/SDP-CRE-040-prototype/experiments/EXP-01-copy-graph
```

## Actual output, compacted without changing values

The script emits JSON. Here each row preserves its field order after `mode`:
`root_fresh`, `child_shared_with_source`, `internal_alias_preserved`, `cycle_rebased`,
`source_tags_after`, `second_child_tags_after`.

```text
assignment   false true  true  false [base, edit] [base, edit]
shallow      true  true  true  false [base, edit] [base, edit]
deep         true  false true  true  [base]       [base, edit]
replace      true  true  true  false [base, edit] [base, edit]
split-memos  true  false false false [base]       [base]
```

## Interpretation

The hypothesis holds for this graph. A shallow copy and replacement keep the original child. A deep
copy creates one independent shared child and a back edge to the returned new root. The split case
creates two independent copied subgraphs. Each contains its own cycle, but neither child's back edge
reaches the root we assembled as the result. Topology changed despite the word “deep.”

## Additional controlled checks

The tests also examine default dataclass copy versus replacement, post-init call counts, recomputed
`init=False` fields, required `InitVar`, the `copy.replace` version boundary, a shared plain function,
a rejected actual file object, a custom sharing hook, list subclass behavior, incomplete memo retention after failure, a
custom replacement hook on 3.14, and mutable closure state retained by a copied function. Exact executed
results belong to the validation record. These checks use synthetic data and temporary file paths.

## Limitations and next variation

This is semantic evidence for known classes on the recorded CPython runtimes. Custom hooks can
change outcomes. No free-threaded stress, async provider integration, hostile input validation,
performance, or memory comparison is claimed. The source is stable during each operation.

Next, add a second root that shares the same child and predict copying the pair in one call versus
two calls. Explain where the memo's lifetime belongs. Do not copy a live resource merely to see what
happens; decide its ownership and reconstruction contract first.
