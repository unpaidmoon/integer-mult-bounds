"""Exact Q(sqrt(2), sqrt(3), i) and literal finite Fourier circuits.

Only fixed finite domains are accepted. No predecessor code is imported.
Floating point has no acceptance role.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class Q:
    """Coefficients of (sqrt(2))^a (sqrt(3))^b i^c, in mask order."""

    coefficients: tuple[Fraction, ...]

    def __post_init__(self):
        if len(self.coefficients) != 8:
            raise ValueError("field dimension must be eight")
        if any(not isinstance(x, Fraction) for x in self.coefficients):
            raise ValueError("field coefficients must be rational")

    def __add__(self, other):
        other = rational(other) if not isinstance(other, Q) else other
        return Q(tuple(a + b for a, b in zip(self.coefficients, other.coefficients)))

    __radd__ = __add__

    def __neg__(self):
        return Q(tuple(-x for x in self.coefficients))

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q) else -rational(other))

    def __mul__(self, other):
        other = rational(other) if not isinstance(other, Q) else other
        out = [Fraction(0)] * 8
        for a, x in enumerate(self.coefficients):
            if not x:
                continue
            for b, y in enumerate(other.coefficients):
                if not y:
                    continue
                shared = a & b
                factor = (2 if shared & 1 else 1) * (3 if shared & 2 else 1)
                factor *= -1 if shared & 4 else 1
                out[a ^ b] += x * y * factor
        return Q(tuple(out))

    __rmul__ = __mul__

    def __truediv__(self, divisor):
        if not isinstance(divisor, (int, Fraction)) or not divisor:
            raise ValueError("division requires a nonzero rational")
        return Q(tuple(x / divisor for x in self.coefficients))

    def conjugate(self):
        return Q(tuple(-x if a & 4 else x for a, x in enumerate(self.coefficients)))

    def squared_modulus(self):
        return self * self.conjugate()

    def serial(self):
        return [str(x) for x in self.coefficients]


def rational(value):
    return Q((Fraction(value),) + (Fraction(0),) * 7)


def basis(mask):
    if type(mask) is not int or not 0 <= mask < 8:
        raise ValueError("invalid field basis")
    return Q(tuple(Fraction(int(a == mask)) for a in range(8)))


ZERO, ONE, I = rational(0), rational(1), basis(4)
SQRT2, SQRT3 = basis(1), basis(2)
FLOOR_SQUARED = rational(2) - SQRT3 * Fraction(8, 9)


def nonnegative(value):
    """Exact sign on Q(sqrt(3)); reject other ordered-subfield requests."""
    if any(value.coefficients[a] for a in (1, 3, 4, 5, 6, 7)):
        raise ValueError("ordered comparison requires Q(sqrt(3))")
    a, b = value.coefficients[0], value.coefficients[2]
    if a >= 0 and b >= 0:
        return True
    if a < 0 and b <= 0:
        return False
    return a * a >= 3 * b * b if a >= 0 else 3 * b * b >= a * a


def root(order, exponent):
    if order not in (2, 4, 8):
        raise ValueError("finite replay supports axes 2, 4, 8")
    generator = {2: -ONE, 4: I, 8: SQRT2 * (ONE + I) / 2}[order]
    result = ONE
    for _ in range(exponent % order):
        result = result * generator
    return result


def group(shape):
    if not 1 <= len(shape) <= 3 or any(q not in (2, 4, 8) for q in shape):
        raise ValueError("invalid finite group shape")
    size = 1
    for q in shape:
        size *= q
    if size > 8:
        raise ValueError("finite replay group limit is eight")
    return tuple(product(*(range(q) for q in shape)))


def add(shape, x, y):
    return tuple((a + b) % q for q, a, b in zip(shape, x, y))


def character(shape, x, y):
    result = ONE
    for q, a, b in zip(shape, x, y):
        result = result * root(q, a * b)
    return result


def transform(values, table, sign):
    if sign not in (-1, 1):
        raise ValueError("Fourier sign must be positive or negative")
    size = len(values)
    if not 2 <= size <= 8 or len(table) != size:
        raise ValueError("invalid transform dimension")
    out = []
    for row in table:
        if len(row) != size:
            raise ValueError("invalid character table")
        terms = zip(row, values)
        out.append(sum(((z if sign == 1 else z.conjugate()) * v
                        for z, v in terms), ZERO) / size)
    return tuple(out)


def validate(shape, offset, weights):
    points = group(shape)
    if offset not in points or not any(offset):
        raise ValueError("translation must be nonzero")
    if any(add(shape, offset, offset)):
        raise ValueError("translation must have order two")
    if len(weights) != len(points):
        raise ValueError("phase count differs from group size")
    if any(w.squared_modulus() != ONE for w in weights):
        raise ValueError("weights must have modulus one")
    return points


def optimal_weights(shape, offset):
    points = group(shape)
    weights = tuple((SQRT3 - I * basis(3) * character(shape, offset, x)) / 3
                    for x in points)
    validate(shape, offset, weights)
    return weights


def basis_errors(shape, offset, alpha, beta=None, omega=None, inverse_sign=1):
    """N^4 times squared errors of the literal three-pass basis-input circuit.

    Separate phases are accepted for controls escaping the shared contract.
    """
    points = validate(shape, offset, alpha)
    beta = alpha if beta is None else beta
    omega = tuple(w.conjugate() for w in alpha) if omega is None else omega
    validate(shape, offset, beta)
    validate(shape, offset, omega)
    size = len(points)
    table = tuple(tuple(character(shape, x, y) for y in points) for x in points)
    shifted = tuple(points.index(add(shape, x, offset)) for x in points)
    forwards = tuple(transform(tuple(ONE if j == k else ZERO for j in range(size)),
                               table, -1) for k in range(size))
    errors = []
    for s, left in enumerate(forwards):
        for t, right in enumerate(forwards):
            multiplied = tuple(alpha[j] * left[shifted[j]] * beta[j]
                               * right[shifted[j]] for j in range(size))
            final = transform(multiplied, table, inverse_sign)
            wanted = add(shape, points[s], points[t])
            error = ZERO
            for j, x in enumerate(points):
                value = omega[j] * final[shifted[j]]
                if x == wanted:
                    value = value - rational(Fraction(1, size * size))
                error = error + value.squared_modulus()
            errors.append(error * size**4)
    return tuple(errors)


def coefficient_error(shape, offset, weights):
    """Relative squared Frobenius error before changing Fourier inputs."""
    points = validate(shape, offset, weights)
    values = tuple(character(shape, offset, x) for x in points)
    total = ZERO
    for x, wx in enumerate(weights):
        for y, wy in enumerate(weights):
            ratio = wx.conjugate() * wy * wy * values[x] * values[y]
            total = total + (ratio - ONE).squared_modulus()
    return total / len(points)**2


def moment_error(shape, offset, weights):
    points = validate(shape, offset, weights)
    a = tuple(w * character(shape, offset, x) for w, x in zip(weights, points))
    m = sum(a, ZERO) / len(points)
    n = sum((character(shape, offset, x) * z * z
             for x, z in zip(points, a)), ZERO) / len(points)
    term = m.conjugate() * n
    return rational(2) - term - term.conjugate()
