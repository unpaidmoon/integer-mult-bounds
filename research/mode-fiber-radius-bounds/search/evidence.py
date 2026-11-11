"""Non-certifying search (scipy/HiGHS): interior lattice points near zonotope faces and vertices,
each recorded with an exact 0/1 subset-sum witness z. Output: evidence_<seed>.json."""
import itertools, json, sys
from pathlib import Path
import numpy as np
from scipy.optimize import milp, linprog, LinearConstraint, Bounds
M = np.array([[c[i] for c in json.load(open(Path(__file__).resolve().parents[3] / 'research/coded-native-caller/NORMALIZERS.json'))['mode_columns']] for i in range(112)], dtype=float); n = 112
H8 = {tuple(int(v) for v in (np.abs(r) % 2)) for r in M} | {(0,) * 8, (1,) * 8}
in_L = lambda t: tuple(int(v) % 2 for v in t) in H8
SMALL = [np.array(u, float) for u in itertools.product(range(-2, 3), repeat=8)
         if any(u) and sum(map(abs, u)) <= 8 and in_L(u)]
def margin(t):
    c = np.zeros(n + 1); c[-1] = -1
    A_ub = np.vstack([np.hstack([-np.eye(n), np.ones((n, 1))]), np.hstack([np.eye(n), np.ones((n, 1))])])
    r = linprog(c, A_ub=A_ub, b_ub=np.r_[np.zeros(n), np.ones(n)], A_eq=np.hstack([M.T, np.zeros((8, 1))]),
                b_eq=t, bounds=[(None, None)] * n + [(None, 0.5)])
    return -r.fun if r.status == 0 else -1
def witness(t):
    r = milp(np.zeros(n), constraints=[LinearConstraint(M.T, t, t)], integrality=np.ones(n),
             bounds=Bounds(0, 1), options={'time_limit': 30})
    return None if r.status != 0 else [i for i in range(n) if r.x[i] > 0.5]
seed, trials = int(sys.argv[1]), int(sys.argv[2]); rng = np.random.default_rng(seed)
out = []; failures = []
for trial in range(trials):
    k = int(rng.integers(0, 8))
    if k:
        T = rng.choice(n, k, replace=False); Q, _ = np.linalg.qr(M[T].T, mode='complete')
        f = Q[:, k:] @ rng.normal(size=8 - k)
    else:
        f = rng.normal(size=8)
    s = M @ f; W = np.where(np.abs(s) < 1e-9)[0]; y = (s > 0).astype(float)
    q = int(rng.choice([2, 3, 4, 6]))
    for _ in range(30):
        y[W] = rng.integers(0, q + 1, len(W)) / q; t0 = M.T @ y
        if np.allclose(t0, np.round(t0)) and in_L(np.round(t0)): break
    else:
        continue
    t0 = np.round(t0); inward = [u for u in SMALL if f @ u > 1e-9]
    for j in rng.permutation(len(inward))[:6]:
        t = t0 - inward[j]; m = margin(t)
        if m <= 1e-9: continue
        z = witness(t)
        rec = {'t': [int(v) for v in t], 'face_rank': k, 'q': q, 'lp_margin': round(m, 9)}
        if z is None: failures.append(rec); print('NO WITNESS', rec, flush=True)
        else: rec['z'] = z; out.append(rec)
json.dump({'seed': seed, 'trials': trials, 'records': out, 'no_witness': failures},
          open('evidence_%d.json' % seed, 'w'), separators=(',', ':'))
print('seed', seed, 'interior points', len(out) + len(failures), 'without witness', len(failures))
