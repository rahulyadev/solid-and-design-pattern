"""Small target whose module dictionary makes execution count observable."""

from __future__ import annotations

execution_count = int(globals().get("execution_count", 0)) + 1


class Marker:
    def __init__(self, generation: int) -> None:
        self.generation = generation


marker = Marker(execution_count)
