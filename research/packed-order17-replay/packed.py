"""Bounded exact signed Kronecker products. Produced by Nick Petalas. Apache-2.0."""

from functools import reduce
from itertools import chain
from math import gcd

MAX_SIZE = 16
MAX_BITS = 4096


def validate(matrix):
    """Validate the only public arithmetic boundary before allocating packs."""
    rows, denominator = matrix
    size = len(rows)
    if not 1 <= size <= MAX_SIZE or type(denominator) is not int or denominator <= 0:
        raise ValueError("positive denominator and dimension 1..16 required")
    if denominator.bit_length() > MAX_BITS:
        raise ValueError("denominator exceeds 4096 bits")
    if any(len(row) != size for row in rows):
        raise ValueError("square matrix required")
    if any(len(entry) != 2 for row in rows for entry in row):
        raise ValueError("Gaussian integer pair required")
    # The int descriptor also rejects non-integer components. No per-value
    # Python wrapper is needed to compute the magnitude bound.
    components = chain.from_iterable(chain.from_iterable(rows))
    maximum_bits = max(map(int.bit_length, components))
    if maximum_bits > MAX_BITS:
        raise ValueError("integer components exceed 4096 bits")
    return size, maximum_bits


def pack(vector, bits):
    real = imag = 0
    for index, (x, y) in enumerate(vector):
        real += x << (bits * index)
        imag += y << (bits * index)
    return real, imag


def middle(product, bits, size):
    shift = bits * (size - 1)
    rounded = (product + (1 << (shift - 1))) >> shift if shift else product
    base = 1 << bits
    residue = rounded % base
    return residue - base if residue >= base // 2 else residue


def multiply(left, right):
    """Return exactly the source's reduced Gaussian-rational matrix product."""
    size, left_bits = validate(left)
    other_size, right_bits = validate(right)
    if size != other_size:
        raise ValueError("equal matrix sizes required")
    bits = left_bits + right_bits + (2 * size).bit_length()
    a, da = left
    b, db = right
    rows = [pack(row, bits) for row in a]
    columns = [pack(column[::-1], bits) for column in zip(*b, strict=True)]
    output = []
    for ar, ai in rows:
        row = []
        for br, bi in columns:
            real = middle(ar * br, bits, size) - middle(ai * bi, bits, size)
            imag = middle(ar * bi, bits, size) + middle(ai * br, bits, size)
            row.append((real, imag))
        output.append(row)
    denominator = da * db
    common = reduce(gcd, (v for row in output for entry in row for v in entry), denominator)
    result = tuple(tuple((x // common, y // common) for x, y in row) for row in output)
    return result, denominator // common
