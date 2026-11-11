"""Exact paired-neighbour path reduction. Apache-2.0.

The source-specific application was produced by Nick Petalas.
Binary Lagrangian geometry and min-plus elimination are classical.
"""

from itertools import combinations


def need(condition, message):
    if not condition:
        raise ValueError(message)


def binary_rank(rows, width):
    need(1 <= width <= 9 and len(rows) <= 2 * width, "bounded binary basis")
    need(all(0 <= x < 1 << (2 * width) for x in rows), "binary coordinate range")
    pivots = [0] * (2 * width)
    rank = 0
    for value in rows:
        for bit in range(2 * width - 1, -1, -1):
            if value >> bit & 1:
                if pivots[bit]:
                    value ^= pivots[bit]
                else:
                    pivots[bit] = value
                    rank += 1
                    break
    return rank


def neighbours(width):
    """Two distinct neighbours for each nonzero normal x, in paired order."""
    need(1 <= width <= 9, "supported width")
    origin = tuple(1 << (width + j) for j in range(width))
    images = []
    for normal in range(1, 1 << width):
        pivot = (normal & -normal).bit_length() - 1
        for tag in range(2):
            axis = normal | (tag << (width + pivot))
            images.append(tuple(v ^ axis if (v >> width & normal).bit_count() % 2
                                else v for v in origin))
    need(len(images) == 2 * ((1 << width) - 1), "complete paired domain")
    return tuple(images)


def label_distance(left, right):
    if left == right:
        return 0
    return 1 if left // 2 == right // 2 else 2


def transform(values, prefix):
    """Return min_i(values[i] + min(distance(i,k),prefix) - 2), with witnesses."""
    need(4 <= len(values) <= 1022 and len(values) % 2 == 0, "paired label domain")
    need(1 <= prefix <= 9 and all(type(x) is int for x in values), "integer prefix cost")
    pair_minima = []
    for pair in range(len(values) // 2):
        index = min((2 * pair, 2 * pair + 1), key=lambda i: (values[i], i))
        pair_minima.append((values[index], index))
    best_two = sorted(pair_minima)[:2]
    result = []
    for label in range(len(values)):
        other = best_two[0] if best_two[0][1] // 2 != label // 2 else best_two[1]
        options = ((values[label] - 2, label),
                   (values[label ^ 1] - 1, label ^ 1),
                   (other[0] + min(2, prefix) - 2, other[1]))
        result.append(min(options))
    return tuple(result)


def path_minimum(left, middle, right, prefix):
    need(len(left) == len(middle) == len(right), "equal path domains")
    lcost, rcost = transform(left, prefix), transform(right, prefix)
    return min((middle[k] + lcost[k][0] + rcost[k][0],
                (lcost[k][1], k, rcost[k][1])) for k in range(len(middle)))


def induced_paths(vertices, edges):
    need(len(vertices) <= 184 and len(edges) <= 264, "bounded source graph")
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        need(a in vertices and b in vertices and a != b, "internal simple edge")
        need(b not in adjacency[a], "no duplicate internal edge")
        adjacency[a].add(b)
        adjacency[b].add(a)
    paths = []
    for middle in sorted(vertices):
        for left, right in combinations(sorted(adjacency[middle]), 2):
            if right not in adjacency[left]:
                paths.append((left, middle, right))
    return tuple(paths)
