"""Dimension-only schedules for the exact Leibniz determinant, through size five."""

from itertools import permutations
from math import prod


def make_schedules():
    """Initialize the bounded immutable table; matrix values never enter it."""
    return tuple(
        tuple(
            (p, (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n)))
            for p in permutations(range(n))
        )
        for n in range(6)
    )


SCHEDULES = make_schedules()


def determinant(matrix):
    """Evaluate every Leibniz term with its precomputed sign, without division."""
    n = len(matrix)
    if n == 1 and len(matrix[0]) == 1:
        return matrix[0][0]
    if n == 2 and len(matrix[0]) == len(matrix[1]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if n > 5 or any(len(row) != n for row in matrix):
        raise ValueError("square determinant dimension must be between zero and five")
    return sum(
        sign * prod(matrix[i][p[i]] for i in range(n))
        for p, sign in SCHEDULES[n]
    )
