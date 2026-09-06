# EXP-01 — Partial family acquisition and reverse cleanup

## Question

If an Abstract Factory opens several related resource-bearing products and the second acquisition
fails, who closes the first product?

## Prediction

Write the expected trace before running. Pay attention to whether `primary.close` appears before
the construction error is caught and, on success, whether cleanup is last-in-first-out.

No learner prediction has been recorded by the maintainer.

## Run

From the repository root:

~~~bash
uv run --locked python units/creational/SDP-CRE-020-abstract-factory/experiments/EXP-01-atomic-family-acquisition/family_acquisition_probe.py
uv run --locked pytest -q -p no:cacheprovider units/creational/SDP-CRE-020-abstract-factory/experiments/EXP-01-atomic-family-acquisition
~~~

## Maintainer-observable contract

`contextlib.ExitStack` registers each successful context manager immediately. If a later
acquisition fails, leaving the stack unwinds already-entered products. Successful acquisition
closes products in reverse entry order. The Python 3.11 and 3.14 `contextlib` documentation both
describe this stack behavior; it is not a garbage-collection assumption.

## Explain

1. Why can the client not close a product whose constructor never returned it?
2. Why is one `try` around all acquisition and use phases too coarse for useful diagnostics?
3. Should a concrete factory return an `ExitStack`, or should the composition/client boundary own
   the stack? Defend the ownership contract.
4. What changes for `AsyncExitStack` and cancellation during `__aenter__`?

## Limitation

The probe uses deterministic in-memory resources and synchronous context managers. It demonstrates
cleanup order, not network rollback, transaction atomicity, thread safety, or distributed
consistency.
