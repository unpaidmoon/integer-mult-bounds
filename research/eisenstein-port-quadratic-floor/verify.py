#!/usr/bin/env python3
"""Exact finite corroboration for the written port-quadratic theorem."""

import hashlib
import itertools
import json
from pathlib import Path
import sys

MAX_DIMENSION = 5


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_form(rows):
    n = len(rows)
    require(0 <= n <= MAX_DIMENSION, "dimension outside 0..5")
    require(all(type(row) is int and 0 <= row < (1 << n)
                for row in rows), "invalid binary row")
    for i in range(n):
        require(not (rows[i] >> i) & 1, "nonzero alternating diagonal")
        for j in range(n):
            require((rows[i] >> j) & 1 == (rows[j] >> i) & 1,
                    "nonsymmetric form")


def binary_rank(rows):
    pivots = {}
    for original in rows:
        value = original
        for bit in range(MAX_DIMENSION - 1, -1, -1):
            if not (value >> bit) & 1:
                continue
            if bit in pivots:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return len(pivots)


def pairing(rows, x, y):
    return sum(((x >> i) & 1) * ((rows[i] & y).bit_count() & 1)
               for i in range(len(rows))) & 1


def isotropic_basis(rows):
    validate_form(rows)
    n = len(rows)
    remaining = [1 << i for i in range(n)]
    answer = []
    for _ in range(n // 2 + 1):
        pair = next(((i, j) for i in range(len(remaining))
                     for j in range(i + 1, len(remaining))
                     if pairing(rows, remaining[i], remaining[j])), None)
        if pair is None:
            answer.extend(remaining)
            break
        i, j = pair
        e, f = remaining[i], remaining[j]
        answer.append(e)
        remaining = [v ^ (e if pairing(rows, v, f) else 0)
                     ^ (f if pairing(rows, v, e) else 0)
                     for k, v in enumerate(remaining) if k not in (i, j)]
    else:
        raise ValueError("symplectic elimination exhausted")
    require(binary_rank(answer) == len(answer), "dependent construction")
    require(all(pairing(rows, x, y) == 0
                for x in answer for y in answer), "nonisotropic construction")
    require(2 * (n - len(answer)) == binary_rank(rows), "wrong dimension")
    return tuple(answer)


def subspaces(n):
    """Enumerate subspaces by intersection with each coordinate hyperplane."""
    require(type(n) is int and 0 <= n <= MAX_DIMENSION, "bad space dimension")
    spaces = [((0,), ())]
    for k in range(n):
        updated = list(spaces)
        for elements, basis in spaces:
            remaining = set(range(1 << k))
            for representative in range(1 << k):
                if representative not in remaining:
                    continue
                coset = {representative ^ x for x in elements}
                remaining.difference_update(coset)
                v = representative | (1 << k)
                extension = tuple(sorted(elements + tuple(x ^ v for x in elements)))
                updated.append((extension, basis + (v,)))
        spaces = updated
    require(len({elements for elements, _ in spaces}) == len(spaces),
            "duplicate subspace")
    return tuple(spaces)


def quadratic_value(edges, x):
    return sum(((x >> i) & 1) * ((x >> j) & 1) for i, j in edges) & 1


def truth_affine(values, elements, basis, offset):
    """Test affine truth values using all generator translations, without B."""
    origin = values[offset]
    for v in elements:
        for e in basis:
            if values[offset ^ v ^ e] ^ values[offset ^ v] != values[offset ^ e] ^ origin:
                return False
    return True


def form_rows(n, edges):
    rows = [0] * n
    for i, j in edges:
        rows[i] |= 1 << j
        rows[j] |= 1 << i
    return tuple(rows)


def check_quadratic_forms():
    counts = {"quadratic_forms": 0, "subspace_restrictions": 0,
              "translated_restrictions": 0, "attaining_subspaces": 0}
    rank_profile = {}
    for n in range(MAX_DIMENSION + 1):
        spaces = subspaces(n)
        possible = tuple(itertools.combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = tuple(e for i, e in enumerate(possible) if (mask >> i) & 1)
            rows = form_rows(n, edges)
            basis = isotropic_basis(rows)
            target = len(basis)
            values = tuple(quadratic_value(edges, x) for x in range(1 << n))
            observed = -1
            for elements, candidate in spaces:
                affine = truth_affine(values, elements, candidate, 0)
                if affine:
                    observed = max(observed, len(candidate))
                    if len(candidate) == target:
                        counts["attaining_subspaces"] += 1
                counts["subspace_restrictions"] += 1
                # Every translation on all forms through dimension four.
                if n <= 4:
                    for offset in range(1 << n):
                        require(truth_affine(values, elements, candidate, offset)
                                == affine, "translation changed criterion")
                        counts["translated_restrictions"] += 1
            require(observed == target, "truth-table maximum disagrees")
            restricted = tuple(x for x in range(1 << n)
                               if binary_rank(basis + (x,)) == target)
            require(truth_affine(values, restricted, basis, 0), "attainer not affine")
            rank_profile[str(binary_rank(rows))] = rank_profile.get(str(binary_rank(rows)), 0) + 1
            counts["quadratic_forms"] += 1
    counts["rank_profile"] = rank_profile
    return counts


def coordinate_loss(values, n):
    """Independent complete coordinate-face search, including nonzero fixings."""
    for loss in range(n + 1):
        for fixed in itertools.combinations(range(n), loss):
            free = tuple(i for i in range(n) if i not in fixed)
            basis = tuple(1 << i for i in free)
            elements = tuple(sum(((mask >> j) & 1) << i
                                 for j, i in enumerate(free))
                             for mask in range(1 << len(free)))
            for pattern in range(1 << loss):
                offset = sum(((pattern >> j) & 1) << i
                             for j, i in enumerate(fixed))
                if truth_affine(values, elements, basis, offset):
                    return loss
    raise ValueError("coordinate search exhausted")


def check_strict_fixture():
    # u0,u1,v0,v1,z. All four K2,2 monomials are retained.
    edges = ((0, 2), (0, 3), (1, 2), (1, 3))
    values = tuple(quadratic_value(edges, x) for x in range(32))
    rows = form_rows(5, edges)
    require(binary_rank(rows) == 2, "fixture polar rank")
    require(coordinate_loss(values, 5) == 2, "fixture coordinate loss")
    require(len(isotropic_basis(rows)) == 4, "fixture affine loss")
    # The literal hyperplane u0=u1 has four independent coordinates.
    hyperplane = tuple(x for x in range(32) if (x & 1) == ((x >> 1) & 1))
    require(all(values[x] == 0 for x in hyperplane), "hyperplane does not kill q")
    recovered = 0
    for port in range(40):
        for x in range(32):
            sent = x ^ (values[x] << 4) if port == 0 else x
            decoded = sent ^ (values[sent] << 4) if port == 0 else sent
            require(decoded == x, "local decoder failure")
            recovered += 1
    return {"ports": 40, "bits_per_port": 5, "coordinate_floor": 198,
            "polar_floor": 199, "actual_fixture_charge": 200,
            "local_receiver_cases": recovered, "hyperplane_inputs": len(hyperplane)}


def check_vector_quadratic_maps():
    """Check simultaneous restriction across two ports and three output bits."""
    configurations = 0
    products = 0
    spaces = subspaces(2)
    for column_a in range(8):
        for column_b in range(8):
            expected = 4 - bool(column_a) - bool(column_b)
            maximum = -1
            for left, lb in spaces:
                for right, rb in spaces:
                    domain = tuple(x | (y << 2) for x in left for y in right)
                    basis = lb + tuple(v << 2 for v in rb)
                    values = tuple((column_a if (x & 3) == 3 else 0)
                                   ^ (column_b if (x >> 2) == 3 else 0)
                                   ^ ((x & 1) | (((x >> 3) & 1) << 1))
                                   for x in range(16))
                    affine = truth_affine(values, domain, basis, 0)
                    if affine:
                        maximum = max(maximum, len(basis))
                    products += 1
            require(maximum == expected, "product maximum disagrees")
            # Distinct nonzero columns may also be equal; independence of ports
            # prevents cancellation from increasing the product restriction.
            configurations += 1
    return {"vector_maps": configurations, "product_subspace_restrictions": products}


def check_controls():
    cases = [(((1,),), "invalid binary row"),
             ((1,), "nonzero alternating diagonal"),
             ((2, 0), "nonsymmetric form"),
             ((8, 0), "invalid binary row"),
             ((0,) * 6, "dimension outside 0..5"),
             ((-1,), "invalid binary row")]
    for rows, reason in cases:
        try:
            isotropic_basis(rows)
        except ValueError as error:
            require(str(error) == reason, "wrong rejection reason")
        else:
            raise ValueError("invalid form accepted")
    # Model counterexamples: cross-port coupling and two independent forms.
    rows = form_rows(2, ((0, 1),))
    require(pairing(rows, 1, 2) == 1, "rank mutant survived")
    require(pairing(rows, 1, 1) == 0, "alternation mutant survived")
    # A diagonal x=y kills cross-port xy but destroys independent demands.
    cross = (0, 0, 0, 1)
    require(truth_affine(cross, (0, 3), (3,), 0), "diagonal control")
    require(not truth_affine(cross, (0, 1, 2, 3), (1, 2), 0),
            "independent-product control")
    # q1=x0*x1 and q2=x0*x2 have separate maximal planes whose intersection
    # need not be maximal. Taking only the rank of q1+q2 misses this contract.
    q1 = tuple(quadratic_value(((0, 1),), x) for x in range(8))
    q2 = tuple(quadratic_value(((0, 2),), x) for x in range(8))
    plane = (0, 3, 4, 7)
    require(not truth_affine(q2, plane, (3, 4), 0), "second-form control")
    require(truth_affine(q1, (0, 1), (1,), 0), "positive truth control")
    return {"invalid_forms_rejected": len(cases), "boundary_controls": 4}


def authenticate_sources(package):
    manifest_path = package / "SOURCES.json"
    require(manifest_path.stat().st_size <= 1_048_576, "manifest exceeds byte bound")
    manifest = json.loads(manifest_path.read_text())
    require(len(manifest["files"]) <= 8, "source inventory exceeds bound")
    inputs = {}
    for source in manifest["files"]:
        if source["usage"] != "input":
            continue
        path = package.parent.parent / source["path"]
        require(path.stat().st_size <= 1_048_576, "source exceeds byte bound")
        payload = path.read_bytes()
        require(len(payload) <= 1_048_576, "source exceeds byte bound")
        digest = hashlib.sha256(payload).hexdigest()
        require(digest == source["sha256"], "changed source: " + source["path"])
        inputs[source["path"]] = digest
    require(len(inputs) == 4, "source inventory changed")
    return inputs


def main():
    require(len(sys.argv) == 1, "no arguments accepted")
    package = Path(__file__).resolve().parent
    inputs = authenticate_sources(package)
    evidence = {**check_quadratic_forms(), **check_strict_fixture(),
                **check_vector_quadratic_maps(), **check_controls()}
    names = ("README.md", "PROOF.md", "verify.py", "TASK.json", "SOURCES.json", "VERIFY.json")
    sources = {name: hashlib.sha256((package / name).read_bytes()).hexdigest()
               for name in names}
    print("PASS_EISENSTEIN_PORT_QUADRATIC_FLOOR " + json.dumps(
        {"claim_type": "scoped proof with finite corroboration", "evidence": evidence,
         "package_sha256": sources, "input_sha256": inputs}, sort_keys=True))


if __name__ == "__main__":
    main()
