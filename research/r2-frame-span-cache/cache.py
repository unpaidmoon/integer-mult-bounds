"""Bounded exact binary-frame span reuse. Apache-2.0, Nick Petalas."""


class SpanCache:
    """Own immutable results for one loaded audit, never frame identities."""

    def __init__(self, original, capacity=4096):
        if type(capacity) is not int or not 0 <= capacity <= 4096:
            raise ValueError('span cache capacity')
        self.original = original
        self.capacity = capacity
        self.values = {}
        self.calls = 0
        self.hits = 0
        self.misses = 0

    def __call__(self, rows):
        # The pinned audit supplies JSON lists. Other inputs keep the original
        # behavior, including float/bool rejection and any original exception.
        self.calls += 1
        if type(rows) not in (list, tuple) or len(rows) > 9:
            self.misses += 1
            return self.original(rows)
        if any(type(x) is not int for x in rows):
            self.misses += 1
            return self.original(rows)
        key = tuple(rows)
        result = self.values.get(key)
        if result is not None:
            self.hits += 1
            return result
        self.misses += 1
        result = self.original(rows)
        if type(result) is not frozenset or not 1 <= len(result) <= 512:
            raise ValueError('immutable span result')
        if len(self.values) < self.capacity:
            self.values[key] = result
        return result

    def report(self):
        return {'calls': self.calls, 'hits': self.hits, 'misses': self.misses,
                'entries': len(self.values), 'capacity': self.capacity}
