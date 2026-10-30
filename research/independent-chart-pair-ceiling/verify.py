#!/usr/bin/env python3
"""Independent one-transvection chart pairs on the retained center contacts.

The coherent-contact ceiling priced one chart, one common transvection on an
adjacent pair, and one common alternative on one original-chart group. This
verifier prices every ordered pair of one-transvection charts at every pair of
variable contacts. Python 3.12 standard library only. No selected-frontier
change is claimed.
"""
from collections import Counter, defaultdict
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research" / "sol1337-contact-frontier"))
import build_graph  # noqa: E402

# Paid part of the single-contact minimum. Rank 0 is not part of S_j.
D_STAR = (0, 1, 0, 0, 0, 0, 0, 1, -1, 0)
# Recomputed single-contact census. Counts match the #4867 screen.
SINGLE_CLASSES = {
    (-4, 4, 0, 0, 0, 0, 0, 0, 0, 0): 117530,
    (-3, 3, -1, 1, 0, 0, 0, 0, 0, 0): 32512,
    (-3, 2, 1, 0, 0, 0, 0, 0, 0, 0): 21420,
    (-2, 1, 1, 0, 0, 0, 0, 0, -1, 1): 5106,
    (-2, 1, 1, 0, 0, 0, 0, 1, -1, 0): 2547,
    (-2, 1, 1, 0, 0, 0, 0, 0, 0, 0): 2547,
    (-3, 3, 0, 0, 0, 0, 0, 0, -1, 1): 2048,
    (-3, 3, 0, 0, 0, 0, 0, 0, 0, 0): 1137,
    (-2, 2, -1, 1, 0, 0, 0, 0, -1, 1): 1024,
    (-3, 3, 0, 0, 0, 0, 0, 1, -1, 0): 1020,
    (-2, 2, -1, 1, 0, 0, 0, 1, -1, 0): 504,
    (-2, 2, -1, 1, 0, 0, 0, 0, 0, 0): 504,
    (-3, 4, -1, 0, 0, 0, 0, 0, 0, 0): 96,
    (-2, 2, 0, 0, 0, 0, 0, 0, 0, 0): 30,
    (-1, 1, 0, 0, 0, 0, 0, 0, -1, 1): 7,
    (-2, 2, 0, 0, 0, 0, 0, 0, -1, 1): 7,
    (-2, 3, -1, 0, 0, 0, 0, 1, -1, 0): 6,
    (-1, 1, 0, 0, 0, 0, 0, 1, -1, 0): 3,
}


def need(ok, message):
    if not ok:
        raise SystemExit("FAIL: " + message)


def axes(lag, n=9):
    """Canonical transvections that move this Lagrangian. 2*(2^n-1) vectors."""
    mask = (1 << n) - 1
    rows = [(lag[i] >> n) | ((lag[i] & mask) << n) | (1 << (2 * n + i)) for i in range(n)]
    pivots = []
    k = 0
    for j in range(2 * n):
        if k >= n:
            break
        z = k
        while z < n and not (rows[z] >> j & 1):
            z += 1
        if z == n:
            continue
        rows[k], rows[z] = rows[z], rows[k]
        row = rows[k]
        for i in range(n):
            if i != k and (rows[i] >> j & 1):
                rows[i] ^= row
        pivots.append(j)
        k += 1
    need(k == n, "Lagrangian basis is dependent")
    dual = [0] * n
    for j in range(n):
        for i in range(n):
            if rows[i] >> (2 * n + j) & 1:
                dual[j] |= 1 << pivots[i]
    base = [0] * (1 << n)
    out = []
    for mask_b in range(1, 1 << n):
        j = (mask_b & -mask_b).bit_length() - 1
        base[mask_b] = base[mask_b & (mask_b - 1)] ^ dual[j]
        out.append(base[mask_b])
        out.append(base[mask_b] ^ lag[j])
    return out


def symp(a, b):
    return (((a & 511) & (b >> 9)).bit_count() + ((a >> 9) & (b & 511)).bit_count()) & 1


def turn(lag, axis):
    return [x ^ axis if symp(x, axis) else x for x in lag]


def binary_rank(rows):
    pivots = [0] * 18
    rank = 0
    for x in rows:
        while x:
            i = x.bit_length() - 1
            pivot = pivots[i]
            if pivot:
                x ^= pivot
            else:
                pivots[i] = x
                rank += 1
                break
    return rank


def dist(a, b):
    return binary_rank(a + b) - 9


def prefixes(delta):
    low = 0
    above = sum(delta[1:])
    out = [0] * 10
    for j in range(1, 10):
        out[j] = low + j * above
        low += j * delta[j]
        above -= delta[j]
    return out


def certified(delta, low_need=1, high_need=0):
    """S_j(delta) >= low_need for j<=7 and >= high_need for j>=8."""
    low = 0
    above = sum(delta[1:])
    for j in range(1, 10):
        bound = low_need if j <= 7 else high_need
        if low + j * above < bound:
            return False
        low += j * delta[j]
        above -= delta[j]
    return True


def load_graph(directory):
    meta = build_graph.build(directory)
    text = (directory / "center-contact-graph.txt").read_text().splitlines()
    n, nframes, nmaps, nedges = map(int, text[0].split())
    frame = []
    fixed = []
    cursor = 1
    for _ in range(n):
        a, b = map(int, text[cursor].split())
        frame.append(a)
        fixed.append(b)
        cursor += 1
    lags = []
    for _ in range(nframes):
        lags.append(list(map(int, text[cursor].split())))
        cursor += 1
    cursor += nmaps
    incident = defaultdict(list)
    internal = []
    for _ in range(nedges):
        a, b, rank, sign, mp = map(int, text[cursor].split())
        cursor += 1
        need(sign == 1, "every retained edge is a positive paid constraint")
        if fixed[a] == 0 or fixed[b] == 0:
            need(mp == 0, "a variable contact meets a nontrivial warp map")
        if fixed[a] == 0:
            incident[a].append((b, rank, frame[b]))
        if fixed[b] == 0 and a != b:
            incident[b].append((a, rank, frame[a]))
        if fixed[a] == 0 and fixed[b] == 0 and a != b:
            internal.append((a, b, rank))
    return meta, frame, fixed, lags, incident, internal


def main():
    with tempfile.TemporaryDirectory(prefix="chart-pairs-") as raw:
        meta, frame, fixed, lags, incident, internal = load_graph(Path(raw))
    need(meta["newly_variable_center_contacts"] == 184, "184 variable contacts")
    need(meta["nodes"] == 19197 and meta["edges"] == 34830, "retained graph size")
    need(meta["independent_center_reward"] == 0, "no free center reward")
    need(meta["paid"] == {"1": 2201, "2": 412, "3": 510, "4": 127, "5": 40, "8": 8}
         or meta["paid"] == {1: 2201, 2: 412, 3: 510, 4: 127, 5: 40, 8: 8},
         "baseline paid histogram")
    selected = [i for i, flag in enumerate(fixed) if flag == 0]
    need(len(selected) == 184, "fixed-bit census")
    need(all(len(incident[i]) == 4 for i in selected), "every variable contact has degree 4")
    pair_key = {(min(a, b), max(a, b)) for a, b, _ in internal}
    need(len(internal) == len(pair_key) == 264, "264 simple internal edges")
    rank0 = [(a, b) for a, b, rank in internal if rank == 0]
    rank8 = [(a, b) for a, b, rank in internal if rank == 8]
    need(len(rank0) == 256 and len(rank8) == 8, "internal ranks are 256 zeros and 8 eights")
    need(all(frame[a] == 0 and frame[b] == 0 for a, b in rank0), "rank-0 edges stay inside the empty chart")
    singletons = [i for i in selected if frame[i] != 0]
    need(len(singletons) == 8 and len({frame[i] for i in singletons}) == 8, "eight distinct singleton charts")
    need(sum(frame[i] == 0 for i in selected) == 176, "176 empty-chart contacts")
    for a, b in rank8:
        ends = {frame[a], frame[b]}
        need(0 in ends and len(ends) == 2, "each rank-8 edge joins a singleton to the empty chart")
    need(all(frame[a] == 0 or frame[b] == 0 for a, b, _ in internal),
         "singleton charts form an independent set")

    needed = {0} | {frame[i] for i in selected}
    for node in selected:
        for _, _, other_frame in incident[node]:
            needed.add(other_frame)
    images = {}
    for fid in needed:
        images[fid] = [turn(lags[fid], axis) for axis in axes(lags[fid])]
        need(len(images[fid]) == 1022, "1022 one-transvection charts")

    empty = images[0]
    origin = lags[0]
    histogram = Counter()
    distance_one = set()
    for i in range(1022):
        need(dist(empty[i], origin) == 1, "every alternative leaves the empty chart")
        for j in range(i, 1022):
            gap = dist(empty[i], empty[j])
            histogram[gap] += 1
            if i != j and gap == 1:
                distance_one.add((i, j))
    need(histogram == {0: 1022, 1: 511, 2: 521220}, "empty-chart neighbor distances")
    expected_partners = {(i, i + 1) for i in range(0, 1022, 2)}
    need(distance_one == expected_partners, "distance-1 charts form the emitted matching")

    classes = Counter()
    node_delta = {}
    for node in selected:
        fid = frame[node]
        deltas = []
        for image in images[fid]:
            delta = [0] * 10
            for _, rank, other_frame in incident[node]:
                new_rank = dist(image, lags[other_frame])
                delta[new_rank] += 1
                delta[rank] -= 1
            need(certified(delta), "single-contact move fails the d* majorization")
            classes[tuple(delta)] += 1
            deltas.append(delta)
        node_delta[node] = deltas
    need(sum(classes.values()) == 188048, "single-contact case count")
    need(dict(classes) == SINGLE_CLASSES, "single-contact classes drifted from the #4867 census")
    star = prefixes(D_STAR)
    need(star[1:] == [1, 1, 1, 1, 1, 1, 1, 0, 0], "d* prefix vector")
    need(certified(D_STAR), "positive control rejected d*")
    dropped = (0, 0, 0, 0, 0, 0, 0, 1, -1, 0)
    need(not certified(dropped), "failure control accepted a move with the rank-1 payment removed")
    need(not certified([0] * 10), "failure control accepted the identity histogram")

    # Two copies of d* plus the distance-1 correction are NOT certified.
    # Enumeration of real partner assignments is therefore load-bearing.
    partner_synthetic = [2 * D_STAR[r] for r in range(10)]
    partner_synthetic[0] += 1
    partner_synthetic[1] -= 1
    need(not certified(partner_synthetic), "failure control accepted the crude partner bound")
    same_synthetic = [2 * D_STAR[r] for r in range(10)]
    same_synthetic[0] += 2
    same_synthetic[1] -= 2
    need(not certified(same_synthetic), "failure control accepted the crude same-chart bound")
    far_synthetic = [2 * D_STAR[r] for r in range(10)]
    far_synthetic[0] += 1
    far_synthetic[1] -= 1
    far_synthetic[2] += 1
    need(certified(far_synthetic), "distance-2 correction of two minimum moves must still certify")

    same_cases = 0
    same_sharp = False
    partner_cases = 0
    partner_min = 99
    for a, b in rank0:
        left, right = node_delta[a], node_delta[b]
        for i in range(1022):
            same = [left[i][r] + right[i][r] for r in range(10)]
            same[0] += 2
            same[1] -= 2
            need(certified(same), "same-chart adjacent pair loses the certificate")
            same_cases += 1
            if prefixes(same)[1:] == star[1:]:
                same_sharp = True
            partner = i ^ 1
            joint = [left[i][r] + right[partner][r] for r in range(10)]
            joint[0] += 1
            joint[1] -= 1
            need(certified(joint), "partner-chart adjacent pair loses the certificate")
            partner_cases += 1
            s1 = sum(joint[1:])
            if s1 < partner_min:
                partner_min = s1
    need(same_cases == 256 * 1022, "same-chart case count")
    need(partner_cases == 256 * 1022, "partner-chart case count")
    need(same_sharp, "same-chart family does not attain the d* prefix")
    need(partner_min >= 1, "partner S_1 census")

    rank8_cases = 0
    preserved = 0
    for a, b in rank8:
        fa, fb = frame[a], frame[b]
        left_images, right_images = images[fa], images[fb]
        left, right = node_delta[a], node_delta[b]
        left_rank = [dist(image, lags[fb]) for image in left_images]
        right_rank = [dist(image, lags[fa]) for image in right_images]
        i = next((i for i, rank_i in enumerate(left_rank) if rank_i == 8), None)
        j = next((j for j, rank_j in enumerate(right_rank) if rank_j == 8), None)
        need(i is not None and j is not None, "rank-8 edge has no rank-preserving chart")
        preserved += 1
        image_i = left_images[i]
        gap = dist(image_i, right_images[j])
        sample = [left[i][r] + right[j][r] for r in range(10)]
        sample[8] += 1
        sample[left_rank[i]] -= 1
        sample[right_rank[j]] -= 1
        sample[gap] += 1
        need(direct_joint(a, b, image_i, right_images[j], incident, lags, frame) == sample,
             "rank-8 correction formula drifted")
        for i in range(1022):
            image_i = left_images[i]
            rank_i = left_rank[i]
            row = left[i]
            for j in range(1022):
                gap = dist(image_i, right_images[j])
                joint = [row[r] + right[j][r] for r in range(10)]
                joint[8] += 1
                joint[rank_i] -= 1
                joint[right_rank[j]] -= 1
                joint[gap] += 1
                need(certified(joint, low_need=2, high_need=2),
                     "rank-8 chart pair is below prefix 2")
                rank8_cases += 1
    need(preserved == 8, "rank-preserving control count")
    need(rank8_cases == 8 * 1022 * 1022, "rank-8 case count")

    # One direct check each for the rank-0 formulas.
    a, b = rank0[0]
    image = images[0][0]
    partner_image = images[0][1]
    same = [node_delta[a][0][r] + node_delta[b][0][r] for r in range(10)]
    same[0] += 2
    same[1] -= 2
    need(direct_joint(a, b, image, image, incident, lags, frame) == same, "same-chart formula drifted")
    partner = [node_delta[a][0][r] + node_delta[b][1][r] for r in range(10)]
    partner[0] += 1
    partner[1] -= 1
    need(direct_joint(a, b, image, partner_image, incident, lags, frame) == partner,
         "partner formula drifted")

    print(
        "singles=188048 classes=18 same_chart=261632 partner=261632 "
        "rank8=8355872 partner_min_S1=%d same_chart_attains_dstar=yes" % partner_min
    )
    print("PASS_INDEPENDENT_CHART_PAIR_CEILING")


def direct_joint(a, b, image_a, image_b, incident, lags, frame):
    """Recompute the joint histogram from incident edges, charging the shared edge once."""
    delta = [0] * 10
    seen = set()
    for owner, image in ((a, image_a), (b, image_b)):
        for other, rank, other_frame in incident[owner]:
            key = (owner, other) if owner < other else (other, owner)
            if key in seen:
                continue
            seen.add(key)
            if other == a or other == b:
                new_rank = dist(image_a, image_b)
            else:
                new_rank = dist(image, lags[other_frame])
            delta[new_rank] += 1
            delta[rank] -= 1
    return delta


if __name__ == "__main__":
    main()
