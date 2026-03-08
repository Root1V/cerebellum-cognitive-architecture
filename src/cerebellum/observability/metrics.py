class Metrics:

    def __init__(self):
        self.counters: dict[str, int] = {}

    def increment(self, name: str) -> None:
        self.counters[name] = self.counters.get(name, 0) + 1

    def report(self) -> dict[str, int]:
        return self.counters
    
    