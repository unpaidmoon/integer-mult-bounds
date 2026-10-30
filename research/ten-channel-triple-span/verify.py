#!/usr/bin/env python3
"""Three low-grade frames do not meet the clean mode on the PR #5745 source.

Rational steps use fractions.Fraction. NumPy is used only for arithmetic in
F_631. Every failed check raises SystemExit, including under python -O.

The census follows research/nine-channel-monotone-bound/independent.py
(Ali Romman), Apache-2.0, and does not import it.
"""

import hashlib
import io
import json
import multiprocessing
import os
import sys
import tarfile
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

# One BLAS thread per process. The exhaustive screen forks one process per core,
# and a threaded BLAS pool deadlocks across fork.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np

Q = Fraction
P = 631
ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "research/filtered-native-kappa004/inputs/original-packet.tar.gz"
WORD = "filtered_native_implementation/research/retained_state_next/F9-SOURCE-DAG-ALL8-WORD.json.gz"
MODES = "filtered_native_implementation/upstream/research/involutory-producer-raw-dual/inputs/R/R.json"
ARCHIVE_SHA256 = "595f988e748b1f3b25e7525a226da173966e4278a70f511b2919245cec1b45f7"
WORD_SHA256 = "934fea11e51f674ce2031b7d3127b994a921a9d83317b00359292752563a1775"
WITNESS = (0, -1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0)
EXPECTED_KERNEL_PIVOTS = (0, 6, 12, 1, 2, 3, 4, 5, 17, 13, 19, 18, 35, 23)


def fail(message):
    raise SystemExit("FAIL " + message)


def require(ok, message):
    if not ok:
        fail(message)


def add(a, b, c):
    for i, v in b.items():
        x = a.get(i, Q(0)) + c * v
        if x:
            a[i] = x
        else:
            a.pop(i, None)


def insert_pivot(basis, row):
    row = dict(row)
    while row:
        pivot = min(row)
        if pivot not in basis:
            scale = row[pivot]
            basis[pivot] = {i: v / scale for i, v in row.items()}
            return pivot
        add(row, basis[pivot], -row[pivot])
    return None


def analyze(rows):
    """Return nuisance rank and whether a pure mode vector is in the span."""
    basis = {}
    for row0 in rows:
        row = dict(row0)
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = {i: v / scale for i, v in row.items()}
                break
            add(row, basis[pivot], -row[pivot])
    nuisance = sum(1 for pivot in basis if pivot < 1000)
    clean = any(pivot >= 1000 for pivot in basis)
    return nuisance, clean


def idx(ref):
    return ref[1] + (632 if ref[0] == "C" else 0)


def census(word, modes):
    events = word["programs"]["backward"]
    n = 633 + word["owned_extra_slots_by_direction"]["backward"]
    cur = word["canonical"]["start"][:] + [None] * (n - 632)
    before = {}
    for k, event in enumerate(events):
        if event[0] == "scalar" and event[1][0] == "clear":
            d = idx(event[1][1])
            before[k] = cur[d]
            cur[d] = event[2]
        elif event[0] in ("climb", "warp"):
            d = event[2] if event[0] == "climb" else idx(event[1])
            require(cur[d] == event[3], "forward coframe")
            before[k] = cur[d]
            cur[d] = event[4]
    require(cur[:632] == word["canonical"]["final"], "final frames")
    cols = [{i: Q(1)} for i in range(632)] + [{} for _ in range(n - 632)]
    bases = {}
    seen = defaultdict(set)
    projected = {}
    contacts = 0

    def observe(d):
        nonlocal contacts
        frame = cur[d]
        if frame is None or len(word["canonical"]["frames"][frame]) >= 8 or not cols[d]:
            return
        contacts += 1
        key = tuple(sorted(cols[d].items()))
        if key in seen[frame]:
            return
        seen[frame].add(key)
        if key not in projected:
            row = {i: v for i, v in cols[d].items() if i < 224 or word["canonical"]["start"][i] != 0}
            mode = [sum((r[i] * v for i, v in cols[d].items() if i < 112), Q(0)) / 56 for r in modes]
            for j, a in enumerate(mode):
                if a:
                    add(row, {i: x for i, x in enumerate(modes[j]) if x}, -a)
                    row[632 + j] = a
            projected[key] = row
        pivot = insert_pivot(bases.setdefault(frame, {}), projected[key])
        require(pivot is None or pivot < 632, "single-frame clean response %s" % frame)

    for d in range(n):
        observe(d)
    for k in range(len(events) - 1, -1, -1):
        event = events[k]
        typ = event[0]
        changed = []
        if typ == "scalar":
            a = event[1]
            d = idx(a[1])
            kind = a[0]
            if kind == "add":
                src = idx(a[2])
                require(d != src and cur[d] == event[2] and cur[src] == event[2], "ADD coframe")
                add(cols[src], cols[d], Q(a[3], a[4]))
                changed = [src]
            elif kind == "scale":
                require(a[2] and cur[d] == event[2], "SCALE coframe")
                cols[d] = {i: v * Q(a[2], a[3]) for i, v in cols[d].items()}
                changed = [d]
            elif kind == "clear":
                cols[d] = {}
                changed = [d]
            else:
                fail("unhandled scalar %s" % kind)
        elif typ in ("climb", "warp"):
            d = event[2] if typ == "climb" else idx(event[1])
            changed = [d]
            require(cur[d] == event[4], "reverse coframe")
        elif typ not in ("physical_add", "adapter", "phase"):
            fail("unhandled event %s" % typ)
        if k in before:
            cur[d] = before[k]
        for d in changed:
            observe(d)
    meta = {
        "all_event_contacts": contacts,
        "distinct_frame_columns": sum(map(len, seen.values())),
        "projected_columns": len(projected),
        "frames": len(bases),
    }
    return bases, meta


def load_source():
    raw = ARCHIVE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == ARCHIVE_SHA256, "archive sha256")
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        word_bytes = archive.extractfile(WORD).read()
        require(hashlib.sha256(word_bytes).hexdigest() == WORD_SHA256, "word sha256")
        word = json.loads(__import__("gzip").decompress(word_bytes))
        modes = json.loads(archive.extractfile(MODES).read())
    modes = [[Q(x) for x in row] for row in modes]
    gram = [sum(modes[i][k] * modes[j][k] for k in range(len(modes[0]))) for i in range(8) for j in range(8)]
    require(gram == [56 if i == j else 0 for i in range(8) for j in range(8)], "RR^T = 56 I")
    return word, modes


def modq(value):
    den = int(value.denominator) % P
    require(den != 0, "denominator divisible by 631")
    return (int(value.numerator) % P) * pow(den, -1, P) % P


def build(bases):
    frames = sorted(bases)
    coords = sorted({i for basis in bases.values() for row in basis.values() for i in row if i < 632})
    index = {c: j for j, c in enumerate(coords)}
    require(len(coords) == 274, "nuisance coordinates %s" % len(coords))
    rows = []
    owner = []
    rational = []
    pivots_of = []
    for fi, frame in enumerate(frames):
        pivots_of.append(set(bases[frame]))
        for row0 in bases[frame].values():
            sparse = {}
            for i, v in row0.items():
                key = index[i] if i < 632 else 1000 + i - 632
                sparse[key] = v
            rational.append(sparse)
            rows.append(row0)
            owner.append(fi)
    m = len(coords)
    r = len(rational)
    matrix = np.zeros((r, m), dtype=np.int64)
    for i, sparse in enumerate(rational):
        for key, value in sparse.items():
            if key < 1000:
                matrix[i, key] = modq(value)
    starts = []
    dims = []
    cursor = 0
    for fi, frame in enumerate(frames):
        d = len(bases[frame])
        starts.append(cursor)
        dims.append(d)
        require(owner[cursor] == fi and owner[cursor + d - 1] == fi, "row grouping")
        cursor += d
    require(cursor == r, "row count")
    proj = np.random.default_rng(20261030).integers(0, P, size=(m, 64), dtype=np.int64)
    syn = matrix @ proj % P
    return {
        "frames": frames,
        "rational": rational,
        "matrix": matrix,
        "syn": syn,
        "starts": starts,
        "dims": dims,
        "pivots": pivots_of,
        "owner": owner,
        "m": m,
    }


def batch_det(matrices):
    """Product of non-pivoted diagonals, or 0 when a diagonal pivot vanishes.

    A nonzero value is the determinant over F_631. Zero means singular or an
    unlucky pivot order; it is never treated as a proof of independence.
    """
    batch, n, _ = matrices.shape
    if n == 0:
        return np.ones(batch, dtype=np.int64)
    current = np.array(matrices, copy=True)
    det = np.ones(batch, dtype=np.int64)
    active = np.ones(batch, dtype=bool)
    inv = batch_det.inv
    for col in range(n):
        piv = current[:, col, col]
        good = active & (piv != 0)
        det = np.where(good, det * piv % P, det)
        invp = inv[np.where(good, piv, 1)]
        for row in range(col + 1, n):
            factor = current[:, row, col] * invp % P
            factor = np.where(good, factor, 0)
            current[:, row, :] = (current[:, row, :] - factor[:, None] * current[:, col, :]) % P
        active = good
    return np.where(active, det % P, 0)


batch_det.inv = np.array([0] + [pow(i, -1, P) for i in range(1, P)], dtype=np.int64)


def rank_mod(matrix):
    current = np.array(matrix, copy=True)
    if current.size == 0:
        return 0
    row_count, col_count = current.shape
    rank = 0
    for col in range(col_count):
        if rank == row_count:
            break
        nz = np.flatnonzero(current[rank:, col])
        if len(nz) == 0:
            continue
        pivot_row = rank + int(nz[0])
        if pivot_row != rank:
            current[[rank, pivot_row]] = current[[pivot_row, rank]]
        inv = pow(int(current[rank, col]), -1, P)
        current[rank] = current[rank] * inv % P
        column = current[:, col].copy()
        column[rank] = 0
        nzr = np.flatnonzero(column)
        if len(nzr):
            current[nzr] = (current[nzr] - column[nzr, None] * current[rank]) % P
        rank += 1
    return rank


def rref_basis(matrix):
    current = np.array(matrix, copy=True)
    row_count, col_count = current.shape
    pivots = []
    row = 0
    for col in range(col_count):
        if row == row_count:
            break
        nz = np.flatnonzero(current[row:, col])
        if len(nz) == 0:
            continue
        pivot_row = row + int(nz[0])
        if pivot_row != row:
            current[[row, pivot_row]] = current[[pivot_row, row]]
        inv = pow(int(current[row, col]), -1, P)
        current[row] = current[row] * inv % P
        column = current[:, col].copy()
        column[row] = 0
        nzr = np.flatnonzero(column)
        if len(nzr):
            current[nzr] = (current[nzr] - column[nzr, None] * current[row]) % P
        pivots.append(col)
        row += 1
    return pivots, current[:row]


def frame_rows(data, fi):
    start = data["starts"][fi]
    return data["rational"][start : start + data["dims"][fi]]


def triple_rows(data, i, j, k):
    return frame_rows(data, i) + frame_rows(data, j) + frame_rows(data, k)


def modular_independent(data, triple):
    """Full modular row rank implies the same rows are independent over Q."""
    blocks = []
    for fi in triple:
        start = data["starts"][fi]
        blocks.append(data["matrix"][start : start + data["dims"][fi]])
    stacked = np.vstack(blocks)
    return rank_mod(stacked) == stacked.shape[0]


def q_clean(data, i, j, k):
    nuisance, clean = analyze(triple_rows(data, i, j, k))
    return clean, nuisance


def shared_pairs(data):
    groups = defaultdict(list)
    for fi, pivots in enumerate(data["pivots"]):
        for pivot in pivots:
            groups[pivot].append(fi)
    pairs = set()
    for members in groups.values():
        members = sorted(set(members))
        for a, left in enumerate(members):
            for right in members[:a]:
                pairs.add((right, left))
    return pairs


def confirm_pair(data, i, j):
    di, dj = data["dims"][i], data["dims"][j]
    nuisance, clean = analyze(frame_rows(data, i) + frame_rows(data, j))
    require(not clean, "clean pair %s %s" % (data["frames"][i], data["frames"][j]))
    if nuisance < di + dj:
        return (i, j, di + dj - nuisance, nuisance)
    return None


def screen_pairs(data, pairs):
    """Pairs whose nuisance images may meet. A nonzero minor excludes them."""
    syn = data["syn"]
    starts = data["starts"]
    dims = data["dims"]
    matrix = data["matrix"]
    grouped = defaultdict(list)
    wide = []
    for i, j in pairs:
        n = dims[i] + dims[j]
        if n <= 32:
            grouped[(dims[i], dims[j])].append((i, j))
        else:
            wide.append((i, j))
    candidates = []
    checked = 0
    for (di, dj), group in grouped.items():
        n = di + dj
        for start in range(0, len(group), 1024):
            chunk = group[start : start + 1024]
            batch = len(chunk)
            first = np.empty((batch, n, n), dtype=np.int64)
            second = np.empty((batch, n, n), dtype=np.int64)
            for t, (i, j) in enumerate(chunk):
                first[t, :di] = syn[starts[i] : starts[i] + di, :n]
                first[t, di:] = syn[starts[j] : starts[j] + dj, :n]
                second[t, :di] = syn[starts[i] : starts[i] + di, n : 2 * n]
                second[t, di:] = syn[starts[j] : starts[j] + dj, n : 2 * n]
            live = np.flatnonzero(batch_det(first) == 0)
            if len(live):
                both = live[batch_det(second[live]) == 0]
                for local in both:
                    found = confirm_pair(data, *chunk[int(local)])
                    if found:
                        candidates.append(found)
            checked += batch
        print("pair class", (di, dj), "checked", checked, "intersecting", len(candidates), flush=True)
    for i, j in wide:
        stacked = np.vstack((
            matrix[starts[i] : starts[i] + dims[i]],
            matrix[starts[j] : starts[j] + dims[j]],
        ))
        if rank_mod(stacked) < dims[i] + dims[j]:
            found = confirm_pair(data, i, j)
            if found:
                candidates.append(found)
        checked += 1
    require(checked == len(pairs), "pair screen count %s" % checked)
    return candidates


def fill_equal(target, packed, indexes, width):
    d = packed.shape[1]
    target[:, 0:d, :] = packed[indexes[:, 0], :, 0:width]
    target[:, d : 2 * d, :] = packed[indexes[:, 1], :, 0:width]
    target[:, 2 * d : 3 * d, :] = packed[indexes[:, 2], :, 0:width]


def iter_index_chunks(kind, lists, chunk=4096, outer=None):
    """Yield (N,3) index arrays into the per-dimension frame lists.

    `outer` is an half-open interval of the outermost loop. Splits of that
    loop partition the triples.
    """
    buf = []

    def flush():
        nonlocal buf
        if buf:
            out = np.asarray(buf, dtype=np.int64)
            buf = []
            return out
        return None

    if kind == "aaa":
        n = len(lists[0])
        lo, hi = (0, n) if outer is None else outer
        for i in range(lo, hi):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    buf.append((i, j, k))
                    if len(buf) == chunk:
                        yield flush()
    elif kind == "aab":
        na = len(lists[0])
        nb = len(lists[2])
        lo, hi = (0, na) if outer is None else outer
        for i in range(lo, hi):
            for j in range(i + 1, na):
                for k in range(nb):
                    buf.append((i, j, k))
                    if len(buf) == chunk:
                        yield flush()
    elif kind == "abb":
        na = len(lists[0])
        nb = len(lists[1])
        lo, hi = (0, na) if outer is None else outer
        for i in range(lo, hi):
            for j in range(nb):
                for k in range(j + 1, nb):
                    buf.append((i, j, k))
                    if len(buf) == chunk:
                        yield flush()
    elif kind == "abc":
        na = len(lists[0])
        nb = len(lists[1])
        nc = len(lists[2])
        lo, hi = (0, na) if outer is None else outer
        for i in range(lo, hi):
            for j in range(nb):
                for k in range(nc):
                    buf.append((i, j, k))
                    if len(buf) == chunk:
                        yield flush()
    else:
        fail("unknown class " + kind)
    last = flush()
    if last is not None:
        yield last


def outer_bounds(kind, lists, parts, min_total=0):
    """Partition the outermost triple index into disjoint work slices."""
    if kind == "aaa":
        n = len(lists[0])
        weights = [(n - i - 1) * (n - i - 2) // 2 for i in range(n)]
    elif kind == "aab":
        na, nb = len(lists[0]), len(lists[2])
        weights = [(na - i - 1) * nb for i in range(na)]
    elif kind == "abb":
        na, nb = len(lists[0]), len(lists[1])
        weights = [nb * (nb - 1) // 2] * na
    elif kind == "abc":
        na, nb, nc = len(lists[0]), len(lists[1]), len(lists[2])
        weights = [nb * nc] * na
    else:
        fail("unknown class " + kind)
    total = sum(weights)
    if total == 0:
        return []
    if min_total and total <= min_total:
        return [(0, len(weights))]
    parts = max(1, min(parts, total))
    target = (total + parts - 1) // parts
    bounds = []
    acc = 0
    start = 0
    for i, weight in enumerate(weights):
        acc += weight
        if weight and acc >= target and len(bounds) + 1 < parts and i + 1 < len(weights):
            bounds.append((start, i + 1))
            start = i + 1
            acc = 0
    bounds.append((start, len(weights)))
    return [(lo, hi) for lo, hi in bounds if lo < hi]


def worker_count():
    try:
        n = len(os.sched_getaffinity(0))
    except AttributeError:
        n = os.cpu_count() or 1
    return max(1, n)


def absorb(result, stats, keys):
    if "fail" in result:
        raise SystemExit(result["fail"])
    for key in keys:
        stats[key] += result[key]


# Inherited by forked workers. Assigned before each pool and never mutated after.
_SHARED = {}


def _small_worker(job):
    try:
        data = _SHARED["data"]
        intersecting = _SHARED["intersecting"]
        ids = job["ids"]
        width = job["width"]
        packed = {}
        blocks = []
        for frame_ids in ids:
            key = tuple(frame_ids)
            block = packed.get(key)
            if block is None:
                block = pack_frames(data, frame_ids, 2 * width)
                packed[key] = block
            blocks.append(block)
        local_stats = {"rejected": 0, "deferred": 0, "exact": 0, "seen": 0}
        index_lists = [list(range(len(frame_ids))) for frame_ids in ids]
        for indexes in iter_index_chunks(job["kind"], index_lists, outer=job["outer"]):
            consume_batch(data, ids, indexes, blocks, width, intersecting, local_stats)
            local_stats["seen"] += len(indexes)
        return local_stats
    except SystemExit as exc:
        return {"fail": str(exc)}


def pack_frames(data, frame_ids, width):
    d = data["dims"][frame_ids[0]]
    syn = data["syn"]
    starts = data["starts"]
    packed = np.empty((len(frame_ids), d, width), dtype=np.int64)
    for t, fi in enumerate(frame_ids):
        require(data["dims"][fi] == d, "pack dimension")
        packed[t] = syn[starts[fi] : starts[fi] + d, :width]
    return packed


def fill_projection(dest, blocks, indexes, col, n):
    row = 0
    locals_ = (indexes[:, 0], indexes[:, 1], indexes[:, 2])
    for part, local in zip(blocks, locals_):
        d = part.shape[1]
        dest[:, row : row + d, :] = part[local, :, col : col + n]
        row += d
    require(row == n, "block width")


def consume_batch(data, global_ids, indexes, blocks, width, intersecting, stats):
    """Reject full-rank triples. Queue the rest unless a known pair explains them."""
    n = width
    batch = len(indexes)
    first = np.empty((batch, n, n), dtype=np.int64)
    fill_projection(first, blocks, indexes, 0, n)
    d1 = batch_det(first)
    alive = np.flatnonzero(d1 == 0)
    if len(alive) == 0:
        stats["rejected"] += batch
        return
    second = np.empty((len(alive), n, n), dtype=np.int64)
    fill_projection(second, blocks, indexes[alive], n, n)
    d2 = batch_det(second)
    both = alive[np.flatnonzero(d2 == 0)]
    stats["rejected"] += batch - len(both)
    for local in both:
        i, j, k = (int(global_ids[t][int(indexes[local, t])]) for t in range(3))
        triple = tuple(sorted((i, j, k)))
        if (triple[0], triple[1]) in intersecting or (triple[0], triple[2]) in intersecting or (triple[1], triple[2]) in intersecting:
            stats["deferred"] += 1
            continue
        if modular_independent(data, triple):
            stats["rejected"] += 1
            continue
        clean, _nuisance = q_clean(data, *triple)
        stats["exact"] += 1
        require(not clean, "clean triple %s" % [data["frames"][t] for t in triple])


def sweep_small(data, intersecting, stats):
    by = defaultdict(list)
    for fi, d in enumerate(data["dims"]):
        if d <= 5:
            by[d].append(fi)
    dims = sorted(by)
    class_jobs = []
    for a in dims:
        for b in dims:
            if b < a:
                continue
            for c in dims:
                if c < b:
                    continue
                width = a + b + c
                require(2 * width <= 64, "projection width")
                if a == b == c:
                    if len(by[a]) < 3:
                        continue
                    kind = "aaa"
                    ids = [by[a], by[a], by[a]]
                elif a == b:
                    if len(by[a]) < 2 or len(by[c]) < 1:
                        continue
                    kind = "aab"
                    ids = [by[a], by[a], by[c]]
                elif b == c:
                    if len(by[b]) < 2 or len(by[a]) < 1:
                        continue
                    kind = "abb"
                    ids = [by[a], by[b], by[b]]
                else:
                    kind = "abc"
                    ids = [by[a], by[b], by[c]]
                index_lists = [list(range(len(x))) for x in ids]
                class_jobs.append({
                    "label": (a, b, c),
                    "kind": kind,
                    "ids": ids,
                    "width": width,
                    "bounds": outer_bounds(kind, index_lists, worker_count(), min_total=50000),
                })
    _SHARED["data"] = data
    _SHARED["intersecting"] = intersecting
    workers = worker_count()

    def run_class(class_job):
        jobs = [{
            "kind": class_job["kind"],
            "ids": class_job["ids"],
            "width": class_job["width"],
            "outer": bound,
        } for bound in class_job["bounds"]]
        if workers == 1 or len(jobs) == 1:
            return [_small_worker(job) for job in jobs]
        return pool.map(_small_worker, jobs)

    pool = None
    if workers > 1 and any(len(job["bounds"]) > 1 for job in class_jobs):
        pool = multiprocessing.get_context("fork").Pool(workers)
    try:
        for class_job in class_jobs:
            seen = 0
            for result in run_class(class_job):
                absorb(result, stats, ("rejected", "deferred", "exact"))
                seen += result["seen"]
            print("class", class_job["label"], "triples", seen, flush=True)
            stats["small"] += seen
    finally:
        if pool is not None:
            pool.close()
            pool.join()


def frame_residual(matrix, starts, h, dh, piv, basis):
    """Nuisance rows of frame h reduced against a modular pair RREF."""
    block = matrix[starts[h] : starts[h] + dh]
    return (block - (block[:, piv] @ basis) % P) % P


def extend_pairs(data, pairs, stats, syn0, proj, by_dim):
    """Certify thirds of the given intersecting pairs. `stats` is local."""
    matrix = data["matrix"]
    dims = data["dims"]
    starts = data["starts"]
    for n_pair, (i, j, iota, q_rank) in enumerate(pairs):
        rows = list(range(starts[i], starts[i] + dims[i])) + list(range(starts[j], starts[j] + dims[j]))
        pivots, basis = rref_basis(matrix[rows])
        require(len(pivots) == q_rank, "pair rank drifted mod 631 for %s %s" % (i, j))
        piv = np.asarray(pivots, dtype=np.int64)
        correction = basis @ proj % P
        syn = (syn0 - (matrix[:, piv] @ correction) % P) % P
        for dh, group0 in by_dim.items():
            group = [h for h in group0 if h != i and h != j]
            if not group:
                continue
            if dh > 64:
                pending = []
                for h in group:
                    if rank_mod(frame_residual(matrix, starts, h, dh, piv, basis)) == dh:
                        stats["extensions"] += 1
                    else:
                        pending.append(h)
            else:
                packed = np.empty((len(group), dh, min(128, 2 * dh)), dtype=np.int64)
                take = packed.shape[2]
                for t, h in enumerate(group):
                    packed[t, :, :take] = syn[starts[h] : starts[h] + dh, :take]
                first = batch_det(packed[:, :, :dh])
                alive = np.flatnonzero(first == 0)
                if len(alive) and 2 * dh <= take:
                    alive = alive[batch_det(packed[alive, :, dh : 2 * dh]) == 0]
                stats["extensions"] += len(group) - len(alive)
                pending = [group[int(t)] for t in alive]
            for h in pending:
                if rank_mod(frame_residual(matrix, starts, h, dh, piv, basis)) == dh:
                    stats["extensions"] += 1
                    continue
                clean, nuisance = q_clean(data, i, j, h)
                stats["exact"] += 1
                require(not clean, "clean extension %s" % [data["frames"][t] for t in (i, j, h)])
                require(
                    nuisance <= dims[i] + dims[j] + dh - iota,
                    "extension rank increased the kernel unexpectedly",
                )
        if n_pair and n_pair % 400 == 0 and len(pairs) > 400:
            print("extensions", n_pair, "exact", stats["exact"], flush=True)


def _ext_worker(index):
    try:
        local_stats = {"extensions": 0, "exact": 0}
        extend_pairs(
            _SHARED["data"],
            _SHARED["buckets"][index],
            local_stats,
            _SHARED["syn0"],
            _SHARED["proj"],
            _SHARED["by_dim"],
        )
        return local_stats
    except SystemExit as exc:
        return {"fail": str(exc)}


def certify_extensions(data, pairs, stats):
    """A third frame creates no new mode if its residual rank stays full.

    The size-128 projection of every row is precomputed. Subtracting the pair
    correction in those coordinates equals the projection of the residual, so a
    nonzero minor is still a full-rank certificate. Residual rows themselves are
    formed only for frames whose minors vanish. Pair batches are independent and
    may run concurrently; the coverage check is on their sum.
    """
    matrix = data["matrix"]
    dims = data["dims"]
    m = data["m"]
    proj = np.random.default_rng(20261031).integers(0, P, size=(m, 128), dtype=np.int64)
    syn0 = matrix @ proj % P
    by_dim = defaultdict(list)
    for h, dh in enumerate(dims):
        by_dim[dh].append(h)
    exact_before = stats["exact"]
    workers = worker_count()
    if workers == 1 or len(pairs) < 2:
        extend_pairs(data, pairs, stats, syn0, proj, by_dim)
    else:
        buckets = [[] for _ in range(workers * 4)]
        for t, pair in enumerate(pairs):
            buckets[t % len(buckets)].append(pair)
        _SHARED["data"] = data
        _SHARED["buckets"] = buckets
        _SHARED["syn0"] = syn0
        _SHARED["proj"] = proj
        _SHARED["by_dim"] = by_dim
        pool = multiprocessing.get_context("fork").Pool(workers)
        try:
            done = 0
            for result in pool.imap_unordered(_ext_worker, range(len(buckets))):
                absorb(result, stats, ("extensions", "exact"))
                done += 1
                print("extension batches", done, "exact", stats["exact"], flush=True)
        finally:
            pool.close()
            pool.join()
    covered = stats["extensions"] + (stats["exact"] - exact_before)
    require(covered == len(pairs) * (len(dims) - 2), "extension coverage %s" % covered)
    stats["extensions_pairs"] = len(pairs)


def sweep_large(data, intersecting, stats):
    dims = data["dims"]
    starts = data["starts"]
    matrix = data["matrix"]
    m = data["m"]
    large = [fi for fi, d in enumerate(dims) if d >= 8]
    proj = np.random.default_rng(20261032).integers(0, P, size=(m, 80), dtype=np.int64)
    others = [fi for fi in range(len(dims)) if fi not in set()]
    for anchor in large:
        da = dims[anchor]
        pivots, basis = rref_basis(matrix[starts[anchor] : starts[anchor] + da])
        require(len(pivots) == da, "anchor dropped rank")
        piv = np.asarray(pivots, dtype=np.int64)
        residual = (matrix - (matrix[:, piv] @ basis) % P) % P
        syn = residual @ proj % P
        rest = [fi for fi in range(len(dims)) if fi != anchor and dims[fi] <= dims[anchor]]
        # Each unordered pair of frames whose largest member is this anchor.
        # Ties on dimension use the greatest frame index as the anchor.
        eligible = [fi for fi in rest if dims[fi] < da or fi < anchor]
        by = defaultdict(list)
        for fi in eligible:
            by[dims[fi]].append(fi)
        for b in sorted(by):
            for c in sorted(by):
                if c < b:
                    continue
                width = b + c
                if width > 40:
                    continue
                ids_b, ids_c = by[b], by[c]
                if b == c:
                    local_pairs = [(x, y) for x in range(len(ids_b)) for y in range(x + 1, len(ids_b))]
                    if not local_pairs:
                        continue
                    packed_b = pack_from_syn(syn, starts, ids_b, b, 80)
                    blocks_kind = "aa"
                else:
                    local_pairs = [(x, y) for x in range(len(ids_b)) for y in range(len(ids_c))]
                    packed_b = pack_from_syn(syn, starts, ids_b, b, 80)
                    packed_c = pack_from_syn(syn, starts, ids_c, c, 80)
                    blocks_kind = "ab"
                for start in range(0, len(local_pairs), 4096):
                    chunk = local_pairs[start : start + 4096]
                    batch = len(chunk)
                    first = np.empty((batch, width, width), dtype=np.int64)
                    second = np.empty((batch, width, width), dtype=np.int64)
                    idx = np.asarray(chunk, dtype=np.int64)
                    if blocks_kind == "aa":
                        first[:, 0:b, :] = packed_b[idx[:, 0], :, 0:width]
                        first[:, b:, :] = packed_b[idx[:, 1], :, 0:width]
                        second[:, 0:b, :] = packed_b[idx[:, 0], :, width : 2 * width]
                        second[:, b:, :] = packed_b[idx[:, 1], :, width : 2 * width]
                        globals_b = ids_b
                        globals_c = ids_b
                    else:
                        first[:, 0:b, :] = packed_b[idx[:, 0], :, 0:width]
                        first[:, b:, :] = packed_c[idx[:, 1], :, 0:width]
                        second[:, 0:b, :] = packed_b[idx[:, 0], :, width : 2 * width]
                        second[:, b:, :] = packed_c[idx[:, 1], :, width : 2 * width]
                        globals_b = ids_b
                        globals_c = ids_c
                    d1 = batch_det(first)
                    alive = np.flatnonzero(d1 == 0)
                    if len(alive) == 0:
                        stats["large"] += batch
                        stats["rejected"] += batch
                        continue
                    # Second minor may not fit when 2*width > 80.
                    if 2 * width <= 80:
                        d2 = batch_det(second[alive])
                        both = alive[d2 == 0]
                    else:
                        both = alive
                    stats["rejected"] += batch - len(both)
                    stats["large"] += batch
                    for local in both:
                        g = int(globals_b[int(idx[local, 0])])
                        h = int(globals_c[int(idx[local, 1])])
                        triple = tuple(sorted((anchor, g, h)))
                        if (
                            (triple[0], triple[1]) in intersecting
                            or (triple[0], triple[2]) in intersecting
                            or (triple[1], triple[2]) in intersecting
                        ):
                            stats["deferred"] += 1
                            continue
                        if modular_independent(data, triple):
                            stats["rejected"] += 1
                            continue
                        clean, _nuisance = q_clean(data, *triple)
                        stats["exact"] += 1
                        require(not clean, "clean large triple %s" % [data["frames"][t] for t in triple])
        # Companion pairs whose residual width exceeds the packed minor.
        heavy = [fi for fi in eligible if dims[fi] > 20]
        light = [fi for fi in eligible if dims[fi] <= 20]
        for g in heavy:
            partners = [h for h in heavy if h > g] + [h for h in light if dims[g] + dims[h] > 40]
            for h in partners:
                full = rank_mod(np.vstack((
                    residual[starts[g] : starts[g] + dims[g]],
                    residual[starts[h] : starts[h] + dims[h]],
                )))
                stats["large"] += 1
                if full == dims[g] + dims[h]:
                    stats["rejected"] += 1
                    continue
                triple = tuple(sorted((anchor, g, h)))
                if (
                    (triple[0], triple[1]) in intersecting
                    or (triple[0], triple[2]) in intersecting
                    or (triple[1], triple[2]) in intersecting
                ):
                    stats["deferred"] += 1
                    continue
                triple_rows_idx = (anchor, g, h)
                if modular_independent(data, triple):
                    stats["rejected"] += 1
                    continue
                clean, _nuisance = q_clean(data, *triple_rows_idx)
                stats["exact"] += 1
                require(not clean, "clean huge triple %s" % [data["frames"][t] for t in triple])
        print("anchor", data["frames"][anchor], "dim", da, "exact", stats["exact"], flush=True)


def pack_from_syn(syn, starts, frame_ids, d, width):
    packed = np.empty((len(frame_ids), d, width), dtype=np.int64)
    for t, fi in enumerate(frame_ids):
        packed[t] = syn[starts[fi] : starts[fi] + d, :width]
    return packed


def disjoint_pair_control(data):
    rng = np.random.default_rng(7)
    frames = np.arange(len(data["dims"]))
    seen = 0
    tries = 0
    while seen < 40 and tries < 4000:
        tries += 1
        i, j = [int(x) for x in rng.choice(frames, size=2, replace=False)]
        if i > j:
            i, j = j, i
        if data["pivots"][i] & data["pivots"][j]:
            continue
        nuisance, clean = analyze(frame_rows(data, i) + frame_rows(data, j))
        require(not clean and nuisance == data["dims"][i] + data["dims"][j], "disjoint pivots met")
        seen += 1
    require(seen == 40, "disjoint-pivot control found %s pairs" % seen)


def dim1_witness(bases):
    frames = sorted(frame for frame, basis in bases.items() if len(basis) == 1)
    require(len(frames) == 119, "dimension-1 count %s" % len(frames))
    coords = sorted({i for frame in frames for i in next(iter(bases[frame].values())) if i < 632})
    index = {c: j for j, c in enumerate(coords)}
    rows = []
    for frame in frames:
        row0 = next(iter(bases[frame].values()))
        row = {index[i]: v for i, v in row0.items() if i < 632}
        for j in range(8):
            value = row0.get(632 + j, Q(0))
            if value:
                row[1000 + j] = value
        rows.append(row)
    basis = {}
    kernel = []
    for g, row0 in enumerate(rows):
        row = {i: v for i, v in row0.items() if i < 1000}
        coeff = {g: Q(1)}
        mode = [row0.get(1000 + j, Q(0)) for j in range(8)]
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = (
                    {i: v / scale for i, v in row.items()},
                    {j: v / scale for j, v in coeff.items()},
                    [m / scale for m in mode],
                )
                break
            factor = row[pivot]
            br, bc, bm = basis[pivot]
            add(row, br, -factor)
            for j, v in bc.items():
                x = coeff.get(j, Q(0)) - factor * v
                if x:
                    coeff[j] = x
                else:
                    coeff.pop(j, None)
            mode = [m - factor * bb for m, bb in zip(mode, bm)]
        else:
            kernel.append((coeff, mode))
    require(len(basis) == 105 and len(kernel) == 14, "dimension-1 kernel shape")
    reduced = []
    pivots = []
    for coeff, mode in kernel:
        row = dict(coeff)
        for j, v in enumerate(mode):
            if v:
                row[1000 + j] = v
        for pivot, basis_row in zip(list(pivots), list(reduced)):
            if pivot in row:
                add(row, basis_row, -row[pivot])
        if not row:
            continue
        keys = [i for i in row if i < 1000]
        pivot = min(keys) if keys else min(row)
        scale = row[pivot]
        row = {i: v / scale for i, v in row.items()}
        new_rows = []
        for basis_row in reduced:
            if pivot in basis_row:
                basis_row = dict(basis_row)
                add(basis_row, row, -basis_row[pivot])
            new_rows.append(basis_row)
        reduced = new_rows + [row]
        pivots.append(pivot)
    require(tuple(pivots) == EXPECTED_KERNEL_PIVOTS, "kernel pivots %s" % pivots)
    acc = {}
    for coef, row in zip(WITNESS, reduced):
        if coef:
            add(acc, row, Q(coef))
    # Express the kernel combination in the original 119 generators.
    original = {}
    for coef, row in zip(WITNESS, reduced):
        if not coef:
            continue
        for j, v in row.items():
            if j >= 1000:
                continue
            original[j] = original.get(j, Q(0)) + coef * v
    support = [j for j, v in original.items() if v]
    mode = [acc.get(1000 + j, Q(0)) for j in range(8)]
    require(len(support) == 41, "witness support %s" % len(support))
    require(mode == [Q(0), Q(0), Q(0), Q(0), Q(14), Q(-14), Q(-14), Q(14)], "witness mode %s" % mode)
    # Rebuild from original generators and compare.
    direct = {}
    for j in support:
        add(direct, rows[j], original[j])
    require(all(direct.get(i, Q(0)) == 0 for i in range(len(coords))), "witness nuisance")
    require([direct.get(1000 + j, Q(0)) for j in range(8)] == mode, "witness rebuild")
    return [frames[j] for j in support]


def _collect_indexes(kind, lists, outer=None):
    found = []
    for indexes in iter_index_chunks(kind, lists, chunk=7, outer=outer):
        found.extend(tuple(row) for row in indexes.tolist())
    return found


def self_test():
    eye = np.eye(4, dtype=np.int64)[None, :, :]
    require(int(batch_det(eye)[0]) == 1, "identity det")
    singular = eye.copy()
    singular[0, 0, 0] = 0
    require(int(batch_det(singular)[0]) == 0, "zero pivot")
    rank, clean = analyze([{0: Q(1), 1000: Q(1)}, {0: Q(1)}])
    require(clean and rank == 1, "detector sees a clean pair")
    rank, clean = analyze([{0: Q(1), 1000: Q(1)}, {0: Q(1), 1000: Q(1)}])
    require(rank == 1 and not clean, "matched modes are not clean")
    rank, clean = analyze([{0: Q(1)}, {1: Q(1)}, {2: Q(1)}])
    require(rank == 3 and not clean, "independent triple")
    samples = (
        ("aaa", [list(range(10))] * 3, 120),
        ("aab", [list(range(8)), list(range(8)), list(range(5))], 140),
        ("abb", [list(range(4)), list(range(6)), list(range(6))], 60),
        ("abc", [list(range(3)), list(range(4)), list(range(5))], 60),
    )
    for kind, lists, count in samples:
        full = _collect_indexes(kind, lists)
        parts = []
        for lo, hi in outer_bounds(kind, lists, 4):
            parts.extend(_collect_indexes(kind, lists, (lo, hi)))
        require(parts == full and len(full) == count, "index split %s %s" % (kind, len(parts)))


def main():
    self_test()
    word, modes = load_source()
    bases, meta = census(word, modes)
    require(meta == {
        "all_event_contacts": 15752,
        "distinct_frame_columns": 14816,
        "projected_columns": 12240,
        "frames": 879,
    }, "census %s" % meta)
    witness = dim1_witness(bases)
    grades = word["canonical"]["frames"]
    require(all(len(grades[frame]) < 8 for frame in witness), "witness grade")
    data = build(bases)
    disjoint_pair_control(data)
    pairs = shared_pairs(data)
    require(len(pairs) == 280364, "shared-pivot pairs %s" % len(pairs))
    confirmed = screen_pairs(data, pairs)
    intersecting = {(i, j) for i, j, _iota, _rank in confirmed}
    require(len(intersecting) == 3782, "intersecting pairs %s" % len(intersecting))
    print("intersecting_pairs", len(intersecting), flush=True)
    stats = {"rejected": 0, "deferred": 0, "exact": 0, "small": 0, "large": 0, "extensions": 0}
    sweep_small(data, intersecting, stats)
    sweep_large(data, intersecting, stats)

    def choose(n, k):
        value = 1
        for t in range(k):
            value = value * (n - t) // (t + 1)
        return value

    small_n = sum(1 for d in data["dims"] if d <= 5)
    require(stats["small"] == choose(small_n, 3), "small triples %s" % stats["small"])
    require(stats["large"] == choose(879, 3) - choose(small_n, 3), "large triples %s" % stats["large"])
    certify_extensions(data, confirmed, stats)
    print("PASS_TEN_CHANNEL_TRIPLE_OBSTRUCTION")
    print("upper_support=41")
    print("witness_frames=" + ",".join(str(frame) for frame in witness))
    print("intersecting_pairs=%s exact=%s deferred=%s small=%s large=%s extensions=%s" % (
        len(intersecting), stats["exact"], stats["deferred"], stats["small"], stats["large"], stats["extensions"]))


if __name__ == "__main__":
    main()
