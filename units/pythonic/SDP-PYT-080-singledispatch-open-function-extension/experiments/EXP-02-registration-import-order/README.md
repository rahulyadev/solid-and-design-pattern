# EXP-02 — Registration, module execution, and import order

## Question

What happens when two imported support modules register the same exact runtime type on one generic
function?

## Setup

- [registration_target.py](../../examples/registration_target.py) owns the generic function and
  `ExternalPayload`.
- [extension_alpha.py](../../examples/extension_alpha.py) registers one implementation.
- [extension_beta.py](../../examples/extension_beta.py) registers a competing implementation.
- [registration_order_probe.py](../../examples/registration_order_probe.py) runs each import order
  in a fresh interpreter so the module cache cannot leak one trial into the other.

These competing modules are an intentional failure demonstration, not production architecture.

## Prediction

Predict the handler and result for:

1. `extension_alpha` then `extension_beta`; and
2. `extension_beta` then `extension_alpha`.

Also predict whether importing neither module makes the generic function discover either extension.
No learner prediction is recorded here.

## Run

```bash
uv run --locked python units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/examples/registration_order_probe.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/examples/test_dispatch_probes.py
```

## Maintainer observation

Each fresh interpreter reports the implementation from the module imported last for the exact
`ExternalPayload` key. With no extension import, the `object` fallback remains selected.

Python function decorators are evaluated when a function definition executes. Module loading
executes module code, and later imports normally reuse the cached module. Therefore an extension
module containing `@generic.register(...)` changes that generic function as an import-time effect.
[Python function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions)
and [Python import system](https://docs.python.org/3.14/reference/import.html).

## Explain

`singledispatch` provides registration; it does not provide discovery, duplicate rejection,
dependency trust, ordering policy, or process synchronization. The order-dependent result is
observable in this experiment, but accepting it in production would be a design choice—and usually
a poor one—not a promised conflict policy.

## Refactor implication

Give one module or composition root ownership of startup registration. Import a deterministic list
of approved support modules, inspect the registry, reject duplicate exact-type claims before serving
requests, and keep request-time code read-only. If independently installed distributions must be
found, that is the later `SDP-PYT-090` plugin-discovery problem, not a hidden feature of
`singledispatch`.

## Vary

Run the parent probe twice and explain why its subprocess boundary matters. Then temporarily import
the same extension module twice in one child process and connect the observation to `sys.modules`.
Do not convert the experiment into reload-dependent production code.
