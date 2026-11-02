"""Bounded finite-field row elimination, produced by Nick Petalas. Apache-2.0."""

MAX_ORDER = 25
MAX_ROWS = 729
MAX_COLUMNS = 162


class RowKernel:
    """Own one immutable arithmetic table for one source Field instance."""

    def __init__(self, field):
        if not 2 <= field.q <= MAX_ORDER:
            raise ValueError("field order outside row-kernel contract")
        self.q = field.q
        self.mul = tuple(tuple(row) for row in field.mul)
        self.inv = tuple(field.inv)
        self.neg = tuple(field.neg)
        self.updates = tuple(
            tuple(tuple(field.add[x][field.mul[c][y]] for y in range(field.q))
                  for x in range(field.q))
            for c in range(field.q)
        )

    def rref(self, matrix, width):
        """Return the source's exact full rows and pivot order, without aliasing."""
        if (type(width) is not int or not 0 <= width <= MAX_COLUMNS
                or len(matrix) > MAX_ROWS):
            raise ValueError("matrix outside row-kernel capacity")
        size = len(matrix[0]) if matrix else width
        if (not width <= size <= MAX_COLUMNS
                or any(len(row) != size for row in matrix)
                or any(type(x) is not int or not 0 <= x < self.q
                       for row in matrix for x in row)):
            raise ValueError("invalid row-kernel matrix")
        return self.reduce(matrix, width)

    def reduce(self, matrix, width):
        """Internal source calls already satisfy canonical field/shape contracts."""
        if not 0 <= width <= MAX_COLUMNS or len(matrix) > MAX_ROWS:
            raise ValueError("matrix outside row-kernel capacity")
        if matrix and len(matrix[0]) > MAX_COLUMNS:
            raise ValueError("augmented row outside row-kernel capacity")
        rows = [row[:] for row in matrix]
        pivots = []
        k = 0
        mul, inv, neg = self.mul, self.inv, self.neg
        for j in range(width):
            pivot = next((i for i in range(k, len(rows)) if rows[i][j]), None)
            if pivot is None:
                continue
            rows[k], rows[pivot] = rows[pivot], rows[k]
            scale = mul[inv[rows[k][j]]]
            normalized = [scale[x] for x in rows[k]]
            rows[k] = normalized
            for i in range(len(rows)):
                if i != k and rows[i][j]:
                    update = self.updates[neg[rows[i][j]]]
                    rows[i] = [update[x][y] for x, y in zip(rows[i], normalized)]
            pivots.append(j)
            k += 1
            if k == len(rows):
                break
        return rows, pivots


def install(module):
    """Patch only Field construction and rref in one private source module."""
    original_field = module.Field

    class PreparedField(original_field):
        def __init__(self, p, modulus):
            if (type(p) is int and isinstance(modulus, (tuple, list))
                    and len(modulus) >= 2 and p >= 2
                    and p ** (len(modulus) - 1) > MAX_ORDER):
                raise ValueError("field order outside row-kernel contract")
            super().__init__(p, modulus)
            self.row_kernel = RowKernel(self)

    def prepared_rref(matrix, width, field):
        return field.row_kernel.reduce(matrix, width)

    module.Field = PreparedField
    module.rref = prepared_rref
