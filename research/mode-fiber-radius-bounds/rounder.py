"""Constructive radius-below-two rounder for the PR4933 mode map (PROOF.md, Theorem C).

Exact rational arithmetic, standard library only. Given y in [0,1)^112 whose
mode vector t = M^T y lies in L, returns an integer z with M^T z = t and
max_i |z_i - y_i| < 2. Every step of Theorem C is executed literally, so a
failure of any lemma raises instead of being silently repaired.
Prepared for apoursh with substantial Anthropic Claude assistance. Apache-2.0.
"""
from fractions import Fraction as Q
import itertools


def need(condition, message):
    if not condition:
        raise ValueError(message)


def blocks_of(rows):
    """Support blocks: support -> (row indices, pinned coordinate, pin sign, free coordinates)."""
    out = {}
    for i, r in enumerate(rows):
        out.setdefault(tuple(j for j in range(8) if r[j]), []).append(i)
    info = {}
    for s, ix in out.items():
        fixed = [j for j in s if len({rows[i][j] for i in ix}) == 1]
        need(len(ix) == 8 and len(fixed) == 1, 'block has one pinned coordinate')
        p, free = fixed[0], [j for j in s if j != fixed[0]]
        need({tuple(rows[i][j] for j in free) for i in ix} == set(itertools.product((-1, 1), repeat=3)),
             'block rows are every sign pattern on the free coordinates')
        info[s] = (ix, p, rows[ix[0]][p], free)
    return info


def pairs_for(rows, block, j):
    """Four disjoint row pairs (a, b) of the block with m_a - m_b = 2 e_j or m_a + m_b = 2 e_j (signed)."""
    ix, p, sign, free = block
    out, used = [], set()
    for a in ix:
        if a in used:
            continue
        if j == p:  # antipodal on the free coordinates: m_a + m_b = 2 sign e_p
            b = next(b for b in ix if all(rows[b][k] == -rows[a][k] for k in free))
            out.append(('sum', a, b))
        else:       # flip coordinate j only: m_a - m_b = 2 rows[a][j] e_j
            b = next(b for b in ix if b != a and all(rows[b][k] == rows[a][k] for k in range(8) if k != j))
            out.append(('diff', a, b))
        used.update((a, b))
    need(len(out) == 4, 'four disjoint pairs')
    return out


def null_vector(vectors):
    """A nonzero rational dependency among the given 8-dimensional vectors (len(vectors) == 9)."""
    n = len(vectors)
    a = [[Q(vectors[k][j]) for k in range(n)] for j in range(8)]
    pivots, r = [], 0
    for c in range(n):
        piv = next((i for i in range(r, 8) if a[i][c]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        a[r] = [x / a[r][c] for x in a[r]]
        for i in range(8):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
    freec = next(c for c in range(n) if c not in pivots)
    d = [Q(0)] * n
    d[freec] = Q(1)
    for row, c in enumerate(pivots):
        d[c] = -a[row][freec]
    return d


def vertex(rows, y):
    """Move y within {y' in [0,1]^112 : M^T y' = M^T y} until the fractional rows are independent."""
    y = list(y)
    while True:
        frac = [i for i in range(112) if y[i].denominator != 1]
        if len(frac) <= 8:
            if rank_of([rows[i] for i in frac]) == len(frac):
                return y, frac
            sample, d = frac, small_dependency(rows, frac)
        else:
            sample = frac[:9]
            d = null_vector([rows[i] for i in sample])
        steps = []
        for i, di in zip(sample, d):
            if di > 0:
                steps.append((1 - y[i]) / di)
            elif di < 0:
                steps.append(-y[i] / di)
        step = min(steps)
        for i, di in zip(sample, d):
            y[i] += step * di


def rank_of(vectors):
    rows, r = [[Q(v) for v in vec] for vec in vectors], 0
    for c in range(8):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def small_dependency(rows, frac):
    for k in range(2, len(frac) + 1):
        for sub in itertools.combinations(frac, k):
            if rank_of([rows[i] for i in sub]) < k:
                vecs = [rows[i] for i in sub] + [(0,) * 8] * (9 - k)
                d = null_vector(vecs)[:k]
                if any(d):
                    full = {i: Q(0) for i in frac}
                    full.update(dict(zip(sub, d)))
                    return [full[i] for i in frac]
    raise ValueError('no dependency')


def matching(demand, good):
    """Distinct good blocks for each coordinate with nonzero demand (augmenting paths)."""
    owner = {}

    def augment(j, seen):
        for s in good:
            if j in s and s not in seen:
                seen.add(s)
                if s not in owner or augment(owner[s], seen):
                    owner[s] = j
                    return True
        return False

    for j in [j for j in range(8) if demand[j]]:
        need(augment(j, set()), 'Hall condition failed')
    return {j: s for s, j in owner.items()}


def round_within_two(rows, y, blocks=None):
    blocks = blocks or blocks_of(rows)
    t = [sum(rows[i][j] * y[i] for i in range(112)) for j in range(8)]
    need(all(v.denominator == 1 for v in t), 'integral mode vector')
    ystar, F = vertex(rows, y)
    need(rank_of([rows[i] for i in F]) == len(F) <= 8, 'independent fractional rows')
    z = list(ystar)
    for i in F:  # nearest rounding on F
        z[i] = Q(1) if ystar[i] >= Q(1, 2) else Q(0)
    rprime = [sum((rows[i][j] * (ystar[i] - z[i]) for i in F), Q(0)) for j in range(8)]
    need(all(v.denominator == 1 and abs(v) <= 4 for v in rprime), 'residual in L with |r_j| <= 4')
    h = tuple(int(v) % 2 for v in rprime)
    damaged, used = set(F), set(F)
    supports = {s: tuple(int(j in s) for j in range(8)) for s in blocks}
    u = [0] * 8
    if any(h):
        parts = [s for s, code in supports.items() if code == h]
        if not parts:  # all-ones parity: two complementary supports
            parts = next([s, c] for s in blocks for c in blocks
                         if supports[c] == tuple(1 - v for v in supports[s]))
        for s in parts:
            a = next(i for i in blocks[s][0] if i not in damaged)
            z[a] += 1
            damaged.add(a)
            u = [x + y for x, y in zip(u, rows[a])]
    w = [(rprime[j] - u[j]) / 2 for j in range(8)]
    need(all(v.denominator == 1 and abs(v) <= 2 for v in w), 'even remainder with |w_j| <= 2')
    count = {s: sum(i in damaged for i in blocks[s][0]) for s in blocks}
    good = [s for s in blocks if count[s] <= 2]
    need(len(blocks) - len(good) <= 3, 'at most three heavily damaged blocks')
    assign = matching([int(v) for v in w], good)
    for j, s in assign.items():
        k = int(w[j])
        intact = [pr for pr in pairs_for(rows, blocks[s], j) if pr[1] not in damaged and pr[2] not in damaged]
        need(len(intact) >= abs(k), 'enough intact pairs')
        for kind, a, b in intact[:abs(k)]:
            sign = 1 if k > 0 else -1
            if kind == 'sum':                      # m_a + m_b = 2 pin_sign e_j
                ca = cb = sign * blocks[s][2]
            else:                                  # m_a - m_b = 2 rows[a][j] e_j
                ca, cb = sign * rows[a][j], -sign * rows[a][j]
            z[a] += ca
            z[b] += cb
            damaged.update((a, b))
    need(all(v.denominator == 1 for v in z), 'integral output')
    need([sum(rows[i][j] * z[i] for i in range(112)) for j in range(8)] == t, 'modes preserved')
    err = max(abs(z[i] - y[i]) for i in range(112))
    need(err < 2, 'radius below two')
    return [int(v) for v in z], err
