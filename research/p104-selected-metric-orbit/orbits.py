"""Exact finite E8 frame coverage and signed isometries. Apache-2.0.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance.
Coordinates and root labels retain the geometry.py provenance.
"""
from collections import deque

from geometry import DIM, FIRST, dot, need

PERMUTATIONS = (
    (0, 1, 2, 3, 5, 4, 7, 6),
    (0, 1, 2, 3, 6, 7, 4, 5),
    (0, 1, 3, 2, 4, 5, 7, 6),
    (0, 1, 4, 5, 2, 3, 6, 7),
    (0, 2, 1, 3, 4, 6, 5, 7),
    (1, 0, 2, 3, 4, 5, 7, 6),
)
TYPES = (
    (28, (11, 21, 38, 56, 140, 146, 161, 191),
     ((0, 1), (592, 6), (608, 16), (728, 12), (864, 1))),
    (336, (11, 21, 44, 50, 134, 152, 161, 191),
     ((0, 1), (592, 1), (600, 8), (608, 12), (728, 10))),
    (896, (11, 22, 44, 49, 133, 152, 162, 191),
     ((0, 1), (600, 6), (604, 8), (608, 7), (660, 4), (728, 6), (796, 4))),
)

QUADRATIC = (1, -1456, 520736)  # roots 728 +/- 68*sqrt(2), in mu=16*lambda


def enumerate_frames(vectors):
    """Exhaustive ordered-prefix clique search; every frame occurs once."""
    labels = sorted(vectors)
    adjacent = [sum(1 << j for j, r in enumerate(labels)
                    if dot(vectors[q], vectors[r]) == 0) for q in labels]
    frames = set()

    def extend(prefix, candidates):
        if len(prefix) == DIM:
            frames.add(tuple(labels[i] for i in prefix))
            return
        while candidates.bit_count() >= DIM - len(prefix):
            bit = candidates & -candidates
            i = bit.bit_length() - 1
            candidates ^= bit
            extend(prefix + (i,), candidates & adjacent[i])

    extend((), (1 << len(labels)) - 1)
    return frames


def root_lookup(vectors):
    lookup = {}
    for q, row in vectors.items():
        lookup[row] = q
        lookup[tuple(-x for x in row)] = q
    need(len(lookup) == 240, "ROOT_SIGNED_COUNT")
    return lookup


def checked_action(vectors, transform):
    lookup = root_lookup(vectors)
    action = {}
    for q, row in vectors.items():
        target = transform(row)
        need(target in lookup, "ROOT_CLOSURE")
        action[q] = lookup[target]
    need(set(action.values()) == set(vectors), "ROOT_BIJECTION")
    return action


def reflection_actions(vectors):
    actions = []
    for root in vectors.values():
        def reflect(row):
            product = dot(row, root)
            need(product % 2 == 0, "REFLECTION_INTEGRAL")
            return tuple(x - (product // 2) * a
                         for x, a in zip(row, root, strict=True))
        actions.append(checked_action(vectors, reflect))
    return actions


def stabilizer_actions(vectors, permutations=PERMUTATIONS):
    actions = []
    for permutation in permutations:
        need(sorted(permutation) == list(range(DIM)), "COORDINATE_PERMUTATION")
        actions.append(checked_action(vectors, lambda row: tuple(
            row[permutation[i]] for i in range(DIM))))
    for coordinate in range(DIM):
        actions.append(checked_action(vectors, lambda row: tuple(
            -x if i == coordinate else x for i, x in enumerate(row))))
    need(all(tuple(sorted(action[q] for q in FIRST)) == FIRST
             for action in actions), "STABILIZER_FIXED_FRAME")
    return actions


def orbit(start, actions):
    seen = {start}
    pending = deque([start])
    while pending:
        frame = pending.popleft()
        for action in actions:
            target = tuple(sorted(action[q] for q in frame))
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen


def orbit_partition(domain, actions):
    unseen, result = set(domain), []
    while unseen:
        reached = orbit(min(unseen), actions)
        need(reached <= unseen, "ORBIT_DOMAIN")
        unseen -= reached
        result.append(reached)
    return result
