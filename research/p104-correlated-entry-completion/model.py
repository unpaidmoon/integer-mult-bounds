"""Exact local full-column interface; no predecessor executable is imported.

Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORT_PATH = "research/p104-carrier-code-uniqueness/e8/ports.json"
PORT_SHA = "ba6a0b9cf76b7cccc1ce8b3d1aa78a4aa329b34d45aded694648f0cf43fc9fce"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate(data):
    require(sha256(data).hexdigest() == PORT_SHA, "port source hash")
    ports = json.loads(data)
    require(len(ports) == 104 and len(set(ports)) == 104, "port inventory")
    require(all(type(p) is int and 0 < p < 512 for p in ports), "port type")
    return ports


def ports():
    return authenticate((HERE.parents[1] / PORT_PATH).read_bytes())


def root(port):
    """Three times the A8-coordinate root; all arithmetic is integral."""
    if port.bit_count() == 3:
        return tuple(2 if port >> i & 1 else -1 for i in range(9))
    require(port.bit_count() == 7, "root weight")
    zero = [i for i in range(9) if not port >> i & 1]
    return tuple(3 * ((i == zero[0]) - (i == zero[1])) for i in range(9))


def gram(left, right):
    return Q(sum(a * b for a, b in zip(root(left), root(right))), 9)


def in_frame(port, normals):
    return all((port & n).bit_count() % 2 == 0 for n in normals)


def binary_rank(vectors):
    pivots = {}
    for original in vectors:
        value = original
        while value:
            top = value.bit_length() - 1
            if top not in pivots:
                pivots[top] = value
                break
            value ^= pivots[top]
    return len(pivots)


def xor_span(vectors):
    """Independent exponential span enumeration, used only for nine-bit data."""
    out = {0}
    for vector in vectors:
        out |= {x ^ vector for x in tuple(out)}
    return out


def add(left, right, coefficient=Q(1)):
    require(len(left) == len(right), "row width")
    return tuple(a + coefficient * b for a, b in zip(left, right))


def scale(row, coefficient):
    return tuple(coefficient * a for a in row)


def rank(rows):
    if not rows:
        return 0
    work = [[Q(x) for x in row] for row in rows]
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank row shape")
    pivot = 0
    for col in range(width):
        match = next((r for r in range(pivot, len(work)) if work[r][col]), None)
        if match is None:
            continue
        work[pivot], work[match] = work[match], work[pivot]
        divisor = work[pivot][col]
        work[pivot] = [x / divisor for x in work[pivot]]
        for r in range(len(work)):
            if r != pivot and work[r][col]:
                multiple = work[r][col]
                work[r] = [x - multiple * y for x, y in zip(work[r], work[pivot])]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def in_span(row, rows):
    return rank([*rows, row]) == rank(rows)


def replay(rows, events):
    out = list(rows)
    for event in events:
        require(len(event) == 4, "event shape")
        operation, target, source, coefficient = event
        require(type(target) is int and 0 <= target < len(out), "target index")
        require(type(source) is int and 0 <= source < len(out), "source index")
        if operation == "ADD":
            require(target != source, "ADD alias")
            out[target] = add(out[target], out[source], Q(coefficient))
        else:
            require(operation == "SCALE" and coefficient != 0, "SCALE contract")
            out[target] = scale(out[target], Q(coefficient))
    return out


def fixture():
    ps = ports()
    # Input symbols: all 104 Xs, all 104 Ys, one arbitrary helper h.
    width = 209
    x, y, z = 11, 19, 487
    common = [p for p in ps if in_frame(p, (x, y))]
    first = [p for p in common if in_frame(p, (455,))]
    second = [p for p in common if in_frame(p, (56,))]
    require(len(common) == 24 and len(first) == 16 and len(second) == 8,
            "section sizes")
    require(set(first).isdisjoint(second) and set(first) | set(second) == set(common),
            "section partition")
    require(z in first, "exceptional section")
    require(gram(x, y) == 1 and gram(x, z) == 1 and gram(y, z) == -1,
            "triangle signs")
    zero = tuple(Q(0) for _ in range(width))
    plus, minus, c, e, a, d = [list(zero) for _ in range(6)]
    for p in common:
        i = ps.index(p)
        plus[i], minus[i] = gram(x, p) / 2, gram(y, p) / 2
        if p == z:
            e[i] = plus[i]
        else:
            c[i] = plus[i]
            (a if p in first else d)[i] = plus[i]
    plus, minus, c, e, a, d = map(tuple, (plus, minus, c, e, a, d))
    require(plus == add(c, e) and minus == add(c, e, -1), "Gram response split")
    Y, h = list(zero), list(zero)
    Y[104 + ps.index(y)], h[-1] = Q(1), Q(1)
    Y, h = tuple(Y), tuple(h)
    incoming = [add(Y, e, 2), add(add(a, e, -1), h, -1), add(d, h)]
    expected = [add(Y, plus), minus, add(d, h)]
    return {"ports": ps, "common": common, "first": first, "second": second,
            "Y": Y, "h": h, "c": c, "e": e, "a": a, "d": d,
            "plus": plus, "minus": minus, "incoming": incoming,
            "expected": expected}


MEETING = (("ADD", 1, 2, 1), ("ADD", 0, 1, 1))
INVERSE = (("ADD", 0, 1, -1), ("ADD", 1, 2, -1))
OLD_MEETING = (("ADD", 1, 2, 1), ("ADD", 1, 0, -1),
               ("SCALE", 0, 0, 2), ("ADD", 0, 1, 1))


def endpoint(rows, target):
    require(rows == target, "full-column endpoint")


def cleanup_allowed(query, f):
    # Eliminating Y and h leaves d in span(W,q). This tests the actual
    # necessary-and-sufficient rowspace condition, not a support heuristic.
    require(not any(query[104:]), "cleanup query must be pure live")
    require(in_span(f["d"], [f["minus"], query]), "cleanup query lacks required quotient")


def dyadic_cleanup_coefficients(query, f):
    """Admit the scalar-ring version, without treating every scale as a unit."""
    cleanup_allowed(query, f)
    require(all(Q(v).denominator & (Q(v).denominator - 1) == 0 for v in query),
            "query coefficient is not dyadic")
    iu = f["ports"].index(f["first"][0])
    iv = f["ports"].index(f["second"][0])
    beta = query[iu] / f["minus"][iu]
    rho = query[iv] / f["d"][iv] - beta
    require(query == add(scale(f["d"], rho), f["minus"], beta),
            "query reconstruction")
    numerator = abs(rho.numerator)
    denominator = rho.denominator
    require(numerator != 0 and numerator & (numerator - 1) == 0
            and denominator & (denominator - 1) == 0,
            "cleanup scale is not a dyadic unit")
    return -1 / rho, beta / rho


def public_query_frame(query, ps, frame):
    """Only for a public query with no owned-delivered live component."""
    require(all(p in frame for p, value in zip(ps, query[:104]) if value),
            "public query support outside frame")


def source_hashes():
    names = ["README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "model.py", "verify.py", "test_controls.py"]
    return {name: sha256((HERE / name).read_bytes()).hexdigest() for name in names}
