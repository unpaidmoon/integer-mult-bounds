"""Exact three-query cubic repair for power-of-two retained-child counts.

Nick Petalas/PR6200 supplies the defect and interface; apoursh/PR6212 supplies
the dyadic lower bound and r4 identity; apoursh/PR6215 supplies the restricted
pure-entry-B boundary. New uniform schedule/audit by AAAmirinu with substantial
OpenAI Codex assistance. Apache-2.0. No predecessor code is executed.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUTS = {'research/dyadic-cubic-repair/PROOF.md', 'research/cubic-pure-b-boundary/PROOF.md'}
MONOMIALS = ('A^3', 'A^2*B', 'A*B^2', 'B^3')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_nonfinite(value):
    raise ValueError('nonfinite JSON constant: ' + value)


def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_nonfinite)


def authenticate():
    pins = read_json((HERE / 'SOURCES.json').read_bytes())
    rows = [row for row in pins['files'] if row['usage'] == 'input']
    need(len(rows) == 2 and {row['path'] for row in rows} == INPUTS, 'exact two source proofs')
    hashes = {}
    for row in rows:
        raw = (ROOT / row['path']).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        need(sha == row['sha256'], 'source SHA256: ' + row['path'])
        blob = b'blob ' + str(len(raw)).encode() + b'\0' + raw
        need(hashlib.sha1(blob).hexdigest() == row['git_blob'], 'source Git blob: ' + row['path'])
        hashes[row['path']] = sha
    return hashes


# Polynomials in r, as exact rational coefficients in ascending degree order.
def poly(*coefficients):
    values = [Q(value) for value in coefficients] or [Q(0)]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


ZERO, ONE, R = poly(0), poly(1), poly(0, 1)


def padd(*terms):
    size = max(map(len, terms), default=1)
    return poly(*(sum((term[j] if j < len(term) else Q(0)) for term in terms) for j in range(size)))


def scale(term, factor):
    return poly(*(factor * item for item in term))


def pmul(*terms):
    result = ONE
    for term in terms:
        out = [Q(0)] * (len(result) + len(term) - 1)
        for i, a in enumerate(result):
            for j, b in enumerate(term):
                out[i + j] += a * b
        result = poly(*out)
    return result


def ppow(term, exponent):
    return pmul(*([term] * exponent))


def shift_one(term):
    return padd(*(scale(ppow(poly(1, 1), j), value) for j, value in enumerate(term)))


def common_numerators():
    # These are 6r*c1, 6r*c2 and 6r*c0, with no rational function evaluator.
    return (pmul(poly(-1, 1), poly(-2, 1)),
            scale(poly(-1, 0, 1), 4),
            scale(pmul(poly(-1, 1), poly(2, 5)), -1))


def universal_identity(numerators=None):
    numerators = common_numerators() if numerators is None else numerators
    s1 = scale(pmul(R, poly(-1, 1)), Q(1, 2))
    s2 = scale(pmul(R, poly(-1, 1), poly(-1, 2)), Q(1, 6))
    s3 = ppow(s1, 2)
    recurrences = []
    # Telescoping verifies the chronological power sums for every integer r>=0.
    for exponent, total in ((1, s1), (2, s2), (3, s3)):
        need(total[0] == 0, 'power sum base case')
        delta = padd(shift_one(total), scale(total, -1), scale(ppow(R, exponent), -1))
        need(delta == ZERO, 'power sum finite-difference recurrence')
        recurrences.append({'exponent': exponent, 'sum_polynomial': total, 'residual': delta})
    defect = (ZERO, scale(s1, 3), scale(s2, 3), s3)
    binomial = (1, 3, 3, 1)
    cleared = []
    for j, name in enumerate(MONOMIALS):
        first = pmul(numerators[0], scale(ppow(R, j), binomial[j]))
        middle = pmul(numerators[1], scale(ppow(scale(R, Q(1, 2)), j), binomial[j]))
        last = numerators[2] if j == 0 else ZERO
        represented = padd(first, middle, last)
        target = pmul(scale(R, 6), defect[j])
        residual = padd(represented, scale(target, -1))
        need(residual == ZERO, 'universal cubic coefficient mismatch: ' + name)
        cleared.append({'monomial': name, 'cleared_target': target, 'residual': residual})
    return {'coefficient_order': 'ascending powers of r', 'clearing_denominator': '6r',
            'identity_domain': 'all rational r != 0; claimed schedule uses powers of two r>=4',
            'power_sum_recurrences': recurrences, 'four_cleared_identities': cleared,
            'weight_numerators': numerators}


def dyadic(value):
    denominator = value.denominator
    return denominator > 0 and denominator & (denominator - 1) == 0


def weights(r):
    need(type(r) is int and r >= 4 and r & (r - 1) == 0, 'power-of-two r>=4 domain')
    values = (Q((r - 1) * (r - 2), 6 * r),
              Q(2 * (r * r - 1), 3 * r),
              Q(-(r - 1) * (5 * r + 2), 6 * r))
    need(all(value and dyadic(value) for value in values), 'nonzero dyadic family weights')
    need(values[0] > 0 and values[1] > 0 and values[2] < 0, 'family coefficient signs')
    return values


def cancellation_certificate():
    rows = []
    for residue in (1, 2):
        numerators = ((residue - 1) * (residue - 2),
                      4 * (residue * residue - 1), -(residue - 1) * (5 * residue + 2))
        need(all(value % 3 == 0 for value in numerators), 'mod3 numerator cancellation')
        need(2 * residue % 3 in (1, 2), 'power-of-two residue closure')
        rows.append({'r_mod3': residue, 'next_power_mod3': 2 * residue % 3,
                     'numerators_mod3': [value % 3 for value in numerators]})
    return {'power_zero_residue': 1, 'inductive_residue_rows': rows,
            'after_canceling_three_denominator': '2r, a power of two',
            'nonzero_for_r_ge4': 'c1>0, c2>0, c0<0 by their displayed factors'}


def repair(r):
    c1, c2, c0 = weights(r)
    return (('Q', -c1), ('S', Q(-r, 2)), ('Q', -c2), ('S', Q(-r, 2)), ('Q', -c0))


def children(r):
    return (('Q', Q(1)), ('S', Q(1))) * r


def eager(r):
    return (('Q', Q(1)), ('S', Q(1)), ('S', Q(-1))) * r


def inverse(word):
    return tuple((op, -coefficient) for op, coefficient in reversed(word))


def check_events(word):
    for op, coefficient in word:
        need(op in ('Q', 'S'), 'fixed event alphabet')
        if op == 'Q':
            need(coefficient != 0 and dyadic(coefficient), 'query coefficient outside dyadic ring')
        else:
            need(coefficient != 0 and coefficient.denominator == 1, 'source shear not nonzero integer')


def numeric(state, word):
    y, a, b = state
    for op, coefficient in word:
        if op == 'Q': y += coefficient * a**3
        else: a += coefficient * b
    return y, a, b


def cube(form):
    a, b = form
    return a**3, 3 * a * a * b, 3 * a * b * b, b**3


def symbolic(state, word, trace=False):
    # The arbitrary entry y is an untouched additive symbol, plus this cubic.
    output, a, b = state
    queries = []
    for op, coefficient in word:
        if op == 'Q':
            if trace:
                queries.append((coefficient, a))
            output = tuple(x + coefficient * term for x, term in zip(output, cube(a)))
        else:
            a = tuple(x + coefficient * z for x, z in zip(a, b))
    return (output, a, b), queries


ENTRY = ((Q(0),) * 4, (Q(1), Q(0)), (Q(0), Q(1)))


def check_repair(r, word):
    check_events(word)
    deferred, _ = symbolic(ENTRY, children(r))
    end, forms = symbolic(deferred, word, trace=True)
    need(end[1:] == ENTRY[1:], 'repair source restoration failed')
    need(end[0] == (Q(r), Q(0), Q(0), Q(0)), 'repair output differs from eager')
    return forms


def require_pure_entry_b(forms):
    need(any(coefficient != 0 and form[0] == 0 and form[1] != 0
             for coefficient, form in forms), 'pure entry-B query premise absent')


def chronological_checks(r):
    word, retained, comparator = repair(r), children(r), eager(r)
    for events in (word, retained, comparator, inverse(word), inverse(retained + word)):
        check_events(events)
    need(len(word) == 5 and [op for op, _ in word] == ['Q', 'S', 'Q', 'S', 'Q'],
         'exact three-query two-shear schedule')
    forms = check_repair(r, word)
    need([form for _, form in forms] == [(Q(1), Q(r)), (Q(1), Q(r, 2)), (Q(1), Q(0))],
         'actual chronological entry-coordinate query forms')
    deferred, _ = symbolic(ENTRY, retained)
    result, _ = symbolic(deferred, word)
    eager_result, _ = symbolic(ENTRY, comparator)
    need(result == eager_result, 'symbolic complete eager comparison')
    need(symbolic(result, inverse(word))[0] == deferred, 'symbolic inverse repair')
    need(symbolic(result, inverse(retained + word))[0] == ENTRY, 'symbolic inverse full program')
    need(symbolic(eager_result, inverse(comparator))[0] == ENTRY, 'symbolic inverse eager program')
    values = (Q(-3, 2), Q(-1), Q(0), Q(2, 3), Q(5, 4))
    incoming_y = (Q(-7, 3), Q(0), Q(11, 5))
    cases = 0
    for y, a, b in product(incoming_y, values, values):
        initial = y, a, b
        deferred_state = numeric(initial, retained)
        repaired_state = numeric(deferred_state, word)
        eager_state = numeric(initial, comparator)
        expected = y + r * a**3, a, b
        need(eager_state == expected and repaired_state == expected,
             'dirty rational chronological eager comparison')
        need(numeric(repaired_state, inverse(word)) == deferred_state, 'dirty rational inverse repair')
        need(numeric(repaired_state, inverse(retained + word)) == initial,
             'dirty rational inverse full program')
        need(numeric(eager_state, inverse(comparator)) == initial, 'dirty rational inverse eager')
        cases += 1
    return {'r': r, 'repair': word, 'query_forms_in_entry_coordinates': forms,
            'retained_child_events': len(retained), 'eager_events': len(comparator),
            'appended_queries': 3, 'appended_integer_shears': 2,
            'dirty_rational_cases': cases,
            'numeric_logical_events_executed': cases * (10 * r + 15),
            'symbolic_logical_events_executed': 12 * r + 20,
            'no_pure_entry_B_query': all(form[0] != 0 for _, form in forms)}


def negative_controls():
    r = 16
    good = repair(r)
    wrong_sign = ((good[0][0], -good[0][1]),) + good[1:]
    missing_shear = good[:3] + good[4:]
    wrong_order = (good[1], good[0]) + good[2:]
    source_not_restored = good + (('S', Q(1)),)
    n1, n2, n0 = common_numerators()
    forms = check_repair(r, good)

    def source_only_fault():
        deferred, _ = symbolic(ENTRY, children(r))
        end, _ = symbolic(deferred, source_not_restored)
        need(end[0] == (Q(r), Q(0), Q(0), Q(0)), 'source-only mutant must retain correct output')
        check_repair(r, source_not_restored)

    actions = {
        'wrong_universal_weight': lambda: universal_identity((padd(n1, ONE), n2, n0)),
        'wrong_query_sign': lambda: check_repair(r, wrong_sign),
        'missing_final_shear': lambda: check_repair(r, missing_shear),
        'query_shear_order': lambda: check_repair(r, wrong_order),
        'source_restore_required_even_if_output_matches': source_only_fault,
        'outside_power2_domain': lambda: repair(3),
        'non_dyadic_weight': lambda: check_events((('Q', Q(1, 3)),)),
        'false_pure_entry_B_premise': lambda: require_pure_entry_b(forms),
    }
    expected = {
        'wrong_universal_weight': 'universal cubic coefficient mismatch: A^3',
        'wrong_query_sign': 'repair output differs from eager',
        'missing_final_shear': 'repair source restoration failed',
        'query_shear_order': 'repair output differs from eager',
        'source_restore_required_even_if_output_matches': 'repair source restoration failed',
        'outside_power2_domain': 'power-of-two r>=4 domain',
        'non_dyadic_weight': 'query coefficient outside dyadic ring',
        'false_pure_entry_B_premise': 'pure entry-B query premise absent',
    }
    need(set(actions) == set(expected), 'fixed eight controls')
    reasons = {}
    for name, action in actions.items():
        try:
            action()
        except ValueError as error:
            need(str(error) == expected[name], 'wrong control discriminator: ' + name)
            reasons[name] = str(error)
        else:
            raise ValueError('undetected control: ' + name)
    return reasons


def encode(value):
    if isinstance(value, Q): return str(value)
    if isinstance(value, dict): return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)): return [encode(item) for item in value]
    return value


def verify():
    hashes = authenticate()
    universal = universal_identity()
    cancellation = cancellation_certificate()
    need(weights(4) == (Q(1, 4), Q(5, 2), Q(-11, 4)), 'credited PR6212 r4 control')
    need(weights(16) == (Q(35, 16), Q(85, 8), Q(-205, 16)), 'exact r16 discriminator')
    need(16 % 9 == 7, 'r16 restricted pure-B residue')
    coefficients = []
    for exponent in (2, 3, 4, 5, 6, 10, 16, 32, 64, 128):
        r = 1 << exponent
        c1, c2, c0 = weights(r)
        need(c1 + c2 + c0 == 0, 'numeric A-cube cancellation')
        coefficients.append({'exponent': exponent, 'r': r, 'weights': (c1, c2, c0),
                             'source_shear': Q(-r, 2),
                             'children_materialized': exponent <= 6})
    fixtures = [chronological_checks(r) for r in (4, 8, 16, 32, 64)]
    need(sum(row['dirty_rational_cases'] for row in fixtures) == 375, 'fixed dirty-input count')
    return encode({
        'schema': 'cubic-pow2-repair/1', 'status': 'PASS', 'source_sha256': hashes,
        'universal_polynomial_certificate': universal, 'dyadic_cancellation': cancellation,
        'coefficient_fixtures': coefficients, 'chronological_fixtures': fixtures,
        'symbolic_chronological_arities': len(fixtures),
        'dirty_rational_cases': sum(row['dirty_rational_cases'] for row in fixtures),
        'numeric_logical_events_executed': sum(row['numeric_logical_events_executed'] for row in fixtures),
        'r4_prior_identity_credited': True,
        'r16_scope_discriminator': {
            'weights': weights(16), 'unrestricted_queries': 3, 'integer_shears': 2,
            'query_forms': [(1, 16), (1, 8), (1, 0)],
            'pure_entry_B_query_present': False,
            'predecessor_restricted_floor': 4, 'restricted_floor_applies_to_this_word': False,
        },
        'controls': negative_controls(),
        'scope': {
            'predecessor_code_executed': False,
            'query_lower_bound': 'cited from PR6212, not reproved by finite fixtures',
            'previously_known_counts': 'r4, odd power exponents, and exponents divisible by six',
            'arbitrary_r_classification': False,
            'native_or_rounded_implementation': False,
            'coefficient_preparation_or_physical_tariff_supplied': False,
            'runtime_improvement_or_selected_frontier_claim': False,
            'new_claim': 'uniform three-query/two-integer-shear repair for powers of two r>=4',
        },
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the exact deterministic local receipt')
    args = parser.parse_args()
    result = verify()
    destination = HERE / 'RESULT.json'
    if args.write:
        destination.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')
    else:
        need(read_json(destination.read_bytes()) == result, 'committed exact receipt differs')
    print(json.dumps({key: result[key] for key in (
        'status', 'symbolic_chronological_arities', 'dirty_rational_cases',
        'numeric_logical_events_executed', 'controls')}, sort_keys=True))


if __name__ == '__main__':
    main()
