# SDP-STR-040 — Export preview lab (unsolved)

## Change pressure

A preview route exports bytes before checking permission. Exports can be expensive. The product now
needs repeated previews of a team report with an explicit revision and locale. Permission can change
between previews. Decide whether a representative, a helper or an explicit preview API is appropriate.
This is a separate domain and design problem from the worked catalog; do not copy its cache policy.

The runnable [starter](export_lab.py) and [baseline tests](test_export_lab.py) preserve the flawed
starting behavior. `build_preview` deliberately raises NotImplementedError. No solution or hidden
implementation requirements are included. Baseline tests passing means the starter is reproducible,
not that the product requirement is satisfied.

## Predict → run → observe → explain → refactor → vary

1. **Predict:** Without running, record whether a denied request calls the exporter. Predict which
   fields can change exported bytes and whether the same report name is enough for reuse.
2. **Run:** From the repository root, execute the commands below. Keep predictions alongside results.
3. **Observe:** Record the export count, returned bytes or exception, and target-complete marker.
4. **Explain:** Identify the first incorrect ordering assumption. Distinguish permission identity
   from representation identity; explain whether immutable bytes alone justify reuse.
5. **Refactor:** Preserve `export_lab.py` as the initial attempt. Write your own attempt in a new
   file. Choose the API, permission source, lifecycle and cache policy; you may change the proposed
   builder signature in your attempt. Support permission revocation before every disclosure, no
   exporter work for a denied attempt, no confusion between teams/revisions/locales, and a documented
   response to exporter errors. Decide whether a cache is even justified. Add your own behavioral
   tests and explain why they establish the requirements without relying on private fields.
6. **Vary:** A new rule redacts one field based on the reader's permission group. Explain what must
   change before implementing it. Then consider two concurrent previews and reject any guarantee
   your sequential design cannot honestly provide.

## Commands

Use an existing locked environment; direct all generated state to `/tmp`:

```bash
export PYTHONDONTWRITEBYTECODE=1
export MYPY_CACHE_DIR=/tmp/sdp-str-040/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-040/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-str-040/ruff
export UV_CACHE_DIR=/tmp/sdp-str-040/uv
export COVERAGE_FILE=/tmp/sdp-str-040/coverage
mkdir -p /tmp/sdp-str-040/pytest
python units/structural/SDP-STR-040-proxy/practice/export_lab.py
python -m pytest -p no:cacheprovider \
  --basetemp=/tmp/sdp-str-040/pytest/lab \
  units/structural/SDP-STR-040-proxy/practice
```

The starter runs without pytest; tests require the locked development environment. If imports fail,
run from the repository root and run this practice directory separately from other units. Do not
rewrite the repository's tool configuration or install tools into an unrelated environment.

## Review evidence

Keep your original prediction, first implementation, observed commands, boundary tests and explanation.
Have the reviewer ask one question at a time. Request one progressive hint only after identifying
where reasoning stopped. Do not mark I/D complete merely because baseline tests pass. The later
redaction/concurrency variation supplies a T discussion only when you defend its trade-offs.
