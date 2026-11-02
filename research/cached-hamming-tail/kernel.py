"""Exact fixed-domain Hamming envelopes, produced by Nick Petalas.

Apache-2.0. The shared-tail predicate and caller are SHIN09-git's PR6046.
"""

DIMENSION = 5
LENGTH = 12
SIZE = 1 << DIMENSION
ALL = (1 << SIZE) - 1
NONZERO = ALL - 1
LOW = (0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF, 0x0000FFFF)


def translate(bits, point):
    """Return the bitset {x XOR point : x in bits}."""
    for coordinate in range(DIMENSION):
        step = 1 << coordinate
        if point & step:
            low = LOW[coordinate]
            bits = ((bits & low) << step) | ((bits & (ALL ^ low)) >> step)
    return bits


def tables():
    """Build all 416 reach masks and their 13,312 translations once."""
    masks = []
    translated = []
    cache = {}
    for last in range(SIZE):
        for remaining in range(LENGTH + 1):
            mask = sum(1 << x for x in range(SIZE)
                       if (last ^ x).bit_count() + x.bit_count() <= remaining)
            masks.append(mask)
            if mask not in cache:
                cache[mask] = tuple(translate(mask, p) for p in range(SIZE))
            translated.append(cache[mask])
    assert len(masks) == SIZE * (LENGTH + 1)
    return tuple(masks), tuple(translated)


def envelope(points, seen, support, reach, translated):
    """Inputs are a validated simple prefix and its literal pair support."""
    index = points[-1] * (LENGTH + 1) + LENGTH - len(points) + 1
    future = reach[index] & (ALL ^ seen)
    possible = support
    shifts = translated[index]
    for old in points:
        possible |= shifts[old]
    return future, possible & NONZERO


def cached_reject(reference, reach, translated):
    """Substitute only the tail stage of the source's no-cap caller."""
    def reject(points, highest, mode):
        if mode != "two_without_cap":
            raise ValueError("only the fixed shared-tail no-cap caller is admitted")
        if reference.remaining_reject(points, highest) or reference.union_reject(points):
            return True
        seen = sum(1 << p for p in points)
        future, possible = envelope(points, seen, reference.pair_support(points),
                                    reach, translated)
        return future.bit_count() < LENGTH - len(points) or possible != NONZERO
    return reject


def search(reference):
    """Run the unchanged complete caller with the exact new tail kernel."""
    reach, translated = tables()
    original = reference.reject
    reference.reject = cached_reject(reference, reach, translated)
    try:
        return reference.search("two_without_cap")
    finally:
        reference.reject = original
