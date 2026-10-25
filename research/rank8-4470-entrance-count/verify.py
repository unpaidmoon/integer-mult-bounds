#!/usr/bin/env python3
"""The #4470 frames have fewer monotone rank-8 slots than the u=2 cell needs.

Endpoint census only. This file does not import the joint constructor, does not
replay columns, and does not read the selected k8 word. No new kappa.
"""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-CANONICAL.json.gz"
NATIVE = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz"
PARENT = "research/fresh-helper-boundary/CHANGES.json"
PATCH = "research/joint-helper-lattice/PATCH.json"
JOIN = "research/missing-join-frame/PATCH.json"
SELECTED = "certificates/selected-result.json"
SHA = {
    CANONICAL: "6418ec3da24d548a57f5c3fe5b9062c26c9478e638504a61c387f5cfb5f4ed61",
    NATIVE: "c54b0a3e129d28e6dbf74fa731fc3bb70fe3c6705f07256750fbecddcc842d39",
    PARENT: "cde73b8ff5b3c0d06e69e2293b991b24fd14a16dd4ccab7ff6b3439074a94624",
    PATCH: "296d0e8c58cc70febe042c681ef30d6bb469818c0835fbcaac8aa8d330f5b727",
    JOIN: "9ab5328245ff02c9d0be21d39bcc375f50bc5d7909e9f7b9a3a9a6f812f5bd6e",
    SELECTED: "66974efdced4083c00025f97d95d83909a226cdf801edb9301c195c6641f6903",
}
HELPERS = {9: 326, 8: 47, 7: 7, 4: 28}
OLD_HELPERS = {9: 309, 8: 42, 7: 29, 5: 2, 4: 26}
ROOMS = {9: 326, 8: 271, 7: 7, 4: 28}
ENTRANCES = {0: 470, 1: 159, 2: 1, 5: 2}
FULL_ROOMS = {9: 470, 8: 159, 7: 1, 4: 2}
MAIN_PAIRS = {(1, 9): 112, (0, 8): 112}
MASS = 5586
IDEAL_EIGHTS = 698
KAPPA = "605457647/200000000000"


def fail(why):
    raise ValueError(why)


def need(ok, why):
    if not ok:
        fail(why)


def load_bytes(path):
    data = (ROOT / path).read_bytes()
    need(hashlib.sha256(data).hexdigest() == SHA[path], "sha256 changed for " + path)
    return data


def load_json(path):
    data = load_bytes(path)
    if path.endswith(".gz"):
        data = gzip.decompress(data)
    return json.loads(data)


def reduced(basis):
    """Unique reduced basis of an F_2^9 subspace."""
    pivots = {}
    for value in basis:
        need(type(value) is int and 0 < value < 512, "frame vector outside F2^9")
        row = value
        for bit in sorted(pivots, reverse=True):
            if row & (1 << bit):
                row ^= pivots[bit]
        if row:
            bit = row.bit_length() - 1
            for other in list(pivots):
                if pivots[other] & (1 << bit):
                    pivots[other] ^= row
            pivots[bit] = row
    return tuple(pivots[bit] for bit in sorted(pivots, reverse=True))


def independent(basis):
    row = tuple(basis)
    red = reduced(row)
    need(len(red) == len(row), "dependent frame basis")
    return red


def room_of(entrance, exit_frame):
    left = independent(entrance)
    right = independent(exit_frame)
    need(len(reduced(left + right)) == len(right), "exit does not contain entrance")
    return len(right) - len(left)


def boundaries(apply_joint):
    canonical = load_json(CANONICAL)
    frames = [independent(row) for row in canonical["frames"]]
    start = [int(index) for index in canonical["start"]]
    final = [int(index) for index in canonical["final"]]
    need(len(start) == len(final) == 632, "632 persistent fields")
    original_main = (tuple(start[:224]), tuple(final[:224]))
    parent = load_json(PARENT)
    need(set(parent) == {"entrances", "exits", "gates"}, "parent boundary file")
    need(len(parent["entrances"]) == 117 and len(parent["exits"]) == 42, "parent boundary counts")
    need(len(parent["gates"]) == 395, "parent scalar-contact count")
    for gate in parent["gates"]:
        need(len(gate) == 4 and isinstance(gate[0], str), "parent gate is not a boundary edit")
    for label, field in (("entrances", start), ("exits", final)):
        seen = set()
        for role, old, new in parent[label]:
            need(224 <= role < 632 and role not in seen, "parent helper domain")
            seen.add(role)
            need(field[role] == old and 0 <= new < len(frames), "parent boundary pin")
            field[role] = new
    if apply_joint:
        patch = load_json(PATCH)
        need(patch["source_head"] == "322e0ec764aa7ef7801383feb1f656e460dd8bed", "patch predecessor")
        seen = set()
        counts = Counter()
        for change in patch["changes"]:
            phase, ordinal = change["phase"], change["ordinal"]
            key = (phase, ordinal)
            need(key not in seen, "duplicate patch location")
            seen.add(key)
            old = independent(change["old"])
            new = independent(change["new"])
            need(old != new, "unchanged patch entry")
            counts[phase] += 1
            if phase in ("entrance", "exit"):
                need(224 <= ordinal < 632, "patch changes a non-helper boundary")
                field = start if phase == "entrance" else final
                need(reduced(frames[field[ordinal]]) == old, "patch boundary source pin")
                frames.append(new)
                field[ordinal] = len(frames) - 1
            else:
                need(phase in ("A", "B", "cleanup_tail"), "unknown patch phase")
        need(
            dict(counts) == {"A": 21, "B": 238, "cleanup_tail": 155, "entrance": 38, "exit": 47},
            "patch phase counts",
        )
    need((tuple(start[:224]), tuple(final[:224])) == original_main, "main boundaries moved")
    return frames, start, final


def census(frames, start, final):
    rooms, helpers, entrances, full_rooms, main_pairs = (
        Counter() for _ in range(5)
    )
    for register in range(632):
        entrance = frames[start[register]]
        exit_frame = frames[final[register]]
        gap = room_of(entrance, exit_frame)
        rooms[gap] += 1
        dimension = len(independent(entrance))
        entrances[dimension] += 1
        full_rooms[9 - dimension] += 1
        if register < 224:
            main_pairs[(dimension, len(independent(exit_frame)))] += 1
        else:
            helpers[gap] += 1
    return rooms, helpers, entrances, full_rooms, main_pairs


def slots_of(histogram):
    need(all(rank < 16 for rank in histogram), "a room can hold two rank-8 parts")
    return sum(count for rank, count in histogram.items() if rank >= 8)


def mass_of(histogram):
    return sum(rank * count for rank, count in histogram.items())


def center_jobs(program):
    index = 0
    jobs = 0
    while index < len(program):
        event = program[index]
        if event[0] != "center":
            index += 1
            continue
        need(index + 1 < len(program), "unpaired center event")
        second = program[index + 1]
        need(
            second[0] == "center" and event[1] == second[1] == 0 and event[3] == second[2],
            "center split does not stay on register 0",
        )
        need(sorted((event[4], second[4])) == [3, 5], "center job is not the retained 3+5 pair")
        jobs += 1
        index += 2
    return jobs


def expect_fail(action, why):
    try:
        action()
    except ValueError:
        return
    fail("negative control passed: " + why)


def join_shape():
    join = load_json(JOIN)
    need(
        set(join) == {
            "phase",
            "ordinal",
            "old_frame",
            "new_basis",
            "old_basis",
            "incoming_frames",
            "outgoing_frames",
        },
        "join patch grew a boundary field",
    )
    need((join["phase"], join["ordinal"]) == ("B", 480), "join patch is not the pinned scalar contact")
    independent(join["new_basis"])
    independent(join["old_basis"])


def main():
    join_shape()
    frames, start, final = boundaries(True)
    rooms, helpers, entrances, full_rooms, main_pairs = census(frames, start, final)
    need(dict(rooms) == ROOMS, "pinned room histogram")
    need(dict(helpers) == HELPERS, "published helper profile")
    need(sum(helpers.values()) == 408, "408 helpers")
    need(dict(entrances) == ENTRANCES, "entrance dimensions")
    need(dict(full_rooms) == FULL_ROOMS, "full-terminal room histogram")
    need(dict(main_pairs) == MAIN_PAIRS, "main endpoint pairs")
    need(mass_of(helpers) == 3471, "published helper rank mass")
    slots = slots_of(rooms)
    full_slots = slots_of(full_rooms)
    capacity = mass_of(rooms)
    full_capacity = mass_of(full_rooms)
    need(slots == 597 and full_slots == 629, "rank-8 slot counts")
    need(capacity == 5263 and full_capacity == 5517, "monotone capacities")
    need(slots < IDEAL_EIGHTS and full_slots < IDEAL_EIGHTS, "ideal cell fits")
    need(capacity < MASS and full_capacity < MASS, "mass 5586 fits")
    need(8 * IDEAL_EIGHTS + 2 == MASS, "ideal cell mass")
    need(slots != 648, "k8 slot count was reused")
    programs = load_json(NATIVE)
    need(set(programs) == {"forward", "backward"}, "both native orientations")
    jobs = {name: center_jobs(program) for name, program in programs.items()}
    need(jobs == {"forward": 8, "backward": 8}, "eight fused center jobs")
    need(slots + 8 == 605 and full_slots + 8 == 637, "center-event slot upper bound")
    need(capacity + 64 == 5327 and full_capacity + 64 == 5581, "center-event mass upper bound")
    need(605 < IDEAL_EIGHTS and 637 < IDEAL_EIGHTS, "center-event slots reach 698")
    need(5327 < MASS and 5581 < MASS, "center-event mass reaches 5586")
    old_frames, old_start, old_final = boundaries(False)
    old_rooms, old_helpers, _, _, _ = census(old_frames, old_start, old_final)
    need(dict(old_helpers) == OLD_HELPERS, "predecessor helper profile")
    need(dict(old_rooms) != ROOMS and slots_of(old_rooms) == 575, "joint patch did not move the census")
    expect_fail(lambda: independent((1, 1)), "dependent basis")
    expect_fail(lambda: room_of((1,), (2,)), "non-nested exit")
    expect_fail(lambda: center_jobs([["center", 0, 1, 2, 5]]), "unpaired center")
    selected = load_json(SELECTED)
    need(selected["kappa"] == KAPPA, "selected kappa record changed")
    print(
        "PASS_RANK8_4470_ENTRANCE_COUNT"
        " slots=597/629"
        " capacity=5263/5517"
        " with_centers=605/637/5327/5581"
        " ideal=698"
        " mass=5586"
        " helpers=4:28,7:7,8:47,9:326"
        " no_new_kappa"
    )


if __name__ == "__main__":
    main()
