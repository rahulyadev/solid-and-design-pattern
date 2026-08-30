# EXP-01 — Shape is not a contract

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-030](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-030) |
| Precise question | Can runtime presence and static signature checks accept an object that violates its promised operation? |
| Classification | Standard library (`typing`) and mypy behaviour |
| Status | Run and interpreted by maintainer; learner prediction not recorded |

## Why observation is necessary

Three objects expose a member called `count`. Only one obeys the promise to return the UTF-8
byte length for encodable strings. A runtime check, a static check, and a real call inspect
different things. Keep your own prediction before reading the observed result below.

## Hypothesis and predicted result

The runtime presence check should accept all three ordinary-method objects. The wrongly shaped
method should fail when called with a string. The matching-signature zero counter should call
successfully but return the wrong value for `"ñ"`. Static analysis should reject the wrong
signature and accept the wrong-value implementation.

This is the maintainer's hypothesis, not a prediction attributed to Rahul.

## Environment

```text
Date: 2026-08-30
Operating system / architecture: Linux / x86_64
Python: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation.name: cpython
sys.implementation.cache_tag: cpython-314
Dependencies: standard library for runner; pytest 8.4.2 and mypy 1.20.2 for checks
Flags: PYTHONDONTWRITEBYTECODE=1; pytest cache disabled; external mypy cache
```

## Controls and variables

- Controlled: `ByteCounter` protocol, call `count("ñ")`, input encoding, and interpreter.
- Changed: implementation; correct count, wrong value, or wrong arity.
- Measured: runtime `isinstance`, actual outcome, and mypy's exit code/diagnostic category.
- Isolated static fixtures are strings passed to mypy's `--command`; the intentionally invalid
  assignment is not hidden inside normal production code or suppressed with a type ignore.

## Reproduction commands

Apply the external-environment exports in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/experiments/EXP-01-shape-is-not-contract/shape_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-030-liskov-substitution-behavioural-subtyping/experiments/EXP-01-shape-is-not-contract
```

The tests invoke `python -m mypy --strict --no-incremental --python-version` with the running
interpreter's major/minor version and `--command` for each fixture.

## Observed result

Actual canonical-interpreter runner output:

```text
UTF8Counter: runtime=True; count('ñ')=2
ZeroCounter: runtime=True; count('ñ')=0
WrongArityCounter: runtime=True; count('ñ')=TypeError
```

The executed static tests observed exit code `0` with a success message for `ZeroCounter`, and
exit code `1` with an `[assignment]` incompatibility diagnostic for `WrongArityCounter`.
The enclosing initial unit run passed 75 tests; that is artifact verification, not learner evidence.

## Interpretation

The runtime check admitted even the wrong signature. Static analysis found that signature
problem but did not establish the required numeric meaning. Thus these checks are useful but
answer different questions. A behaviour test supplies the missing witness for this input.

Python documents runtime-checkable protocols as presence checks, not signature/type validation.
[Python typing documentation](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).
The experiment does not imply that all static tools are unable to prove any value property.

## Design conclusion and limitations

Keep static checks, but pair them with explicit behavioural contracts and tests. Do not add
runtime `isinstance` checks as a replacement for proving a provider's promises.

The probe uses ordinary methods, not dynamic attribute hooks; those hooks have version-sensitive
interactions with runtime protocols from Python 3.12 onward. The Python documentation notes
that change. No runtime implementation internals or exact exception-message text are asserted.
Encoding-invalid surrogate strings are outside this probe's stated input domain.

## Sources

- [Python 3.14: runtime_checkable](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).
- [Executable static fixtures and observed checks](test_shape_probe.py).
