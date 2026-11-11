"""Independent changing-column junction audit, with no author-junction imports.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance (research worker A).
Nick Petalas retains the authenticated PR6280 source emitter; Ali Romman the
PR5602 scalar tariff. New checker material is Apache-2.0.
"""
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import product
from pathlib import Path
import argparse
import json

EMITTER_SHA = '9d7b71ed4da90360f8a0f15b7a89599340efbb4eb1ff40054e11e621f85df5bf'
EMITTER_BLOB = '9ead98d5735474d1fd35b101a1f4d50426b7e943'
TARIFF_SHA = '5f0678c768544517780d3511995faf0d7062748e7e780c0adb5c4d9c2749a925'


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def source(package):
    raw = (package / 'source/compiler.py').read_bytes()
    need(sha256(raw).hexdigest() == EMITTER_SHA, 'SOURCE_SHA')
    need(sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
         == EMITTER_BLOB, 'SOURCE_BLOB')
    tariff = package.parents[1] / 'research/p104-coupled-helper-bases/local.py'
    need(sha256(tariff.read_bytes()).hexdigest() == TARIFF_SHA, 'TARIFF_SHA')
    namespace = {'__name__': 'authenticated_source_compiler'}
    exec(compile(raw, 'authenticated_source_compiler.py', 'exec'), namespace)
    return namespace['compile_exchange']


def execute(ops, state):
    state = list(map(F, state))
    for name, destination, origin, coefficient in ops:
        need(type(destination) is int and type(origin) is int
             and 0 <= destination < len(state) and 0 <= origin < len(state), 'ROLES')
        if name == 'ADD':
            need(destination != origin, 'DISTINCT_ROLES')
            state[destination] += coefficient * state[origin]
        else:
            need(name == 'SCALE' and destination == origin and coefficient == -1,
                 'SIGN_ONLY')
            state[destination] *= coefficient
    return state


def price_coefficient(q):
    q = F(q)
    n, d = abs(q.numerator), q.denominator
    need(n > 0, 'NONZERO_PRICE')
    bits, ones, halves = 0, 0, 0
    while n:
        n, digit = divmod(n, 2)
        bits += 1
        ones += digit
    while d > 1:
        d, rem = divmod(d, 2)
        need(rem == 0, 'DYADIC_PRICE')
        halves += 1
    return 2 * (2 + bits + ones + halves)


def price(ops):
    return sum(2 if name == 'SCALE' else price_coefficient(q)
               for name, _, _, q in ops)


def junction(a, b, d):
    a, b, d = (list(map(F, row)) for row in (a, b, d))
    need(len(a) == len(b) == len(d) > 0, 'DIMENSIONS')
    need(sum(x * y for x, y in zip(a, b)) ==
         sum(x * y for x, y in zip(a, d)) == 1, 'DUAL_PAIR')
    n = len(a)
    lower = [('ADD', n, i, q) for i, q in enumerate(a) if q]
    upper = [('ADD', i, n, x - y) for i, (x, y) in enumerate(zip(b, d)) if x != y]
    negative = [(name, dst, src, -q) for name, dst, src, q in lower]
    return negative + upper + lower


def target(a, b, d, state):
    delta = state[-1] - sum(x * y for x, y in zip(a, state[:-1]))
    return [x + (left - right) * delta
            for x, left, right in zip(state[:-1], b, d)] + [state[-1]]


def columns(ops, width):
    return [execute(ops, [int(i == j) for i in range(width)]) for j in range(width)]


def nonlinear_macro(enter, leave, transition, state, first, second, separate):
    state = execute(enter, state)
    state[-1] = first(state[-1])
    state = execute(enter + leave if separate else transition, state)
    state[-1] = second(state[-1])
    return execute(leave, state)


def coefficient_cap(ops):
    return all(abs(q) + 1 < 2 ** 16 for _, _, _, q in ops)


def check(package):
    emit = source(package)
    a, b, d = [F(3), F(5)], [F(2), F(-1)], [F(7), F(-4)]
    entering, leaving, transition = emit(a, b), emit(a, d), junction(a, b, d)
    expected = [target(a, b, d, [F(i == j) for i in range(3)]) for j in range(3)]
    need(entering[-1] == leaving[0] == ('SCALE', 2, 2, F(-1)),
         'ADJACENT_SIGN_PEEPHOLE')
    peepholed = entering[:-1] + leaving[1:]
    need(columns(peepholed, 3) == expected, 'PEEPHOLED_ALL_INPUT_COLUMNS')
    need(price(peepholed) == 142 and len(peepholed) == 12, 'PEEPHOLED_TARIFF')
    need(columns(entering + leaving, 3) == columns(transition, 3) == expected,
         'ALL_INPUT_COLUMNS')
    need((price(entering), price(leaving), price(transition)) == (64, 82, 78), 'TARIFF')
    need((len(entering), len(leaving), len(transition)) == (7, 7, 6), 'INSTRUCTIONS')
    need(coefficient_cap(entering + leaving + transition), 'NAMED_CAP')
    prefix_norms = []
    for length in range(1, len(transition) + 1):
        cols = columns(transition[:length], 3)
        prefix_norms.append(max(sum(abs(col[i]) for col in cols) for i in range(3)))
    envelope = (1 + sum(map(abs, a))) ** 2 * (1 + sum(abs(x - y) for x, y in zip(b, d)))
    need(max(prefix_norms) == 129 and envelope == 729, 'PREFIX_ENVELOPE')
    functions = (lambda t: t, lambda t: t * t + 1, lambda t: F(-2), lambda t: abs(t) - 2)
    count = 0
    for state in product(range(-2, 3), repeat=3):
        for first, second in product(functions, repeat=2):
            literal = nonlinear_macro(entering, leaving, transition, state, first, second, True)
            replaced = nonlinear_macro(entering, leaving, transition, state, first, second, False)
            cleaned = nonlinear_macro(entering, leaving, peepholed, state, first, second, False)
            ax = sum(q * x for q, x in zip(a, state[:-1]))
            gx, hgx = first(ax), second(first(ax))
            direct = [x + bv * (gx - ax) + dv * (hgx - gx)
                      for x, bv, dv in zip(state[:-1], b, d)] + [F(state[-1])]
            need(literal == cleaned == replaced == direct, 'NONLINEAR_MACRO')
            count += 1
    reverse = junction(a, d, b)
    need(columns(reverse, 3) != expected, 'SIGN_CONTROL')
    need(columns(transition[:-2], 3) != expected, 'EXIT_LOWER_CONTROL')
    identity = lambda t: t
    state = [F(0), F(0), F(1)]
    good = nonlinear_macro(entering, leaving, transition, state, identity, identity, False)
    omitted = nonlinear_macro(entering, leaving, [], state, identity, identity, False)
    need(good == state and omitted == [F(-5), F(3), F(1)], 'MISSING_JUNCTION_LEAK')
    different_row = emit([1, 0], [1, 0]) + emit([1, 1], [1, 0])
    need(execute(different_row, [0, 1, 0]) == [-1, 1, 1], 'COMMON_ROW_CONTROL')
    cap_a, cap_b, cap_d = [1, 0], [1, 65534], [1, -65534]
    old = emit(cap_a, cap_b) + emit(cap_a, cap_d)
    new = junction(cap_a, cap_b, cap_d)
    need(coefficient_cap(old) and not coefficient_cap(new), 'DIFFERENCE_CAP_GAP')
    # A caller observing the intermediate restored state distinguishes the new prefix.
    encoded = execute(entering, [1, 0, 7])
    encoded[-1] += 1
    returned = execute(entering, encoded)
    after_new_junction = execute(transition, encoded)
    need(returned[-1] != after_new_junction[-1], 'INTERMEDIATE_OBSERVER_CONTROL')
    return {'status': 'PASS_INDEPENDENT_CHANGING_COLUMN_JUNCTION',
            'source_sha256': EMITTER_SHA, 'tariff_sha256': TARIFF_SHA,
            'linear_input_columns': 3, 'nonlinear_cases': count,
            'complete_two_use_scalar_allowance': {'raw_separate': 292, 'sign_peepholed': 288, 'junction': 224},
            'complete_two_use_scalar_instructions': {'raw_separate': 28, 'sign_peepholed': 26, 'junction': 20},
            'allowance_saved_against_sign_peephole': 64,
            'junction_allowance': 78, 'junction_prefix_norms': list(map(str, prefix_norms)),
            'junction_relative_prefix_bound': str(envelope),
            'named_coefficients_admitted_by_cap': True, 'scope_discriminators': 6,
            'scope': 'Exact endpoints only; same row/roles/chart; no observer or precision admission.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.package.resolve()), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
