# EXP-01 — Staged resource cleanup

## Question

If construction acquires two resources and the second acquisition fails, who closes the first?
After successful construction, who owns both resources and in what order are they closed?

## Hypothesis

An `ExitStack` scoped to construction will close already-entered resources in reverse order on a
later failure. Calling `pop_all()` only after every acquisition succeeds will transfer the cleanup
callbacks to the returned owner without running them.

## Environment and commands actually run

The probe ran on CPython 3.14.7 from the repository's locked Local environment and CPython 3.11.16
from an existing locked compatibility environment. These exact commands ran from the repository
root:

~~~bash
PYTHONPYCACHEPREFIX=/tmp/sdp-cre030-pycache314 \
  /home/parry/projects/solid-and-design-pattern/.venv/bin/python \
  units/creational/SDP-CRE-030-builder/experiments/EXP-01-staged-resource-cleanup/resource_cleanup_probe.py
PYTHONPYCACHEPREFIX=/tmp/sdp-cre030-pycache311 \
  /tmp/sdp-pyt-040-tools.b57yty/venv311/bin/python \
  units/creational/SDP-CRE-030-builder/experiments/EXP-01-staged-resource-cleanup/resource_cleanup_probe.py
~~~

## Actual output

Both runtimes produced:

```text
success: open:schema -> open:sink -> prepared -> use -> close:sink -> close:schema
failure: open:schema -> open-failed:sink -> close:schema -> rejected
```

## Interpretation

- On success, ownership moves only after both resources open; the returned object closes them.
- On failure, no partial Product escapes and the earlier resource is closed.
- Reverse callback order matches nested context-manager cleanup.
- `ExitStack` supplies lifecycle mechanics; it does not make the broader design a Builder.

The Python 3.14 `contextlib` contract states that `ExitStack` callbacks unwind in reverse order and
that `pop_all()` transfers them without invocation. `AsyncExitStack` provides the corresponding
mixed sync/async cleanup boundary and uses `aclose()`.
[Python 3.14 `contextlib`](https://docs.python.org/3.14/library/contextlib.html#contextlib.ExitStack).

## Limitations

This deterministic in-memory probe has no network, filesystem, process, cancellation, or cleanup
failure. It proves call ordering in this implementation, not transaction atomicity. A resource
whose own `__enter__` fails after partial acquisition must still clean up that internal partial
state; an outer `ExitStack` cannot register a context that never entered successfully.
