# SDP-STR-040 — Controlled access and freshness experiment

## Question and hypothesis

Does a cached snapshot bypass a revoked permission, and when does a stored update become visible?
Hypothesis: permission is checked even on a would-be hit; source updates remain hidden until expiry
or invalidation; only the first permitted load invokes the target factory. This supports explanation and
debugging without changing the canonical E+I+D+T profile.

## Environment and commands

Observed on 2026-09-09 with CPython 3.14.7 and CPython 3.11.16. The fake clock starts at zero and is
set to exactly ten seconds; TTL is ten. No sleeping, browser or network is used. From repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/parry/projects/solid-and-design-pattern/.venv/bin/python \
  units/structural/SDP-STR-040-proxy/examples/access_probe.py
PYTHONDONTWRITEBYTECODE=1 /tmp/sdp-cre-040/venv311/bin/python \
  units/structural/SDP-STR-040-proxy/examples/access_probe.py
```

## Actual output on both interpreters

```text
wired | - | 0 | 0 | -
first | 1 | 1 | 1 | miss
cached | 1 | 1 | 1 | hit
revoked | PermissionError | 1 | 1 | denied
expiry | 2 | 1 | 2 | miss
invalidated | 3 | 1 | 3 | miss
closed | 1 | 1 | 3 | -
```

### How to read this visual

Columns mean stage, revision/error (close count on the final row), factory count, real read count,
and observer outcome. After the first read the source is updated to revision 2. Permission is then
revoked, restored, and time advanced to 10. After expiry the source becomes revision 3 and the slot
is explicitly invalidated. Counts are cumulative. The final value 1 means one target close.

### Key insight

A hit preserves an earlier snapshot without preserving earlier permission. Both expiry and explicit
invalidation permit a new value to be loaded while retaining the same target.

### Simplification or limitation

A deterministic observation table of the included sequential synthetic objects. It is not a
performance benchmark, browser rendering, security penetration test or distributed cache test.
Source freshness is controlled here. No wall-clock latency, real resources or cross-process
invalidation is measured. The probe uses a preconstructed spy so its reads and updates are visible;
the factory count measures deferred acquisition, not actual object-construction cost. The separate
worked demo constructs its real MemoryCatalog inside the factory. The tests assert all seven rows,
so changes to policy must reconcile
both code and this interpretation.

## Interpretation and follow-up

The observed output supports the hypothesis within this setup. It also exposes a semantic difference:
revision 1 is still returned after the source changes to revision 2. That is acceptable only for a
consumer whose contract tolerates this reuse window. Explain why neither the expiry result nor the
revocation check proves atomic permission/data consistency. Make your own prediction before varying
time, full key, or the source's behavior.
