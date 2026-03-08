# observability/tracer.py

class Tracer:

    def trace(self, event, data):

        print(f"[TRACE] {event}: {data}")
        