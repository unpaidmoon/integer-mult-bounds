#!/usr/bin/env python3
"""Every unequal T1 endpoint pair has a monotone (6,6,6,7,7,7) chain.

The written argument is PROOF.md. This program rechecks the two endpoint
domains, searches one representative of each symmetry class, and checks the
transported floor word at every unequal endpoint pair. It does not call a
SAT solver and it does not change the selected frontier.
"""

import itertools
import json
from collections import deque
from pathlib import Path

K = 6
LENGTH = 36
TARGET = (6, 6, 6, 7, 7, 7)
ROOT = Path(__file__).resolve().parents[2]

# Orbit sizes of unequal pairs (intersection, D in M_4, D in M_18).
ORBIT_COUNTS = {
    (0, False, True): 60,
    (0, True, False): 60,
    (1, False, False): 180,
    (1, False, True): 360,
    (1, True, False): 360,
    (1, True, True): 180,
    (2, False, False): 360,
    (2, False, True): 180,
    (2, True, False): 180,
    (2, True, True): 360,
}

MOVING_WORD = "012340011223344555014555443322110023"


def fail(message):
    raise SystemExit("FAIL: " + message)


def digits(word):
    return [int(character) for character in word]


def prefixes(word):
    counts = [0] * K
    table = [tuple(counts)]
    for source in word:
        counts[source] += 1
        table.append(tuple(counts))
    return table


def diagonal(table, index):
    early = table[index]
    late = table[39 - index]
    return tuple(early[j] + late[j] for j in range(K))


def mask_of(sum_vec):
    return tuple(source for source, value in enumerate(sum_vec) if value == 7)


def is_target_multiset(sum_vec):
    return tuple(sorted(sum_vec)) == TARGET


def keeps_multiset(word):
    if len(word) != LENGTH:
        return False
    table = prefixes(word)
    if table[LENGTH] != (6, 6, 6, 6, 6, 6):
        return False
    return all(is_target_multiset(diagonal(table, index)) for index in range(4, 19))


def budgets(mask4, deficit, mask18):
    """Early and late letter budgets forced by Lemmas 1 and 2."""
    start = set(mask4)
    finish = set(mask18)
    if deficit not in start:
        prefix = tuple(1 if source in start or source == deficit else 0 for source in range(K))
    else:
        prefix = tuple(
            2 if source == deficit else 1 if source in start else 0 for source in range(K)
        )
    early = tuple(3 - prefix[source] for source in range(K))
    late = tuple(
        3 - (1 if source == deficit else 0) - (1 if source in finish else 0)
        for source in range(K)
    )
    return prefix, early, late


def search_path(mask4, deficit, mask18):
    """Breadth-first path in the finite budget graph, or None."""
    _prefix, early0, late0 = budgets(mask4, deficit, mask18)
    start_mask = 0
    for source in mask4:
        start_mask |= 1 << source
    goal = 0
    for source in mask18:
        goal |= 1 << source

    def pack(early, late, mask):
        packed = mask
        for value in early:
            packed = packed * 4 + value
        for value in late:
            packed = packed * 4 + value
        return packed

    start = (early0, late0, start_mask)
    start_key = pack(*start)
    seen = {start_key}
    queue = deque([start])
    parent = {}
    while queue:
        early, late, mask = queue.popleft()
        packed = pack(early, late, mask)
        for early_letter in range(K):
            if early[early_letter] == 0:
                continue
            for late_letter in range(K):
                if late[late_letter] == 0:
                    continue
                if early_letter == late_letter:
                    next_mask = mask
                else:
                    enters = (mask >> early_letter) & 1
                    leaves = (mask >> late_letter) & 1
                    if enters or not leaves:
                        continue
                    next_mask = mask ^ (1 << early_letter) ^ (1 << late_letter)
                next_early = (
                    early[:early_letter]
                    + (early[early_letter] - 1,)
                    + early[early_letter + 1 :]
                )
                next_late = (
                    late[:late_letter]
                    + (late[late_letter] - 1,)
                    + late[late_letter + 1 :]
                )
                key = pack(next_early, next_late, next_mask)
                if key in seen:
                    continue
                seen.add(key)
                parent[key] = (packed, early_letter, late_letter)
                if next_mask == goal and not any(next_early) and not any(next_late):
                    path = []
                    cursor = key
                    while cursor != start_key:
                        previous, early_letter, late_letter = parent[cursor]
                        path.append((early_letter, late_letter))
                        cursor = previous
                    path.reverse()
                    return path
                queue.append((next_early, next_late, next_mask))
    return None


def assemble(mask4, deficit, mask18, path):
    start = set(mask4)
    if deficit not in start:
        prefix = sorted(list(start) + [deficit])
    else:
        others = sorted(source for source in start if source != deficit)
        prefix = [deficit, deficit, others[0], others[1]]
    early = [early_letter for early_letter, _late_letter in path]
    late = [late_letter for _early_letter, late_letter in reversed(path)]
    return prefix + early + list(mask18) + late + [deficit]


def regions(mask4, deficit, mask18):
    start = set(mask4)
    finish = set(mask18)
    return {
        "both": start & finish,
        "only_start": start - finish,
        "only_finish": finish - start,
        "neither": set(range(K)) - start - finish,
        "deficit": deficit,
    }


def source_map(source_regions, target_regions):
    """Bijection of sources carrying one endpoint triple onto another."""
    image = [None] * K
    for name in ("both", "only_start", "only_finish", "neither"):
        left = sorted(source_regions[name])
        right = sorted(target_regions[name])
        if len(left) != len(right):
            return None
        if source_regions["deficit"] in left:
            left = [source_regions["deficit"]] + [
                source for source in left if source != source_regions["deficit"]
            ]
            right = [target_regions["deficit"]] + [
                source for source in right if source != target_regions["deficit"]
            ]
        for origin, destination in zip(left, right):
            image[origin] = destination
    if any(source is None for source in image) or len(set(image)) != K:
        return None
    return image


def endpoint_census():
    """Recheck the finite domains of the two endpoint lemmas."""
    rows = []
    for early in range(7):
        for bridge in range(4):
            if early + bridge <= 6 and (2 * early + bridge) in (6, 7):
                rows.append((early, bridge, 2 * early + bridge))
    if rows != [(2, 2, 6), (2, 3, 7), (3, 0, 6), (3, 1, 7)]:
        fail(f"s=18 row table changed: {rows}")
    splits18 = 0
    for choice in itertools.product(rows, repeat=K):
        if sum(row[0] for row in choice) != 18:
            continue
        if sum(row[1] for row in choice) != 3:
            continue
        summed = tuple(row[2] for row in choice)
        if not is_target_multiset(summed):
            continue
        splits18 += 1
        pairs = sorted(row[:2] for row in choice)
        if pairs != [(3, 0), (3, 0), (3, 0), (3, 1), (3, 1), (3, 1)]:
            fail(f"unexpected s=18 split: {choice}")
    if splits18 != 20:
        fail(f"s=18 split count changed: {splits18}")

    type_a = 0
    type_b = 0
    other = 0
    domain4 = 0
    for early in itertools.product(range(7), repeat=K):
        if sum(early) != 4:
            continue
        for deficit in range(K):
            domain4 += 1
            summed = tuple(
                early[source] + (5 if source == deficit else 6) for source in range(K)
            )
            if not is_target_multiset(summed):
                continue
            mask = set(mask_of(summed))
            if deficit not in mask and all(
                early[source] == (1 if source in mask or source == deficit else 0)
                for source in range(K)
            ):
                type_a += 1
            elif deficit in mask and all(
                early[source]
                == (2 if source == deficit else 1 if source in mask else 0)
                for source in range(K)
            ):
                type_b += 1
            else:
                other += 1
    if (domain4, type_a, type_b, other) != (756, 60, 60, 0):
        fail(
            "s=4 split census changed: "
            f"domain={domain4} A={type_a} B={type_b} other={other}"
        )
    return 2


def unequal_pairs():
    pairs = []
    for start in itertools.combinations(range(K), 3):
        for finish in itertools.combinations(range(K), 3):
            if start == finish:
                continue
            for deficit in range(K):
                key = (
                    len(set(start) & set(finish)),
                    deficit in start,
                    deficit in finish,
                )
                pairs.append((key, start, deficit, finish))
    return pairs


def main():
    controls = 0
    selected = json.loads((ROOT / "certificates/selected-result.json").read_text())
    if selected.get("kappa") != "781451/250000000":
        fail(f"selected kappa moved: {selected.get('kappa')}")
    controls += 1

    controls += endpoint_census()

    moving = digits(MOVING_WORD)
    if not keeps_multiset(moving):
        fail("recorded moving word lost the multiset")
    moving_table = prefixes(moving)
    if mask_of(diagonal(moving_table, 4)) != (0, 1, 2):
        fail("recorded moving word lost its s=4 mask")
    if mask_of(diagonal(moving_table, 18)) != (0, 1, 4):
        fail("recorded moving word lost its s=18 mask")
    controls += 1

    broken = list(moving)
    broken[4], broken[5] = broken[5], broken[4]
    if keeps_multiset(broken):
        fail("swapped moving-word letters still kept the multiset")
    controls += 1

    pairs = unequal_pairs()
    if len(pairs) != 2280:
        fail(f"unequal pair count changed: {len(pairs)}")
    by_orbit = {}
    for key, start, deficit, finish in pairs:
        by_orbit.setdefault(key, []).append((start, deficit, finish))
    if set(by_orbit) != set(ORBIT_COUNTS):
        fail(f"orbit keys changed: {sorted(by_orbit)}")
    for key, expected in ORBIT_COUNTS.items():
        if len(by_orbit[key]) != expected:
            fail(f"orbit {key} has {len(by_orbit[key])} pairs, expected {expected}")
    if sum(ORBIT_COUNTS.values()) != 2280:
        fail("orbit sizes do not add to 2280")
    controls += 1

    checked = 0
    for key in sorted(by_orbit):
        start, deficit, finish = by_orbit[key][0]
        prefix, early, late = budgets(start, deficit, finish)
        if any(value < 0 for value in early + late) or sum(early) != 14 or sum(late) != 14:
            fail(f"budgets failed on the representative of {key}")
        if sum(prefix) != 4:
            fail(f"prefix sum moved on the representative of {key}")
        path = search_path(start, deficit, finish)
        if path is None or len(path) != 14:
            fail(f"no 14-step path for orbit {key}")
        if sorted(letter for letter, _late in path) != sorted(
            source for source, count in enumerate(early) for _ in range(count)
        ):
            fail(f"early letters missed the budget in orbit {key}")
        if sorted(letter for _early, letter in path) != sorted(
            source for source, count in enumerate(late) for _ in range(count)
        ):
            fail(f"late letters missed the budget in orbit {key}")
        representative = assemble(start, deficit, finish, path)
        if not keeps_multiset(representative):
            fail(f"representative word missed the multiset in orbit {key}")
        table = prefixes(representative)
        if table[18] != (3, 3, 3, 3, 3, 3):
            fail(f"q_18 left 3 in orbit {key}")
        if mask_of(diagonal(table, 4)) != start or mask_of(diagonal(table, 18)) != finish:
            fail(f"endpoint masks moved in orbit {key}")
        source_regions = regions(start, deficit, finish)
        for target_start, target_deficit, target_finish in by_orbit[key]:
            image = source_map(source_regions, regions(target_start, target_deficit, target_finish))
            if image is None:
                fail(f"no source bijection in orbit {key}")
            word = [image[source] for source in representative]
            if not keeps_multiset(word):
                fail(
                    "transported word missed the multiset: "
                    f"{key} {target_start} {target_deficit} {target_finish}"
                )
            transported = prefixes(word)
            if mask_of(diagonal(transported, 4)) != target_start:
                fail(f"transported s=4 mask changed in orbit {key}")
            if mask_of(diagonal(transported, 18)) != target_finish:
                fail(f"transported s=18 mask changed in orbit {key}")
            if transported[18] != (3, 3, 3, 3, 3, 3):
                fail(f"transported q_18 left 3 in orbit {key}")
            checked += 1
    if checked != 2280:
        fail(f"checked {checked} pairs, expected 2280")
    controls += 1

    print(
        "PASS_C6_T1_UNEQUAL_MASK_CHAINS "
        f"pairs=2280 orbits=10 witnesses=10 checked={checked} controls={controls}"
    )


if __name__ == "__main__":
    main()
