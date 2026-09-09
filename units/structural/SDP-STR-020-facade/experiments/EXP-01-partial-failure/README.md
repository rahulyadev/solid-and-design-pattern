# EXP-01 — One task call can leave an uncertain write

This supporting experiment belongs to SDP-STR-020; it does not add X to canonical E+I+D+T evidence.

**Question:** Does a facade exception prove that the archive did not change?

**Hypothesis:** Failures before storage prevent the write attempt. A known store failure alone cannot
distinguish rejection before writing from an acknowledgement lost after writing.

**Method:** Run the same synthetic task in five controlled scenarios. Inject failure at load, render,
before the write, and after the write but before acknowledgement. Inspect the fake archive from the
root after each call. Each scenario receives fresh objects and one facade invocation. This privileged
inspection is an experimental oracle; the normal client cannot infer those facts from its exception.

From the repository root with cache exports from the unit note:

```bash
python units/structural/SDP-STR-020-facade/examples/failure_probe.py
```

The actual environments and observed output are recorded after execution in [VALIDATION.md](../../VALIDATION.md).

| Scenario | Task outcome | Store calls | Stored objects | Steps |
|---|---|---:|---:|---|
| success | acknowledged | 1 | 1 | load,render,store |
| missing | load:not_attempted | 0 | 0 | load |
| render | render:not_attempted | 0 | 0 | load,render |
| store_before | store:unknown | 1 | 0 | load,render,store |
| lost_ack | store:unknown | 1 | 1 | load,render,store |

### How to read this visual

Compare the last two rows: same public error, different actual stored state. “Store calls” counts
attempts, while “stored objects” counts retained data. Read steps left to right in call order.

### Key insight

Moving calls behind a facade reduces client knowledge; it does not turn an uncertain acknowledgement
into evidence of rollback. The test of a blind manual retry demonstrates another stored object.

### Simplification or limitation

This is a controlled observation table, not a timing benchmark or a distributed-system simulator.
The archive is an in-memory sequential fake with infallible close; no network, crash recovery,
concurrent requests, transaction, or durable storage was tested. Browser rendering is not claimed.
The test suite checks the table's values against the actual probe function.
