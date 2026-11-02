"""Direct row products for the retained raw-pencil caller. Apache-2.0."""


def row_product(left, right, width, field):
    """Multiply valid rectangular field matrices, preserving empty shapes.

    The retained caller owns validation. Rows of left have len(right) entries;
    rows of right have width entries. Its dimensions are bounded by its fixed
    replay fixtures. No input row or field table is mutated or retained.
    """
    if width == 0:
        return [[] for _ in left]
    addition = field.add
    if width == 1:
        out = []
        for row in left:
            value = 0
            for coefficient, source in zip(row, right):
                if coefficient:
                    value = addition[value][field.mul[coefficient][source[0]]]
            out.append([value])
        return out
    out = [[0] * width for _ in left]
    for row, target in zip(left, out):
        for coefficient, source in zip(row, right):
            if coefficient:
                multiplication = field.mul[coefficient]
                for column in range(width):
                    target[column] = addition[target[column]][multiplication[source[column]]]
    return out
