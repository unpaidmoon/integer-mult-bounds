#!/usr/bin/env python3
"""A line-born family cannot gain a second unpaid coordinate by erasure.

Unpaid dimension is the surviving birth space: the intersection of every frame
in the history. For a one-dimensional birth that dimension is at most 1, nested
or not. Rewriting an erased direction is paid by the transition rank
dim(A+B) - dim(A∩B), which agrees with the nested Fourier-rank rule when the
frames are nested.

The explicit three-frame erasure on F_2^73 is the schedule named by the open
question in research/three-bank-restored-unpaid. No new kappa.
"""

import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
MARKER = (
    "PASS_COVERAGE_BIRTH_ERASURE line_unpaid_at_most_1=true "
    "erasure_creates_second_unpaid=false no_new_kappa"
)
M_SELECTED = 73


def fail(message):
    raise SystemExit("FAIL_COVERAGE_BIRTH_ERASURE " + message)


def require(condition, message):
    if not condition:
        fail(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def authenticate():
    sources = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    pinned = {row["path"]: row for row in sources["files"] if row["usage"] == "input"}
    expected = {
        "research/split-centres-global/proofs/INHERITED-COMPLEX-GEOMETRY.txt",
        "research/three-bank-restored-unpaid/README.md",
    }
    require(set(pinned) == expected, "input inventory changed")
    for path, row in pinned.items():
        require(sha256(ROOT / path) == row["sha256"], "input drift " + path)
    geometry = " ".join(
        (ROOT / "research/split-centres-global/proofs/INHERITED-COMPLEX-GEOMETRY.txt")
        .read_text(encoding="utf-8")
        .split()
    )
    predecessor = " ".join(
        (ROOT / "research/three-bank-restored-unpaid/README.md").read_text(encoding="utf-8").split()
    )
    require(
        "a nested transition has Fourier rank equal to the dimension difference" in geometry,
        "nested rank rule moved",
    )
    require("The construction below has m=73" in geometry, "selected width moved")
    require(
        "Can a non-nested three-bank schedule, one that erases an initial direction "
        "and rewrites it, leave two unpaid coordinates without becoming a plane port?"
        in predecessor,
        "erasure question moved",
    )


def rref(rows, width):
    active = [row for row in rows if row]
    rank = 0
    pivots = []
    for bit in range(width):
        pivot = next((i for i in range(rank, len(active)) if (active[i] >> bit) & 1), None)
        if pivot is None:
            continue
        active[rank], active[pivot] = active[pivot], active[rank]
        for other in range(len(active)):
            if other != rank and (active[other] >> bit) & 1:
                active[other] ^= active[rank]
        pivots.append(bit)
        rank += 1
    return active[:rank], pivots


def dimension(rows, width):
    return len(rref(rows, width)[0])


def kernel(equations, width):
    rows, pivots = rref(equations, width)
    pivot_row = dict(zip(pivots, rows))
    basis = []
    for free in (bit for bit in range(width) if bit not in pivot_row):
        vec = 1 << free
        for pivot, row in pivot_row.items():
            if bin((row ^ (1 << pivot)) & vec).count("1") & 1:
                vec |= 1 << pivot
        basis.append(vec)
    return basis


def intersection(left, right, width):
    """Basis of span(left) ∩ span(right)."""
    left_rows, _ = rref(list(left), width)
    right_rows, _ = rref(list(right), width)
    variables = len(left_rows) + len(right_rows)
    equations = []
    for bit in range(width):
        equation = 0
        for index, row in enumerate(left_rows):
            if (row >> bit) & 1:
                equation |= 1 << index
        for index, row in enumerate(right_rows):
            if (row >> bit) & 1:
                equation |= 1 << (len(left_rows) + index)
        equations.append(equation)
    vectors = []
    for coefficients in kernel(equations, variables):
        acc = 0
        for index, row in enumerate(left_rows):
            if (coefficients >> index) & 1:
                acc ^= row
        vectors.append(acc)
    return rref(vectors, width)[0]


def transition_rank(left, right, width):
    """dim(left + right) - dim(left ∩ right), equal to the nested difference when nested."""
    joined = dimension(list(left) + list(right), width)
    meet = dimension(left, width) + dimension(right, width) - joined
    return joined - meet


def surviving(frames, width):
    meet = list(frames[0])
    for frame in frames[1:]:
        meet = intersection(meet, frame, width)
    return meet


def account(frames, width):
    require(frames, "empty history")
    birth = dimension(frames[0], width)
    unpaid_basis = surviving(frames, width)
    unpaid = dimension(unpaid_basis, width)
    paid = 0
    for left, right in zip(frames, frames[1:]):
        paid += transition_rank(left, right, width)
    final = dimension(frames[-1], width)
    naive = dimension(intersection(frames[0], frames[-1], width), width)
    return {
        "birth": birth,
        "unpaid": unpaid,
        "paid": paid,
        "final": final,
        "naive_intersection": naive,
        "lower_bound": final - unpaid,
    }


def subspaces_fast(width):
    found = []
    ambient = 1 << width
    for mask in range(1 << ambient):
        if mask & 1 == 0:
            continue
        vectors = [vector for vector in range(ambient) if (mask >> vector) & 1]
        member = set(vectors)
        if any((left ^ right) not in member for left in vectors for right in vectors):
            continue
        found.append(tuple(rref([vector for vector in vectors if vector], width)[0]))
    return found


def contains(host, guest, width):
    return dimension(list(host) + list(guest), width) == dimension(host, width)


def check_step_lemma(width, spaces):
    """Leaving rank dominates the birth directions dropped at that step."""
    checked = 0
    for host in spaces:
        guests = [space for space in spaces if contains(host, space, width)]
        for nxt in spaces:
            leaving = dimension(host, width) - dimension(intersection(host, nxt, width), width)
            for birth in guests:
                dropped = dimension(birth, width) - dimension(intersection(birth, nxt, width), width)
                require(dropped <= leaving, "step lemma failed")
                checked += 1
    return checked


def check_histories(width, spaces, births):
    checked = 0
    max_line_unpaid = 0
    naive_traps = 0
    for birth in births:
        for middle in spaces:
            for final in spaces:
                row = account((birth, middle, final), width)
                require(row["unpaid"] <= row["birth"], "unpaid exceeded the birth")
                require(row["naive_intersection"] <= row["birth"], "endpoint intersection exceeded the birth")
                require(row["paid"] >= row["lower_bound"], "paid rank fell below the ledger")
                if row["birth"] == 1:
                    require(row["unpaid"] <= 1, "line birth reached unpaid 2")
                    max_line_unpaid = max(max_line_unpaid, row["unpaid"])
                    if row["naive_intersection"] > row["unpaid"]:
                        naive_traps += 1
                checked += 1
    return checked, max_line_unpaid, naive_traps


def full_basis(width):
    return tuple(1 << bit for bit in range(width))


def evaluate():
    authenticate()
    # The list-membership helper is unused; the fast enumerator is the census.
    # The census below is the finite check. The general step is proved in PROOF.md.
    spaces3 = subspaces_fast(3)
    spaces4 = subspaces_fast(4)
    require(len(spaces3) == 16, "F_2^3 subspace count moved")
    require(len(spaces4) == 67, "F_2^4 subspace count moved")
    lines3 = [space for space in spaces3 if dimension(space, 3) == 1]
    lines4 = [space for space in spaces4 if dimension(space, 4) == 1]
    require(len(lines3) == 7 and len(lines4) == 15, "line counts moved")

    step3 = check_step_lemma(3, spaces3)
    step4 = check_step_lemma(4, spaces4)
    hist3, max3, traps3 = check_histories(3, spaces3, spaces3)
    hist4, max4, traps4 = check_histories(4, spaces4, lines4)
    require(hist3 == 16 ** 3, "m=3 census incomplete")
    require(max3 <= 1 and max4 <= 1, "census produced a second unpaid coordinate")
    require(traps3 > 0 and traps4 > 0, "naive intersection never disagreed with unpaid")

    # Explicit erasure asked for by the predecessor, inside the selected width.
    birth = (1,)
    erased = (1 << 1,)
    full = full_basis(M_SELECTED)
    erasure = account((birth, erased, full), M_SELECTED)
    require(erasure["birth"] == 1, "erasure birth moved")
    require(erasure["unpaid"] == 0, "erasure left a surviving birth direction")
    require(erasure["naive_intersection"] == 1, "rewritten line left the final frame")
    require(erasure["paid"] == 2 + (M_SELECTED - 1), "erasure charge moved")
    require(erasure["paid"] >= erasure["lower_bound"] == M_SELECTED, "erasure ledger failed")
    require(erasure["unpaid"] != 2, "control failed to reject unpaid 2 after erasure")

    # Cleared source from the predecessor: intersection zero, still not unpaid 2.
    cleared = account((birth, erased), M_SELECTED)
    require(cleared["naive_intersection"] == 0 and cleared["unpaid"] == 0, "cleared source count moved")
    require(not contains(erased, birth, M_SELECTED), "cleared source was nested")

    # Nested selected climb: unpaid stays 1 and the acquired rank is 72.
    selected = account((birth, full), M_SELECTED)
    require(
        selected == {
            "birth": 1,
            "unpaid": 1,
            "paid": M_SELECTED - 1,
            "final": M_SELECTED,
            "naive_intersection": 1,
            "lower_bound": M_SELECTED - 1,
        },
        "selected line count moved",
    )

    # A side bank that does not contain the birth line is not a second unpaid
    # direction. Putting that bank into the family history erases the line, so
    # the surviving birth drops to 0. Leaving the family frame untouched, which
    # is the predecessor's reading of a side bank, keeps unpaid 1.
    bank = (0b010, 0b100)
    side_in_history = account((birth, bank, birth), M_SELECTED)
    require(side_in_history["unpaid"] == 0, "a missing birth line survived the side bank")
    require(side_in_history["unpaid"] != 2, "control failed to reject unpaid 2 from a side bank")
    family_beside_bank = account((birth, full), M_SELECTED)

    # Two unpaid coordinates occur for a plane birth, which is the other contract.
    plane = (0b001, 0b010)
    plane_row = account((plane, plane, full), M_SELECTED)
    require(plane_row["unpaid"] == 2 and plane_row["birth"] == 2, "plane birth did not keep two unpaid")
    require(plane_row["paid"] == M_SELECTED - 2, "plane climb charge moved")

    rng = random.Random(73)
    random_checks = 0
    for _ in range(400):
        width = 8
        frames = []
        for _step in range(6):
            rows = [rng.randrange(1 << width) for _ in range(rng.randrange(0, width + 1))]
            frames.append(tuple(rref(rows, width)[0]))
        row = account(frames, width)
        require(row["unpaid"] <= row["birth"], "random unpaid exceeded the birth")
        require(row["naive_intersection"] <= row["birth"], "random endpoint intersection exceeded the birth")
        require(row["paid"] >= row["lower_bound"], "random ledger failed")
        if row["birth"] <= 1:
            require(row["unpaid"] <= 1, "random line birth reached unpaid 2")
        random_checks += 1

    return {
        "m3_subspaces": len(spaces3),
        "m4_subspaces": len(spaces4),
        "step_lemma_m3": step3,
        "step_lemma_m4": step4,
        "histories_m3": hist3,
        "line_histories_m4": hist4,
        "max_line_unpaid_m3": max3,
        "max_line_unpaid_m4": max4,
        "naive_traps_m3": traps3,
        "naive_traps_m4": traps4,
        "erasure_unpaid": erasure["unpaid"],
        "erasure_naive_intersection": erasure["naive_intersection"],
        "erasure_paid": erasure["paid"],
        "erasure_lower_bound": erasure["lower_bound"],
        "cleared_unpaid": cleared["unpaid"],
        "selected_unpaid": selected["unpaid"],
        "selected_paid": selected["paid"],
        "side_bank_in_history_unpaid": side_in_history["unpaid"],
        "family_beside_side_bank_unpaid": family_beside_bank["unpaid"],
        "plane_unpaid": plane_row["unpaid"],
        "random_histories_m8": random_checks,
        "line_unpaid_at_most_1": True,
        "erasure_creates_second_unpaid": False,
        "no_new_kappa": True,
    }


def main():
    observed = evaluate()
    result_path = PACKAGE / "RESULT.json"
    if "--write" in __import__("sys").argv:
        result_path.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
    stored = json.loads(result_path.read_text(encoding="utf-8"))
    require(observed == stored, "RESULT.json does not match the execution")
    print(MARKER)


if __name__ == "__main__":
    main()
