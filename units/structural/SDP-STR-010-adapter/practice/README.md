# Unsolved route boundary lab — SDP-STR-010

Today's trip display calls an owned route feed that returns whole minutes. It works. A new external
feed returns `{route_id, elapsed_seconds, status, revision}`. `elapsed_seconds` can be null; status
may be `ready`, `pending`, or `closed`. The two feeds must coexist during migration. No implementation
of the new feed or target boundary is supplied. Use synthetic data and choose your own API.

Preserve `route_lab.py`, baseline tests, your first prediction, and your first attempt. Create
separate attempt files; later corrections must not erase your reasoning. Worked stock examples
demonstrate a different contract and do not settle this lab's rounding or status decisions.

## Predict → run → observe → explain → refactor → vary

1. **Predict:** Trace two calls and an unknown route. Predict which old behaviors would break if
   elapsed seconds were passed into the existing label unchanged.
2. **Run:** Run the starter and its baseline tests with the unit's `/tmp` environment exports.
3. **Observe:** Record actual output and calls. Preserve any mismatch with your prediction.
4. **Explain:** Write a target contract before choosing function, callable, or object. Identify
   information that cannot be translated without a product decision.
5. **Refactor:** Support old and new providers through your chosen boundary. Write behavioral tests
   against that contract. No nominal inheritance or named pattern is required for credit.
6. **Vary:** After review, choose one new pressure below. Revise the contract before the code.

## Acceptance questions to settle and test

- Can a 61-second trip be displayed as one minute, or must it round upward? Who owns that policy?
- How will the consumer distinguish zero, pending, closed, missing, and provider failure?
- What happens when the returned route ID differs from the requested ID or revision is unsupported?
- Which fields and values are mandatory? Will a numeric string or boolean be accepted? Explain why.
- Who opens/closes the external client? Can two callers share it? What does a second read observe?
- What safe diagnostic information helps detect drift without exposing raw provider payloads?
- Can the old caller stay unchanged while preserving your newly written contract? If not, state
   precisely which requirement makes an unchanged caller impossible.

These are design obligations, not a hidden reference implementation. The baseline suite checks only
the old behavior and deliberately does not certify the target. Request one progressive hint only
after an attempt; review names the first missing reasoning step before offering another question.

## Commands

From the repository root with a locked development interpreter selected as `python` and the exports
in the [unit commands](../README.md#20-run-and-study):

```bash
python units/structural/SDP-STR-010-adapter/practice/route_lab.py
python -m pytest -p no:cacheprovider units/structural/SDP-STR-010-adapter/practice
```

The unchanged starter prints `NORTH: 7 min` then `target_complete=False`.

## Later variations

Choose one: provider now streams partial routes; the read becomes asynchronous; provider v2 reports
milliseconds; cached trips carry an observation timestamp; an operation starts charging a fare.
Explain the contract change and one rejected alternative. Completion requires a preserved attempt,
edge cases, tests, and explanation; generated examples do not advance learning state.
