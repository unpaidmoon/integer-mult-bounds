#!/usr/bin/env python3
"""Selected-pool native floor for the q2 event58 suffix.

Native mass is at least 20, so a suffix of mass 16 is impossible.
The neutral rewrite has mass 22. No new kappa. Apache-2.0.
"""
import hashlib
import json
from collections import deque
from fractions import Fraction
from pathlib import Path

from monomials import decode, identity, rank, signature

HERE = Path(__file__).resolve().parent
FRESH = 3072
OPERATORS_SHA256 = "057a8d5de8c64e63d37db78b26d83164fe1b64d71ce322b1d2cecadcccffd079"
TARGET = 16
MINIMUM = 20
UPPER = 22


def need(cond, message):
    if not cond:
        raise ValueError(message)


def load_ops():
    raw_bytes = (HERE / "operators.json").read_bytes()
    need(hashlib.sha256(raw_bytes).hexdigest() == OPERATORS_SHA256, "operators.json bytes drifted")
    raw = json.loads(raw_bytes)
    return {name: decode(raw[name]) for name in ("K", "T", "W")}


def close(generators):
    start = identity(12)
    seen = {signature(start): start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for gen in generators:
            nxt = gen @ current
            key = signature(nxt)
            if key not in seen:
                seen[key] = nxt
                queue.append(nxt)
    return seen


def fresh(g):
    return (g.offset & FRESH) != 0


def add_term(acc, inp, element, coeff, index):
    key = (inp, index[signature(element)])
    acc[key] = acc.get(key, 0) + Fraction(coeff)
    if acc[key] == 0:
        del acc[key]
    return acc


def mul_bank(row, factor, elems, index):
    out = {}
    for (inp, gi), coeff in row.items():
        key = (inp, index[signature(factor @ elems[gi])])
        out[key] = out.get(key, 0) + coeff
        if out[key] == 0:
            del out[key]
    return out


def add_bank(dst, src, coeff):
    out = dict(dst)
    for key, value in src.items():
        out[key] = out.get(key, 0) + coeff * value
        if out[key] == 0:
            del out[key]
    return out


def even_rows(K, W, elems, index):
    """Even cores z, before the final fresh T on every bank.

    Inputs are (a, u, b, r, z, c).
    """
    a, u, b, r, z, c = range(6)
    z0 = {}
    add_term(z0, a, K, 1, index)
    z4 = {}
    add_term(z4, z, K, 1, index)
    z5 = {}
    add_term(z5, c, identity(12), 1, index)
    z2 = {}
    add_term(z2, a, K, -1, index)
    add_term(z2, b, identity(12), 1, index)
    add_term(z2, r, identity(12), -1, index)
    add_term(z2, z, K, -1, index)
    z1 = {}
    add_term(z1, b, identity(12), 1, index)
    add_term(z1, r, identity(12), -1, index)
    add_term(z1, a, W @ K, -1, index)
    add_term(z1, b, W, -1, index)
    add_term(z1, z, W @ K, -1, index)
    z3 = {}
    add_term(z3, u, K, 1, index)
    add_term(z3, b, K, 1, index)
    add_term(z3, a, K @ W @ K, -1, index)
    add_term(z3, b, K @ W, -1, index)
    add_term(z3, z, K @ W @ K, -1, index)
    return [z0, z1, z2, z3, z4, z5]


def neutral_rewrite(K, T, W, elems, index):
    """The predecessor's mass-22 gate list: three K, six T, one W."""
    banks = [{(i, index[signature(identity(12))]): Fraction(1)} for i in range(6)]

    def unary(bank, gate):
        banks[bank] = mul_bank(banks[bank], gate, elems, index)

    def add(dst, src, coeff):
        banks[dst] = add_bank(banks[dst], banks[src], Fraction(coeff))

    unary(4, K)
    add(3, 4, 1)
    add(2, 3, -1)
    for bank in range(6):
        unary(bank, T)
    unary(0, K)
    add(2, 0, -1)
    banks[3] = {key: -value for key, value in banks[3].items()}
    add(3, 4, 1)
    add(3, 0, -2)
    add(1, 0, -1)
    add(3, 2, -2)
    add(1, 2, -1)
    add(3, 4, -2)
    add(1, 4, -1)
    add(3, 2, 1)
    add(1, 2, 1)
    add(1, 3, -1)
    unary(3, W)
    add(1, 3, 1)
    add(3, 0, 1)
    add(3, 2, 1)
    add(3, 4, 1)
    unary(1, K)
    banks[1], banks[3] = banks[3], banks[1]
    return banks


def amplitude(phase):
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[phase % 4]


def operator_matrix(g):
    """Permutation-and-phase action on the four low bits. Entries are (re, im) = i^phase."""
    matrix = [[(Fraction(0), Fraction(0)) for _ in range(16)] for _ in range(16)]
    for x in range(16):
        y = g.act(x)
        need(y < 16, "even operator leaked out of bits 0-3")
        re, im = amplitude(g.q(x) + g.global_phase)
        matrix[y][x] = (Fraction(re), Fraction(im))
    return matrix


def matmul(left, right):
    out = [[(Fraction(0), Fraction(0)) for _ in range(16)] for _ in range(16)]
    for i in range(16):
        for k in range(16):
            ar, ai = left[i][k]
            if ar == 0 and ai == 0:
                continue
            for j in range(16):
                br, bi = right[k][j]
                out[i][j] = (out[i][j][0] + ar * br - ai * bi, out[i][j][1] + ar * bi + ai * br)
    return out


def matrices_equal(left, right):
    return all(left[i][j] == right[i][j] for i in range(16) for j in range(16))


def embed(rows, elems):
    """Place a 6 by 6 matrix over the even algebra into a 96 by 96 matrix over Q(i)."""
    big = [[(Fraction(0), Fraction(0)) for _ in range(96)] for _ in range(96)]
    cache = {}
    for i, row in enumerate(rows):
        for (col, gi), coeff in row.items():
            key = signature(elems[gi])
            block = cache.get(key)
            if block is None:
                block = operator_matrix(elems[gi])
                cache[key] = block
            for x in range(16):
                for y in range(16):
                    re, im = block[y][x]
                    slot = big[i * 16 + y][col * 16 + x]
                    big[i * 16 + y][col * 16 + x] = (slot[0] + coeff * re, slot[1] + coeff * im)
    return big


def complex_rank(matrix):
    size = len(matrix)
    work = [row[:] for row in matrix]

    def nonzero(value):
        return value[0] != 0 or value[1] != 0

    def divide(numer, denom):
        dr, di = denom
        den = dr * dr + di * di
        return ((numer[0] * dr + numer[1] * di) / den, (numer[1] * dr - numer[0] * di) / den)

    def axpy(acc, factor, other):
        fr, fi = factor
        return (acc[0] - (fr * other[0] - fi * other[1]), acc[1] - (fr * other[1] + fi * other[0]))

    used = set()
    found = 0
    for col in range(size):
        pivot = next((row for row in range(size) if row not in used and nonzero(work[row][col])), None)
        if pivot is None:
            continue
        used.add(pivot)
        found += 1
        pivot_value = work[pivot][col]
        for row in range(size):
            if row == pivot or not nonzero(work[row][col]):
                continue
            factor = divide(work[row][col], pivot_value)
            work[row] = [axpy(work[row][k], factor, work[pivot][k]) for k in range(size)]
    return found


def main():
    ops = load_ops()
    K, T, W = ops["K"], ops["T"], ops["W"]
    need(signature(K @ T) == signature(T @ K) and signature(W @ T) == signature(T @ W), "T is central on the generators")
    sign = T @ T
    need(signature(sign) == signature(K @ K) and signature(sign) != signature(identity(12)), "T squared is K squared, a central sign")
    need(signature(T @ T @ T @ T) == signature(identity(12)), "T has order 4")
    need(fresh(T) and fresh(T.inv()) and not fresh(K) and not fresh(W), "only T meets the fresh plane")
    need(K.rows == identity(12).rows and T.rows == identity(12).rows, "K and T do not permute addresses")
    need(W.rows != identity(12).rows, "W moves an address plane")
    for name, gate, paid in (("K", K, 2), ("T", T, 2), ("W", W, 4)):
        need(rank(gate.polar()) == paid and rank(gate.inv().polar()) == paid, name + " polar rank")

    full = close([K, K.inv(), T, T.inv(), W, W.inv()])
    need(len(full) == 256, "selected pool closes at 256 monomials")
    even_group = close([K, K.inv(), W, W.inv()])
    need(len(even_group) == 128 and all(not fresh(g) for g in even_group.values()), "K and W generate the 128 even monomials")
    odd_hits = {signature(T @ g) for g in even_group.values()}
    need(odd_hits.isdisjoint(even_group) and odd_hits | set(even_group) == set(full), "every monomial is uniquely even or T times even")

    without_w = close([K, K.inv(), T, T.inv()])
    need(all(g.rows == identity(12).rows for g in without_w.values()), "K and T never create W's plane swap")
    tw = close([T, T.inv(), W, W.inv()])
    one_k = {signature(g) for g in tw.values()}
    for left in tw.values():
        for right in tw.values():
            one_k.add(signature(left @ K @ right))
    kwkt = K @ W @ K @ T
    need(signature(kwkt) not in one_k, "K W K T is outside the one-K bimodule")

    elems = list(full.values())
    index = {signature(g): i for i, g in enumerate(elems)}
    cores = even_rows(K, W, elems, index)
    for row in cores:
        for (_, gi) in row:
            need(signature(elems[gi]) in even_group, "core monomials are even")
    by_cores = [mul_bank(row, T, elems, index) for row in cores]
    by_circuit = neutral_rewrite(K, T, W, elems, index)
    need(by_cores == by_circuit, "neutral rewrite equals T applied to the six even cores")
    row3_a = [(elems[gi], coeff) for (inp, gi), coeff in by_circuit[3].items() if inp == 0]
    need(len(row3_a) == 1 and row3_a[0][1] == -1 and signature(row3_a[0][0]) == signature(kwkt),
         "row 3, input a is exactly -K W K T")
    swap_terms = [elems[gi] for row in by_circuit for (_, gi), _ in row.items() if elems[gi].rows == W.rows]
    need(swap_terms, "the matrix uses W's address rows")

    rho = {signature(identity(12)): operator_matrix(identity(12))}
    queue = deque([identity(12)])
    while queue:
        current = queue.popleft()
        for gen in (K, K.inv(), W, W.inv()):
            nxt = gen @ current
            key = signature(nxt)
            product = matmul(operator_matrix(gen), rho[signature(current)])
            if key not in rho:
                rho[key] = operator_matrix(nxt)
                queue.append(nxt)
            need(matrices_equal(rho[key], product), "low-bit map is a representation of the even group")
    need(len(rho) == 128, "representation covers every even monomial")
    embedded = embed(cores, elems)
    found = complex_rank(embedded)
    collapsed = [row if i != 1 else cores[0] for i, row in enumerate(cores)]
    collapsed_rank = complex_rank(embed(collapsed, elems))
    need(found == 96, "even-core representation rank")
    need(collapsed_rank == 80, "replacing one core by another drops the rank by 16")
    # Five generators would embed as a 96 by 80 factor, rank at most 80.
    need(found > 5 * 16, "six module generators are necessary")

    fresh_cost = 6 * 2
    k_cost = 2 * 2
    w_cost = 4
    minimum = fresh_cost + k_cost + w_cost
    need(minimum == MINIMUM and minimum > TARGET and UPPER == 3 * 2 + 6 * 2 + 4 and UPPER > minimum,
         "floor 20 sits strictly above 16 and strictly below the replayed 22")
    print(
        "PASS_CUT58_LOCAL16_NATIVE_FLOOR"
        f" minimum={minimum} target16=impossible upper={UPPER}"
        " fresh_queries=6 k_queries=2 w_queries=1 group=256 no_new_kappa"
    )


if __name__ == "__main__":
    main()
