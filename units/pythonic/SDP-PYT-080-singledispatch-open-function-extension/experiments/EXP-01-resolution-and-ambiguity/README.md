# EXP-01 — Resolution, exact overrides, and ABC ambiguity

## Question

What can the public `singledispatch` API make observable about inheritance, exact registration,
invalid parameterized aliases, and unrelated ABC matches?

## Prediction

Before running [dispatch_mechanics_probe.py](../../examples/dispatch_mechanics_probe.py), predict:

1. whether `True` selects an `int` implementation before `bool` is registered;
2. whether adding an exact `bool` implementation changes `dispatch(bool)`;
3. whether `list[int]` is a valid runtime registration key; and
4. whether two unrelated registered ABCs are silently ordered for one virtual subclass.

No learner prediction is recorded here.

## Run

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/examples/dispatch_mechanics_probe.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/examples/test_dispatch_probes.py
```

## Maintainer observation

On both supported runtimes, the probe records:

- `bool` first resolves to the registered `int` implementation because `bool` subclasses `int`;
- an exact `bool` registration then wins;
- registering `list[int]` raises `TypeError`; and
- unrelated `Iterable` and `Container` virtual matches raise `RuntimeError` for ambiguous dispatch.

The Python documentation says an unregistered exact type is resolved through MRO and that the base
function is registered for `object`. It also instructs callers to register `list` explicitly when a
handler annotation is `list[int]`. PEP 443 documents the ABC ambiguity case and says dispatch does
not guess between unrelated virtual ABC matches.
[Python 3.14 `singledispatch`](https://docs.python.org/3.14/library/functools.html#functools.singledispatch)
and [PEP 443, Abstract Base Classes](https://peps.python.org/pep-0443/#abstract-base-classes).

## Explain

The observation is about documented selection and public `dispatch()` behavior. The probe does not
read the private cache, reconstruct CPython's internal data structures, or claim that `bool` was a
good domain model. An exact application type is usually clearer than leaning on surprising built-in
inheritance.

## Refactor implication

Register broad ABCs only when their semantic contract is honest, and test concrete runtime types
that matter. If overlap is legitimate, introduce a more specific type relationship or choose an
explicit decision function instead of relying on accidental precedence.

## Vary

Add a direct class whose declared bases are `Iterable` and `Container`. Predict how its explicit MRO
changes the result, then compare that observation with PEP 443. Remove the temporary variation after
recording it.
