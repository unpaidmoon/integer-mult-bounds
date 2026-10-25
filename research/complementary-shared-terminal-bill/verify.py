#!/usr/bin/env python3
"""Shared ordinary-terminal bill for the complementary B/C pair.

The predecessor package research/complementary-consumer-feasibility proves that
every serial n>=2 consumer on the fixed 224 owners has a strictly negative
optimistic moment. This verifier does not replay that native audit. It prices
one changed premise outside that serial family: the 56 ordinary Q^{-1} terminals
share one rank-one child.

Apache-2.0. Prepared by unpaidmoon with substantial Cursor Grok assistance.
The Laurent word and direct-primitive constants are the predecessor's, credited
to Chris R / Clear1nsight and the retained B/C supplier authors.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "research" / "complementary-consumer-feasibility" / "RESULT.json"
EXPECTED_SHA = "aa5976ab8e1b2bd63f1958769f53738ca3e755d4ade9828690031a9321926630"


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, 0) + v
    return {k: v for k, v in c.items() if v}


def mul(a, b):
    c = {}
    for k, v in a.items():
        for l, w in b.items():
            e = tuple(x + y for x, y in zip(k, l))
            c[e] = c.get(e, 0) + v * w
    return {k: v for k, v in c.items() if v}


def mon(a=0, b=0, q=0, c=1):
    return {(a, b, q): F(c)} if c else {}


def mm(a, b):
    return [[add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j])) for j in range(2)] for i in range(2)]


def sh(c):
    return [[mon(), {}], [c, mon()]]


def diag(x, y):
    return [[x, {}], [{}, y]]


def gaussian(stage):
    return mon(1 if stage == 1 else 0, 1 if stage == 2 else 0, 0)


def source(stage, kind):
    d = gaussian(stage)
    if kind == "A":
        return mm(diag(d, d), sh(mon(q=-1)))
    if kind == "B":
        return mm(diag(d, mul(d, mon(q=1))), sh(mon(q=-1)))
    if kind == "C":
        return mm(diag(d, d), mm(sh(mon(q=-1)), diag(mon(q=1), mon())))
    raise ValueError(kind)


def artanh_ln(r, terms=48):
    """Return rational lower and upper bounds for ln(r), r an integer >= 2."""
    y = F(r - 1, r + 1)
    total = F(0)
    power = y
    square = y * y
    for k in range(terms):
        total += power / F(2 * k + 1)
        power *= square
    lower = 2 * total
    remainder = 2 * power / (F(2 * terms + 1) * (1 - square))
    return lower, lower + remainder


def log_bounds():
    ln2 = artanh_ln(2)
    ln3 = artanh_ln(3)
    ln5 = artanh_ln(5)
    ln7 = artanh_ln(7)

    def combine(parts):
        lo = sum((n * bounds[0] for n, bounds in parts), F(0))
        hi = sum((n * bounds[1] for n, bounds in parts), F(0))
        return lo, hi

    return {
        2: ln2,
        3: ln3,
        4: combine([(2, ln2)]),
        5: ln5,
        6: combine([(1, ln2), (1, ln3)]),
        7: ln7,
        8: combine([(3, ln2)]),
        14: combine([(1, ln2), (1, ln7)]),
        15: combine([(1, ln3), (1, ln5)]),
    }


def pow_bounds(base, numer, denom, bits=32):
    """Rational bounds for base**(numer/denom), checked by integer powers."""
    if numer == 0:
        return F(1), F(1)
    if numer == denom:
        return F(base), F(base)
    scale = 1 << bits
    rhs_unit = base ** numer
    den_scale = scale ** denom

    def ge(n):
        return n ** denom >= rhs_unit * den_scale

    low, high = scale, base * scale
    while low < high:
        mid = (low + high) // 2
        if ge(mid):
            high = mid
        else:
            low = mid + 1
    upper = F(low, scale)
    need(ge(low) and (low == scale or not ge(low - 1)), "root upper search")
    return F(low - 1, scale), upper


def mass(hist):
    return sum(rank * count for rank, count in hist.items())


def moment(coeffs, t):
    if t == 1:
        return sum(n * r for r, n in coeffs.items())
    if t == 0:
        return sum(coeffs.values())
    total = F(0)
    for r, n in coeffs.items():
        total += n * F(r) ** t
    return total


def derivative_lower_bound(coeffs, logs, left, right):
    total = F(0)
    for rank, count in coeffs.items():
        if rank == 1 or count == 0:
            continue
        lo_ln, hi_ln = logs[rank]
        if count > 0:
            power_lo, _power_hi = pow_bounds(rank, left.numerator, left.denominator)
            total += count * power_lo * lo_ln
        else:
            _power_lo, power_hi = pow_bounds(rank, right.numerator, right.denominator)
            total += count * power_hi * hi_ln
    return total


def certify():
    raw = PREDECESSOR.read_bytes()
    need(sha256(raw).hexdigest() == EXPECTED_SHA, "predecessor RESULT.json sha256")
    receipt = json.loads(raw)
    need(receipt["status"] == "PASS_SCOPED_COMPLEMENTARY_SERIAL_SCREEN", "predecessor status")
    need(receipt["complete_pair_rank_deficit"] == 176, "predecessor deficit")
    need(receipt["persistent_independent_inputs"] == 1040, "predecessor census size")
    paid = {int(k): v for k, v in receipt["complete_pair_paid"].items()}
    targets = {int(k): v for k, v in receipt["complete_pair_targets"].items()}
    need(mass(paid) - mass(targets) == 176, "predecessor rank-mass identity")
    profiles = receipt["profiles"]
    rank_one = profiles["B"]["paid"]["1"] + profiles["C"]["paid"]["1"] + 56
    need(rank_one == paid[1] == 4023, "56 ordinary terminals are exactly the added rank-one jobs")
    need(profiles["B"]["direct_gap_mass"] == 8 and profiles["C"]["direct_gap_mass"] == 0, "direct gaps")
    need(sum(targets.values()) == 1040, "224 main banks plus 816 helper returns")
    need(targets[14] == 112 and targets[15] == 112, "legal diagonal census")

    identity = [[mon(), {}], [{}, mon()]]
    exceptional = [source(1, "C"), source(2, "B"), sh(mon(c=-2))]
    ordinary = [source(1, "A"), source(2, "A"), sh(mon(q=-1, c=-2))]
    product = mon(1, 1)
    central = mon(q=1)
    for name, word, target in (
        ("exceptional", exceptional, diag(mul(product, central), mul(product, central))),
        ("ordinary", ordinary, diag(product, product)),
    ):
        value = identity
        for op in word:
            value = mm(op, value)
        need(value == target, name + " endpoint")
    bare = identity
    for op in ordinary[:2]:
        bare = mm(op, bare)
    need(mm(sh(mon(c=-2)), bare) != diag(product, product), "ordinary Q inverse is necessary")

    shared = dict(paid)
    shared[1] -= 55
    need(shared[1] == 3968, "one shared child replaces 56 terminals")
    need(mass(shared) - mass(targets) == 121, "shared rank-mass deficit")
    need(sum(targets.values()) == 1040, "ownership-disjoint census unchanged")

    coeffs = Counter(targets)
    coeffs.subtract(shared)
    need(moment(coeffs, 1) == -121, "exact shared moment at exponent 1")
    logs = log_bounds()
    for rank, (lo, hi) in logs.items():
        need(0 < lo < hi, "log bounds ordered at " + str(rank))
    cuts = [F(0), F(1, 16), F(1, 8), F(1, 4), F(1, 2), F(3, 4), F(1)]
    lowers = []
    for left, right in zip(cuts, cuts[1:]):
        lower = derivative_lower_bound(coeffs, logs, left, right)
        need(lower > 0, "moment derivative on [" + str(left) + "," + str(right) + "]")
        lowers.append(str(lower))
    # Derivative positive on [0,1] and M(1)=-121 imply M(t)<0 on the interval.
    need(moment(coeffs, 0) == sum(targets.values()) - sum(shared.values()) < -121, "endpoint order")

    def envelope(n):
        return 224 * (7 * n + 1) - n * (224 * 7 + 112)

    for n in range(2, 8):
        need(envelope(n) == 224 - 112 * n <= 0, "serial rank-mass envelope")
    need(envelope(2) == 0, "two C calls only tie at exponent 1")
    # The 55 saved terminals are not summands of this envelope.
    need("56" not in receipt["uniform_optimistic_moment_bound"], "optimistic bound ignores the ordinary terminals")

    # Reject a false zero-deficit reading of the same census.
    need(mass(shared) - mass(targets) != 0, "shared bill is not balanced")
    return {
        "status": "PASS_SHARED_ORDINARY_TERMINAL_STILL_LOSES",
        "new_kappa": False,
        "changed_premise": "56 ordinary L(-2 Q^{-1}) terminals share one rank-one Q^{-1} child; finite broadcast is free",
        "ownership_disjoint_targets": {"14": 112, "15": 112, "helpers": 816},
        "shared_rank_one_paid": shared[1],
        "rank_mass_deficit": 121,
        "moment_at_exponent_one": -121,
        "derivative_lower_bounds": lowers,
        "serial_envelope_unchanged": True,
        "synthesis_authorized": False,
    }


def main():
    result = certify()
    print(result["status"])


if __name__ == "__main__":
    main()
