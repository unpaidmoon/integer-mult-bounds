#!/usr/bin/env python3
"""Exact checks for the #4100 common-cover row reservation.

The written ceil pad does not fit in the reserved row bits. The group order
Gamma is |O(73,2)| for the standard dot product, and the depth recurrence
does halve. See PROOF.md.
"""

import hashlib
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPLEX = ROOT / "research/unconditional-batched-crt/COMPLEX.md"
AUDIT = ROOT / "research/unconditional-batched-crt/AUDIT.md"

SENTENCES = (
    "Set W=322560 and Gamma=2^1296 product_{i=1}^{36}(2^(2i)-1).",
    "This is |O(73,2)|: the all-one vector has norm1 and its perpendicular space",
    "is symplectic of dimension72. Count successive symplectic pairs.",
    "Define D(e)=0 for e<73 and D(e)=1+D(48floor(e/73)) otherwise.",
    "Every child r floor(e/73), r<=48, decreases D, and two levels halve e.",
    "Reserve q=ceil(log2((W Gamma)^D(h))) row bits. Pad their complete range",
    "to R=ceil(2^q/(W Gamma)^D(h))*(W Gamma)^D(h), a factor less than two.",
)
AUDIT_SENTENCE = (
    "Whole-call hosting and exact phases | PR4088's literal fill and "
    "all112-port Z4 checks provide finite identities; COMPLEX.md supplies "
    "the arbitrary-f lift and complete-cover execution."
)
GAMMA_SHA256 = "50b58aaac98e621e9917d6c3bced5e276398b68918bbd57ac8d784d3d58db00b"
W = 322560
WIDTH = 73
MAX_CHILD_RANK = 48


def dot(x, y):
    return (x & y).bit_count() & 1


def rank(rows, n):
    active = list(rows)
    found = 0
    for col in range(n):
        pivot = None
        for i in range(found, len(active)):
            if (active[i] >> col) & 1:
                pivot = i
                break
        if pivot is None:
            continue
        active[found], active[pivot] = active[pivot], active[found]
        for i in range(len(active)):
            if i != found and (active[i] >> col) & 1:
                active[i] ^= active[found]
        found += 1
    return found


def product_order(m):
    """2^{m^2} * product_{i=1}^{m} (2^{2i}-1), with the m=0 value 1."""
    order = 1 << (m * m)
    for i in range(1, m + 1):
        order *= (1 << (2 * i)) - 1
    return order


def pair_order(m):
    """product_{k=1}^{m} (2^{2k}-1) 2^{2k-1}."""
    order = 1
    for k in range(1, m + 1):
        order *= ((1 << (2 * k)) - 1) * (1 << (2 * k - 1))
    return order


def gamma_integer():
    return product_order(36)


def odd_part_of_stock_base():
    odd = 1
    for i in range(1, 37):
        odd *= (1 << (2 * i)) - 1
    if odd % 2 != 1 or odd % 3 != 0:
        raise AssertionError("Gamma's cofactor is not an odd multiple of 3")
    if (W & -W).bit_length() - 1 != 10 or W // (1 << 10) != 315:
        raise AssertionError("W is not 2^10 * 315")
    return 315 * odd


def ceil_log2(n):
    if n < 1:
        raise AssertionError("logarithm requires a positive integer")
    return (n - 1).bit_length()


def written_pad(n):
    q = ceil_log2(n)
    universe = 1 << q
    copies = (universe + n - 1) // n
    return q, universe, copies * n


def fitting_pad(n):
    q = ceil_log2(n)
    universe = 1 << q
    copies = universe // n
    return q, universe, copies * n


def written_pad_fits_with_strict_factor(n):
    _q, universe, reserved = written_pad(n)
    return reserved <= universe and reserved // n < 2


@cache
def depth(width):
    if width < WIDTH:
        return 0
    return 1 + depth(MAX_CHILD_RANK * (width // WIDTH))


def perp_basis(n):
    one = (1 << n) - 1
    basis = []
    for vector in range(1 << n):
        if dot(vector, one) != 0:
            continue
        if rank(basis + [vector], n) == len(basis) + 1:
            basis.append(vector)
        if len(basis) == n - 1:
            break
    if len(basis) != n - 1:
        raise AssertionError("all-ones perpendicular space has the wrong dimension")
    return basis


def symplectic_count(n):
    """Linear automorphisms of 1^perp that preserve the dot product."""
    if n % 2 != 1:
        raise AssertionError("the all-ones norm is 1 only in odd dimension")
    one = (1 << n) - 1
    if dot(one, one) != 1:
        raise AssertionError("all-ones norm is not 1")
    basis = perp_basis(n)
    dim = n - 1
    gram = [[dot(basis[i], basis[j]) for j in range(dim)] for i in range(dim)]
    if rank([sum(((gram[i][j]) << j) for j in range(dim)) for i in range(dim)], dim) != dim:
        raise AssertionError("the perpendicular form is degenerate")

    def embed(coords):
        point = 0
        for i in range(dim):
            if (coords >> i) & 1:
                point ^= basis[i]
        return point

    def form(left, right):
        return dot(embed(left), embed(right))

    count = 0
    singular = 0
    mask = (1 << dim) - 1
    for bits in range(1 << (dim * dim)):
        images = [(bits >> (i * dim)) & mask for i in range(dim)]
        if any(form(images[i], images[j]) != form(1 << i, 1 << j) for i in range(dim) for j in range(dim)):
            continue
        if rank(images, dim) != dim:
            singular += 1
            continue
        count += 1
    if singular:
        raise AssertionError("a singular map preserved the perpendicular form")
    return count


def orthonormal_bases(n):
    """Ordered bases of F_2^n with v_i · v_j = delta_ij, and their sums."""
    count = 0
    fixes_all_ones = True
    one = (1 << n) - 1
    chosen = []

    def rec():
        nonlocal count, fixes_all_ones
        if len(chosen) == n:
            count += 1
            total = 0
            for vector in chosen:
                total ^= vector
            if total != one:
                fixes_all_ones = False
            return
        for vector in range(1 << n):
            if dot(vector, vector) != 1:
                continue
            if any(dot(vector, earlier) != 0 for earlier in chosen):
                continue
            chosen.append(vector)
            rec()
            chosen.pop()

    rec()
    return count, fixes_all_ones


def check_sources():
    complex_text = COMPLEX.read_text(encoding="utf-8")
    audit_text = AUDIT.read_text(encoding="utf-8")
    for sentence in SENTENCES:
        if sentence not in complex_text:
            raise AssertionError("COMPLEX.md no longer contains the audited sentence: " + sentence)
    if AUDIT_SENTENCE not in audit_text:
        raise AssertionError("AUDIT.md no longer names the complete-cover obligation")


def check_group_order():
    if product_order(0) != 1:
        raise AssertionError("the empty symplectic product is 1")
    for m in range(0, 37):
        if product_order(m) != pair_order(m):
            raise AssertionError("symplectic pair count disagrees at m=" + str(m))
    gamma = gamma_integer()
    if gamma.bit_length() != 2628 or (gamma & -gamma).bit_length() - 1 != 1296:
        raise AssertionError("Gamma does not have 2628 bits and 2-valuation 1296")
    digest = hashlib.sha256(str(gamma).encode("ascii")).hexdigest()
    if digest != GAMMA_SHA256:
        raise AssertionError("Gamma decimal hash changed: " + digest)
    # n = 1 is the trivial odd orthogonal group. n = 3, 5 match Sp(2) and Sp(4).
    expected = {1: 1, 3: product_order(1), 5: product_order(2)}
    for n, order in expected.items():
        bases, fixes = orthonormal_bases(n)
        if bases != order or not fixes:
            raise AssertionError("dot-product orthogonal count failed at n=" + str(n))
        if n > 1 and symplectic_count(n) != order:
            raise AssertionError("perpendicular symplectic count failed at n=" + str(n))
    return gamma


def check_padding(stock_odd):
    if stock_odd % 2 != 1 or stock_odd <= 1:
        raise AssertionError("the stock cofactor is not an odd integer above 1")
    # A pure power of two is the case the written formula does handle.
    if not written_pad_fits_with_strict_factor(8):
        raise AssertionError("control: a power-of-two stock must fit")
    if written_pad_fits_with_strict_factor(3):
        raise AssertionError("control: N=3 must already exhibit the ceil defect")
    for exponent in range(1, 5):
        valuation = 1306 * exponent
        odd = pow(stock_odd, exponent)
        n = odd << valuation
        q, universe, reserved = written_pad(n)
        if reserved != 2 * n or reserved <= universe or reserved // n != 2:
            raise AssertionError("written pad did not fail at D=" + str(exponent))
        if q != valuation + ceil_log2(odd):
            raise AssertionError("bit count does not split into valuation plus odd logarithm")
        _qf, universe_fit, fitting = fitting_pad(n)
        if fitting != n or fitting > universe_fit or not 1 < universe_fit / n < 2:
            raise AssertionError("the single fitting copy is not N")
        if (2 * n).bit_length() - 1 != q:
            # 2N needs exactly q+1 bits: 2^q < 2N < 2^{q+1}, so bit_length is q+1.
            raise AssertionError("the written range does not take exactly one extra bit")
        if (2 * n).bit_length() != q + 1:
            raise AssertionError("q+1 bits do not hold the written range")


def check_depth():
    if 2 * (MAX_CHILD_RANK ** 2) >= WIDTH ** 2:
        raise AssertionError("two maximum-rank steps do not contract below one half")
    for width in range(0, WIDTH):
        if depth(width) != 0:
            raise AssertionError("D is nonzero below width 73")
    for width in range(WIDTH, 4001):
        if depth(width) != 1 + depth(MAX_CHILD_RANK * (width // WIDTH)):
            raise AssertionError("recurrence mismatch")
        for rank_value in range(1, MAX_CHILD_RANK + 1):
            child = rank_value * (width // WIDTH)
            if depth(child) > depth(width) - 1:
                raise AssertionError("a legal child did not decrease D")
    for width in range(WIDTH, 100001):
        once = MAX_CHILD_RANK * (width // WIDTH)
        twice = MAX_CHILD_RANK * (once // WIDTH) if once >= WIDTH else 0
        if twice * 2 >= width:
            raise AssertionError("two levels failed to halve")
    if depth(WIDTH) != 1 or depth(MAX_CHILD_RANK) != 0:
        raise AssertionError("the first node does not drop to a leaf child")


def main():
    check_sources()
    gamma = check_group_order()
    check_padding(odd_part_of_stock_base())
    check_depth()
    print(
        "PASS_COMPLEX_COVER_ROW_RESERVATION"
        f" gamma_bits={gamma.bit_length()}"
        f" gamma_sha256={GAMMA_SHA256}"
        " written_factor=2"
        " written_fits=false"
        " repair_copy=1"
        " repair_factor_lt_2=true"
        " depth_halves=true"
        " dot_orders=1,6,720"
        " no_new_kappa"
    )


if __name__ == "__main__":
    main()
