"""Exact three-source paid clean-row schedules, produced by Nick Petalas.

Apache-2.0. Contract and predecessors are credited in README.md.
"""

from fractions import Fraction
from itertools import permutations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prices(values, count):
    require(isinstance(values, (tuple, list)), "price sequence required")
    require(len(values) == count, "wrong price count")
    require(all(type(x) in (int, Fraction) and x > 0 for x in values),
            "positive exact rational prices required")
    return tuple(values)


def optimum(source_prices, output_prices):
    b = prices(source_prices, 3)
    a = prices(output_prices, 7)
    even = min(a[m - 1] for m in (3, 5, 6))
    odd = min(a[m - 1] for m in (1, 2, 4, 7))
    return 2 * sum(b) + sum(a) + min(2 * min(b), even + odd)


def permute(mask, order):
    return sum(((mask >> j) & 1) << order[j] for j in range(3))


def six_cycles():
    # Omitted (even, odd) pairs are (3,1), (3,4), and (3,7).
    templates = ((0, 2, 6, 7, 5, 4, 0),
                 (0, 1, 5, 7, 6, 2, 0),
                 (0, 1, 5, 4, 6, 2, 0))
    result = {}
    for template in templates:
        for order in permutations(range(3)):
            cycle = tuple(permute(v, order) for v in template)
            missing = tuple(m for m in range(1, 8) if m not in cycle)
            even = next(m for m in missing if m.bit_count() % 2 == 0)
            odd = next(m for m in missing if m.bit_count() % 2 == 1)
            result[(even, odd)] = cycle
    require(len(result) == 12, "incomplete six-cycle construction")
    return tuple(result[key] for key in sorted(result))


def gray_cycle(axis):
    require(type(axis) is int and 0 <= axis < 3, "invalid Gray axis")
    order = (axis,) + tuple(j for j in range(3) if j != axis)
    return tuple(permute(k ^ (k >> 1), order) for k in range(8)) + (0,)


def word_for(cycle):
    require(isinstance(cycle, tuple) and len(cycle) in (7, 9), "cycle size")
    require(cycle[0] == cycle[-1] == 0, "cycle boundary")
    require(all(type(v) is int and 0 <= v < 8 for v in cycle), "cube vertex")
    require(len(set(cycle[:-1])) == len(cycle) - 1, "repeated vertex")
    reads = {v: [] for v in cycle[:-1]}
    for mask in range(1, 8):
        if mask in reads:
            reads[mask].append(mask)
        else:
            pairs = [(u, v) for u in reads for v in reads if u < v and u ^ v == mask]
            require(bool(pairs), "unavailable output representation")
            u, v = min(pairs)
            reads[u].append(mask)
            reads[v].append(mask)
    word = [("INIT", 0)]
    for index in range(len(cycle) - 1):
        vertex, following = cycle[index:index + 2]
        delta = vertex ^ following
        require(delta in (1, 2, 4), "non-singleton source step")
        word.extend(("A", mask) for mask in reads[vertex])
        word.append(("B", delta.bit_length() - 1))
    word.append(("RELEASE", 0))
    return tuple(word)


def profile(word):
    """Check a bounded explicit witness using formal source masks."""
    require(isinstance(word, tuple) and 2 <= len(word) <= 128, "word size")
    require(word[0] == ("INIT", 0), "missing initial allocation")
    require(word[-1] == ("RELEASE", 0), "missing release")
    current = 0
    outputs = [0] * 7
    counts = [0] * 10
    for op, index in word[1:-1]:
        require(type(index) is int, "integer operation index required")
        if op == "B":
            require(0 <= index < 3, "source index")
            current ^= 1 << index
            counts[index] += 1
        elif op == "A":
            require(1 <= index < 8, "output index")
            outputs[index - 1] ^= current
            counts[index + 2] += 1
        else:
            raise ValueError("operation outside alphabet or owned lifetime")
    require(current == 0, "owned row not restored")
    require(outputs == list(range(1, 8)), "wrong target update")
    return tuple(counts)


def frontier():
    cycles = six_cycles() + tuple(gray_cycle(axis) for axis in range(3))
    words = tuple(word_for(cycle) for cycle in cycles)
    require(len(set(profile(word) for word in words)) == 15, "frontier size")
    return words


def choose_word(source_prices, output_prices):
    b = prices(source_prices, 3)
    a = prices(output_prices, 7)
    costs = b + a
    words = frontier()
    return min(words, key=lambda word: sum(x * y for x, y in zip(profile(word), costs)))
