"""Isolate deliberately flawed class experiments from the importing process."""

import json
import subprocess
import sys

SOURCE = """
import json
from pickle import dumps, loads

class Base:
    cached = None
    def __new__(cls):
        if cls.cached is None:
            cls.cached = super().__new__(cls)
        return cls.cached

class Child(Base):
    initialized = False
    def __init__(self):
        Child.initialized = True

base = Base()
child = Child()

class Failed:
    cached = None
    def __new__(cls):
        if cls.cached is None:
            cls.cached = super().__new__(cls)
        return cls.cached
    def __init__(self):
        self.partial = True
        raise ValueError('synthetic setup failure')

try:
    Failed()
except ValueError:
    pass

class Mutable:
    cached = None
    init_calls = 0
    def __new__(cls):
        if cls.cached is None:
            cls.cached = super().__new__(cls)
        return cls.cached
    def __init__(self):
        type(self).init_calls += 1
        self.revision = 'r1'

live = Mutable()
payload = dumps(live)
live.revision = 'r2'
restored = loads(payload)
print(json.dumps({
    'child_is_base': child is base,
    'child_has_child_type': isinstance(child, Child),
    'child_init_ran': Child.initialized,
    'failed_object_still_cached': Failed.cached is not None,
    'partial_state_reachable': Failed.cached.partial,
    'pickle_preserved_identity': restored is live,
    'live_revision_after_restore': live.revision,
    'mutable_init_calls': Mutable.init_calls,
}, sort_keys=True))
"""


def observe_mechanics() -> dict[str, bool | int | str]:
    completed = subprocess.run(
        [sys.executable, "-c", SOURCE],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    result: dict[str, bool | int | str] = json.loads(completed.stdout)
    return result


if __name__ == "__main__":
    print(json.dumps(observe_mechanics(), indent=2, sort_keys=True))
