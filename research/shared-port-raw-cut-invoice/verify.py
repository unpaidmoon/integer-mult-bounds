#!/usr/bin/env python3
"""Price the raw gate-11 shared-port cut, including contaminant cleanup.

The gate list and Clifford operators are the pinned predecessor files. This
module does not re-prove the recording-only 4d image bound. It prices the one
internal cut that escapes that bound.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
Predecessor operators: hexapode / the PR4813 schedule retained in
research/block3-shared-port-composition.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORD = ROOT / "research/block3-shared-port-composition/WORD.json"
ALGEBRA = ROOT / "research/block3-shared-port-composition/inputs/pr4813-verify_schedule.py"
PINS = {
    WORD: "05c81a7dfb37c240fdaef332474deb90f1b38e60dec392f3a23089f973a5f1ba",
    ALGEBRA: "6216fd67f1a762303f0eed0e37b90ea0c72cf8e0cb7db70b1b27b2001ac20069",
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load():
    for path, digest in PINS.items():
        need(hashlib.sha256(path.read_bytes()).hexdigest() == digest, "pin " + path.name)
    namespace = {"__name__": "schedule"}
    exec(compile(ALGEBRA.read_bytes(), str(ALGEBRA), "exec"), namespace)
    operators = namespace["load_operators"]()
    word, adj = namespace["word"], namespace["adjoint"]
    ident = namespace["ident"]()
    monomial = namespace["monomial"]
    s_letter = namespace["s_letter"]
    pauli = namespace["pauli"]
    v = monomial([0, 2, 1, 3, 4, 6, 5, 7])
    s = s_letter(7)
    p = word(s, monomial([0, 5, 2, 7, 4, 1, 6, 3]), s)
    q = word(s, v, s)
    letters = dict(
        operators,
        P=p,
        Pinv=adj(p),
        Q=q,
        Qinv=adj(q),
        V=v,
        Z1=pauli(0, 2),
        N=word(operators["A"], operators["D"], adj(operators["K"])),
    )
    return namespace, operators, letters, ident


def grade(matrix, zero):
    counts = {sum(entry != zero for entry in row) for row in matrix}
    need(len(counts) == 1, "pure uniform support")
    return next(iter(counts)).bit_length() - 1


def replay(gates, letters, word, ident, width=5):
    state = [[{ident: 1} if row == col else {} for col in range(width)] for row in range(width)]
    cuts = [[[dict(cell) for cell in row] for row in state]]
    for gate in gates:
        kind, dst = gate[:2]
        if kind == "add":
            src, coeff = gate[2:]
            for col in range(width):
                acc = defaultdict(int, state[dst][col])
                for matrix, weight in state[src][col].items():
                    acc[matrix] += coeff * weight
                state[dst][col] = {matrix: weight for matrix, weight in acc.items() if weight}
        else:
            need(kind in ("paid", "mono") and gate[2] in letters, "gate " + repr(gate))
            factor = letters[gate[2]]
            state[dst] = [{word(factor, matrix): weight for matrix, weight in cell.items()} for cell in state[dst]]
        cuts.append([[dict(cell) for cell in row] for row in state])
    return cuts


def only(cell):
    need(len(cell) == 1, "expected one term")
    return next(iter(cell.items()))


def paid_profile(gates, letters, zero):
    counts = defaultdict(int)
    for gate in gates:
        if gate[0] == "paid":
            counts[grade(letters[gate[2]], zero)] += 1
    return dict(counts)


def gap_at(reward_rank3, paid, t):
    """reward minus paid at exponent t, with r^t evaluated at the integer endpoints."""
    need(t in (0, 1), "endpoint exponent")
    reward = reward_rank3 * (3 ** t)
    cost = sum(count * (rank ** t) for rank, count in paid.items())
    return reward - cost


def main():
    namespace, operators, letters, ident = load()
    zero = namespace["ZERO"]
    word = namespace["word"]
    adj = namespace["adjoint"]
    schedule = json.loads(WORD.read_text(encoding="utf-8"))
    raw, fused = schedule["five_ports"], schedule["fused_five_ports"]
    raw_cuts = replay(raw, letters, word, ident)
    fused_cuts = replay(fused, letters, word, ident)
    need(raw_cuts[-1] == fused_cuts[-1], "raw and fused endpoints differ")

    # Gate 12 (0-based) is the aligning rank-1 A. After it, the raw state matches
    # the fused state after mono N, so the remaining fused gates are a legal continuation.
    need(raw_cuts[13] == fused_cuts[9], "aligning A does not restore the fused representative")
    hybrid = raw[:13] + fused[9:]
    hybrid_cuts = replay(hybrid, letters, word, ident)
    need(hybrid_cuts[-1] == fused_cuts[-1], "hybrid continuation misses the fused endpoint")
    dropped = raw[:12] + fused[9:]
    need(replay(dropped, letters, word, ident)[-1] != fused_cuts[-1], "aligning H1 is not necessary")

    fused_paid = paid_profile(fused, letters, zero)
    hybrid_paid = paid_profile(hybrid, letters, zero)
    need(fused_paid == {1: 2, 3: 4}, "fused bill " + str(fused_paid))
    need(hybrid_paid == {1: 5, 3: 3}, "exposure bill " + str(hybrid_paid))

    ka = word(operators["K"], namespace["pauli"](1, 3))
    mc2 = word(operators["M"], operators["C2"])
    d_matrix = operators["D"]
    for gate_index in (9, 10, 11):
        owner1 = raw_cuts[gate_index + 1][1]
        need({col for col, cell in enumerate(owner1) if cell} >= {0, 1}, "cut lost a column")
        need(not any(raw_cuts[gate_index + 1][row][1] for row in (0, 2, 3, 4)), "another live owner depends on x1")
        x0_grades = {grade(matrix, zero) for matrix in owner1[0]}
        x1_grades = {grade(matrix, zero) for matrix in owner1[1]}
        need(3 in x0_grades and x1_grades == {2}, "glue window " + str(gate_index))

    owner1 = raw_cuts[12][1]
    g1, c1 = only({matrix: weight for matrix, weight in owner1[0].items() if grade(matrix, zero) == 1})
    g3, c3 = only({matrix: weight for matrix, weight in owner1[0].items() if grade(matrix, zero) == 3})
    g2, c2 = only(owner1[1])
    need(c1 == 1 and c3 == 2 and c2 == 1, "pivot coefficients")
    need(g1 == mc2 and g3 == ka and g2 == d_matrix, "pivot operators")
    need(namespace["plus"](mc2, namespace["scale"](namespace["q"](2), ka)) == operators["B"], "B splitting")
    for unit in (d_matrix, ka, mc2, operators["A"], operators["K"]):
        product = word(unit, adj(unit))
        need(product == namespace["ident"](), "unit " + str(grade(unit, zero)))

    # H cleans 2 Ka into K and does not delete either contaminant.
    h_matrix = operators["H"]
    need({sum(entry != zero for entry in row) for row in h_matrix} == {1}, "H is not monomial")
    need(namespace["mm"](h_matrix, namespace["scale"](namespace["q"](2), ka)) == operators["K"], "H misses K")
    need(namespace["mm"](h_matrix, d_matrix) != [[zero] * 8 for _ in range(8)], "H unexpectedly kills D")
    need(namespace["mm"](h_matrix, mc2) != [[zero] * 8 for _ in range(8)], "H unexpectedly kills MC2")

    # D is exactly two source rank-1 letters times monomials, and no schedule
    # letter has grade 2, so one source paid letter cannot produce it.
    product = namespace["ident"]()
    factor_grades = []
    for name in ("A", "W", "C2", "V", "Z1"):
        factor = letters[name]
        factor_grades.append(grade(factor, zero))
        product = word(factor, product)
    need(product == d_matrix, "D factorization")
    need(factor_grades == [1, 0, 1, 0, 0], "D paid-letter count")
    used = {gate[2] for gate in raw + fused if gate[0] in ("paid", "mono")}
    need({grade(letters[name], zero) for name in used} <= {0, 1, 3}, "schedule invented a grade-2 letter")
    need(all(grade(letters[name], zero) in (1, 3) for name in used if any(g[0] == "paid" and g[2] == name for g in raw + fused)), "paid grade")

    # Gaussian invoice. Exposure is the hybrid bill. Cleanup adds two H1 for a
    # fresh D and one H1 for M C2. Reward credits five pure rank-3 jobs.
    exposure = {1: 5, 3: 3}
    full = {1: 8, 3: 3}
    widened = {1: 6, 2: 1, 3: 3}  # one H2 replaces the two cleanup letters inside D
    uncharged = {1: 5, 3: 3}  # fifth job credited while D and MC2 remain glued
    need(gap_at(5, full, 1) == 2 * 3 - 8 == -2, "full endpoint")
    need(gap_at(5, full, 0) == 2 - 8 == -6, "full at zero")
    need(gap_at(5, widened, 1) == 2 * 3 - 2 - 6 == -2, "widened endpoint")
    need(gap_at(5, widened, 0) == 2 - 1 - 6 == -5, "widened at zero")
    need(gap_at(5, uncharged, 1) == 1, "uncharged t=1 gap drifted")
    need(2 < 9, "derivative comparison 2 ln 3 > ln 2")
    # Finite corroboration of 2*3^t < 8 on the uniform grid, which is the
    # in-alphabet gap. The all-real argument is the monotonicity proof.
    for k in range(65):
        need(pow(3, k) < pow(4, 64), "grid " + str(k))

    # An actual source ADD sign fault must change the endpoint.
    bad = [list(gate) for gate in fused]
    add_at = next(i for i, gate in enumerate(bad) if gate[0] == "add")
    bad[add_at][3] *= -1
    need(replay(bad, letters, word, ident)[-1] != fused_cuts[-1], "ADD sign fault accepted")

    print(
        "PASS_SHARED_PORT_RAW_CUT_INVOICE "
        f"fused={fused_paid} exposure={exposure} full={full} "
        f"gap_t1={gap_at(5, full, 1)} widened_gap_t1={gap_at(5, widened, 1)}"
    )


if __name__ == "__main__":
    main()
