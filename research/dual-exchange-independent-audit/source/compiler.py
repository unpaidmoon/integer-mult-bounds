"""Division-free dual-pair exchange, produced by Nick Petalas; Apache-2.0."""

from fractions import Fraction

MAX_DIMENSION = 16
MAX_NUMERATOR_BITS = 64
MAX_DENOMINATOR_BITS = 33


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pair(a, b):
    """Validate a bounded dyadic dual pair at the public compiler boundary."""
    need(type(a) in (list, tuple) and type(b) in (list, tuple), "Vector containers")
    need(1 <= len(a) == len(b) <= MAX_DIMENSION, "Matching bounded dimensions")
    need(all(type(q) in (int, Fraction) for q in (*a, *b)), "Exact coefficients")
    a, b = tuple(map(Fraction, a)), tuple(map(Fraction, b))
    for q in (*a, *b):
        need(abs(q.numerator).bit_length() <= MAX_NUMERATOR_BITS, "Numerator bound")
        d = q.denominator
        need(d.bit_length() <= MAX_DENOMINATOR_BITS and d & (d - 1) == 0,
             "Bounded dyadic denominator")
    need(sum(x * y for x, y in zip(a, b)) == 1, "Dual pairing equals one")
    return a, b


def addition_cost(q):
    """PR5602's real scalar ADD allowance for a nonzero dyadic coefficient."""
    q = Fraction(q)
    n, d = abs(q.numerator), q.denominator
    need(n > 0 and d & (d - 1) == 0, "Nonzero dyadic ADD")
    return 2 * (3 + n.bit_length() - 1 + n.bit_count() + d.bit_length() - 1)


def allowance(operations):
    """Price this compiler's ADDs and its one sign SCALE."""
    need(len(operations) <= 3 * MAX_DIMENSION + 1, "Exchange operation bound")
    total = 0
    for op, destination, source, q in operations:
        if op == "ADD":
            need(destination != source, "Distinct ADD roles")
            total += addition_cost(q)
        else:
            need(op == "SCALE" and destination == source and q == -1,
                 "Only sign SCALE")
            total += 2
    return total


def compile_exchange(a, b, repeat="cheapest"):
    """Emit S=[[I-ba,b],[a,0]] on n data roles and arbitrary spare role n.

    'cheapest' minimizes the declared tariff among these two factorizations.
    It does not solve unrestricted circuit optimization.
    """
    a, b = pair(a, b)
    need(repeat in ("a", "b", "cheapest"), "Known factorization")
    if repeat == "cheapest":
        a_cost = sum(addition_cost(q) for q in a if q)
        b_cost = sum(addition_cost(q) for q in b if q)
        repeat = "a" if a_cost < b_cost else "b"
    spare = len(a)
    upper = [("ADD", i, spare, q) for i, q in enumerate(b) if q]
    lower = [("ADD", spare, i, q) for i, q in enumerate(a) if q]
    sign = [("SCALE", spare, spare, Fraction(-1))]
    if repeat == "b":
        negative = [(op, r, s, -q) for op, r, s, q in lower]
        return upper + negative + upper + sign
    negative = [(op, r, s, -q) for op, r, s, q in upper]
    return sign + lower + negative + lower
