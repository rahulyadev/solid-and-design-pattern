# EXP-01 — Sharing and retained allocations

| Field | Value |
|---|---|
| Owning unit | [SDP-STR-070](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-str-070) |
| Precise question | For equivalent placed-tile workloads, how do sharing and owner lifetime change retained traced allocations as key repetition changes? |
| Classification | CPython observation through the standard-library tracemalloc API |
| Status | Reproduced |

## Why observation is necessary

Identical tile references alone do not reveal allocation size or the cost of retaining unused
values. Measuring only placements misses pixel payloads and pool overhead. This controlled
experiment observes a complete constructed workload and two owner-release stages.

## Hypothesis

With many repeated keys, explicit sharing and a scoped pool should retain less traced memory than
fresh construction. With all unique keys, the sharing index should add cost. Dropping placements
alone should leave catalog/pool values retained; clearing those owners should release their values
when no other borrowers remain. Exact byte totals are not predicted as portable constants.

## Environment

Executed 2026-09-09. Linux 7.0.0-31-generic, x86_64, glibc 2.43. Standard library only for the probe.
Existing environments were read without installation or modification:

- `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`: CPython 3.14.7.
- `/tmp/sdp-cre-040/venv311/bin/python`: CPython 3.11.16.

Exact version/build and GIL configuration observations are in the outputs below. The missing
3.11 `Py_GIL_DISABLED` configuration variable is reported as None, not inferred as a measured
free-threading result. These are ordinary builds; no free-threaded execution is claimed.

`PYTHONDONTWRITEBYTECODE=1` is exported. All cache/log/temporary paths use `/tmp` as documented in
[validation](../../VALIDATION.md). The driver launches each trial in a fresh child interpreter with
that environment. No custom allocator flag or timing measurement is used.

## Controls and variables

- Controlled: 4000 placements, 32-by-32 byte payloads, deterministic seed order, IDs and positions,
  construction APIs, one thread, no I/O within construction, and three trials per cell.
- Changed: K=8 or K=4000 distinct specifications; fresh construction, explicit catalog or dynamic pool.
- Measured: retained traced bytes after construction; live Tile identity count; sample checksum;
  retained bytes after deleting placements and after clearing the remaining owner.
- Each cell gets three fresh-process trials. Imports finish and `gc.collect()` runs before starting
  tracing. There is no warm-up because this measures a cold constructed object population, not speed.
- `get_traced_memory()[0]` minus the pre-build baseline is measured before allocating the identity
  set and checksum. Those diagnostics keep a few small bookkeeping values alive in later stages.
  The after-drop/after-clear totals therefore need not reach zero.
- The explicit mode builds its catalog during the traced interval; it is not given a free preloaded
  payload. Both shared modes retain their owner until the clear stage. Fresh mode has no owner index.
  Key creation/integer reuse and dictionary representations differ naturally between those designs.

The explicit catalog's integer index and the pool's TileKey index make this a comparison of three
complete representations, not a causal isolation of dictionary overhead to the byte. There is no
RSS, allocation peak, retained-native-buffer or wall-clock measurement.

## Reproduction command

From the repository root after applying the `/tmp` settings in validation, run with each interpreter:

```bash
python units/structural/SDP-STR-070-flyweight/examples/memory_probe.py
```

Source: [memory_probe.py](../../examples/memory_probe.py). Workload contract tests assert matching
placements, samples and expected live-object counts with small inputs. They intentionally do not
assert exact platform byte totals. The driver verifies repeated-trial checksum consistency; compare
checksums across modes for each K below. A checksum alone is not a full equivalence proof.

## Observed result

All three measurements per cell are recorded, not just a selected best result.

```text
implementation=cpython version=3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
platform=Linux-7.0.0-31-generic-x86_64-with-glibc2.43 Py_GIL_DISABLED=0
N=4000 side=32 trials=3 fresh_process_per_trial=True
K=8 mode=fresh live_tiles=4000 checksum=330000 retained_bytes=[5213424, 5213424, 5213424] median=5213424 after_drop=[96, 96, 96] after_clear=[96, 96, 96]
K=8 mode=explicit live_tiles=8 checksum=330000 retained_bytes=[547000, 547000, 547000] median=547000 after_drop=[9768, 9768, 9768] after_clear=[160, 160, 160]
K=8 mode=pooled live_tiles=8 checksum=330000 retained_bytes=[547392, 547392, 547392] median=547392 after_drop=[10096, 10096, 10096] after_clear=[488, 488, 488]
K=4000 mode=fresh live_tiles=4000 checksum=517360 retained_bytes=[5333200, 5333200, 5333200] median=5333200 after_drop=[96, 96, 96] after_clear=[96, 96, 96]
K=4000 mode=explicit live_tiles=4000 checksum=517360 retained_bytes=[5480648, 5480648, 5480648] median=5480648 after_drop=[4943416, 4943416, 4943416] after_clear=[192, 192, 192]
K=4000 mode=pooled live_tiles=4000 checksum=517360 retained_bytes=[5481072, 5481072, 5481072] median=5481072 after_drop=[4943744, 4943744, 4943744] after_clear=[520, 520, 520]
```

```text
implementation=cpython version=3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]
platform=Linux-7.0.0-31-generic-x86_64-with-glibc2.43 Py_GIL_DISABLED=None
N=4000 side=32 trials=3 fresh_process_per_trial=True
K=8 mode=fresh live_tiles=4000 checksum=330000 retained_bytes=[5181088, 5181088, 5181088] median=5181088 after_drop=[92, 92, 92] after_clear=[92, 92, 92]
K=8 mode=explicit live_tiles=8 checksum=330000 retained_bytes=[546664, 546664, 546664] median=546664 after_drop=[9704, 9704, 9704] after_clear=[160, 160, 160]
K=8 mode=pooled live_tiles=8 checksum=330000 retained_bytes=[547048, 547048, 547048] median=547048 after_drop=[10024, 10024, 10024] after_clear=[480, 480, 480]
K=4000 mode=fresh live_tiles=4000 checksum=517360 retained_bytes=[5300864, 5300864, 5300864] median=5300864 after_drop=[92, 92, 92] after_clear=[92, 92, 92]
K=4000 mode=explicit live_tiles=4000 checksum=517360 retained_bytes=[5448344, 5448344, 5448344] median=5448344 after_drop=[4911412, 4911412, 4911412] after_clear=[188, 188, 188]
K=4000 mode=pooled live_tiles=4000 checksum=517360 retained_bytes=[5448728, 5448728, 5448728] median=5448728 after_drop=[4911732, 4911732, 4911732] after_clear=[508, 508, 508]
```

## Interpretation

For K=8, all three modes produce checksum 330000. Fresh mode keeps 4000 tiles, while each shared
mode keeps eight. On 3.14.7 the fresh retained population is 5,213,424 traced bytes; the explicit
catalog is 547,000 and the pool is 547,392. This supports sharing for this workload and also shows
that explicit reuse captures essentially the same payload saving without the dynamic factory.

For K=4000, all three modes produce checksum 517360 and retain 4000 tiles. The 3.14.7 fresh
population is 5,333,200 bytes; the pool is 5,481,072. Here pooling costs more retained memory.
The 3.11.16 observations have the same direction with different exact totals. Identical repeated
trial totals show repeatability in this environment; they are not universal allocator constants.

After dropping placements, the K=4000 pool still retains about 4.94 million traced bytes on 3.14.7.
After clearing it, 520 bytes remain measured, including the empty owner and probe bookkeeping.
The controlled graph has no outside borrowers. Separate weak-reference tests cover the contrasting
case where a live placement keeps a tile alive after clear.

## Visual interpretation

| Stage | Fresh construction | Explicit catalog / pool |
|---|---|---|
| Placements live | Placements own all tile values | Placements and owner index both reach tiles |
| Placements dropped | No tile owner remains | Owner index still reaches tiles |
| Owner cleared | No change needed | No tile owner remains in this controlled graph |

### How to read this visual

Read downward for the lifetime stages, and compare owners across columns. The table represents
references conceptually; the observed byte totals are in the output rather than encoded as geometry.

### Key insight

Sharing can reduce repeated payloads while increasing the lifetime of values that are no longer used.

### Simplification or limitation

A real borrower outside this graph could retain tiles after clear. The table is not an allocator,
RSS, timing or concurrency diagram. No browser rendering was performed.

## Design conclusion and limitations

Start with explicit immutable reuse. Introduce a scoped pool when dynamic repeated specifications
justify it. Choose a capacity/error policy and a lifecycle before claiming memory savings. A pool
is worse in the controlled all-unique case; “fewer constructions” is not a universal optimization.

The workload uses synthetic bytes generated by a fixed formula. Its distributions are deliberately
extreme and its process lifetimes short. Actual cache hit patterns, differing payload sizes, live
revisions, multiple workers, native resources and allocator reuse can change results. The three
fresh processes per cell are reproducibility controls, not a statistical performance study. Values
are collected explicitly between release stages; this does not promise prompt finalization elsewhere.
No timing benchmark or production memory improvement is claimed.

## Sources

The measured quantity follows [tracemalloc's current traced-block size API](https://docs.python.org/3.14/library/tracemalloc.html#tracemalloc.get_traced_memory).
The [data model's object-lifetime contract](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types)
explains why references and cleanup guarantees must be distinguished. The workload and output above
are original execution evidence, not values copied from documentation.
