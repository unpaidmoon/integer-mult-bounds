"""Non-certifying local search (numpy) for a row basis of L minimizing the max column l1 norm tau.
Usage: python basis_search.py SEED RESTARTS"""
import json, sys
from pathlib import Path
import numpy as np
M = np.array([[c[i] for c in json.load(open(Path(__file__).resolve().parents[3] / 'research/coded-native-caller/NORMALIZERS.json'))['mode_columns']] for i in range(112)])
def score(B):
    MB = M[B].T.astype(float)
    if round(abs(np.linalg.det(MB))) != 16: return None
    N = np.setdiff1d(np.arange(112), B)
    W = np.round(np.linalg.solve(MB, M[N].T.astype(float))).astype(int)
    c = np.abs(W).sum(0); return (int(c.max()), int((c == c.max()).sum()))
rng = np.random.default_rng(int(sys.argv[1])); best = None
for restart in range(int(sys.argv[2])):
    while True:
        B = list(rng.choice(112, 8, replace=False)); s = score(B)
        if s: break
    improved = True
    while improved:
        improved = False
        for pos in rng.permutation(8):
            for cand in rng.permutation(112):
                if cand in B: continue
                C = B.copy(); C[pos] = cand; sc = score(C)
                if sc and sc < s: B, s, improved = C, sc, True
    if best is None or s < best[0]:
        best = (s, sorted(int(b) for b in B)); print(restart, best, flush=True)
