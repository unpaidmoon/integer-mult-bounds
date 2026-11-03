"""Exact tail-only modular elimination, produced by Nick Petalas. Apache-2.0."""


def validate(matrix, prime):
    if not matrix:
        raise IndexError("empty modular matrix")
    width = len(matrix[0])
    if len(matrix) > 64 or width > 64:
        raise ValueError("matrix capacity exceeded")
    if any(len(row) != width for row in matrix):
        raise ValueError("ragged modular matrix")
    if not isinstance(prime, int) or prime < 2:
        raise ValueError("invalid field modulus")
    return width


def tail_rank(matrix, prime, inverse, counts=None):
    """Preserve pivot order and residues, skipping proved-zero row prefixes."""
    width = validate(matrix, prime)
    rows = [[int(x.numerator) * inverse(int(x.denominator) % prime, prime) % prime
             for x in row] for row in matrix]
    height = len(rows)
    pivot = 0
    for column in range(width):
        selected = next((i for i in range(pivot, height) if rows[i][column]), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        factor = pow(rows[pivot][column], -1, prime)
        rows[pivot][column:] = [(x * factor) % prime for x in rows[pivot][column:]]
        if counts is not None:
            counts["full_products"] += width
            counts["tail_products"] += width - column
        for i in range(pivot + 1, height):
            if rows[i][column]:
                factor = rows[i][column]
                rows[i][column:] = [(x - factor * y) % prime
                                   for x, y in zip(rows[i][column:], rows[pivot][column:])]
                if counts is not None:
                    counts["full_products"] += width
                    counts["tail_products"] += width - column
        pivot += 1
        if pivot == height:
            break
    if counts is not None:
        counts["kernel_calls"] += 1
    return pivot
