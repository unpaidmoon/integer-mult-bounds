#!/usr/bin/env python3
"""Exact corroboration of PROOF.md; @CubeJerry / OpenAI Codex; Apache-2.0.

No predecessor executable code is imported. All guards survive Python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import product
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BASE = '2485805a6d47f36ea83ddde6327d453ac82d44dc'
INPUTS = {
    'research/dyadic-cubic-repair/PROOF.md':
    '1296f12278e198b6a22d8d88355cd58c1ee4fc2ab0e6941721614bb06cb1e7d5',
    'research/cubic-pure-b-boundary/PROOF.md':
    'f97362ac07cd0ff1fff0d7bb74e5497996eb21f12282825731e779cbed5e0792',
}
PREDECESSOR_HEAD = '3d21b913efac1e3731bee7f0f4f4a8a84fecec37'
PREDECESSOR_BLOB = 'eb613b0b3c723838caa46c9cebeb71c64b1fcf04'


class Rejected(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise Rejected(reason)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'DUPLICATE_JSON_KEY')
        out[key] = value
    return out


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def authenticate():
    manifest = read_json(HERE / 'SOURCES.json')
    need(manifest['base_commit'] == BASE, 'SOURCE_BASE')
    rows = {row['path']: row for row in manifest['files']}
    for path, digest in INPUTS.items():
        need(rows[path]['usage'] == 'input' and rows[path]['sha256'] == digest,
             'SOURCE_DECLARATION')
        need(sha256((ROOT / path).read_bytes()).hexdigest() == digest,
             'SOURCE_BYTES:' + path)
    row = manifest['retained_predecessor']
    need(row['head'] == PREDECESSOR_HEAD and row['git_blob'] == PREDECESSOR_BLOB
         and row['local_path'] == 'sources/pr6246-PROOF.md', 'PREDECESSOR_DECLARATION')
    data = (HERE / row['local_path']).read_bytes()
    blob = sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    need(blob == PREDECESSOR_BLOB, 'PREDECESSOR_BYTES')
    need(sha256(data).hexdigest() == row['sha256'], 'PREDECESSOR_SHA256')


def dyadic(x):
    return x.denominator & (x.denominator - 1) == 0


def pow2(n):
    return n > 0 and n & (n - 1) == 0


def moments(r):
    s1 = F(r*(r-1), 2)
    return s1, F(r*(r-1)*(2*r-1), 6), s1*s1


def weights(r, d):
    need(type(r) is int and r >= 3, 'ARITY_DOMAIN')
    need(d != 0, 'ZERO_SPACING')
    s1, s2, _ = moments(r)
    w2 = (s2-d*s1)/(2*d*d)
    w1 = (2*d*s1-s2)/(d*d)
    return -w1-w2, w1, w2


def check_decomposition(r, d, ws, require_ring=True):
    need(type(r) is int and r >= 3, 'ARITY_DOMAIN')
    need(d != 0, 'ZERO_SPACING')
    need(len(ws) == 3 and all(w != 0 for w in ws), 'NONZERO_THREE_QUERIES')
    if require_ring:
        need(dyadic(d) and all(dyadic(w) for w in ws), 'NON_DYADIC')
    got = tuple(sum(w*(i*d)**k for i, w in enumerate(ws)) for k in range(4))
    need(got == (F(0),)+moments(r), 'DEFECT_COEFFICIENTS')


# Polynomials in r,d: exact coefficient identities, not evaluation samples.
def add(*ps):
    out = {}
    for p in ps:
        for k, value in p.items():
            out[k] = out.get(k, F(0))+value
    return {k: v for k, v in out.items() if v}


def mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            key = i+k, j+l
            out[key] = out.get(key, F(0))+x*y
    return {k: v for k, v in out.items() if v}


def scale(c, p):
    return {k: c*v for k, v in p.items() if c*v}


def power(p, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def shift_r(p):
    out = {}
    for (i, j), value in p.items():
        for k in range(i+1):
            out = add(out, {(k, j): value*comb(i, k)})
    return out


def polynomial_checks():
    one, r, d = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}
    rm1 = add(r, scale(-1, one))
    s1 = scale(F(1, 2), mul(r, rm1))
    s2 = scale(F(1, 6), mul(mul(r, rm1), add(scale(2, r), scale(-1, one))))
    ms = [{}, s1, s2, mul(s1, s1)]
    count = 0
    for k, p in enumerate(ms[1:], 1):
        need(add(shift_r(p), scale(-1, p), scale(-1, power(r, k))) == {},
             'POWER_SUM_RECURRENCE')
        need(p.get((0, 0), 0) == 0, 'POWER_SUM_BASE')
        count += 1
    factored = mul(add(scale(2, d), scale(-1, r)),
                   add(scale(2, d), scale(-1, r), one))
    expanded = add(scale(4, power(d, 2)),
                   scale(-2, mul(add(scale(2, r), scale(-1, one)), d)), mul(r, rm1))
    need(factored == expanded, 'SPACING_FACTORIZATION')
    count += 1
    for branch in (0, 1):
        u = r if branch == 0 else rm1
        if branch == 0:
            ns = [scale(-1, mul(rm1, add(scale(5, r), scale(2, one)))),
                  scale(4, add(power(r, 2), scale(-1, one))),
                  mul(rm1, add(r, scale(-2, one)))]
        else:
            ns = [scale(-1, mul(r, add(scale(5, r), scale(-7, one)))),
                  scale(4, mul(r, add(r, scale(-2, one)))), mul(r, add(r, one))]
        for k in range(4):
            lhs = add(*(mul(n, power(scale(F(i, 2), u), k)) for i, n in enumerate(ns)))
            need(lhs == scale(6, mul(u, ms[k])), 'UNIFORM_COEFFICIENT_IDENTITY')
            count += 1
    return count


def children(r):
    return [('cube', F(1)), ('shear', F(1))]*r


def repair(r, u):
    need(u in (r, r-1), 'SPACING_BRANCH')
    d = F(u, 2)
    w0, w1, w2 = weights(r, d)
    check_decomposition(r, d, (w0, w1, w2))
    out = [] if u == r else [('shear', F(-1))]
    return out+[('cube', -w2), ('shear', -d), ('cube', -w1),
                ('shear', -d), ('cube', -w0)]


def inverse(events):
    return [(kind, -value) for kind, value in reversed(events)]


def symbolic(events, initial=None):
    # y coordinates: Y,A^3,A^2B,AB^2,B^3. a=alpha*A+beta*B; b=B.
    alpha, beta, y = initial or (F(1), F(0), (F(1), F(0), F(0), F(0), F(0)))
    y = list(y)
    for kind, value in events:
        need(dyadic(value), 'EVENT_RING')
        if kind == 'shear':
            beta += value
        elif kind == 'cube':
            for k in range(4):
                y[k+1] += value*comb(3, k)*alpha**(3-k)*beta**k
        elif kind == 'cube_b':
            y[4] += value
        else:
            raise Rejected('EVENT_ALPHABET')
    return alpha, beta, tuple(y)


def check_program(r, events):
    need(events[:2*r] == children(r), 'RETAINED_CHILDREN')
    alpha, beta, y = symbolic(events)
    need((alpha, beta) == (1, 0), 'SOURCES_NOT_RESTORED')
    need(y == (1, r, 0, 0, 0), 'WRONG_EAGER_OUTPUT')
    need(symbolic(inverse(events), (alpha, beta, y))
         == (1, 0, (1, 0, 0, 0, 0)), 'FULL_INVERSE')


def numeric(events, state):
    y, a, b = state
    for kind, value in events:
        if kind == 'shear':
            a += value*b
        elif kind == 'cube':
            y += value*a*a*a
        elif kind == 'cube_b':
            y += value*b*b*b
        else:
            raise Rejected('EVENT_ALPHABET')
    return y, a, b


def controls():
    passed = []
    def rejects(name, reason, call):
        try:
            call()
        except Rejected as exc:
            need(str(exc) == reason, 'WRONG_REJECTION:'+name)
        else:
            raise Rejected('CONTROL_ACCEPTED:'+name)
        passed.append(name)
    ws = weights(33, F(16))
    prefix, tail = children(33), repair(33, 32)
    rejects('r2_outside_classification', 'ARITY_DOMAIN', lambda: weights(2, F(1)))
    rejects('boolean_arity', 'ARITY_DOMAIN', lambda: weights(True, F(1)))
    rejects('zero_spacing', 'ZERO_SPACING', lambda: weights(33, F(0)))
    rejects('r33_wrong_branch_has_odd_denominator', 'NON_DYADIC',
            lambda: check_decomposition(33, F(33, 2), weights(33, F(33, 2))))
    rejects('r14_equal_step_does_not_imply_general_floor', 'NON_DYADIC',
            lambda: check_decomposition(14, F(13, 2), weights(14, F(13, 2))))
    rejects('wrong_spacing_even_with_fitted_lower_moments', 'DEFECT_COEFFICIENTS',
            lambda: check_decomposition(33, F(15), weights(33, F(15)), False))
    rejects('changed_weight', 'DEFECT_COEFFICIENTS',
            lambda: check_decomposition(33, F(16), (ws[0], ws[1]+F(1, 32), ws[2])))
    rejects('omitted_initial_shear', 'SOURCES_NOT_RESTORED',
            lambda: check_program(33, prefix+tail[1:]))
    swapped = [tail[1], tail[0]]+tail[2:]
    rejects('query_before_initial_shear', 'WRONG_EAGER_OUTPUT',
            lambda: check_program(33, prefix+swapped))
    rejects('omitted_final_query', 'WRONG_EAGER_OUTPUT',
            lambda: check_program(33, prefix+tail[:-1]))
    rejects('fused_or_missing_original_child', 'RETAINED_CHILDREN',
            lambda: check_program(33, prefix[2:]+tail))
    altered = tail.copy()
    altered[4] = ('shear', F(-15))
    rejects('wrong_return_shear', 'SOURCES_NOT_RESTORED',
            lambda: check_program(33, prefix+altered))
    rejects('output_feedback_outside_alphabet', 'EVENT_ALPHABET',
            lambda: symbolic([('source_from_y', F(1))]))
    rejects('duplicate_receipt_key', 'DUPLICATE_JSON_KEY',
            lambda: json.loads('{"r":33,"r":129}', object_pairs_hook=unique_object))
    return passed


def evidence():
    authenticate()
    polynomial_count = polynomial_checks()
    eligible, classification_rows = [], []
    for r in range(3, 1025):
        for u in (r, r-1):
            ws = weights(r, F(u, 2))
            check_decomposition(r, F(u, 2), ws, False)
            valid = all(dyadic(w) for w in ws)
            need(valid == pow2(u), 'FINITE_CLASSIFICATION')
            classification_rows.append([r, u, list(map(str, ws)), valid])
            if valid:
                eligible.append([r, u])
    spacing_count = 0
    for r in range(3, 41):
        for numerator in range(-32, 257):
            if numerator == 0:
                continue
            d = F(numerator, 8)
            ws = weights(r, d)
            actual = sum(w*(i*d)**3 for i, w in enumerate(ws)) == moments(r)[2]
            need(actual == (2*d in (r, r-1)), 'FINITE_SPACING_EXHAUSTION')
            spacing_count += 1
    large = []
    for s in [1, 2, 3, 4, 5, 7, 11, 17, 31, 64, 128]:
        r, u = 2**s+1, 2**s
        ws = weights(r, F(u, 2))
        check_decomposition(r, F(u, 2), ws)
        s1, s2, s3 = moments(r)
        deferred = (F(1), F(r), (F(1), F(r), 3*s1, 3*s2, s3))
        tail = repair(r, u)
        eager = symbolic(tail, deferred)
        need(eager == (1, 0, (1, r, 0, 0, 0)), 'LARGE_REPAIR')
        need(symbolic(inverse(tail), eager) == deferred, 'LARGE_REPAIR_INVERSE')
        large.append({'s': s, 'r': str(r), 'weights_w0_w1_w2': list(map(str, ws))})
    programs, symbolic_events = [], 0
    for r, u in eligible:
        if r > 257:
            continue
        tail = repair(r, u)
        word = children(r)+tail
        check_program(r, word)
        deferred = symbolic(children(r))
        need(symbolic(inverse(tail), symbolic(word)) == deferred, 'REPAIR_INVERSE')
        programs.append([r, u])
        symbolic_events += 3*len(word)+2*r+len(tail)
    # PR6212's unequal-step positive scope control, not a new construction.
    scope_tail = [('shear', F(-9)), ('cube', F(-91)), ('shear', F(-1)),
                  ('cube', F(91)), ('shear', F(-4)), ('cube_b', F(-2730))]
    check_program(14, children(14)+scope_tail)
    centered_tail = [('shear', F(-85)), ('cube', F(1)), ('shear', F(70)),
                     ('cube', F(-34)), ('shear', F(-35)), ('cube', F(33))]
    check_program(50, children(50)+centered_tail)
    numeric_cases = numeric_events = 0
    values = [F(-3, 2), F(0), F(5, 4)]
    for r in [3, 4, 16, 33, 65, 129, 257]:
        u = r if pow2(r) else r-1
        word = children(r)+repair(r, u)
        for state in product(values, repeat=3):
            out = numeric(word, state)
            y, a, b = state
            need(out == (y+r*a**3, a, b), 'DIRTY_ENDPOINT')
            need(numeric(inverse(word), out) == state, 'DIRTY_FULL_INVERSE')
            numeric_cases += 1
            numeric_events += 2*len(word)
    rejected = controls()
    invoice = Counter(f'{kind}:{value}' for kind, value in repair(33, 32))
    return {
        'status': 'PASS_CUBIC_EQUAL_STEP_CLASSIFICATION',
        'scope': 'Written all-r equal-step theorem with exact finite corroboration; no new kappa.',
        'polynomial_identities': polynomial_count,
        'arity_domain': [3, 1024], 'rational_decompositions': len(classification_rows),
        'classification_sha256': sha256(canonical(classification_rows).encode()).hexdigest(),
        'eligible_arity_and_twice_spacing': eligible,
        'spacing_scan': {'arity': [3, 40], 'd': 'k/8; -32<=k<=256; k!=0', 'cases': spacing_count},
        'large_new_branch_fixtures': large, 'literal_symbolic_programs': programs,
        'literal_symbolic_events': symbolic_events,
        'dirty_numeric_cases': numeric_cases,
        'dirty_numeric_events_including_inverses': numeric_events,
        'unequal_step_positive_scope_control': 'PR6212 r14: three integer queries accepted',
        'centered_equal_step_scope_control': 'r50: slopes -35,0,35 accepted; zero must be at an end in the theorem',
        'negative_controls': rejected,
        'r33': {'weights_w0_w1_w2': list(map(str, weights(33, F(16)))),
                'defect_A2B_AB2_B3': list(map(str, (3*moments(33)[0], 3*moments(33)[1], moments(33)[2]))),
                'repair_event_prices': dict(sorted(invoice.items())), 'original_children_retained': 33},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true', help='emit evidence without receipt comparison')
    args = parser.parse_args()
    result = evidence()
    if not args.emit:
        need(canonical(result) == canonical(read_json(HERE/'RESULT.json')), 'RECEIPT_MISMATCH')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
