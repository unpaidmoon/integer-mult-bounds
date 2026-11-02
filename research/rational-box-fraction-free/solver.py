"""Bounded rational solves by classical fraction-free elimination.

Produced by Nick Petalas. Apache-2.0.
"""
from fractions import Fraction
from math import lcm


def integer_rows(matrix, rhs):
    """Clear each augmented row with its own positive denominator."""
    size = len(matrix)
    if not 1 <= size <= 6 or len(rhs) != size:
        raise ValueError("Use square systems of size 1..6")
    result = []
    for row, value in zip(matrix, rhs):
        if len(row) != size:
            raise ValueError("Wrong matrix row size")
        entries = list(row) + [value]
        if any(type(x) is not Fraction for x in entries):
            raise ValueError("Use exact Fraction entries")
        if any(abs(x.numerator) > 10**9 or x.denominator > 10**9 for x in entries):
            raise ValueError("Input rational limit is 10^9")
        scale = lcm(*(x.denominator for x in entries))
        result.append([x.numerator * (scale // x.denominator) for x in entries])
    return result


def solve(matrix, rhs):
    """Return the unique solution, or None for a singular coefficient matrix."""
    rows = integer_rows(matrix, rhs)
    size = len(rows)
    previous = 1
    for column in range(size - 1):
        pivot = next((i for i in range(column, size) if rows[i][column]), None)
        if pivot is None:
            return None
        rows[column], rows[pivot] = rows[pivot], rows[column]
        diagonal = rows[column][column]
        for i in range(column + 1, size):
            for j in range(column + 1, size + 1):
                numerator = diagonal * rows[i][j] - rows[i][column] * rows[column][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ValueError("Fraction-free division invariant failed")
                rows[i][j] = quotient
            rows[i][column] = 0
        previous = diagonal
    if not rows[-1][size - 1]:
        return None
    answer = [Fraction(0)] * size
    for i in range(size - 1, -1, -1):
        tail = sum((rows[i][j] * answer[j] for j in range(i + 1, size)), Fraction(0))
        answer[i] = (rows[i][-1] - tail) / rows[i][i]
    return answer
