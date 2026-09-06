# EXP-02 — Context entry, exit, propagation, and suppression

| Field | Value |
|---|---|
| Unit | [SDP-PYT-040](../../README.md) |
| Evidence role | Required experiment (`X`) |
| Probe | [context_lifecycle_probe.py](../../examples/context_lifecycle_probe.py) |
| Last run | 2026-09-06 |
| Runtime | CPython 3.14.7 |
| Status | Reproduced by maintainer; not learner evidence |

## Question

Which callbacks occur on normal exit, body failure, deliberate suppression, and failed entry? Does
the generator-based manager preserve the original body exception while still closing its sink?

## Hypothesis recorded before the run

Normal flow will acquire, run the body, report commit, and close. A body `RuntimeError` will be
raised back into the generator-based manager, report abort, close, and propagate as the same
exception object. A manager returning true for `LookupError` will suppress a `KeyError`, allowing
the next statement to run. If `__enter__()` itself raises, `__exit__()` will not be called.

## Exact environment

| Item | Observed value |
|---|---|
| OS | Linux x86_64 |
| Runtime | CPython 3.14.7 |
| Dependency use | Standard library and the unit example only |
| Resources | Observable in-memory synthetic sinks |
| Network/files | None |
| Bytecode | Disabled with `PYTHONDONTWRITEBYTECODE=1` |

## Command

From the repository root, using the locked external environment documented in the practice guide:

```bash
python units/pythonic/SDP-PYT-040-iterators-generators-context-managers/examples/context_lifecycle_probe.py
```

## Actual output

```json
{"body_failure": {"closed": true, "same_exception_propagated": true, "trace": ["acquire", "body", "abort:RuntimeError", "close"]}, "entry_failure": ["enter", "caught"], "normal": {"closed": true, "trace": ["acquire", "body", "commit", "close"]}, "selective_suppression": ["enter", "body", "exit:KeyError", "continued"]}
```

The automated contract test also passed in the canonical environment.

## Interpretation

All four paths matched the hypothesis. The manager’s `finally` cleanup ran after successful entry
on both normal and exceptional bodies. Re-raising inside the generator-based manager preserved the
body exception object. The class-based suppressor received `KeyError` as an exception type and
returned true, so execution continued. Failed entry produced only `enter` then the outer catch;
there was no exit callback to perform cleanup.

Therefore acquisition must clean up its own partial failure before raising, while `__exit__()` owns
only lifetimes whose entry completed. Suppression is an explicit policy, not an automatic benefit
of `with`.

## Limitations

- The sink is in memory; closing a file, lock, socket, or transaction can fail differently.
- The probe does not inject cleanup failure or claim rollback of earlier writes.
- It covers synchronous contexts, not async cancellation or `__aexit__()`.
- Trace order is application-level evidence, not an interpreter-internal trace.
- Maintainer reproduction does not count as Rahul’s prediction, practice, recall, or transfer.

## Transfer prompt

If cleanup can also raise while a body error is active, what should be reported, and how will
operators find both failures without treating the operation as successful?
