"""Exact quadratic signed translations; all arithmetic in this file is binary."""


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def monomials(n):
    require(type(n) is int and 1 <= n <= 9, "Dimension in 1..9")
    return tuple(1 << i for i in range(n)) + tuple(
        (1 << i) | (1 << j) for i in range(n) for j in range(i + 1, n)
    )


def validate(element, n):
    terms = monomials(n)
    columns, phase = element
    require(type(columns) is tuple and len(columns) == n, "Matrix shape")
    require(all(type(x) is int and 0 <= x < 1 << n for x in columns), "Columns")
    require(type(phase) is int and 0 <= phase < 1 << len(terms), "Phase range")
    require(all((columns[i] >> j & 1) == (columns[j] >> i & 1)
                for i in range(n) for j in range(n)), "Symmetric matrix")


def symmetric(bits, n):
    columns = [0] * n
    for k, term in enumerate(monomials(n)):
        if bits >> k & 1:
            indices = [i for i in range(n) if term >> i & 1]
            i, j = indices[0], indices[-1]
            columns[i] ^= 1 << j
            if i != j:
                columns[j] ^= 1 << i
    return tuple(columns)


def diagonal(columns):
    return sum((column >> i & 1) << i for i, column in enumerate(columns))


def image(columns, vector):
    answer = 0
    for i, column in enumerate(columns):
        if vector >> i & 1:
            answer ^= column
    return answer


def parity(a, b):
    return (a & b).bit_count() & 1


def phase_value(bits, vector, terms):
    answer = 0
    for k, term in enumerate(terms):
        if bits >> k & 1 and vector & term == term:
            answer ^= 1
    return answer


def cross_phase(left, right, n):
    """Recover the degree-at-most-two cross term by Boolean interpolation."""
    values = []
    terms = monomials(n)
    for vector in terms:
        values.append(parity(diagonal(left) ^ image(left, vector),
                             image(right, vector)))
    coefficients = values[:n]
    for k, term in enumerate(terms[n:], n):
        indices = [i for i in range(n) if term >> i & 1]
        coefficients.append(values[k] ^ values[indices[0]] ^ values[indices[1]])
    return sum(value << k for k, value in enumerate(coefficients))


def compose(left, right, n):
    """The left map acts after the right map, retaining the exact sign."""
    s, h = left
    t, k = right
    return tuple(a ^ b for a, b in zip(s, t)), h ^ k ^ cross_phase(s, t, n)


def inverse(element, n):
    columns, phase = element
    return columns, phase ^ cross_phase(columns, columns, n)


def action(element, c, a, n):
    columns, phase = element
    moved = image(columns, c)
    sign = parity(diagonal(columns) ^ moved, a)
    sign ^= phase_value(phase, c, monomials(n))
    return sign, (c << n) | (a ^ moved)


def generator(q, n):
    require(type(q) is int and 0 <= q < 1 << n, "Generator label")
    return tuple(q if q >> i & 1 else 0 for i in range(n)), 0
