#!/usr/bin/env python3
"""Exact price of a weight-3 step on the five-source dirty connector.

Standard library only. No assert statements, so python -O runs the same checks.
Every loop has an explicit finite bound.

The interface is research/universal-connector-boundary: five read-only sources,
one arbitrarily dirty connector z, and all 31 nonzero output rows. Every nonempty
source subset S is one complete call T_S, charged one dispatch plus |S| source
additions. A readout A_m costs one dispatch and one addition. Prices are o >= 0
per dispatch and p > 0 per addition.

A source word is a closed walk in F_2^5. Row m is a difference of two prefixes
exactly when two readouts can realize it. Rows that are not differences need at
least four readouts. This file proves that every correct schedule using at least
one weight-3 call costs at least 72o + 76p, and exhibits a schedule attaining it.
"""

import random

N = 5
NMASK = (1 << N) - 1
FULL = ((1 << (NMASK + 1)) - 1) - 1  # bits 1..31
READOUTS = 2 * NMASK
CENSUS_LIMIT = 5 ** 9  # 1,953,125 nine-singleton words

# One triple (14 = {1,2,3}), two DUOs (24 = {3,4}, 12 = {2,3}) and seven singletons.
WITNESS = [8, 1, 16, 14, 16, 1, 16, 2, 24, 12]
# Published DUO word. Recomputed here; not trusted as a price.
DUO = [1, 2, 8, 18, 12, 16, 1, 2, 4, 2]
# Published one-triple near-cover from research/one-triple-ten-step-obstruction.
NEAR = [1, 8, 1, 2, 1, 16, 4, 8, 16, 7]


def fail(message):
    raise SystemExit("FAIL " + message)


def require(ok, message):
    if not ok:
        fail(message)


def weight(mask):
    return mask.bit_count()


def prefixes(steps):
    state = 0
    out = [0]
    for step in steps:
        require(1 <= step <= NMASK, "toggle outside F_2^5: %r" % (step,))
        state ^= step
        out.append(state)
    return out


def difference_mask(points):
    seen = 0
    unique = []
    for point in points:
        if (seen >> point) & 1:
            continue
        seen |= 1 << point
        unique.append(point)
    mask = 0
    for i, left in enumerate(unique):
        for right in unique[i + 1:]:
            mask |= 1 << (left ^ right)
    return mask & FULL


def missing_rows(steps):
    pre = prefixes(steps)
    require(pre[-1] == 0, "word is not closed")
    return NMASK - difference_mask(pre).bit_count()


def build_schedule(steps):
    """Two readouts at the first boundary pair of every nonzero mask."""
    pre = prefixes(steps)
    require(pre[-1] == 0, "schedule word is not closed")
    first = {}
    for i in range(len(pre)):
        for j in range(i + 1, len(pre)):
            first.setdefault(pre[i] ^ pre[j], (i, j))
    at = {boundary: [] for boundary in range(len(pre))}
    for row in range(1, NMASK + 1):
        pair = first.get(row)
        require(pair is not None, "no readout pair for row %d" % row)
        at[pair[0]].append(row)
        at[pair[1]].append(row)
    ops = []
    for boundary in range(len(pre)):
        for row in at[boundary]:
            ops.append(("A", row))
        if boundary < len(steps):
            ops.append(("T", steps[boundary]))
    return ops


def schedule_cost(ops):
    queries = len(ops)
    additions = 0
    for kind, arg in ops:
        additions += weight(arg) if kind == "T" else 1
    return queries, additions


def evaluate_generic(ops):
    """z carries z0 in bit 0 and B_j x_j in bit 1+j. Correctness is exact for every map."""
    connector = 1
    rows = [0] * (NMASK + 1)
    for kind, arg in ops:
        if kind == "T":
            for source in range(N):
                if (arg >> source) & 1:
                    connector ^= 1 << (1 + source)
        else:
            rows[arg] ^= connector
    if connector != 1:
        return False
    for row in range(1, NMASK + 1):
        want = 0
        for source in range(N):
            if (row >> source) & 1:
                want |= 1 << (1 + source)
        if rows[row] != want:
            return False
    return True


def apply_map(matrix, vector, width):
    out = 0
    for bit in range(width):
        if (vector >> bit) & 1:
            out ^= matrix[bit]
    return out


def run_concrete(ops, matrices_b, matrices_a, sources, z0, y0, width):
    connector = z0
    rows = list(y0)
    for kind, arg in ops:
        if kind == "T":
            for source in range(N):
                if (arg >> source) & 1:
                    connector ^= apply_map(matrices_b[source], sources[source], width)
        else:
            rows[arg] ^= apply_map(matrices_a[arg], connector, width)
    if connector != z0:
        return False
    for row in range(1, NMASK + 1):
        total = 0
        for source in range(N):
            if (row >> source) & 1:
                total ^= apply_map(matrices_b[source], sources[source], width)
        if rows[row] != (y0[row] ^ apply_map(matrices_a[row], total, width)):
            return False
    return True


def check_concrete(ops):
    width = 3
    identity = [1 << bit for bit in range(width)]
    sources = [1, 2, 3, 4, 5]
    z0 = 7
    y0 = [((row * 3) + 1) & 7 for row in range(NMASK + 1)]
    mats_b = [list(identity) for _ in range(N)]
    mats_a = [list(identity) for _ in range(NMASK + 1)]
    require(
        run_concrete(ops, mats_b, mats_a, sources, z0, y0, width),
        "fixed dirty identity-map trial failed",
    )
    rng = random.Random(20261111)
    for _ in range(40):
        mats_b = [[rng.randrange(1 << width) for _ in range(width)] for _ in range(N)]
        mats_a = [[rng.randrange(1 << width) for _ in range(width)] for _ in range(NMASK + 1)]
        sources = [rng.randrange(1 << width) for _ in range(N)]
        z0 = rng.randrange(1 << width)
        y0 = [rng.randrange(1 << width) for _ in range(NMASK + 1)]
        require(
            run_concrete(ops, mats_b, mats_a, sources, z0, y0, width),
            "random dirty trial failed",
        )


def nine_and_ten_point_counts():
    """Covers containing 0 and the standard basis. Translation and GL(5,2) reduce to this."""
    base = [0] + [1 << source for source in range(N)]
    rest = [point for point in range(1, NMASK + 1) if point not in base]
    counts = {9: 0, 10: 0}
    span = len(rest)
    for extra in (3, 4):
        # combinations of `extra` points from 26, written as nested index loops
        chosen = [0] * extra
        # start at the first increasing tuple
        for i in range(extra):
            chosen[i] = i
        while True:
            points = list(base)
            for index in chosen:
                points.append(rest[index])
            if difference_mask(points) == FULL:
                counts[len(base) + extra] += 1
            cursor = extra - 1
            while cursor >= 0 and chosen[cursor] == span - extra + cursor:
                cursor -= 1
            if cursor < 0:
                break
            chosen[cursor] += 1
            for follow in range(cursor + 1, extra):
                chosen[follow] = chosen[follow - 1] + 1
    return counts


def weight_min(length):
    """Least even source-addition count of a length-`length` walk with a weight-3 step."""
    # One weight-3 step and length-1 singletons sum to length+2, which may be odd.
    total = length + 2
    if total & 1:
        total += 1
    return total


def uncovered_floor(size):
    pairs = size * (size - 1) // 2
    least = NMASK - pairs
    if least < 0:
        least = 0
    if size <= 9 and least < 1:
        least = 1
    return least


def check_corner():
    """The only (T, s, u) whose addition lower bound is below 76."""
    below = []
    query_floor = None
    for length in range(1, 41):
        for size in range(1, length + 1):
            missing = uncovered_floor(size)
            additions = weight_min(length) + 2 * missing
            queries = length + 2 * missing
            if query_floor is None or queries < query_floor:
                query_floor = queries
            if additions < 14:
                below.append((length, size, missing, weight_min(length)))
    require(query_floor == 10, "query support floor is %r, not 10" % (query_floor,))
    require(below == [(10, 10, 0, 12)], "unexpected addition corners %r" % (below,))


def dp_weight3_count():
    counts = [0] * (NMASK + 1)
    counts[0] = 1
    for _ in range(9):
        nxt = [0] * (NMASK + 1)
        for mask in range(NMASK + 1):
            have = counts[mask]
            if have == 0:
                continue
            for source in range(N):
                nxt[mask ^ (1 << source)] += have
        counts = nxt
    return sum(counts[mask] for mask in range(NMASK + 1) if weight(mask) == 3)


def census_weight3_corner():
    """Every closed ten-step word with one triple and nine singletons, triple rotated last.

    Rotation translates the prefix set, so it preserves differences. The closing
    triple is the XOR of the nine singleton steps. Words with a repeated prefix
    have at most nine points and are excluded by the nine-point check; this scan
    records full covers among the ten-point words.
    """
    digits = [0] * 9
    seen_words = 0
    weight3 = 0
    full = 0
    best = 0
    while seen_words < CENSUS_LIMIT:
        xor = 0
        state = 0
        seen = 1
        repeat = False
        for digit in digits:
            bit = 1 << digit
            xor ^= bit
            state ^= bit
            if (seen >> state) & 1:
                repeat = True
            seen |= 1 << state
        if weight(xor) == 3:
            weight3 += 1
            if not repeat and seen.bit_count() == 10:
                points = [0]
                state = 0
                for digit in digits:
                    state ^= 1 << digit
                    points.append(state)
                covered = difference_mask(points).bit_count()
                if covered > best:
                    best = covered
                if covered == NMASK:
                    full += 1
        seen_words += 1
        cursor = 8
        while cursor >= 0:
            digits[cursor] += 1
            if digits[cursor] < N:
                break
            digits[cursor] = 0
            cursor -= 1
        else:
            break
    require(seen_words == CENSUS_LIMIT, "singleton census ended at %d words" % seen_words)
    return weight3, full, best


def check_witness():
    weights = [weight(step) for step in WITNESS]
    require(weights.count(3) == 1 and weights.count(2) == 2 and weights.count(1) == 7,
            "witness weights %r" % (weights,))
    require(missing_rows(WITNESS) == 0, "witness does not cover every row")
    require(sum(weights) == 14 and len(WITNESS) == 10, "witness length or addition count")
    ops = build_schedule(WITNESS)
    require(schedule_cost(ops) == (72, 76), "witness schedule cost %r" % (schedule_cost(ops),))
    require(evaluate_generic(ops), "witness fails the generic-operator replay")
    check_concrete(ops)
    # A dropped readout is no longer correct for arbitrary dirt.
    damaged = [op for op in ops if op != ("A", 1)]
    require(not evaluate_generic(damaged), "dropping row 1 was still accepted")
    # Replacing the triple by a singleton leaves the walk unclosed or short of cover.
    broken = list(WITNESS)
    broken[3] = 1
    pre = prefixes(broken)
    require(pre[-1] != 0 or difference_mask(pre) != FULL, "broken witness still covers")


def check_controls():
    duo_ops = build_schedule(DUO)
    require(schedule_cost(duo_ops) == (72, 74), "DUO control cost %r" % (schedule_cost(duo_ops),))
    require(evaluate_generic(duo_ops), "DUO control fails generic replay")
    require(all(weight(step) != 3 for step in DUO), "DUO control uses a weight-3 step")
    require(missing_rows(NEAR) == 2, "near-cover missing-row count %d" % missing_rows(NEAR))
    require(weight(NEAR[-1]) == 3, "near-cover does not end in a triple")
    # Ten steps, twelve additions, two missing rows: addition floor 78, not a 74-addition word.
    require(12 + READOUTS + 4 == 78, "near-cover arithmetic")
    counts = nine_and_ten_point_counts()
    require(counts[9] == 0, "nine-point normal form found %d covers" % counts[9])
    require(counts[10] == 80, "ten-point normal form count %d" % counts[10])
    require(difference_mask(prefixes(DUO)[:-1]) == FULL, "DUO prefixes are not a cover")


def main():
    # The nine-point exclusion is an input to the corner table, so it runs first.
    check_controls()
    check_corner()
    weight3, full, best = census_weight3_corner()
    require(weight3 == dp_weight3_count(), "DP weight-3 count disagrees with the census")
    require(full == 0, "a ten-step one-triple nine-singleton word covers every row")
    require(best == 29, "ten-point one-triple maximum is %d nonzero rows" % best)
    check_witness()
    print(
        "PASS_WEIGHT3_TOGGLE_PRICE queries=72 additions=76 "
        "duo=(72,74) nine_point_covers=0 weight3_full_covers=0 "
        "best_nonzero=29 weight3_sequences=%d no_new_kappa" % weight3
    )


if __name__ == "__main__":
    main()
