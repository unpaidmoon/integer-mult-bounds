#!/usr/bin/env python3
"""Separate exact coefficient-elimination path; stdlib only, no primary imports.

By @CubeJerry with substantial OpenAI Codex assistance; Apache-2.0.
This is another implementation by the same AI-assisted contributor, not a
claim of independent human review or a formal proof kernel.
"""
from fractions import Fraction
from hashlib import sha1, sha256
from math import comb
from pathlib import Path
import argparse
import json

F = Fraction
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def authenticate():
    for relative, expected in [
        ('research/dyadic-cubic-repair/PROOF.md',
         '1296f12278e198b6a22d8d88355cd58c1ee4fc2ab0e6941721614bb06cb1e7d5'),
        ('research/cubic-pure-b-boundary/PROOF.md',
         'f97362ac07cd0ff1fff0d7bb74e5497996eb21f12282825731e779cbed5e0792'),
    ]:
        require(sha256((ROOT/relative).read_bytes()).hexdigest() == expected,
                'INPUT_BYTES:'+relative)
    data = (HERE/'sources/pr6246-PROOF.md').read_bytes()
    require(sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            == 'eb613b0b3c723838caa46c9cebeb71c64b1fcf04', 'RETAINED_PROOF_BYTES')


def append_block(left, right):
    """Concatenate [0,n) with n+[0,m); zeroth moment is its length."""
    n = left[0]
    return tuple(left[k]+sum(comb(k, j)*n**(k-j)*right[j]
                              for j in range(k+1)) for k in range(4))


def block_moments(n):
    total, block = (0, 0, 0, 0), (1, 0, 0, 0)
    while n:
        if n % 2:
            total = append_block(total, block)
        block = append_block(block, block)
        n //= 2
    return total


def cube_column(alpha, beta):
    return tuple(F(comb(3, k))*alpha**(3-k)*beta**k for k in range(4))


def eliminate(columns, target):
    """Fit A^3,A^2B,AB^2 by generic exact row reduction, then test B^3."""
    rows = [[F(columns[j][i]) for j in range(3)]+[F(target[i])] for i in range(3)]
    for pivot in range(3):
        source = next((i for i in range(pivot, 3) if rows[i][pivot]), None)
        require(source is not None, 'SINGULAR_DIRECTIONS')
        rows[pivot], rows[source] = rows[source], rows[pivot]
        divisor = rows[pivot][pivot]
        rows[pivot] = [x/divisor for x in rows[pivot]]
        for i in range(3):
            if i != pivot:
                factor = rows[i][pivot]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[pivot])]
    ws = tuple(rows[i][-1] for i in range(3))
    residual = tuple(sum(ws[j]*columns[j][i] for j in range(3))-target[i]
                     for i in range(4))
    return ws, residual


def ring_member(q):
    denominator = q.denominator
    while denominator % 2 == 0:
        denominator //= 2
    return denominator == 1


def is_power_two(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


def target(r):
    _, m1, m2, m3 = block_moments(r)
    return (F(0), F(3*m1), F(3*m2), F(m3))


def fit(r, d, scales=(F(1), F(1), F(1))):
    columns = [cube_column(alpha, alpha*i*d) for i, alpha in enumerate(scales)]
    return eliminate(columns, target(r))


def integrate_tail(r, directions, ws):
    """Construct and execute a descending source walk from the actual endpoint.

    This derives shears from successive directions, without the primary's
    prewritten six-event recipe. Output starts at the uncorrected defect.
    """
    slope = F(r)
    residual = list(target(r))
    events = []
    for direction, weight in sorted(zip(directions, ws), reverse=True):
        if direction != slope:
            events.append(('L', direction-slope))
            slope = direction
        events.append(('Q', -weight))
        residual = [x-weight*y for x, y in zip(residual, cube_column(F(1), slope))]
    require(slope == 0, 'TAIL_SOURCE')
    require(residual == [0, 0, 0, 0], 'TAIL_OUTPUT')
    return events


def run():
    authenticate()
    records, eligible, scaled_tests = [], [], 0
    for r in range(3, 258):
        sums = block_moments(r)
        literal = tuple(sum(j**k for j in range(r)) for k in range(4))
        require(sums == literal, 'BLOCK_VS_LITERAL_READERS')
        for u in (r, r-1):
            d = F(u, 2)
            ws, residual = fit(r, d)
            require(residual == (0, 0, 0, 0), 'SOLVED_CUBIC')
            valid = all(ring_member(w) for w in ws)
            require(valid == is_power_two(u), 'EXACT_CLASSIFICATION')
            records.append([r, u, list(map(str, ws)), valid])
            if valid:
                eligible.append([r, u])
                events = integrate_tail(r, [F(0), d, 2*d], ws)
                require(sum(kind == 'Q' for kind, _ in events) == 3, 'QUERY_COUNT')
                require(sum(kind == 'L' for kind, _ in events) == (2 if u == r else 3),
                        'SHEAR_COUNT')
            # Unit rescalings preserve feasibility; odd nonunit rescalings
            # cannot turn any excluded normalized weight into a dyadic one.
            for scales in [(F(1, 2), F(-2), F(4)), (F(3), F(-5, 2), F(7, 4))]:
                gammas, res = fit(r, d, scales)
                require(res == (0, 0, 0, 0), 'NONMONIC_IDENTITY')
                require(tuple(g*a**3 for g, a in zip(gammas, scales)) == ws,
                        'NORMALIZATION')
                actual = all(ring_member(g) for g in gammas)
                require(not actual or valid, 'NONMONIC_FALSE_ESCAPE')
                if scales[0] == F(1, 2):
                    require(actual == valid, 'UNIT_RESCALE')
                scaled_tests += 1
    large = []
    for s in [1, 2, 5, 7, 11, 17, 31, 64, 128]:
        r, d = 2**s+1, F(2**s, 2)
        ws, residual = fit(r, d)
        require(residual == (0, 0, 0, 0) and all(ring_member(w) for w in ws),
                'LARGE_BINARY_BLOCK')
        integrate_tail(r, [F(0), d, 2*d], ws)
        large.append([s, str(r), list(map(str, ws))])
    ws33, residual = fit(33, F(16))
    require(ws33 == (F(-869, 32), F(341, 16), F(187, 32)) and not any(residual),
            'R33_FIXED_FIXTURE')
    centered_columns = [cube_column(F(1), F(t)) for t in (-35, 0, 35)]
    centered_ws, centered_residual = eliminate(centered_columns, target(50))
    require(centered_ws == (-1, -33, 34) and not any(centered_residual),
            'CENTERED_POSITIVE_SCOPE_CONTROL')
    # Distinct failure cases, checked against the actual fourth coefficient.
    controls = []
    for r, d in [(33, F(15)), (33, F(-16)), (33, F(1, 3)), (129, F(65))]:
        _, residual = fit(r, d)
        require(residual[:3] == (0, 0, 0) and residual[3] != 0,
                'WRONG_SPACING_CONTROL')
        controls.append(f'wrong_spacing:r={r}:d={d}')
    try:
        fit(33, F(0))
    except ValueError as exc:
        require(str(exc) == 'SINGULAR_DIRECTIONS', 'SINGULAR_REASON')
        controls.append('zero_spacing_singular')
    else:
        raise ValueError('ZERO_SPACING_ACCEPTED')
    # The r14 Pell repair is rational with coefficient 91/11; it cannot be
    # smuggled into R by multiplying its forms by nonzero dyadic scalars.
    require(not ring_member(F(91, 11)), 'PELL_DENOMINATOR_CONTROL')
    controls.append('r14_rational_two_query_weight_not_dyadic')
    return {'status': 'PASS_CUBIC_EQUAL_STEP_CROSSCHECK',
            'method': 'binary block concatenation; generic rational elimination; normalized nonmonic forms',
            'arity_domain': [3, 257], 'eliminated_systems': len(records),
            'systems_sha256': sha256(encode(records).encode()).hexdigest(),
            'eligible_arity_and_twice_spacing': eligible,
            'nonmonic_systems': scaled_tests, 'large_new_branch_fixtures': large,
            'centered_scope_control': 'r50 weights -1,-33,34 on slopes -35,0,35',
            'negative_controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = run()
    if not args.emit:
        expected = json.loads((HERE/'CROSSCHECK.json').read_text(encoding='utf-8'))
        require(encode(result) == encode(expected), 'CROSSCHECK_RECEIPT_MISMATCH')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
