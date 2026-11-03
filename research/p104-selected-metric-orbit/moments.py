"""Exact root second moments behind the Hermitian extension. Apache-2.0.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance.
The lead proposed the skew-sector identity; worker A checked its derivation
and implemented these independent root-moment obligations.
"""
from geometry import DIM, dot, need
from verify import rejected


def second_moment(rows):
    return [[sum(row[i] * row[j] for row in rows) for j in range(DIM)]
            for i in range(DIM)]


def check_tight(moment):
    need(moment == [[60 * int(i == j) for j in range(DIM)] for i in range(DIM)],
         "MOMENT_TIGHT_FRAME")


def check_star(root, neighbors):
    expected = [[36 * int(i == j) - 9 * root[i] * root[j] for j in range(DIM)]
                for i in range(DIM)]
    need(second_moment(neighbors) == expected, "MOMENT_ORTHOGONAL_STAR")
    need(len(neighbors) == 63, "MOMENT_STAR_DEGREE")


def check_moments(vectors):
    need(len(vectors) == 120, "MOMENT_ROOT_COUNT")
    tight = second_moment(list(vectors.values()))
    check_tight(tight)
    for root in vectors.values():
        neighbors = [row for row in vectors.values() if dot(root, row) == 0]
        check_star(root, neighbors)
    damaged = [row[:] for row in tight]
    damaged[0][0] += 1
    rejected(lambda: check_tight(damaged), "MOMENT_TIGHT_FRAME")
    root = next(iter(vectors.values()))
    neighbors = [row for row in vectors.values() if dot(root, row) == 0]
    rejected(lambda: check_star(root, neighbors[:-1]), "MOMENT_ORTHOGONAL_STAR")
    return {"full_tight_frame_coefficient": 15,
            "orthogonal_stars_checked": 120, "orthogonal_star_coefficient": 9,
            "skew_sector_lower_bound": "101/2", "negative_controls": 2}
