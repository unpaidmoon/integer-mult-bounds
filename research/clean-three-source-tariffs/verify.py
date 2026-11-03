#!/usr/bin/env python3
"""Bounded independent corroboration, produced by Nick Petalas. Apache-2.0."""

from fractions import Fraction
from hashlib import sha256
from heapq import heappop, heappush
from itertools import product
import json
from pathlib import Path
import sys

from connector import choose_word, frontier, optimum, profile, require

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def authenticate():
    manifest = json.loads((PACKAGE / "SOURCES.json").read_text())
    result = {}
    for row in manifest["files"]:
        if row["usage"] == "input":
            path = ROOT / row["path"]
            digest = sha256(path.read_bytes()).hexdigest()
            require(digest == row["sha256"], "changed predecessor input: " + row["path"])
            result[row["path"]] = digest
    for path in sorted(PACKAGE.iterdir()):
        if path.is_file():
            result[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    return result


def read_lengths(visited):
    """Independent subset-XOR oracle; at most 128 subsets of seven vertices."""
    vertices = tuple(m for m in range(1, 8) if visited & (1 << m))
    lengths = [99] * 8
    lengths[0] = 0
    for subset in range(1 << len(vertices)):
        value = 0
        for index, vertex in enumerate(vertices):
            if subset & (1 << index):
                value ^= vertex
        lengths[value] = min(lengths[value], subset.bit_count())
    return tuple(lengths[1:])


def source_oracle(b):
    """All finite source walks via 1024 lifted states, without a word cutoff."""
    distances = {(0, 1): 0}
    heap = [(0, 0, 1)]
    # At most 1024 settled states, three outgoing edges each, and one seed.
    for _ in range(3074):
        if not heap:
            break
        cost, vertex, visited = heappop(heap)
        if distances[(vertex, visited)] != cost:
            continue
        for axis in range(3):
            target = vertex ^ (1 << axis)
            seen = visited | (1 << target)
            key = (target, seen)
            new_cost = cost + b[axis]
            if key not in distances or new_cost < distances[key]:
                distances[key] = new_cost
                heappush(heap, (new_cost, target, seen))
    require(not heap, "source-state bound exhausted")
    require(len(distances) <= 1024, "source-state capacity")
    return tuple((seen, cost) for (vertex, seen), cost in distances.items() if vertex == 0)


def enumerate_words(lengths):
    candidates = set()
    examined = restored = 0
    for length in range(9):
        for steps in product(range(3), repeat=length):
            examined += 1
            counts = tuple(steps.count(j) for j in range(3))
            if any(c == 0 or c % 2 for c in counts):
                continue
            restored += 1
            current, seen = 0, 1
            for axis in steps:
                current ^= 1 << axis
                seen |= 1 << current
            require(current == 0, "enumeration restoration invariant")
            candidates.add(counts + lengths[seen])
    minimal = {v for v in candidates if not any(
        other != v and all(x <= y for x, y in zip(other, v)) for other in candidates)}
    expected = {profile(word) for word in frontier()}
    require(minimal == expected, "independent finite Pareto mismatch")
    require(examined == 9841 and restored == 1350, "word enumeration coverage")
    return {"source_words": examined, "restored_spanning_words": restored,
            "distinct_minimum_read_profiles": len(candidates), "pareto_profiles": len(minimal)}


def tariff_checks(lengths):
    checked = 0
    for b in product((1, 3, 11), repeat=3):
        states = source_oracle(b)
        usable = tuple((cost, lengths[seen]) for seen, cost in states
                       if max(lengths[seen]) < 99)
        for a in product((1, 4), repeat=7):
            independent = min(cost + sum(x * y for x, y in zip(reads, a))
                              for cost, reads in usable)
            require(independent == optimum(b, a), "heterogeneous tariff mismatch")
            checked += 1
    for index in range(24):
        b = tuple(Fraction(1 + (index + j) % 7, 2 + j) for j in range(3))
        a = tuple(Fraction(1 + (index * (j + 1)) % 13, 2 + j) for j in range(7))
        independent = min(cost + sum(x * y for x, y in zip(lengths[seen], a))
                          for seen, cost in source_oracle(b) if max(lengths[seen]) < 99)
        chosen = profile(choose_word(b, a))
        require(independent == optimum(b, a) == sum(x * y for x, y in zip(chosen, b + a)),
                "rational tariff or selected schedule mismatch")
        checked += 1
    return checked


def exposed_profiles():
    count = 0
    for word in frontier():
        vector = profile(word)
        if sum(vector[:3]) == 6:
            b = (10, 10, 10)
            a = tuple(1 if value == 2 else 4 for value in vector[3:])
        else:
            b = tuple(1 if value == 4 else 2 for value in vector[:3])
            a = (4,) * 7
        values = [(sum(x * y for x, y in zip(profile(w), b + a)), profile(w))
                  for w in frontier()]
        best = min(value for value, _ in values)
        winners = [v for value, v in values if value == best]
        require(winners == [vector], "frontier profile not positively exposed")
        require(best == optimum(b, a), "exposed price formula")
        count += 1
    return count


def apply_matrix(rows, value):
    return sum(((row & value).bit_count() % 2) << j for j, row in enumerate(rows))


def execute(word, sources, targets, dirty, fresh, b_maps, a_maps):
    helper = fresh
    result = list(targets)
    for op, index in word:
        if op == "INIT":
            helper = 0  # An explicitly paid zeroing pass, not borrowed zero data.
        elif op == "B":
            helper ^= apply_matrix(b_maps[index], sources[index])
        elif op == "A":
            result[index - 1] ^= apply_matrix(a_maps[index - 1], helper)
        elif op == "RELEASE":
            require(helper == 0, "rectangular-map helper restoration")
        else:
            raise ValueError("unknown execution operation")
    return sources, tuple(result), dirty, helper


def matrix_cases():
    count = 0
    # Sources/output rows have width two; the owned and unused dirty row have width three.
    widths = (2,) * 10 + (3, 3)
    states = [0] + [1 << bit for bit in range(26)]
    states += [((index + 1) * 1234567) % (1 << 26) for index in range(16)]
    for seed in range(16):
        b_maps = tuple(tuple((seed * 7 + j * 3 + k) % 4 for k in range(3))
                       for j in range(3))
        a_maps = tuple(tuple((seed * 5 + m * 3 + k * 2) % 8 for k in range(2))
                       for m in range(7))
        for state in states:
            fields = []
            for width in widths:
                fields.append(state & ((1 << width) - 1))
                state >>= width
            sources, targets = tuple(fields[:3]), tuple(fields[3:10])
            expected = []
            for mask in range(1, 8):
                accumulated = 0
                for j in range(3):
                    if mask & (1 << j):
                        accumulated ^= apply_matrix(b_maps[j], sources[j])
                expected.append(targets[mask - 1] ^ apply_matrix(a_maps[mask - 1], accumulated))
            for word in frontier():
                actual = execute(word, sources, targets, fields[10], fields[11], b_maps, a_maps)
                require(actual == (sources, tuple(expected), fields[10], 0),
                        "arbitrary dirty rectangular-map endpoint")
                count += 1
    return count


def controls():
    count = 0
    invalid_prices = [((0, 1, 1), (1,) * 7), ((-1, 1, 1), (1,) * 7),
                      ((True, 1, 1), (1,) * 7), ((1.0, 1, 1), (1,) * 7),
                      ((1, 1), (1,) * 7), ((1, 1, 1), (1,) * 6),
                      ((1, 1, 1), (1,) * 6 + (0,))]
    for b, a in invalid_prices:
        try:
            optimum(b, a)
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid tariff accepted")
    for word in frontier():
        first_b = next(i for i, action in enumerate(word) if action[0] == "B")
        first_a = next(i for i, action in enumerate(word) if action[0] == "A")
        mutants = (word[1:], word[:-1], word[:first_b] + word[first_b + 1:],
                   word[:first_a] + word[first_a + 1:],
                   word[:1] + (("INIT", 0),) + word[1:],
                   word[:1] + (("B", 3),) + word[1:],
                   word[:1] + (("A", 0),) + word[1:])
        for mutant in mutants:
            try:
                profile(mutant)
            except ValueError:
                count += 1
            else:
                raise ValueError("malformed or semantically false word accepted")
    return count


def main():
    files = authenticate()
    lengths = {seen: read_lengths(seen) for seen in range(1, 256, 2)}
    counts = enumerate_words(lengths)
    counts["visited_sets"] = len(lengths)
    counts["heterogeneous_tariffs"] = tariff_checks(lengths)
    counts["positively_exposed_profiles"] = exposed_profiles()
    counts["rectangular_dirty_cases"] = matrix_cases()
    counts["rejecting_controls"] = controls()
    receipt = {"status": "PASS_CLEAN_THREE_SOURCE_ALL_TARIFFS", "counts": counts,
               "claim_type": "scoped proof with finite corroboration",
               "python": sys.version.split()[0], "sha256": files}
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
