#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exhaustive audit of the PR #3942 new-gap and interaction reductions.

The pinned search engine is the price oracle. This verifier does not call
bridge_census and does not replay the 11.9-million-row variable census.
"""
from __future__ import annotations

import gzip
import json
import multiprocessing
import sys
from bisect import bisect_left
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import types

P = Path(__file__).resolve().parent
PINNED = P / "pinned"
PHASES = ("A", "B", "restore")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def module(name, path):
    value = types.ModuleType(name)
    value.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), value.__dict__)
    return value


S = module("pinned_search", PINNED / "search.py")
R = S.R


def load(tag):
    return json.loads(gzip.decompress((PINNED / "inputs" / f"BORROW-WORD-43{tag}.json.gz").read_bytes()))


def touches(gate):
    return set(R.touched(gate))


def independent_frames(low, high, dimension):
    """Subset-XOR quotient bases. Does not call the pinned join/basis routine."""
    low_points = {x for x in range(512) if low >> x & 1}
    high_points = {x for x in range(512) if high >> x & 1}
    covered = set(low_points)
    representatives = []
    for vector in sorted(high_points - low_points):
        if vector not in covered:
            representatives.append(vector)
            covered.update(vector ^ x for x in low_points)
    answer = set()
    for combo in combinations(representatives, dimension - R.rank(low)):
        points = set()
        span = {0}
        for vector in combo:
            span |= {vector ^ x for x in span}
        for base in low_points:
            points.update(base ^ y for y in span)
        if len(points) == 1 << dimension:
            answer.add(sum(1 << x for x in points))
    return answer


def localized(original, section, index, pair, dimension, delta):
    return any((dimension, delta) in original.get((section, index, cut), ())
               for cut in range(pair - 1, pair + 3))


def swap_section(word, section, index, cut, vectors):
    """In-place section swap. Returns the previous gate list for restoration."""
    gates = word[section]
    gate = deepcopy(gates[index])
    crossed = gates[index + 1:cut] if cut > index else gates[cut:index]
    require(all(R.crosses(gate, other) for other in crossed), "noncommuting barrier")
    coefficient = Fraction(gate[3], gate[4])
    for other in crossed:
        if other[0] == "scale" and other[1] in R.touched(gate):
            power = (1 if other[1] == gate[1] else -1) * (1 if cut > index else -1)
            coefficient *= Fraction(other[2], other[3]) ** power
    gate[3:5] = [coefficient.numerator, coefficient.denominator]
    gate[-1] = list(R.basis(R.span(tuple(vectors))))
    updated = gates.copy()
    updated.pop(index)
    updated.insert(cut - (cut > index), gate)
    word[section] = updated
    return gates


def frame_sequences(gates):
    sequences = {}
    for gate in gates:
        frame = (gate[0], tuple(gate[-1]))
        for register in R.touched(gate):
            sequences.setdefault(register, []).append(frame)
    return sequences


def original_prices(word):
    prices = {}
    for section in PHASES:
        adds = [i for i, gate in enumerate(word[section]) if gate[0] == "add"]
        for index, cut, dimension, _low, _high, delta in S.candidates(word, section, adds):
            prices.setdefault((section, index, cut), set()).add((dimension, delta))
    return prices


def segment_bounds(word):
    """Entry and exit frames. A later adjacent swap does not change them."""
    nodes, where, _bill = R.tracing(word)
    info = {}
    corridors = {}
    for section in PHASES:
        gates = word[section]
        for lo, hi in R.segments(word, section):
            occurrences = {}
            for index in range(lo, hi):
                for register in R.touched(gates[index]):
                    occurrences.setdefault(register, []).append(index)
            entries, exits = {}, {}
            for register, indices in occurrences.items():
                entries[register] = nodes[register][where[((section, indices[0]), register)]][2]
                exits[register] = nodes[register][where[((section, indices[-1]), register)] + 1][3]
            info[(section, lo)] = (hi, entries, exits)
            rows = []
            for index in range(lo, hi):
                if gates[index][0] != "add":
                    continue
                rows.append((index, *corridor(gates, index, lo, hi)))
            corridors[(section, lo)] = rows
    return info, corridors


def corridor(gates, index, lo, hi):
    lower = index
    while lower > lo and R.crosses(gates[index], gates[lower - 1]):
        lower -= 1
    upper = index + 1
    while upper < hi and R.crosses(gates[index], gates[upper]):
        upper += 1
    return lower, upper


def gap_rows(gates, section, pair, bounds, corridors):
    """Prices at the single new gap, using gate frames rather than a fresh trace."""
    lo = next(lo for lo, hi in R.segments(S_WORD, section) if lo <= pair < hi)
    hi, entries, exits = bounds[(section, lo)]
    occurrences = {}
    for index in range(lo, hi):
        for register in R.touched(gates[index]):
            occurrences.setdefault(register, []).append(index)
    rows = []
    for index, lower0, upper0 in corridors[(section, lo)]:
        if index in (pair, pair + 1) or upper0 < pair or lower0 > pair + 2:
            continue
        lower, upper = corridor(gates, index, lo, hi)
        cut = pair + 1
        if not (lower <= cut <= upper) or cut == index + 1:
            continue
        base = [0] * 10
        frame = R.span(tuple(gates[index][-1]))
        frame_rank = R.rank(frame)
        for register in R.touched(gates[index]):
            indices = occurrences[register]
            position = indices.index(index)
            before = R.span(tuple(gates[indices[position - 1]][-1])) if position else entries[register]
            after = (R.span(tuple(gates[indices[position + 1]][-1]))
                     if position + 1 < len(indices) else exits[register])
            before_rank, after_rank = R.rank(before), R.rank(after)
            base[frame_rank - before_rank] -= 1
            base[after_rank - frame_rank] -= 1
            base[after_rank - before_rank] += 1
        ranked = []
        masks = []
        for register in R.touched(gates[index]):
            indices = [value for value in occurrences[register] if value != index]
            position = bisect_left(indices, cut)
            before = R.span(tuple(gates[indices[position - 1]][-1])) if position else entries[register]
            after = (R.span(tuple(gates[indices[position]][-1]))
                     if position < len(indices) else exits[register])
            ranked.append((R.rank(before), R.rank(after)))
            masks.append((before, after))
        low = R.join(masks[0][0], masks[1][0])
        high = masks[0][1] & masks[1][1]
        if not R.contained(low, high):
            continue
        for dimension in range(R.rank(low), R.rank(high) + 1):
            delta = base.copy()
            for before_rank, after_rank in ranked:
                delta[after_rank - before_rank] -= 1
                delta[dimension - before_rank] += 1
                delta[after_rank - dimension] += 1
            delta[0] = 0
            require(sum(rank * count for rank, count in enumerate(delta)) == 0, "rank mass drift")
            rows.append((index, dimension, tuple(delta)))
    return rows


# Segment lookup uses the loaded provider. Workers set this before pricing.
S_WORD = None


def audit_pairs(word, pairs, original, bounds, corridors):
    global S_WORD
    S_WORD = word
    bridge = nonbridge = negative = 0
    failures = []
    for (section, pair), (index, cut, frame) in pairs:
        saved = swap_section(word, section, index, cut, R.basis(frame))
        try:
            left, right = touches(saved[pair]), touches(saved[pair + 1])
            for position, dimension, delta in gap_rows(word[section], section, pair, bounds, corridors):
                used = touches(word[section][position])
                if used & left and used & right:
                    bridge += 1
                    if not R.all_power_nonnegative(delta):
                        negative += 1
                        failures.append(("negative-bridge", section, pair, position, dimension))
                else:
                    nonbridge += 1
                    if not localized(original, section, position, pair, dimension, delta):
                        failures.append(("unlocalized", section, pair, position, dimension, list(delta)))
        finally:
            word[section] = saved
        if len(failures) > 8:
            break
    return {"bridge": bridge, "nonbridge": nonbridge, "negative": negative, "failures": failures}


def oracle_sample(word, fixed):
    """Evenly spaced pairs, plus pairs that sit on a segment edge or beside a non-ADD."""
    items = list(fixed.items())
    step = max(1, len(items) // 24)
    chosen = items[::step][:24]
    seen = set(chosen)
    edge = []
    for key, spec in items:
        section, pair = key
        gates = word[section]
        bounds = [hi for lo, hi in R.segments(word, section) if lo <= pair < hi]
        lo = next(lo for lo, hi in R.segments(word, section) if lo <= pair < hi)
        hi = bounds[0]
        window = range(max(lo, pair - 3), min(hi, pair + 5))
        if pair - lo <= 2 or hi - (pair + 2) <= 2 or any(gates[i][0] != "add" for i in window):
            edge.append((key, spec))
    estep = max(1, len(edge) // 24) if edge else 1
    for item in edge[::estep][:24]:
        if item not in seen:
            chosen.append(item)
            seen.add(item)
    return chosen


def agree_with_oracle(word, fixed, bounds, corridors):
    """The trace-free gap pricer matches candidates() on the pinned sample."""
    global S_WORD
    S_WORD = word
    checked = 0
    for (section, pair), (index, cut, frame) in oracle_sample(word, fixed):
        saved = swap_section(word, section, index, cut, R.basis(frame))
        try:
            third = [position for position, gate in enumerate(word[section])
                     if gate[0] == "add" and position not in (pair, pair + 1)]
            slow = sorted((position, dimension, delta) for position, _cut, dimension, _low, _high, delta
                          in S.candidates(word, section, third, window=(pair + 1, pair + 1)))
            fast = sorted(gap_rows(word[section], section, pair, bounds, corridors))
            require(slow == fast, "trace-free gap pricer drifted at " + section + " " + str(pair))
        finally:
            word[section] = saved
        checked += 1
    return checked


def others_before(cut, index):
    """How many gates other than the moved ADD sit strictly before this cut."""
    return cut if cut <= index else cut - 1


def placement_prices(word, section, index):
    found = {}
    for _index, cut, dimension, _low, _high, delta in S.candidates(word, section, [index]):
        found.setdefault((others_before(cut, index), dimension), set()).add(delta)
    return found


def audit_variable(word, variable):
    """Disjoint frame sequences are invariant. Same-ADD composition matches a direct move."""
    sequence_changes = composed = options = 0
    failures = []
    for section, index, cut, frame, first_delta, _kind in variable:
        before = frame_sequences(word[section])
        direct = placement_prices(word, section, index)
        moved_registers = touches(word[section][index])
        saved = swap_section(word, section, index, cut, R.basis(frame))
        try:
            after = frame_sequences(word[section])
            for register, sequence in before.items():
                if register in moved_registers:
                    continue
                if after.get(register, []) != sequence:
                    failures.append(("disjoint-sequence", section, index, register))
                    break
            changed = any(after.get(register) != before.get(register) for register in moved_registers)
            if not changed:
                failures.append(("frame-sequence-unchanged", section, index, cut))
            else:
                sequence_changes += 1
            moved = cut - (cut > index)
            second = placement_prices(word, section, moved)
            bad = False
            for key, deltas in second.items():
                for delta in deltas:
                    options += 1
                    total = tuple(a + b for a, b in zip(first_delta, delta))
                    if total not in direct.get(key, ()):
                        failures.append(("composition", section, index, cut, key[0], key[1]))
                        bad = True
                        break
                if bad:
                    break
            if not bad:
                composed += 1
        finally:
            word[section] = saved
        if len(failures) > 8:
            break
    return {"sequence_changes": sequence_changes, "composed": composed,
            "composition_options": options, "failures": failures}


def audit_lattices(intervals):
    checked = 0
    max_quotient = 0
    for low, high, dimension in intervals:
        quotient = R.rank(high) - R.rank(low)
        max_quotient = max(max_quotient, quotient)
        require(quotient <= 3, "PROOF.md §4 quotient bound failed")
        require(set(S.frames(low, high, dimension)) == independent_frames(low, high, dimension),
                "first-frame lattice mismatch")
        checked += 1
    return {"intervals": checked, "max_quotient": max_quotient}


def controls():
    counts = Counter()
    low, high = 1, R.span((1, 2, 4))
    require([len(independent_frames(low, high, dimension)) for dimension in range(4)] == [1, 7, 7, 1],
            "F2^3 lattice")
    counts["known_lattice"] += 1
    require(not R.all_power_nonnegative((0, 1, -2, 1, 0, 0, 0, 0, 0, 0)), "profitable profile accepted")
    counts["profitable_rejected"] += 1
    try:
        S.frames(1, R.span((1, 2, 4, 8, 16)), 1)
    except ValueError:
        counts["resource_guard"] += 1
    else:
        raise ValueError("quotient resource guard accepted a rank-5 interval")
    empty = {}
    require(not localized(empty, "A", 3, 10, 2, (0, 1)), "empty price map localized")
    present = {("A", 3, 12): {(2, (0, 1))}}
    require(localized(present, "A", 3, 10, 2, (0, 1)), "window price missed")
    require(not localized(present, "A", 3, 9, 2, (0, 1)), "outside window localized")
    counts["localisation_predicate"] += 3
    return dict(counts)


_STATE = {}


def _init(word, original, bounds, corridors):
    _STATE["word"] = word
    _STATE["original"] = original
    _STATE["bounds"] = bounds
    _STATE["corridors"] = corridors


def _pairs(chunk):
    return audit_pairs(_STATE["word"], chunk, _STATE["original"], _STATE["bounds"], _STATE["corridors"])


def _moves(chunk):
    return audit_variable(_STATE["word"], chunk)


def chunks(items, count):
    buckets = [[] for _ in range(count)]
    for index, item in enumerate(items):
        buckets[index % count].append(item)
    return [bucket for bucket in buckets if bucket]


def audit_provider(tag, workers):
    word = load(tag)
    fixed, variable, _counts, intervals = S.first_moves(word)
    lattices = audit_lattices(intervals)
    prices = original_prices(word)
    bounds, corridors = segment_bounds(word)
    oracle_pairs = agree_with_oracle(word, fixed, bounds, corridors)
    workers = min(workers, len(fixed), len(variable))
    context = multiprocessing.get_context("fork")
    with context.Pool(workers, initializer=_init, initargs=(word, prices, bounds, corridors)) as pool:
        pair_rows = pool.map(_pairs, chunks(list(fixed.items()), workers))
        move_rows = pool.map(_moves, chunks(variable, workers))
    pair = Counter()
    move = Counter()
    failures = []
    for row in pair_rows:
        pair["bridge"] += row["bridge"]
        pair["nonbridge"] += row["nonbridge"]
        pair["negative"] += row["negative"]
        failures.extend(row["failures"])
    for row in move_rows:
        move["sequence_changes"] += row["sequence_changes"]
        move["composed"] += row["composed"]
        move["composition_options"] += row["composition_options"]
        failures.extend(row["failures"])
    require(not failures, "reduction failure: " + json.dumps(failures[:4]))
    require(pair["negative"] == 0, "negative bridge price")
    require(move["sequence_changes"] == len(variable), "a changed frame left its registers")
    require(move["composed"] == len(variable), "same-ADD composition drifted")
    require(lattices["max_quotient"] <= 3, "quotient above the stated bound")
    return {
        "provider": tag,
        "fixed_pairs": len(fixed),
        "variable_moves": len(variable),
        "bridge_prices": pair["bridge"],
        "nonbridge_prices": pair["nonbridge"],
        "composed_moves": move["composed"],
        "composition_options": move["composition_options"],
        "intervals": lattices["intervals"],
        "max_quotient": lattices["max_quotient"],
        "oracle_pairs": oracle_pairs,
    }


def main():
    tags = sys.argv[1:] or ["base", "extra"]
    require(tags and set(tags) <= {"base", "extra"}, "provider must be base and/or extra")
    predicate = controls()
    workers = min(4, multiprocessing.cpu_count() or 1)
    rows = [audit_provider(tag, workers) for tag in tags]
    expected_path = P / "EXPECTED.json"
    payload = {"providers": rows, "controls": predicate}
    if not expected_path.exists():
        print(json.dumps(payload, sort_keys=True))
        raise SystemExit("EXPECTED.json missing; inspect stdout and pin it")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    pinned = [row for row in expected["providers"] if row["provider"] in tags]
    require(rows == pinned, "provider receipt drifted: " + json.dumps(rows))
    require(predicate == expected["controls"], "control receipt drifted: " + json.dumps(predicate))
    print(json.dumps({
        "status": "PASS_STAGED544_NEW_GAP_AUDIT",
        "providers": rows,
        "controls": predicate,
        "new_kappa": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
