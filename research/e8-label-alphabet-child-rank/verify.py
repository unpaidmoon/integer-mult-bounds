#!/usr/bin/env python3
"""Largest support-pairing rank on the fixed E8 label alphabet, and the rank-9 screen.

The 120 line representatives use the same doubled-coordinate enumeration as
research/complex-frame-pair-decoders/verify.py. A term costs the F2 rank of
(<r_i, r_j> + 1) mod 2 between its row and column supports. That matrix has
rank 9, so no term on this alphabet costs more than 9, and an explicit 9-line
minor shows that 9 is attained.

The selected local mass, read from the pinned assembly, is then screened in
research/complex-local-word-ceiling. Putting every paid unit on rank 9 is the
cheapest same-mass shape whose children have pairing rank at most 9. Its
relaxation at a = 1/99 is still above 1. Rank 44 in the same calculator is the
first pure cap that clears that target, so this alphabet cannot supply the
children that threshold asks for.

usage: verify.py [--write]
"""
import itertools
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research" / "complex-local-word-ceiling"))
import ceiling as C  # noqa: E402

M, PAIRS, PORTS, STAGES, CENTRE = 73, 4, 112, 9, 64
FAMILIES = 2 * PAIRS * PORTS
TARGET = Q(1, 99)
WITNESS = (0, 1, 2, 4, 6, 8, 10, 12, 56)
WITNESS_VECTORS = (
    (2, 2, 0, 0, 0, 0, 0, 0),
    (2, -2, 0, 0, 0, 0, 0, 0),
    (2, 0, 2, 0, 0, 0, 0, 0),
    (2, 0, 0, 2, 0, 0, 0, 0),
    (2, 0, 0, 0, 2, 0, 0, 0),
    (2, 0, 0, 0, 0, 2, 0, 0),
    (2, 0, 0, 0, 0, 0, 2, 0),
    (2, 0, 0, 0, 0, 0, 0, 2),
    (1, 1, 1, 1, 1, 1, 1, 1),
)
RESULT_PATH = HERE / "RESULT.json"


def require(ok, why):
    if not ok:
        raise SystemExit("FAIL: " + why)


def e8_roots():
    """240 roots in doubled coordinates, PR717 enumeration order."""
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                vector = [0] * 8
                vector[i], vector[j] = 2 * si, 2 * sj
                roots.append(tuple(vector))
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(tuple(signs))
    return roots


def inner(x, y):
    product = sum(a * b for a, b in zip(x, y))
    require(product % 4 == 0, "doubled coordinates are not an even lattice vector")
    return product // 4


def neg(vector):
    return tuple(-coordinate for coordinate in vector)


def lines():
    chosen, seen = [], set()
    for root in e8_roots():
        key = root if root > neg(root) else neg(root)
        if key not in seen:
            seen.add(key)
            chosen.append(root)
    return chosen


def pairing_rows(representatives):
    count = len(representatives)
    rows = []
    products = []
    for i, left in enumerate(representatives):
        mask = 0
        row = []
        for j, right in enumerate(representatives):
            value = inner(left, right)
            row.append(value)
            if (value + 1) & 1:
                mask |= 1 << j
        rows.append(mask)
        products.append(row)
    require(count == 120, "E8 has 120 lines")
    return rows, products


def f2_basis(rows):
    """Highest-bit Gaussian basis. Membership reduces from the top pivot."""
    basis = {}
    for vector in rows:
        reduced = vector
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in basis:
                reduced ^= basis[pivot]
            else:
                basis[pivot] = reduced
                break
    return basis


def in_span(vector, basis):
    reduced = vector
    while reduced:
        pivot = reduced.bit_length() - 1
        if pivot not in basis:
            return False
        reduced ^= basis[pivot]
    return True


def f2_rank(rows):
    return len(f2_basis(rows))


def independent_indices(rows, count):
    basis = {}
    chosen = []
    for index, vector in enumerate(rows):
        reduced = vector
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in basis:
                reduced ^= basis[pivot]
            else:
                basis[pivot] = reduced
                chosen.append(index)
                break
        if len(chosen) == count:
            return chosen, basis
    raise SystemExit("FAIL: pairing rank is below the requested witness size")


def pivot_columns(originals):
    work = list(originals)
    used = [False] * len(work)
    columns = []
    for column in range(120):
        bit = 1 << column
        source = next((row for row in range(len(work)) if not used[row] and work[row] & bit), None)
        if source is None:
            continue
        used[source] = True
        columns.append(column)
        for row in range(len(work)):
            if row != source and work[row] & bit:
                work[row] ^= work[source]
        if len(columns) == len(work):
            break
    return columns


def mask_of(indices):
    value = 0
    for index in indices:
        value |= 1 << index
    return value


def selected_local():
    record = json.loads((ROOT / "certificates/selected-result.json").read_text(encoding="utf-8"))
    assembly = json.loads((ROOT / record["certificate"]).read_text(encoding="utf-8"))
    independent = json.loads(
        (ROOT / "research/community-frontier1094-audit/INDEPENDENT1094.json").read_text(encoding="utf-8")
    )
    profile = {int(rank): count for rank, count in assembly["complex_profile"].items()}
    idle = {int(rank): count for rank, count in independent["owner"]["idle"].items()}
    calls, live = independent["price"]["calls"], independent["price"]["live"]
    require(profile == {int(rank): count for rank, count in independent["owner"]["profile"].items()},
            "assembly profile disagrees with the independent owner profile")
    require(calls % STAGES == 0 and live == FAMILIES * (calls // STAGES),
            "live stock is not 2*4*112 families per nine-stage replica")
    mass = sum(rank * count for rank, count in profile.items())
    require(mass == (M - 1) * live + CENTRE * calls, "coverage identity mass = 72W + 64N fails")
    local = {}
    for rank, count in profile.items():
        paid = count - idle.get(rank, 0)
        require(paid >= 0 and paid % calls == 0, "local rank %s is not uniform per call" % rank)
        if paid:
            local[rank] = paid // calls
    local_mass = sum(rank * count for rank, count in local.items())
    require(local_mass * calls + sum(rank * count for rank, count in idle.items()) == mass,
            "local plus idle does not recover the complex profile")
    return record, local, local_mass


def fraction_pair(bounds):
    return [str(bounds[0]), str(bounds[1])]


def build():
    representatives = lines()
    require(len(e8_roots()) == 240, "E8 has 240 roots")
    rows, products = pairing_rows(representatives)
    require(all(products[i][i] == 2 for i in range(120)), "a line has norm squared 2")
    off = {products[i][j] for i in range(120) for j in range(120) if i != j}
    require(off == {-1, 0, 1}, "distinct lines have inner products in {-1, 0, 1}")
    basis = f2_basis(rows)
    require(len(basis) == 9, "the 120 by 120 label pairing does not have F2 rank 9")
    require(all(in_span(row, basis) for row in rows), "a pairing row lies outside the rank-9 span")
    chosen, _ = independent_indices(rows, 9)
    require(tuple(chosen) == WITNESS, "the greedy rank-9 witness moved")
    require(tuple(representatives[index] for index in WITNESS) == WITNESS_VECTORS,
            "witness lines are not the pinned doubled roots")
    columns = pivot_columns([rows[index] for index in chosen])
    require(tuple(columns) == WITNESS, "the witness minor is not the pinned principal minor")
    column_mask = mask_of(columns)
    minor_rows = [rows[index] & column_mask for index in chosen]
    require(f2_rank(minor_rows) == 9, "the exhibited 9-line minor is singular")
    for drop in range(9):
        kept = [minor_rows[row] for row in range(9) if row != drop]
        require(f2_rank(kept) == 8, "deleting one witness line did not drop the minor rank to 8")
    extra = rows[WITNESS[-1]] ^ (1 << 200)
    require(f2_rank(rows + [extra]) == 10, "the rank routine cannot see a rank-10 extension")
    require(not in_span(extra, basis), "a bit outside the 120 columns stayed in the label span")

    record, local, local_mass = selected_local()
    require(local == {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8},
            "selected per-call local profile changed")
    require(local_mass == 5586 and max(local) == 8, "selected local mass or maximum rank changed")
    require(max(local) <= 9, "the selected word already uses a pairing rank above the alphabet cap")

    ideal = {9: Q(local_mass, 9)}
    remainder = local_mass - 9 * (local_mass // 9)
    integer_shape = {9: local_mass // 9}
    if remainder:
        integer_shape[remainder] = 1
    require(sum(rank * count for rank, count in integer_shape.items()) == local_mass,
            "integer rank-9 shape does not conserve mass")
    for small in range(1, 9):
        low_small, high_small = C.child_cost(small, M, TARGET)
        _low_nine, high_nine = C.child_cost(9, M, TARGET)
        require(high_nine / 9 < low_small / small,
                "rank-9 cost per unit is not strictly below rank %s" % small)
    ideal_at_target = C.relax(ideal, M, FAMILIES, STAGES, CENTRE, TARGET)
    require(ideal_at_target[0] > 1, "ideal rank-9 moment does not exceed 1 at a = 1/99")
    ideal_ceiling = C.ceiling(ideal, M, FAMILIES, STAGES, CENTRE, grid=Q(1, 10 ** 12))
    integer_ceiling = C.ceiling(integer_shape, M, FAMILIES, STAGES, CENTRE, grid=Q(1, 10 ** 12))
    cap43 = C.ceiling({43: Q(local_mass, 43)}, M, FAMILIES, STAGES, CENTRE, grid=Q(1, 10 ** 12))
    cap44 = C.ceiling({44: Q(local_mass, 44)}, M, FAMILIES, STAGES, CENTRE, grid=Q(1, 10 ** 12))
    cap43_at_target = C.relax({43: Q(local_mass, 43)}, M, FAMILIES, STAGES, CENTRE, TARGET)
    cap44_at_target = C.relax({44: Q(local_mass, 44)}, M, FAMILIES, STAGES, CENTRE, TARGET)
    require(ideal_ceiling[1] < TARGET and integer_ceiling[1] < TARGET and cap43[1] < TARGET,
            "a rank at most 43 cleared a = 1/99 in this calculator")
    require(cap43_at_target[0] > 1, "pure rank 43 is not already over budget at a = 1/99")
    require(cap44_at_target[1] < 1 and cap44[0] > TARGET,
            "pure rank 44 does not still have relaxation room at a = 1/99")
    kappa = Q(record["kappa"])
    kappa_cap = ideal_ceiling[1] / (1 + ideal_ceiling[1])
    require(kappa_cap > kappa, "the rank-9 planning cap is not above the selected kappa")
    require(kappa_cap < Q(1, 99) / (1 + Q(1, 99)), "the rank-9 planning cap reached the 1/99 kappa target")

    return {
        "lines": 120,
        "roots": 240,
        "pairing_rank": 9,
        "witness_lines": list(WITNESS),
        "witness_rank": 9,
        "selected_local_profile": {str(rank): count for rank, count in sorted(local.items())},
        "selected_local_mass": local_mass,
        "selected_local_max_rank": max(local),
        "ideal_rank9_relax_at_1_99": fraction_pair(ideal_at_target),
        "ideal_rank9_ceiling": fraction_pair(ideal_ceiling),
        "integer_rank9_profile": {str(rank): count for rank, count in sorted(integer_shape.items())},
        "integer_rank9_ceiling": fraction_pair(integer_ceiling),
        "pure_cap_43_ceiling": fraction_pair(cap43),
        "pure_cap_43_relax_at_1_99": fraction_pair(cap43_at_target),
        "pure_cap_44_ceiling": fraction_pair(cap44),
        "pure_cap_44_relax_at_1_99": fraction_pair(cap44_at_target),
        "target": "1/99",
        "selected_kappa": record["kappa"],
        "ideal_rank9_kappa_cap": str(kappa_cap),
        "alphabet_clears_target": False,
    }


def main():
    result = build()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write" in sys.argv:
        RESULT_PATH.write_text(encoded, encoding="utf-8")
    require(RESULT_PATH.read_text(encoding="utf-8") == encoded, "RESULT.json does not match the recomputation")
    print(
        "PASS_E8_LABEL_ALPHABET_CHILD_RANK pairing_rank=9 "
        "ideal_ceiling=%s below_1/99 cap44_clears selected_max_rank=8 no_new_kappa"
        % result["ideal_rank9_ceiling"][1]
    )


if __name__ == "__main__":
    main()
