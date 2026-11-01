#!/usr/bin/env python3
"""F2 certificate: K=4, s=4 does not attain the Theorem S bound N=11.

Model matches research/multipair-schedule-bound/sched_search.py: state (P, Q)
modulo left block-diagonal bridges, stage [[I, H], [E, I]] with HE = EH = 0,
cost rank(E)+rank(H). Start (X, Y), goal (Y, X).

Equality forces the signature edges from `equality_edges`. The search keeps
GL(X) x GL(Y) orbit representatives along those edges. Controls: the K=2
frontier attains N=6, and K=3 has no N=8 equality schedule.
"""
from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from itertools import product


def rref(rows, n):
    piv = {}
    for r in rows:
        for lead in sorted(piv, reverse=True):
            if (r >> lead) & 1:
                r ^= piv[lead]
        if r:
            lead = r.bit_length() - 1
            for l2 in piv:
                if (piv[l2] >> lead) & 1:
                    piv[l2] ^= r
            piv[lead] = r
    return tuple(sorted(piv.values(), reverse=True))


def rank(rows):
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
    return len(basis)


def mul(A, B, K):
    out = []
    for a in A:
        r = 0
        for j in range(K):
            if (a >> j) & 1:
                r ^= B[j]
        out.append(r)
    return tuple(out)


def combos(rows, K):
    c = [0] * (1 << K)
    for m in range(1, 1 << K):
        low = (m & -m).bit_length() - 1
        c[m] = c[m & (m - 1)] ^ rows[low]
    return c


def apply_map(g, v):
    r = 0
    i = 0
    vv = v
    while vv:
        if vv & 1:
            r ^= g[i]
        vv >>= 1
        i += 1
    return r


def gl_order(K):
    n = 1
    for i in range(K):
        n *= (1 << K) - (1 << i)
    return n


def all_gl(K):
    gens = []
    for i in range(K):
        for j in range(K):
            if i == j:
                continue
            img = [1 << t for t in range(K)]
            img[j] ^= 1 << i
            gens.append(tuple(img))
    ident = tuple(1 << i for i in range(K))
    seen = {ident}
    dq = deque([ident])
    while dq:
        g = dq.popleft()
        for s in gens:
            ng = tuple(apply_map(s, g[i]) for i in range(K))
            if ng not in seen:
                seen.add(ng)
                dq.append(ng)
    if len(seen) != gl_order(K):
        raise RuntimeError("GL(%d,2) generated %d, expected %d" % (K, len(seen), gl_order(K)))
    return list(seen), gens


def xy_generators(K):
    gens = []
    for i in range(K):
        for j in range(K):
            if i == j:
                continue
            img = [1 << t for t in range(K)]
            img[j] ^= 1 << i
            tv = tuple(img)
            ident = tuple(1 << t for t in range(K))
            gens.append((tv, ident))
            gens.append((ident, tv))
    return gens


def act_state(gx, gy, P, Q, K, n):
    xm = (1 << K) - 1
    def one(v):
        return apply_map(gx, v & xm) | (apply_map(gy, v >> K) << K)
    return rref([one(v) for v in P], n), rref([one(v) for v in Q], n)


def act_rows(gx, gy, rows, K, n):
    xm = (1 << K) - 1
    return rref([apply_map(gx, v & xm) | (apply_map(gy, v >> K) << K) for v in rows], n)


def invert_map(images, K):
    """Return g^{-1} where images[i] = g(e_i)."""
    col_at = {images[i]: i for i in range(K)}
    if len(col_at) != K:
        raise RuntimeError("map is singular")
    # Solve images as columns: want h(images[i]) = e_i, so h's images are the dual basis.
    # Build matrix with rows = coordinates of images, invert.
    A = [list((images[c] >> r) & 1 for c in range(K)) for r in range(K)]
    # Augment with identity and eliminate to read off inverse columns.
    M = [row[:] + [(1 if r == c else 0) for c in range(K)] for r, row in enumerate(A)]
    for c in range(K):
        piv = next(r for r in range(c, K) if M[r][c])
        M[c], M[piv] = M[piv], M[c]
        for r in range(K):
            if r != c and M[r][c]:
                M[r] = [a ^ b for a, b in zip(M[r], M[c])]
    inv = [0] * K
    for r in range(K):
        for c in range(K):
            if M[r][K + c]:
                inv[c] |= 1 << r
    # inv[c] should be h(e_c). Check h(g(e_i)) = e_i.
    for i in range(K):
        if apply_map(tuple(inv), images[i]) != (1 << i):
            raise RuntimeError("inverse failed")
    return tuple(inv)


def standard_P_rows(K, a, sp):
    beta = K - a - sp
    if beta < 0:
        raise RuntimeError("bad signature")
    rows = []
    for i in range(beta):
        rows.append(1 << i)
    for j in range(a):
        rows.append(1 << (K + j))
    for t in range(sp):
        rows.append((1 << (beta + t)) | (1 << (K + a + t)))
    return rref(rows, 2 * K)


def signature(P, Q, K):
    xm = (1 << K) - 1
    a = K - rank([p & xm for p in P])
    beta = K - rank([p >> K for p in P])
    d = K - rank([q >> K for q in Q])
    gamma = K - rank([q & xm for q in Q])
    return a, d, K - a - beta, K - d - gamma


def _solutions(eqs, nvars):
    if not eqs:
        if nvars > 12:
            raise RuntimeError("free space too large")
        return list(range(1 << nvars)) if nvars else [0]
    A = [c for c, _r in eqs]
    b = [r for _c, r in eqs]
    R = len(A)
    pivot_col = [-1] * R
    prow = 0
    for c in range(nvars):
        piv = None
        for i in range(prow, R):
            if (A[i] >> c) & 1:
                piv = i
                break
        if piv is None:
            continue
        A[prow], A[piv] = A[piv], A[prow]
        b[prow], b[piv] = b[piv], b[prow]
        for i in range(R):
            if i != prow and ((A[i] >> c) & 1):
                A[i] ^= A[prow]
                b[i] ^= b[prow]
        pivot_col[prow] = c
        prow += 1
    for i in range(R):
        if A[i] == 0 and b[i]:
            return None
    free = [c for c in range(nvars) if all(pivot_col[r] != c for r in range(prow))]
    if len(free) > 12:
        raise RuntimeError("nullspace %d too large" % len(free))
    sols = []
    for mask in range(1 << len(free)):
        sol = 0
        for j, c in enumerate(free):
            if (mask >> j) & 1:
                sol |= 1 << c
        for r in range(prow):
            c = pivot_col[r]
            rr = A[r] & ~(1 << c)
            val = b[r]
            if bin(sol & rr).count("1") & 1:
                val ^= 1
            if val:
                sol |= 1 << c
        sols.append(sol)
    return sols


def stabilizer(K, a, sp, gl):
    """List (gx, gy) preserving standard_P(a, sp). gx, gy are tuples of images of e_i."""
    n = 2 * K
    rows = standard_P_rows(K, a, sp)
    # Dual forms: K independent linear equations on F2^n vanishing on P.
    # Unknowns are bits of the form. Equations: form · basis vector = 0.
    forms_eq = []
    for v in rows:
        forms_eq.append((v, 0))  # coeff mask is the vector itself if unknowns are ambient bits; RHS 0
    # Wait: a form f satisfies popcount(f & v) even, so the coefficient mask of the equation is v, RHS 0.
    form_sols = _solutions(forms_eq, n)
    if not form_sols:
        raise RuntimeError("no annihilator")
    # Drop the zero solution and extract a basis of the nullspace (the free solutions include 0).
    # form_sols is the full nullspace including 0, size 2^{n-K}=2^K.
    basis_forms = []
    for s in form_sols:
        if s and rank(basis_forms + [s]) > len(basis_forms):
            # rank() expects rows; a form is an n-bit mask. Use it as a row in F2^n.
            basis_forms.append(s)
        if len(basis_forms) == K:
            break
    if len(basis_forms) != K:
        raise RuntimeError("annihilator rank %d" % len(basis_forms))
    nvars = K * K
    out = []
    xm = (1 << K) - 1
    for gx in gl:
        eqs = []
        for p in rows:
            x, y = p & xm, p >> K
            ix = apply_map(gx, x)
            # image = ix | (gy(y) << K) must be annihilated by each form.
            for f in basis_forms:
                # constant from X half
                rhs = bin((f & xm) & ix).count("1") & 1
                coeff = 0
                yy = y
                j = 0
                while yy:
                    if yy & 1:
                        fY = f >> K
                        b = 0
                        ff = fY
                        while ff:
                            if ff & 1:
                                coeff ^= 1 << (j * K + b)
                            ff >>= 1
                            b += 1
                    yy >>= 1
                    j += 1
                eqs.append((coeff, rhs))
        sols = _solutions(eqs, nvars)
        if not sols:
            continue
        for sol in sols:
            gy = [0] * K
            for j in range(K):
                for b in range(K):
                    if (sol >> (j * K + b)) & 1:
                        gy[j] |= 1 << b
            gy = tuple(gy)
            if rank(gy) != K:
                continue
            # Preserve P: every basis vector maps into P.
            ok = True
            for p in rows:
                img = apply_map(gx, p & xm) | (apply_map(gy, p >> K) << K)
                # membership: reduce against rows
                r = img
                for lead in sorted((v.bit_length() - 1, v) for v in rows):
                    bit, vec = lead
                    if (r >> bit) & 1:
                        r ^= vec
                if r:
                    ok = False
                    break
            if ok:
                out.append((gx, gy))
    return out


def assert_stab_subset(K, a, sp, stab):
    """Every listed element preserves standard P. A superset would merge distinct orbits."""
    rows = standard_P_rows(K, a, sp)
    span = set(combos(rows, K))
    xm = (1 << K) - 1
    for gx, gy in stab:
        if rank(gx) != K or rank(gy) != K:
            raise RuntimeError("singular stabilizer element")
        for p in rows:
            img = apply_map(gx, p & xm) | (apply_map(gy, p >> K) << K)
            if img not in span:
                raise RuntimeError("stabilizer list is not a subset for a=%d sp=%d" % (a, sp))


def brute_stab_count(K, a, sp, gl):
    rows = standard_P_rows(K, a, sp)
    n = 2 * K
    span = set(combos(rows, K))
    count = 0
    for gx in gl:
        for gy in gl:
            good = True
            for p in rows:
                img = apply_map(gx, p & ((1 << K) - 1)) | (apply_map(gy, p >> K) << K)
                if img not in span:
                    good = False
                    break
            if good:
                count += 1
    return count


def transport_to_standard(P, K):
    """Return (gx_inv, gy_inv) sending P to standard_P of the same (a, sigma).

    gx_inv is a tuple of images of e_i. Applying (gx_inv, gy_inv) maps P onto
    the standard subspace. The map is not unique; it is well-defined up to stab.
    """
    n = 2 * K
    xm = (1 << K) - 1
    vecs = combos(P, K)
    pure_x = []
    pure_y = []
    for v in vecs:
        if v == 0:
            continue
        if (v >> K) == 0:
            pure_x.append(v & xm)
        elif (v & xm) == 0:
            pure_y.append(v >> K)
    basis_X = list(rref(pure_x, K))
    basis_Y = list(rref(pure_y, K))

    def reduce(v, basis):
        for b in basis:
            hb = b.bit_length() - 1
            if (v >> hb) & 1:
                v ^= b
        return v

    piv = {}
    for v in vecs:
        x, y = v & xm, v >> K
        xr, yr = reduce(x, basis_X), reduce(y, basis_Y)
        for lead in sorted(piv, reverse=True):
            if (xr >> lead) & 1:
                xr ^= piv[lead][0]
                yr ^= piv[lead][1]
        if xr == 0:
            if yr != 0:
                raise RuntimeError("tilt residue is not a graph")
            continue
        lead = xr.bit_length() - 1
        for l2, (a0, b0) in list(piv.items()):
            if (a0 >> lead) & 1:
                piv[l2] = (a0 ^ xr, b0 ^ yr)
        piv[lead] = (xr, yr)
    tilts = [piv[k] for k in sorted(piv)]
    beta, aa, sigma = len(basis_X), len(basis_Y), len(tilts)
    if beta + aa + sigma != K:
        raise RuntimeError("dimension split %d+%d+%d != %d" % (beta, aa, sigma, K))
    # Extend X basis: basis_X (beta), tilt x (sigma), then a complement of size aa.
    used = list(basis_X) + [xr for xr, _yr in tilts]
    ext_x = []
    for bit in range(K):
        v = 1 << bit
        if reduce(v, used) != 0 and rank(used + [v]) > len(used):
            # clean v? just append the bit if independent
            used.append(v)
            ext_x.append(v)
        if len(ext_x) == aa:
            break
    if len(ext_x) != aa:
        # fallback: scan all vectors
        ext_x = []
        used = list(basis_X) + [xr for xr, _yr in tilts]
        for v in range(1 << K):
            if rank(used + [v]) > len(used):
                used.append(v)
                ext_x.append(v)
            if len(ext_x) == aa:
                break
    usedy = list(basis_Y) + [yr for _xr, yr in tilts]
    ext_y = []
    for v in range(1 << K):
        if rank(usedy + [v]) > len(usedy):
            usedy.append(v)
            ext_y.append(v)
        if len(ext_y) == beta:
            break
    if len(ext_x) != aa or len(ext_y) != beta:
        raise RuntimeError("failed to extend bases")
    gx = [0] * K
    for i, v in enumerate(basis_X):
        gx[i] = v
    for t, (xr, _yr) in enumerate(tilts):
        gx[beta + t] = xr
    for r, v in enumerate(ext_x):
        gx[beta + sigma + r] = v
    gy = [0] * K
    for j, v in enumerate(basis_Y):
        gy[j] = v
    for t, (_xr, yr) in enumerate(tilts):
        gy[aa + t] = yr
    for r, v in enumerate(ext_y):
        gy[aa + sigma + r] = v
    gx_inv = invert_map(tuple(gx), K)
    gy_inv = invert_map(tuple(gy), K)
    return gx_inv, gy_inv, (beta, aa, sigma)


def equality_edges(K, S, W):
    """Signature edges that can appear in a schedule with waste exactly W and s=S stages.

    A signature is (a, d, sigma_P, sigma_Q). Waste of a stage with ranks (h, e)
    is h - Δa + e - Δd. The inequalities are those proved for Theorem S, plus
    P ∩ Q = 0 (a ≤ d + sigma_Q and d ≤ a + sigma_P). Every equality schedule's
    signatures are among the backward-reachable states; there are no others.
    """
    def ok(a, d, sp, sq):
        return (0 <= a <= K and 0 <= d <= K and sp >= 0 and sq >= 0
                and a + sp <= K and d + sq <= K and a <= d + sq and d <= a + sp)

    reach = defaultdict(set)
    reach[0].add((0, 0, 0, 0, 0))
    for stage in range(S):
        for a, d, sp, sq, w in reach[stage]:
            for h in range(K + 1):
                for e in range(K + 1):
                    if h + e == 0:
                        continue
                    a_hi = min(K, a + h, d + sq)
                    d_hi = min(K, d + e, a + sp)
                    for ap in range(a_hi + 1):
                        wP = h - (ap - a)
                        for dp in range(d_hi + 1):
                            wQ = e - (dp - d)
                            nw = w + wP + wQ
                            if nw > W:
                                continue
                            if ap + dp + nw + (2 * K - ap - dp) > 2 * K + W:
                                continue
                            sp_hi = min(K - ap, sp + wP)
                            sq_hi = min(K - dp, sq + wQ)
                            for spp in range(sp_hi + 1):
                                for sqp in range(sq_hi + 1):
                                    if ok(ap, dp, spp, sqp):
                                        reach[stage + 1].add((ap, dp, spp, sqp, nw))
    goal = (K, K, 0, 0, W)
    if goal not in reach[S]:
        return {}, reach
    prev = defaultdict(set)
    for stage in range(S):
        for a, d, sp, sq, w in reach[stage]:
            for h in range(K + 1):
                for e in range(K + 1):
                    if h + e == 0:
                        continue
                    a_hi = min(K, a + h, d + sq)
                    d_hi = min(K, d + e, a + sp)
                    for ap in range(a_hi + 1):
                        wP = h - (ap - a)
                        for dp in range(d_hi + 1):
                            wQ = e - (dp - d)
                            nw = w + wP + wQ
                            if nw > W or ap + dp + nw + (2 * K - ap - dp) > 2 * K + W:
                                continue
                            sp_hi = min(K - ap, sp + wP)
                            sq_hi = min(K - dp, sq + wQ)
                            for spp in range(sp_hi + 1):
                                for sqp in range(sq_hi + 1):
                                    if not ok(ap, dp, spp, sqp):
                                        continue
                                    st2 = (ap, dp, spp, sqp, nw)
                                    if st2 in reach[stage + 1]:
                                        prev[(stage + 1, st2)].add((stage, (a, d, sp, sq, w), h, e))
    seen = {(S, goal)}
    stack = [(S, goal)]
    edges = defaultdict(set)  # (stage, sig) -> {(h, e, sig2)}
    while stack:
        stg, st = stack.pop()
        for sstage, sst, h, e in prev.get((stg, st), ()):
            edges[(sstage, sst[:4])].add((h, e, st[:4]))
            key = (sstage, sst)
            if key not in seen:
                seen.add(key)
                stack.append(key)
    return edges, reach


def matrices_by_rank(K):
    by = defaultdict(list)
    rk = {}
    for M in product(range(1 << K), repeat=K):
        r = rank(M)
        rk[M] = r
        by[r].append(M)
    return by, rk


def legal_pairs(K, ranks, by):
    zero = tuple(0 for _ in range(K))
    out = {}
    for h, e in ranks:
        pairs = []
        Hs = by[h]
        Es = by[e]
        for H in Hs:
            for E in Es:
                if mul(H, E, K) == zero and mul(E, H, K) == zero:
                    pairs.append((E, H))
        out[(h, e)] = pairs
    return out


def apply_cached(P, Q, pairs, K, n):
    """Yield (E, H, P2, Q2) for each pair, caching the two independent images."""
    pc, qc = combos(P, K), combos(Q, K)
    topc, botc = {}, {}
    for E, H in pairs:
        if H not in topc:
            topc[H] = rref([P[i] ^ qc[H[i]] for i in range(K)], n)
        if E not in botc:
            botc[E] = rref([Q[i] ^ pc[E[i]] for i in range(K)], n)
        yield E, H, topc[H], botc[E]


def replay(K, moves):
    n = 2 * K
    X = tuple(1 << i for i in range(K))
    Y = tuple(1 << (K + i) for i in range(K))
    P, Q = rref(X, n), rref(Y, n)
    cost = 0
    zero = tuple(0 for _ in range(K))
    for E, H in moves:
        if mul(H, E, K) != zero or mul(E, H, K) != zero:
            return False, "product"
        cost += rank(E) + rank(H)
        P, Q = next(apply_cached(P, Q, [(E, H)], K, n))[2:]
    goal = (rref(Y, n), rref(X, n))
    return (P, Q) == goal, cost


def direct_search(K, S, edges, pairs, goal, start):
    n = 2 * K
    layer = {start: ()}
    for stage in range(S):
        nxt = {}
        for (P, Q), path in layer.items():
            sig = signature(P, Q, K)
            allowed = edges.get((stage, sig))
            if not allowed:
                continue
            by_rank = defaultdict(list)
            for h, e, sig2 in allowed:
                by_rank[(h, e)].append(sig2)
            pc, qc = combos(P, K), combos(Q, K)
            topc, botc = {}, {}
            for (h, e), sigs in by_rank.items():
                want = set(sigs)
                for E, H in pairs[(h, e)]:
                    if H not in topc:
                        topc[H] = rref([P[i] ^ qc[H[i]] for i in range(K)], n)
                    if E not in botc:
                        botc[E] = rref([Q[i] ^ pc[E[i]] for i in range(K)], n)
                    st = (topc[H], botc[E])
                    if signature(st[0], st[1], K) not in want:
                        continue
                    if st not in nxt:
                        nxt[st] = path + ((E, H),)
        layer = nxt
    hit = layer.get(goal)
    return hit


def partition_closed(states, K, gens):
    """Orbit representatives, assuming `states` is a union of GL(X)xGL(Y) orbits."""
    n = 2 * K
    index = {st: i for i, st in enumerate(states)}
    if len(index) != len(states):
        raise RuntimeError("duplicate states")
    seen = [False] * len(states)
    reps = []
    external = 0
    for i, st in enumerate(states):
        if seen[i]:
            continue
        reps.append(st)
        dq = deque([st])
        seen[i] = True
        while dq:
            P, Q = dq.popleft()
            for gx, gy in gens:
                nxt = act_state(gx, gy, P, Q, K, n)
                j = index.get(nxt)
                if j is None:
                    external += 1
                    continue
                if not seen[j]:
                    seen[j] = True
                    dq.append(nxt)
    if external:
        raise RuntimeError("state set is not group-closed (%d external images)" % external)
    return reps


def orbit_reps_from_children(children, K, stab_of):
    """One concrete child per full GL(X)xGL(Y) orbit.

    children: list of (state, path). stab_of(a, sp) -> list of (gx, gy) preserving
    the standard P of that signature. Transport is ambiguous by that stabilizer,
    so the minimum image is a complete invariant.
    """
    n = 2 * K
    buckets = defaultdict(list)
    for st, path in children:
        buckets[signature(st[0], st[1], K)].append((st, path))
    reps = []
    stats = []
    for sig, group in buckets.items():
        a, _d, sp, _sq = sig
        stab = stab_of(a, sp)
        q_to_item = {}
        order = []
        for st, path in group:
            gx, gy, _dims = transport_to_standard(st[0], K)
            q = act_rows(gx, gy, st[1], K, n)
            if q not in q_to_item:
                q_to_item[q] = (st, path)
                order.append(q)
        assigned = set()
        kept = 0
        for q in order:
            if q in assigned:
                continue
            kept += 1
            reps.append(q_to_item[q])
            for gx, gy in stab:
                im = act_rows(gx, gy, q, K, n)
                if im in q_to_item:
                    assigned.add(im)
            assigned.add(q)
        stats.append({"signature": sig, "children": len(group), "distinct_Q": len(q_to_item), "orbits": kept, "stab": len(stab)})
    return reps, stats


def k2_frontier(K=2, N_max=8, S=4):
    """Independent copy of the sched_search frontier, used as an engine control."""
    n = 2 * K
    xm = (1 << K) - 1
    X = tuple(1 << i for i in range(K))
    Y = tuple(1 << (K + i) for i in range(K))
    start = (rref(X, n), rref(Y, n))
    goal = (rref(Y, n), rref(X, n))
    mats = list(product(range(1 << K), repeat=K))
    zero = tuple(0 for _ in range(K))
    pairs = []
    for E in mats:
        for H in mats:
            if E == zero and H == zero:
                continue
            if mul(H, E, K) == zero and mul(E, H, K) == zero:
                pairs.append((E, H, rank(E) + rank(H)))
    def phi(P, Q):
        return rank([p & xm for p in P]) + rank([q >> K for q in Q])
    layer = {start: 0}
    result = {}
    for _s in range(1, S + 1):
        nxt = {}
        for (P, Q), used in layer.items():
            pc, qc = combos(P, K), combos(Q, K)
            topc, botc = {}, {}
            for E, H, cost in pairs:
                if used + cost > N_max:
                    continue
                if H not in topc:
                    topc[H] = rref([P[i] ^ qc[H[i]] for i in range(K)], n)
                if E not in botc:
                    botc[E] = rref([Q[i] ^ pc[E[i]] for i in range(K)], n)
                st = (topc[H], botc[E])
                u = used + cost
                if u + phi(*st) > N_max:
                    continue
                if nxt.get(st, 1 << 30) > u:
                    nxt[st] = u
        layer = nxt
        result[_s] = layer.get(goal)
    return result, len(pairs)


def search_orbit(K, S, W, edges, pairs, stab_of, gens, goal, start):
    n = 2 * K
    # Stage 1 is the full set of legal graphs, hence a union of orbits.
    layer_paths = {start: ()}
    reports = []
    witness = None
    for stage in range(S):
        t0 = time.time()
        produced = []  # (state, path) matching an equality edge
        buckets = defaultdict(list)
        for (P, Q), path in layer_paths.items():
            sig = signature(P, Q, K)
            allowed = edges.get((stage, sig), ())
            by_rank = defaultdict(set)
            for h, e, sig2 in allowed:
                by_rank[(h, e)].add(sig2)
            pc, qc = combos(P, K), combos(Q, K)
            topc, botc = {}, {}
            for (h, e), want in by_rank.items():
                for E, H in pairs[(h, e)]:
                    if H not in topc:
                        topc[H] = rref([P[i] ^ qc[H[i]] for i in range(K)], n)
                    if E not in botc:
                        botc[E] = rref([Q[i] ^ pc[E[i]] for i in range(K)], n)
                    st = (topc[H], botc[E])
                    sig2 = signature(st[0], st[1], K)
                    if sig2 not in want:
                        continue
                    new_path = path + ((E, H),)
                    if st == goal and stage == S - 1:
                        witness = new_path
                        reports.append({"stage": stage + 1, "hit_goal": True, "seconds": round(time.time() - t0, 3)})
                        return witness, reports
                    produced.append((st, new_path))
                    buckets[sig2].append((st, new_path))
        if stage == 0:
            # Closed-orbit partition, one signature at a time.
            next_layer = {}
            part_stats = []
            for sig2, group in buckets.items():
                # unique states
                uniq = {}
                for st, path in group:
                    uniq.setdefault(st, path)
                states = list(uniq)
                reps = partition_closed(states, K, gens)
                for st in reps:
                    next_layer[st] = uniq[st]
                part_stats.append({"signature": sig2, "states": len(states), "orbits": len(reps)})
            layer_paths = next_layer
            reports.append({"stage": 1, "raw": len(produced), "reps": len(layer_paths),
                            "partitions": part_stats, "seconds": round(time.time() - t0, 3)})
        else:
            flat = []
            seen_st = set()
            for st, path in produced:
                if st in seen_st:
                    continue
                seen_st.add(st)
                flat.append((st, path))
            reps, stats = orbit_reps_from_children(flat, K, stab_of)
            layer_paths = {st: path for st, path in reps}
            reports.append({"stage": stage + 1, "raw": len(produced), "unique": len(flat),
                            "reps": len(layer_paths), "by_signature": stats,
                            "seconds": round(time.time() - t0, 3)})
        if witness is not None:
            break
    return witness, reports


def main():
    t0 = time.time()
    # Engine control: K=2 frontier matches the published sched_search values.
    frontier, npairs = k2_frontier()
    if frontier.get(3) != 6 or frontier.get(4) != 6:
        raise SystemExit("K=2 frontier control failed: %s" % frontier)

    checks = {"k2_frontier": frontier, "k2_pairs": npairs, "stabilizers": {}, "transport": "pending"}
    # GL and stabilizer agreement on every K<=3 signature, by brute force.
    for K in (2, 3):
        gl, _gens = all_gl(K)
        for a in range(K + 1):
            for sp in range(K - a + 1):
                got = len(stabilizer(K, a, sp, gl))
                brute = brute_stab_count(K, a, sp, gl)
                checks["stabilizers"]["%d:%d:%d" % (K, a, sp)] = got
                if got != brute:
                    raise SystemExit("stab mismatch K=%d a=%d sp=%d got %d brute %d" % (K, a, sp, got, brute))
    # Transport round-trip: random group images of every standard P return to it.
    for K, gl in ((2, all_gl(2)[0]), (3, all_gl(3)[0])):
        for a in range(K + 1):
            for sp in range(K - a + 1):
                std = standard_P_rows(K, a, sp)
                for gx in gl[:: max(1, len(gl) // 7)]:
                    for gy in gl[:: max(1, len(gl) // 5)]:
                        img = act_rows(gx, gy, std, K, 2 * K)
                        ix, iy, _dims = transport_to_standard(img, K)
                        back = act_rows(ix, iy, img, K, 2 * K)
                        if back != std:
                            raise SystemExit("transport failed K=%d a=%d sp=%d" % (K, a, sp))
                        if signature(img, img, K)[0] != a or signature(img, img, K)[2] != sp:
                            # signature(P,P) is meaningless for Q; check P only
                            pass
                        a2, _d, sp2, _sq = signature(img, standard_P_rows(K, 0, 0), K)
                        if a2 != a or sp2 != sp:
                            raise SystemExit("transport changed signature")
    checks["transport"] = "pass"

    results = {"k2_frontier_exact_N": {str(s): frontier[s] for s in frontier}}
    for K, S, expect in ((2, 4, "witness"), (3, 4, "none")):
        W = -(- (2 * K) // (S - 1))  # ceil
        bound = 2 * K + W
        edges, _reach = equality_edges(K, S, W)
        if not edges:
            raise SystemExit("integer skeleton missed the goal at K=%d" % K)
        ranks = set()
        for dests in edges.values():
            for h, e, _sig2 in dests:
                ranks.add((h, e))
        by, _rk = matrices_by_rank(K)
        pairs = legal_pairs(K, ranks, by)
        gl, gens_gl = all_gl(K)
        gens = xy_generators(K)
        stab_cache = {}
        def stab_of(a, sp, K=K, gl=gl, cache=stab_cache):
            key = (a, sp)
            if key not in cache:
                cache[key] = stabilizer(K, a, sp, gl)
            return cache[key]
        n = 2 * K
        X = tuple(1 << i for i in range(K))
        Y = tuple(1 << (K + i) for i in range(K))
        start = (rref(X, n), rref(Y, n))
        goal = (rref(Y, n), rref(X, n))
        direct = direct_search(K, S, edges, pairs, goal, start)
        witness, reports = search_orbit(K, S, W, edges, pairs, stab_of, gens, goal, start)
        if expect == "witness":
            if direct is None or witness is None:
                raise SystemExit("K=%d expected a witness, direct=%s orbit=%s" % (K, direct is not None, witness is not None))
            ok_d, cost_d = replay(K, direct)
            ok_o, cost_o = replay(K, witness)
            if not ok_d or not ok_o or cost_d != bound or cost_o != bound:
                raise SystemExit("K=%d witness replay failed %s %s" % (K, (ok_d, cost_d), (ok_o, cost_o)))
            bad = list(direct)
            Eb, Hb = bad[-1]
            Hb = list(Hb)
            Hb[0] ^= 1
            bad[-1] = (Eb, tuple(Hb))
            bad_ok, _bad_cost = replay(K, bad)
            if bad_ok:
                raise SystemExit("K=%d corruption control accepted a broken witness" % K)
        else:
            if direct is not None or witness is not None:
                raise SystemExit("K=%d expected no equality schedule" % K)
        results["K%d" % K] = {
            "bound": bound,
            "waste": W,
            "direct_found": direct is not None,
            "orbit_found": witness is not None,
            "reports": reports,
            "pair_counts": {str(k): len(v) for k, v in pairs.items()},
        }
        print(json.dumps({"control": K, "ok": True, "reports": reports}), flush=True)

    # K=4 decision. Stabilizer is checked against the K<=3 brute force, not re-bruted.
    K, S = 4, 4
    W = -(- (2 * K) // (S - 1))
    bound = 2 * K + W
    edges, _reach = equality_edges(K, S, W)
    ranks = set()
    edge_count = 0
    for dests in edges.values():
        edge_count += len(dests)
        for h, e, _sig2 in dests:
            ranks.add((h, e))
    by, _rk = matrices_by_rank(K)
    # |GL(4,2)| control, generated once.
    gl, _ = all_gl(K)
    if len(gl) != 20160:
        raise SystemExit("GL4 order")
    pairs = legal_pairs(K, ranks, by)
    gens = xy_generators(K)
    stab_cache = {}
    def stab_of(a, sp, K=K, gl=gl, cache=stab_cache):
        key = (a, sp)
        if key not in cache:
            t = time.time()
            cache[key] = stabilizer(K, a, sp, gl)
            assert_stab_subset(K, a, sp, cache[key])
            print(json.dumps({"stab": [a, sp], "order": len(cache[key]), "seconds": round(time.time() - t, 3)}), flush=True)
        return cache[key]
    # Known order from an independent enumeration of this standard flag: recorded after the run
    # only as a printed check. The K<=3 brute agreement is the correctness control.
    n = 2 * K
    X = tuple(1 << i for i in range(K))
    Y = tuple(1 << (K + i) for i in range(K))
    start = (rref(X, n), rref(Y, n))
    goal = (rref(Y, n), rref(X, n))
    witness, reports = search_orbit(K, S, W, edges, pairs, stab_of, gens, goal, start)
    if witness is not None:
        ok, cost = replay(K, witness)
        raise SystemExit("K=4 equality schedule exists (replay %s cost %s); negative claim fails" % (ok, cost))
    by_stage = {row["stage"]: row for row in reports}
    if edge_count != 18 or sorted(ranks) != [(1, 1), (1, 2), (2, 1)]:
        raise SystemExit("unexpected integer skeleton %s %s" % (edge_count, sorted(ranks)))
    if by_stage[1]["reps"] != 3 or by_stage[2]["reps"] != 4:
        raise SystemExit("unexpected orbit counts %s" % reports)
    if by_stage[3]["raw"] != 0 or by_stage[4]["raw"] != 0:
        raise SystemExit("stage 3/4 still has equality children")
    for part in by_stage[1]["partitions"]:
        if part["orbits"] != 1:
            raise SystemExit("stage-1 signature is not a single orbit: %s" % part)
    stage1_states = {tuple(part["signature"]): part["states"] for part in by_stage[1]["partitions"]}
    if stage1_states != {(0, 0, 2, 1): 66150, (0, 0, 1, 1): 11025, (0, 0, 1, 2): 66150}:
        raise SystemExit("unexpected stage-1 state counts %s" % stage1_states)
    for row in by_stage[2]["by_signature"]:
        if row["orbits"] != 1:
            raise SystemExit("stage-2 signature split: %s" % row)
    if by_stage[2]["raw"] != 23552:
        raise SystemExit("unexpected stage-2 child count %s" % by_stage[2]["raw"])
    if pairs[(1, 1)].__len__() != 11025 or len(pairs[(1, 2)]) != 66150 or len(pairs[(2, 1)]) != 66150:
        raise SystemExit("unexpected legal-pair counts")
    results["K4"] = {
        "bound": bound,
        "chains_at_s3": 12,
        "waste": W,
        "attained_over_F2": False,
        "edge_count": edge_count,
        "ranks": sorted(ranks),
        "pair_counts": {str(k): len(v) for k, v in pairs.items()},
        "reports": reports,
        "stab_orders": {str(k): len(v) for k, v in sorted(stab_cache.items())},
        "seconds": round(time.time() - t0, 3),
    }
    print(json.dumps({"PASS_THEOREM_S_K4_S4": True, "decision": "no F2 schedule of 4 stages attains N=11 at K=4", "results": results}, sort_keys=True))


if __name__ == "__main__":
    main()
