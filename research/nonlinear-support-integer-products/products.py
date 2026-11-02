"""Exact Gaussian-dyadic matrix products with one denominator per operand.

Produced by Nick Petalas. Apache-2.0.
"""
from fractions import Fraction

MAX_DIMENSION = 16
MAX_NUMERATOR_BITS = 256
MAX_DENOMINATOR_BITS = 64
ZERO = (Fraction(0), Fraction(0))


def scaled(matrix, zero):
    """Validate a bounded square matrix and clear its dyadic denominators."""
    size = len(matrix)
    if not 1 <= size <= MAX_DIMENSION:
        raise ValueError("matrix dimension")
    exponent = 0
    nonzero = []
    for row in matrix:
        if len(row) != size:
            raise ValueError("square matrix required")
        entries = []
        for column, entry in enumerate(row):
            if entry is zero:
                continue
            if len(entry) != 2:
                raise ValueError("Gaussian pair required")
            if any(type(value) is not Fraction for value in entry):
                raise ValueError("Fraction components required")
            if not entry[0].numerator and not entry[1].numerator:
                continue
            for value in entry:
                denominator = value.denominator
                if denominator & (denominator - 1):
                    raise ValueError("non-dyadic component")
                bits = denominator.bit_length() - 1
                if bits > MAX_DENOMINATOR_BITS:
                    raise ValueError("denominator capacity")
                if abs(value.numerator).bit_length() > MAX_NUMERATOR_BITS:
                    raise ValueError("numerator capacity")
                exponent = max(exponent, bits)
            entries.append((column, entry))
        nonzero.append(entries)
    rows = []
    for row in nonzero:
        converted = []
        for column, (real, imaginary) in row:
            re = real.numerator << (exponent - (real.denominator.bit_length() - 1))
            im = imaginary.numerator << (exponent - (imaginary.denominator.bit_length() - 1))
            converted.append((column, (re, im)))
        rows.append(converted)
    return rows, exponent


def product(left, right, zero=ZERO):
    """Return the ordinary matrix product, with exact Fraction output pairs."""
    if type(zero) is not tuple or len(zero) != 2 or any(
            type(value) is not Fraction or value.numerator for value in zero):
        raise ValueError("zero pair required")
    a, first = scaled(left, zero)
    b, second = scaled(right, zero)
    size = len(a)
    if len(b) != size:
        raise ValueError("matrix dimensions differ")
    denominator = 1 << (first + second)
    output = [[zero for _ in range(size)] for _ in range(size)]
    for i, row in enumerate(a):
        real = [0] * size
        imaginary = [0] * size
        for k, (ar, ai) in row:
            for j, (br, bi) in b[k]:
                real[j] += ar * br - ai * bi
                imaginary[j] += ar * bi + ai * br
        for j in range(size):
            if real[j] or imaginary[j]:
                output[i][j] = (Fraction(real[j], denominator),
                                Fraction(imaginary[j], denominator))
    return output
