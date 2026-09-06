# EXP-01 — Owned Product lifetime

## Question

When a factory creates a short-lived Product for one workflow call, does cleanup still happen if
using that Product raises?

## Hypothesis

With cleanup in `finally`, both paths will end in `close`. The failure path will preserve the
original `RuntimeError` after cleanup.

## Environment and command

The exact interpreter patch versions and observed check date are recorded in
[VALIDATION.md](../../VALIDATION.md).

~~~bash
uv run --locked python units/creational/SDP-CRE-010-factory-method/experiments/EXP-01-owned-product-lifetime/lifetime_probe.py
uv run --locked pytest -q -p no:cacheprovider units/creational/SDP-CRE-010-factory-method/experiments/EXP-01-owned-product-lifetime
~~~

## Observed output

```text
success=construct>use>close
failure=construct>use>close>caught:RuntimeError
```

The output above is maintained only after the commands are run during validation. Tests protect
the same ordering.

## Interpretation

Factory Method chooses or constructs a Product; it does not automatically decide who owns that
Product or who closes it. In this example, the workflow creates the Product and therefore closes
it in `finally`. A long-lived Product injected from outside would usually remain owned outside.

## How to read this visual

Read each trace left to right. `construct` establishes ownership, `use` performs the workflow call,
and `close` ends the owned lifetime. `caught:RuntimeError` then records handling outside that
lifetime.

## Key insight

Construction indirection and resource ownership are separate decisions. State the lifetime
contract explicitly.

## Simplification or limitation

This is deterministic synchronous Python code. It does not model cancellation, asynchronous
context managers, partial external effects, cleanup failure, connection pools, or process death.

## Sources

Python's data-model documentation warns against depending on garbage collection for timely
resource release and recommends explicit closure via `try`/`finally` or `with`.
[Python 3.14 data model](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).
