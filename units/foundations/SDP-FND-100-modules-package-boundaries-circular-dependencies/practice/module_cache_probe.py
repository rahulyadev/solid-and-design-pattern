"""A tiny module whose namespace records each execution for cache experiments."""

_previous_executions = globals().get("EXECUTIONS", 0)
if not isinstance(_previous_executions, int):
    raise TypeError("EXECUTIONS must remain an integer")
EXECUTIONS = _previous_executions + 1

TOKEN = object()
