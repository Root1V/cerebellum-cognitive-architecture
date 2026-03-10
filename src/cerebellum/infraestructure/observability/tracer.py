# observability/tracer.py
from typing import Any


class Tracer:

    def trace(self, event: str, data: Any) -> None:
        print(f"[TRACE] {event}: {data}")
        