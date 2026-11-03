"""Intersection counters produced by Nick Petalas. Apache-2.0.

Ali Romman's PR5729 supplies the injected population and threshold routines.
"""


def need(condition, message):
    if not condition:
        raise ValueError(message)


def checked_rows(generators, width, maximum, batch_bits):
    need(type(width) is int and 0 <= width <= 127, "width outside 0..127")
    need(type(maximum) is int and 0 <= maximum <= width, "invalid weight bound")
    need(type(batch_bits) is int and 1 <= batch_bits <= 20, "invalid batch size")
    rows = []
    pivots = {}
    for index, row in enumerate(generators):
        need(index < 27, "dimension exceeds 27")
        need(type(row) is int and 0 < row < 1 << width, "invalid generator")
        residual = row
        for pivot in range(width - 1, -1, -1):
            if residual >> pivot & 1:
                if pivot in pivots:
                    residual ^= pivots[pivot]
                else:
                    pivots[pivot] = residual
                    break
        need(residual != 0, "dependent generators")
        rows.append(row)
    count = min(batch_bits, len(rows))
    need(len(rows) - count <= 16, "batch count exceeds 65536")
    return tuple(rows), count


def lane_columns(rows, width, count, mask):
    columns = [0] * width
    for index in range(count):
        block = 1 << index
        pattern = mask // ((1 << (2 * block)) - 1) * (((1 << block) - 1) << block)
        row = rows[index]
        for coordinate in range(width):
            if row >> coordinate & 1:
                columns[coordinate] ^= pattern
    return columns


def translated_planes(base, intersection, offset_weight, mask, powers):
    """Compute base + offset_weight - 2*intersection modulo 2**powers."""
    result = []
    carry = 0
    for power in range(powers):
        a = base[power] if power < len(base) else 0
        b = mask if offset_weight >> power & 1 else 0
        parity = a ^ b
        result.append(parity ^ carry)
        carry = (a & b) | (parity & carry)
    borrow = 0
    for power in range(powers):
        a = result[power]
        b = intersection[power - 1] if 1 <= power <= len(intersection) else 0
        result[power] = a ^ b ^ borrow
        borrow = ((~a) & (b | borrow)) | (b & borrow)
    return result


def selected_word(rows, coefficient, offset):
    word = offset
    for index in range(min(20, len(rows))):
        if coefficient >> index & 1:
            word ^= rows[index]
    return word


def low_weight_words(generators, width, maximum, batch_bits=16, *,
                     population_planes, at_most):
    rows, count = checked_rows(generators, width, maximum, batch_bits)
    lanes = 1 << count
    mask = (1 << lanes) - 1
    columns = lane_columns(rows, width, count, mask)
    base = population_planes(columns)
    offset = 0
    for index in range(1 << (len(rows) - count)):
        if index:
            changed = (index & -index).bit_length() - 1
            offset ^= rows[count + changed]
        terms = [columns[j] for j in range(width) if offset >> j & 1]
        intersection = population_planes(terms)
        planes = translated_planes(base, intersection, offset.bit_count(),
                                   mask, width.bit_length())
        hits = at_most(planes, maximum, mask)
        for _ in range(lanes):
            if not hits:
                break
            low = hits & -hits
            coefficient = low.bit_length() - 1
            yield selected_word(rows, coefficient, offset)
            hits ^= low
        need(hits == 0, "lane extraction exhausted")
