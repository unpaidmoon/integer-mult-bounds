#!/usr/bin/env python3
"""Owned-lineage factorization and scoped review of PR6170's owned-layer floor framework.  Apache-2.0.

Prepared for Matarener with Claude (Anthropic), via Claude Code.  Python 3.12, standard library plus NumPy
(integer arithmetic only).  Nothing is imported from PR6170.

Layers:
  1. own exact replay of the PR5907, PR6030, PR6144 and PR6167 words in real values and in PR6170's P_M
     accounting (every owned MOVE arrival becomes a fresh symbol): owned-delivery matrix C, PUB + C = I,
     R1, R3, NEED, Z, rank C, owned paid, symbol ancestry (SAME/STRICT, merges, branching);
  2. lineage factorization (PROOF.md, Lemma 1): for every lineage, C^lineage = alpha_j beta_i on every
     non-orthogonal pair, path paid >= rank_F2 Gamma[supp alpha, supp beta]; X = sum alpha beta^T agrees
     with I on all non-orthogonal pairs and has rank 8;
  3. root data of the E8 completion (exact integers): Gram of the 104 roots from X, closure to 240 roots,
     simple roots; facts F1 (support spans of root lines), F2 (pair ranks of root directions) and
     F3 (branching landings of root-direction pairs);
  4. (--flats; replays only PR6030 and layers 3-4) all 440,880 one-dimensional flats of the E8 arrangement as W-orbits of the fundamental
     coweights (exact integers): support spans and all span-pair ranks (fact F1 for every flat).
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip, json, sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORDS = {'5907': 'research/p104-helper468-rung-removal/WORD.json.gz',
         '6030': 'research/p104-helper470-twin-rung-removal/WORD.json.gz',
         '6144': 'research/p104-root-relay-descent-2/WORD.json.gz',
         '6167': 'research/p104-retained-operand-descent/WORD.json.gz'}


def log(kind, **data):
    print(kind, json.dumps(data, sort_keys=True, default=str)[:400], flush=True)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def authenticate():
    for row in json.loads((HERE/'SOURCES.json').read_text())['files']:
        if row['usage'] == 'input':
            need(sha256((ROOT/row['path']).read_bytes()).hexdigest() == row['sha256'], 'source pin '+row['path'])


def span(basis):
    s = {0}
    for v in basis:
        s |= {x ^ v for x in s}
    return frozenset(s)


def reduce_basis(vecs):
    """canonical reduced echelon basis of the F2 span (tuple, sorted)"""
    piv = {}
    for v in vecs:
        for p in sorted(piv, reverse=True):
            if (v >> p) & 1:
                v ^= piv[p]
        if v:
            p = v.bit_length()-1
            for q in piv:
                if (piv[q] >> p) & 1:
                    piv[q] ^= v
            piv[p] = v
    return tuple(sorted(piv.values()))


def f2rank(vecs):
    return len(reduce_basis(vecs))


def dot2(a, b):
    return bin(a & b).count('1') & 1


def qrank(rows):
    M = [dict(r) for r in rows if r]
    rank = 0
    for c in sorted({k for r in M for k in r}):
        p = next((i for i in range(rank, len(M)) if M[i].get(c)), None)
        if p is None:
            continue
        M[rank], M[p] = M[p], M[rank]
        pr = M[rank]
        for i in range(rank+1, len(M)):
            a = M[i].get(c)
            if a:
                f = a/pr[c]
                t = dict(M[i])
                for k, v in pr.items():
                    t[k] = t.get(k, 0)-f*v
                M[i] = {k: v for k, v in t.items() if v}
        rank += 1
    return rank


def addrow(t, s, q):
    t = dict(t)
    for k, v in s.items():
        t[k] = t.get(k, 0)+q*v
    return {k: v for k, v in t.items() if v}


# ---------------------------------------------------------------- layers 1-2
def owned_layer(name):
    w = json.loads(gzip.decompress((ROOT/WORDS[name]).read_bytes()))
    F = w['frames']
    S = [span(f) for f in F]
    n, m = w['public'], w['owned_fields']
    live, ports = list(w['live']), list(w['ports'])
    need(len(live) == len(ports) == 104, 'P104 ports')
    xidx = {x: j for j, x in enumerate(live)}
    cur = list(w['initial'])+[None]*m
    real = [{r: Q(1)} for r in range(n+m)]
    pm = [{r: Q(1)} for r in range(n+m)]
    sym = []
    for i, e in enumerate(w['program']):
        op, r = e[0], e[1]
        if op == 'MOVE':
            a, b, private = e[2], e[3], e[4]
            need(cur[r] == a and (S[b] < S[a] if private else S[a] < S[b]), 'nesting at %d' % i)
            if private:
                anc = sorted({k[1] for k in pm[r] if isinstance(k, tuple)})
                # P3a: public part of the mover's value has x-content on ports of the gather frame
                need(all(ports[xidx[k]] in S[a] for k in pm[r] if k in xidx), 'P3a at %d' % i)
                sym.append({'g': a, 'L': b, 'rho': dict(real[r]), 'anc': anc})
                pm[r] = {('s', len(sym)-1): Q(1)}
            cur[r] = b
        elif op in ('INIT', 'CLEAR'):
            real[r], pm[r] = {}, {}
            cur[r] = e[2] if op == 'INIT' else None
        else:
            q, f = Q(e[-2]), e[-1]
            need(cur[r] == f, 'chart at %d' % i)
            if op == 'SCALE':
                real[r] = {k: q*v for k, v in real[r].items()}
                pm[r] = {k: q*v for k, v in pm[r].items()}
            else:
                s = e[2]
                need(cur[s] == f, 'common chart at %d' % i)
                if op == 'COPY':
                    real[r] = {k: q*v for k, v in real[s].items()}
                    pm[r] = {k: q*v for k, v in pm[s].items()}
                else:
                    real[r] = addrow(real[r], real[s], q)
                    pm[r] = addrow(pm[r], pm[s], q)
    for x in live:
        need(real[x+112] == {x+112: Q(1), x: Q(1)}, 'real Y final')
    ns = len(sym)
    U = [[pm[x+112].get(('s', k), Q(0)) for x in live] for k in range(ns)]
    V = [[s['rho'].get(x, Q(0)) for x in live] for s in sym]
    G = [[dot2(ports[j], ports[i]) for i in range(104)] for j in range(104)]
    C = [[sum(U[k][j]*V[k][i] for k in range(ns)) for i in range(104)] for j in range(104)]
    pub_ok = all(pm[x+112].get(xi, 0)+C[j][i] == (1 if i == j else 0)
                 for j, x in enumerate(live) for i, xi in enumerate(live))
    r3 = sum(1 for j in range(104) for i in range(104) if G[j][i] and C[j][i] != (1 if i == j else 0))
    orth = sum(1 for j in range(104) for i in range(104) if i != j and not G[j][i])
    needc = sum(1 for j in range(104) for i in range(104) if i != j and not G[j][i] and C[j][i])
    r1 = sum(1 for k, s in enumerate(sym) for j in range(104) if U[k][j] and any(dot2(b, ports[j]) for b in F[s['L']]))
    strict = sum(1 for s in sym for a in s['anc'] if S[sym[a]['L']] != S[s['g']])
    merges = sum(1 for s in sym if len(s['anc']) > 1)
    kids = Counter(a for s in sym for a in s['anc'])
    branching = sum(1 for v in kids.values() if v > 1)
    paid = sum(len(F[s['g']])-len(F[s['L']]) for s in sym)
    out = {'symbols': ns, 'owned_paid': paid, 'rankQ_C': qrank([{i: C[j][i] for i in range(104) if C[j][i]} for j in range(104)]),
           'NEED': needc, 'Z': orth-needc, 'orthogonal_ordered_pairs': orth, 'PUB_plus_C_eq_I': pub_ok,
           'R1_violations': r1, 'R3_violations': r3, 'STRICT_edges': strict, 'merges': merges, 'branching_symbols': branching}
    # lineages
    child = {a: k for k, s in enumerate(sym) for a in s['anc']}
    roots = [k for k, s in enumerate(sym) if not s['anc']]
    paths = []
    for r0 in roots:
        p, k = [], r0
        while k is not None:
            p.append(k); k = child.get(k)
        paths.append(p)
    X = [[Q(0)]*104 for _ in range(104)]
    mism, costs, ranks = 0, [], []
    for p in paths:
        Cp = [[sum(U[k][j]*V[k][i] for k in p) for i in range(104)] for j in range(104)]
        alpha, beta = {}, {}
        rem = {(j, i) for j in range(104) for i in range(104) if G[j][i] and Cp[j][i]}
        while rem:
            j0, i0 = min(rem)
            alpha[j0], beta[i0] = Q(1), Cp[j0][i0]
            grown = True
            while grown:
                grown = False
                for (j, i) in sorted(rem):
                    if j in alpha and i not in beta:
                        beta[i] = Cp[j][i]/alpha[j]; grown = True
                    elif i in beta and j not in alpha:
                        alpha[j] = Cp[j][i]/beta[i]; grown = True
                    if j in alpha and i in beta:
                        rem.discard((j, i))
        mism += sum(1 for j in range(104) for i in range(104) if G[j][i] and Cp[j][i] != alpha.get(j, 0)*beta.get(i, 0))
        Sa = sorted(j for j in alpha if alpha[j]); Tb = sorted(i for i in beta if beta[i])
        ranks.append(f2rank([sum(1 << t for t, i in enumerate(Tb) if G[j][i]) for j in Sa]))
        costs.append(sum(len(F[sym[k]['g']])-len(F[sym[k]['L']]) for k in p))
        for j in Sa:
            for i in Tb:
                X[j][i] += alpha[j]*beta[i]
    xg = sum(1 for j in range(104) for i in range(104) if G[j][i] and X[j][i] != (1 if i == j else 0))
    out.update({'lineages': len(paths), 'lineage_paid': sorted(costs), 'lineage_rankF2': sorted(ranks),
                'rank_one_mismatches': mism, 'cost_bound_holds': all(r <= c for r, c in zip(ranks, costs)),
                'X_Gamma_eq_I_violations': xg,
                'rankQ_X': qrank([{i: X[j][i] for i in range(104) if X[j][i]} for j in range(104)])})
    log('L1_L2', word=name, **out)
    return out, X, ports


# ---------------------------------------------------------------- layer 3: exact root data
def root_data(X, ports):
    n = 104
    G = [[0]*n for _ in range(n)]
    for i in range(n):
        need(X[i][i] == 1, 'unit diagonal')
        G[i][i] = 2
        for j in range(n):
            if i != j:
                if X[i][j] == 0:
                    need(X[j][i] == 0, 'E8 completion zero pattern')
                else:
                    need(X[i][j]*X[j][i] == Q(1, 4) and (X[i][j] > 0) == (X[j][i] > 0), 'E8 completion entries')
                G[i][j] = 0 if X[i][j] == 0 else (1 if X[i][j] > 0 else -1)
    # basis of 8 roots and rational coordinates of all 104
    piv = []
    for j in range(n):
        cand = piv+[j]
        if np.linalg.matrix_rank(np.array([[G[a][b] for b in cand] for a in cand], dtype=float)) == len(cand):
            piv = cand
        if len(piv) == 8:
            break
    Gb = [[Q(G[a][b]) for b in piv] for a in piv]
    inv = invert(Gb)
    coords = [tuple(sum(inv[r][c]*G[piv[c]][j] for c in range(8)) for r in range(8)) for j in range(n)]
    ip = lambda u, v: sum(u[a]*Gb[a][b]*v[b] for a in range(8) for b in range(8))
    for j in range(n):
        for k in range(n):
            need(ip(coords[j], coords[k]) == G[j][k], 'root coordinates')
    # reflection closure in exact integers: scale coordinates by the common denominator d
    from math import lcm
    d = lcm(*[x.denominator for c in coords for x in c])
    Gi = np.array([[int(x) for x in row] for row in Gb], dtype=np.int64)
    Vs = np.array([[int(x*d) for x in c] for c in coords], dtype=np.int64)
    Vs = np.unique(np.concatenate([Vs, -Vs]), axis=0)
    while True:
        IP = Vs @ Gi @ Vs.T
        need((IP % (d*d) == 0).all(), 'integral inner products')
        IP //= d*d
        new = (Vs[None, :, :]-IP[:, :, None]*Vs[:, None, :]).reshape(-1, 8)
        nxt = np.unique(np.concatenate([Vs, new]), axis=0)
        if len(nxt) == len(Vs):
            break
        Vs = nxt
    roots = {tuple(Q(int(x), d) for x in v) for v in Vs}
    need(len(roots) == 240, 'E8 closure')
    # simple roots for a generic functional, integer coordinates in the simple basis
    gen = [Q(7**t+3*t, 1) for t in range(8)]
    pos = [r for r in roots if sum(g*x for g, x in zip(gen, r)) > 0]
    posset = set(pos)
    simple = [r for r in pos if not any(tuple(r[t]-a[t] for t in range(8)) in posset for a in pos)]
    need(len(simple) == 8, 'simple roots')
    Cart = [[int(ip(a, b)) for b in simple] for a in simple]
    Sinv = invert([[simple[c][r] for c in range(8)] for r in range(8)])
    to_simple = lambda v: tuple(sum(Sinv[r][c]*v[c] for c in range(8)) for r in range(8))
    allroots = []
    for r in roots:
        s = to_simple(r)
        need(all(x.denominator == 1 for x in s), 'integral root')
        allroots.append(tuple(int(x) for x in s))
    p104 = [tuple(int(x) for x in to_simple(c)) for c in coords]
    return np.array(Cart, dtype=np.int64), allroots, p104


def invert(M):
    k = len(M)
    A = [list(M[i])+[Q(int(i == j)) for j in range(k)] for i in range(k)]
    for c in range(k):
        p = next(i for i in range(c, k) if A[i][c])
        A[c], A[p] = A[p], A[c]
        A[c] = [x/A[c][c] for x in A[c]]
        for i in range(k):
            if i != c and A[i][c]:
                A[i] = [x-A[i][c]*y for x, y in zip(A[i], A[c])]
    return [row[k:] for row in A]


def canon_line(v):
    v = np.asarray(v, dtype=np.int64)
    nz = np.nonzero(v)[0]
    if v[nz[0]] < 0:
        v = -v
    g = np.gcd.reduce(np.abs(v[nz]))
    return tuple((v//g).tolist())


def layer3(Cart, allroots, p104, ports):
    R = np.array(p104, dtype=np.int64)            # 104 x 8, simple coordinates
    lines = sorted({canon_line(r) for r in allroots})
    need(len(lines) == 120, 'root lines')
    inP = [canon_line(r) in {canon_line(q) for q in p104} for r in [np.array(l) for l in lines]]
    vals = (np.array(lines) @ Cart) @ R.T           # <line, P104 root>
    supp = [np.nonzero(row)[0].tolist() for row in vals]
    keys = [reduce_basis([ports[j] for j in s]) for s in supp]
    f1 = Counter((p, len(s), len(k)) for p, s, k in zip(inP, supp, keys))
    dim8 = {k for k in keys if len(k) == 8}
    pair = Counter()
    for a in range(120):
        for b in range(120):
            if set(supp[a]) & set(supp[b]):
                r = f2rank([sum(1 << t for t, i in enumerate(supp[b]) if dot2(ports[j], ports[i])) for j in supp[a]])
                pair[(r, inP[a], inP[b])] += 1
    # F3: branching landings, z = y_a - mu y_b perpendicular to some P104 root (mu != 0)
    tree = Counter()
    for a in range(120):
        for b in range(a+1, 120):
            best = 9
            for k in range(104):
                pa, pb = int(vals[a][k]), int(vals[b][k])
                if pa == 0 or pb == 0:
                    continue
                z = pb*np.array(lines[a], dtype=np.int64)-pa*np.array(lines[b], dtype=np.int64)
                s = np.nonzero((z @ Cart) @ R.T)[0].tolist()
                best = min(best, f2rank([ports[j] for j in s]))
            tree[(best, inP[a], inP[b])] += 1
    out = {'root_lines': 120, 'F1_root_lines': {str(k): v for k, v in sorted(f1.items())},
           'F1_distinct_dim8_spans': len(dim8),
           'F2_pair_rank': {str(k): v for k, v in sorted(pair.items())},
           'F3_branch_landing_min_span': {str(k): v for k, v in sorted(tree.items())}}
    log('L3', **out)
    return out


# ---------------------------------------------------------------- layer 4: all flats
def layer4(Cart, allroots, p104, ports):
    R = np.array(p104, dtype=np.int64)
    pos = np.array(sorted({canon_line(r) for r in allroots}), dtype=np.int64)   # 120 reflections
    Cinv = np.round(np.linalg.inv(Cart.astype(float))).astype(np.int64)
    need((Cinv @ Cart == np.eye(8, dtype=np.int64)).all(), 'unimodular Cartan')
    spans, total, orbit_sizes = {}, 0, []
    for k in range(8):
        start = np.array(canon_line(Cinv[k]), dtype=np.int64)          # fundamental coweight in root coordinates
        enc = lambda A: ((A.astype(np.int64)+64) * (128**np.arange(8, dtype=np.int64))).sum(axis=1)
        seen = enc(start[None, :])
        layer, allv = start[None, :], [start[None, :]]
        while len(layer):
            cand = []
            for c0 in range(0, len(layer), 2000):
                part = layer[c0:c0+2000]
                ip = part @ Cart @ pos.T                                 # (l, 120)
                new = (part[:, None, :]-ip[:, :, None]*pos[None, :, :]).reshape(-1, 8)
                nz = (new != 0).argmax(axis=1)
                new = new*np.sign(new[np.arange(len(new)), nz])[:, None]
                new = new//np.gcd.reduce(np.abs(new), axis=1)[:, None]
                need((np.abs(new) < 64).all(), 'coordinate range for keys')
                kk, idx = np.unique(enc(new), return_index=True)
                cand.append((kk, new[idx]))
            keys = np.concatenate([c[0] for c in cand]); rows = np.concatenate([c[1] for c in cand])
            keys, idx = np.unique(keys, return_index=True); rows = rows[idx]
            fresh = ~np.isin(keys, seen, assume_unique=True)
            layer = rows[fresh]
            seen = np.union1d(seen, keys[fresh])
            if len(layer):
                allv.append(layer)
        L = np.concatenate(allv)
        orbit_sizes.append(len(L)); total += len(L)
        masks, counts = np.unique(np.packbits((L @ Cart) @ R.T != 0, axis=1), axis=0, return_counts=True)
        for mk, cnt in zip(masks, counts):
            s = np.nonzero(np.unpackbits(mk)[:104])[0]
            key = reduce_basis([ports[j] for j in s])
            spans[key] = spans.get(key, 0)+int(cnt)
        log('L4_orbit', coweight=k, lines=len(L), distinct_spans=len(spans))
    keys = list(spans)
    pr = Counter()
    for A in keys:
        for B in keys:
            pr[f2rank([sum(1 << t for t, b in enumerate(B) if dot2(a, b)) for a in A])] += 1
    out = {'total_lines': total, 'orbit_sizes': orbit_sizes, 'distinct_spans': len(keys),
           'span_dims': dict(sorted(Counter(len(k) for k in keys).items())),
           'lines_with_dim8_span': sum(v for k, v in spans.items() if len(k) == 8),
           'span_pair_rank': dict(sorted(pr.items()))}
    log('L4', **out)
    return out


def main():
    authenticate()
    res = {'words': {}}
    X30 = ports30 = None
    flats = '--flats' in sys.argv and '--write' not in sys.argv
    for name in (['6030'] if flats else WORDS):
        out, X, ports = owned_layer(name)
        res['words'][name] = out
        if name == '6030':
            X30, ports30 = X, ports
    Cart, allroots, p104 = root_data(X30, ports30)
    res['roots'] = layer3(Cart, allroots, p104, ports30)
    if '--flats' in sys.argv:
        res['flats'] = layer4(Cart, allroots, p104, ports30)
    got = json.loads(json.dumps(res, sort_keys=True, default=str))
    if '--write' in sys.argv:
        (HERE/'RESULT.json').write_text(json.dumps(got, indent=1, sort_keys=True)+'\n')
        print('WROTE RESULT.json')
        return
    want = json.loads((HERE/'RESULT.json').read_text())
    if flats:   # --flats replays only PR6030 (source of the completion) and adds layer 4
        need(got['words']['6030'] == want['words']['6030'], 'result differs from RESULT.json: words.6030')
        got.pop('words')
    else:
        need('flats' in want, 'RESULT.json lacks layer 4')
        want = {k: v for k, v in want.items() if k != 'flats'}
    for key in got:
        need(got[key] == want[key], 'result differs from RESULT.json: '+key)
    print('PASS_P104_OWNED_LINEAGE_FLOOR_REVIEW' + ('_WITH_FLATS' if '--flats' in sys.argv else ''))


if __name__ == '__main__':
    main()
