"""Independent closed-rational reconstruction of PR6167's outer receipt.

No predecessor Python module is imported, compiled or called. The source
equations are credited to Ali Romman and the retained PR4359/kappa-rebuild
lineage; PR6214 identifies this independent-audit gap. New audit by AAAmirinu
with substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RECEIPT = 'research/p104-retained-operand-descent/RESULT.json'
BIT_RECEIPT = 'research/query-thinned-controllers/RESULT.json'
INPUTS = {
    RECEIPT, BIT_RECEIPT,
    'research/kappa-rebuild/controller/outer_parameters.py',
    'research/kappa-rebuild/transfer-audit/outer_transfer_audit.py',
    'research/p104-retained-operand-descent/pricing.py',
    'research/p104-retained-operand-independent-audit/README.md',
    'research/pr4359-p7-padding/dependencies/compiler-refill/endpoint.py',
}
K = Q(625729, 200000000)
TESTED = Q(62573, 20000000)
G = Q(1, 1400000000)
ADMITTED_BIT = Q(17, 5000)
ACTUAL_ATOM = Q(1, 250)
LEGACY_ATOM = Q(3, 1000)
OLD_BASELINE = Q('0.001730970419199163702738')
GROUP_COUNTS = {'parameters': 16, 'margins': 9, 'strict_checks': 54, 'functional_checks': 4}


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


def strict_json(raw):
    """Used for every JSON receipt and manifest read, including our own result."""
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_nonfinite)


def authenticate():
    manifest = strict_json((HERE / 'SOURCES.json').read_bytes())
    rows = [row for row in manifest['files'] if row['usage'] == 'input']
    need(len(rows) == 7 and {row['path'] for row in rows} == INPUTS,
         'exact seven source inputs')
    sources = {}
    for row in rows:
        raw = (ROOT / row['path']).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == row['sha256'], 'source SHA256: ' + row['path'])
        blob = b'blob ' + str(len(raw)).encode() + b'\0' + raw
        need(hashlib.sha1(blob).hexdigest() == row['git_blob'], 'source Git blob: ' + row['path'])
        sources[row['path']] = raw
    return sources


def evaluate(g=G, bit=ADMITTED_BIT, atom=ACTUAL_ATOM):
    """Substituted closed forms, not a copy/invocation of the inherited ledger.

    Parameters are perturbable only to exercise explicitly labelled controls.
    The audited source instance is the fixed default family below.
    """
    k = K
    q, a = k + 3 * g, k + 4 * g
    m = (1 - g) * q
    parameters = {
        'kappa': k, 'tested_saving': TESTED, 'complex_uniform_saving': k + 6 * g,
        'b': k + 5 * g, 'a': a, 'q': q, 'bit_saving': bit,
        'epsilon': 1 - g, 'beta': 1 - 3 * g, 'r0': g / 10,
        'stop': g, 'layout': g, 'd': g,
        'cap_xi': Q(29, 32) + m, 'lambda_': 1 - k - 7 * g / 2,
        'lambda_prime': 1 - k - 3 * g,
    }
    margins = {
        'main_transform': m,
        'global_coordinate_router': a,
        'fused_gaussian': g + q * (1 - 3 * g),
        'group_bit_router': g + a * (1 - 3 * g),
        'group_scans': 1 - 2 * g,
        'boundary_algebraic_matrix': m + g,
        'sparse_union_movement': m + g + Q(13, 32),
        'polynomial_products': 1 - g,
        'microbox_face_corrections': 77 + 4 * g,
    }
    # These independently reduced slacks must agree with the savings above.
    row_slacks = {
        'main_transform': g * (3 - k - 3 * g),
        'global_coordinate_router': 4 * g,
        'fused_gaussian': g * (4 - 3 * k - 9 * g),
        'group_bit_router': g * (5 - 3 * k - 12 * g),
        'group_scans': 1 - k - 2 * g,
        'boundary_algebraic_matrix': g * (4 - k - 3 * g),
        'sparse_union_movement': Q(13, 32) + g * (4 - k - 3 * g),
        'polynomial_products': 1 - k - g,
        'microbox_face_corrections': 77 - k + 4 * g,
    }
    need(set(row_slacks) == set(margins), 'independent savings/slack name sets')
    need(all(row_slacks[name] == value - k for name, value in margins.items()),
         'independent savings/slack algebra')
    strict = {
        'actual_bit_above_effective': bit - k - 4 * g,
        'complex_above_effective': g,
        'q_positive': q,
        'complex_endpoint': 2 * g,
        'q_below_effective': g,
        'stop_positive': g,
        'stop_below_one': 1 - g,
        'leaf_saving_above_effective': g * (1 - k - 5 * g),
        'q_below_internal': g,
        'q_below_leaf': g * (2 - k - 5 * g),
        'lambda_above_tau': g / 2,
        'lambda_above_sigma': 3 * g / 2,
        'lambda_above_internal': g / 2,
        'lambda_prime_above_lambda': g / 2,
        'lambda_prime_above_leaf': g * (2 - k - 5 * g),
        'epsilon_positive': 1 - g,
        'epsilon_below_one': g,
        'cap_above_band': Q(13, 32) + m,
        'cap_below_cell': Q(3, 32) - g - m,
        'group_positive': 1 - 3 * g,
        'group_below_dimension': 2 * g,
        'support_router_span': 3 * g,
        'group_gauge_power_slack': Q(3, 16) - 2 * m + 29 * g / 10,
        'actual_logarithmic_group_guard': Q(3, 16) - 2 * m + 3 * g,
        'global_gamma_power_slack': 9 * g / 10,
        'actual_logarithmic_gamma_guard': g,
        'alpha_logarithm_absorption': g / 10,
        'group_key_fits_record': 2 * g,
        'membership_arithmetic_fits_record': g,
        'microbox_halo_volume': 79 + 3 * g,
        'positive_layout_slack': g,
        'short_record_fallback': 1 - k - 5 * g,
        'complex_below_one_over_32': Q(1, 32) - k - 5 * g,
        'strassen_integer_power_gap': Q(2**45 - 7**16),
        'theta_positive_polynomial_power': Q(2),
        'cap_below_phase_cell_power': Q(35, 32) - m,
        'halo_covers_generic_inverse_radius': Q(5),
        'union_tag_work_per_visit_fits_record': 3 * g,
        'union_header_fits_record': 3 * g,
        'source_axis_superpolynomial': g,
        'gaussian_above_main': g * (1 - 2 * q),
        'new_complex_uniform_saving_above_b': g,
        'improvement_over_user_baseline': k - OLD_BASELINE,
        'new_semantic_guard_with_C1_one': g,
        'fine_prime_halo_umbrella': Q(7, 2),
    }
    need(len(strict) == 45, '45 non-row strict predicates')
    strict.update({name + '_above_kappa': value for name, value in row_slacks.items()})
    functional = {
        'new_semantic_group_guard': 3 * g,
        'new_BIT_row_stock_sublinear_in_active_group': (1 - 3 * g) * (1 - LEGACY_ATOM),
        'fixed_halo_explicit_metadata_branch': 77 + 4 * g,
        'actual_new_BIT_stock_sublinear': (1 - 3 * g) * (1 - atom),
    }
    result = {'parameters': parameters, 'margins': margins,
              'strict_checks': strict, 'functional_checks': functional}
    need({group: len(values) for group, values in result.items()} == GROUP_COUNTS,
         'complete independent named inventory')
    return result


def check_positive(result):
    for group in ('strict_checks', 'functional_checks'):
        for name in sorted(result[group]):
            need(result[group][name] > 0, 'nonpositive ' + group + ': ' + name)
    beta = result['parameters']['beta']
    for name in ('actual_new_BIT_stock_sublinear', 'new_BIT_row_stock_sublinear_in_active_group'):
        need(0 < result['functional_checks'][name] < beta < 1,
             'stock not strictly below active group: ' + name)
    need(all(value > result['parameters']['kappa'] for value in result['margins'].values()),
         'row saving fails requested kappa')


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def compare(expected, independent):
    need(set(expected) == set(GROUP_COUNTS), 'outer group name set mismatch')
    for group in GROUP_COUNTS:
        need(set(expected[group]) == set(independent[group]), 'name set mismatch: ' + group)
        for name in sorted(independent[group]):
            observed = expected[group][name]
            need(isinstance(observed, str), 'non-string rational: ' + group + '.' + name)
            need(Q(observed) == independent[group][name], group + ' value mismatch: ' + name)


def controls(reference, reconstructed):
    missing = copy.deepcopy(reference)
    del missing['strict_checks']['alpha_logarithm_absorption']
    wrong_internal = copy.deepcopy(reference)
    # Incorrectly using sigma-tau=-g instead of max(sigma-tau,0)=0
    # would lower internal by (1-g)g, increasing both displayed slacks.
    wrong_internal['strict_checks']['q_below_internal'] = str(G + (1 - G) * G)
    wrong_internal['strict_checks']['lambda_above_internal'] = str(G / 2 + (1 - G) * G)
    confused = copy.deepcopy(reference)
    confused['margins']['main_transform'] = str(reconstructed['margins']['main_transform'] - K)

    def positive_but_different(**updates):
        changed = evaluate(**updates)
        check_positive(changed)
        compare(reference, changed)

    actions = {
        'missing_row': lambda: compare(missing, reconstructed),
        'duplicate_nested_row': lambda: strict_json(
            '{"outer":{"margins":{"main_transform":"1","main_transform":"2"}}}'),
        'wrong_gap_positive': lambda: positive_but_different(g=2 * G),
        'closed_gap': lambda: check_positive(evaluate(g=Q(0))),
        'insufficient_BIT': lambda: check_positive(evaluate(bit=K + 4 * G)),
        'wrong_actual_atom_positive': lambda: positive_but_different(atom=LEGACY_ATOM),
        'wrong_internal_max_branch': lambda: compare(wrong_internal, reconstructed),
        'saving_confused_with_slack': lambda: compare(confused, reconstructed),
    }
    expected_reasons = {
        'missing_row': 'name set mismatch: strict_checks',
        'duplicate_nested_row': 'duplicate JSON key: main_transform',
        'wrong_gap_positive': 'parameters value mismatch: a',
        'closed_gap': 'nonpositive strict_checks: actual_logarithmic_gamma_guard',
        'insufficient_BIT': 'nonpositive strict_checks: actual_bit_above_effective',
        'wrong_actual_atom_positive': 'functional_checks value mismatch: actual_new_BIT_stock_sublinear',
        'wrong_internal_max_branch': 'strict_checks value mismatch: lambda_above_internal',
        'saving_confused_with_slack': 'margins value mismatch: main_transform',
    }
    need(set(actions) == set(expected_reasons), 'exact eight independent controls')
    reasons = {}
    for name, action in actions.items():
        try:
            action()
        except ValueError as error:
            need(str(error) == expected_reasons[name], 'wrong control discriminator: ' + name)
            reasons[name] = str(error)
        else:
            raise ValueError('undetected control: ' + name)
    return reasons


def verify():
    sources = authenticate()
    receipt = strict_json(sources[RECEIPT])
    ordinary = strict_json(sources[BIT_RECEIPT])['ordinary_BIT']
    need(Q(ordinary['atom']) == ACTUAL_ATOM and Q(ordinary['admitted']) == ADMITTED_BIT,
         'actual BIT atom and admitted saving')
    need(receipt['complete_cost']['ordinary_BIT'] == ordinary, 'candidate retained ordinary BIT input')
    need((TESTED - K) / 7 == G, 'exact seven-way gap')
    result = evaluate()
    check_positive(result)
    compare(receipt['complete_cost']['outer'], result)
    beta = result['parameters']['beta']
    m, q = result['margins']['main_transform'], result['parameters']['q']
    need(0 < G < Q(1, 10**8) and 0 < K < Q(1, 250) and
         0 < q < Q(1, 250) and 0 < m < Q(1, 250), 'elementary positivity envelope')
    need((1 - result['parameters']['b']) - (1 - result['parameters']['a']) == -G,
         'negative internal-max argument')
    strict_name = min(result['strict_checks'], key=result['strict_checks'].get)
    margin_name = min(result['margins'], key=result['margins'].get)
    functional_name = min(result['functional_checks'], key=result['functional_checks'].get)
    need(strict_name == 'alpha_logarithm_absorption' and
         result['strict_checks'][strict_name] == Q(1, 14000000000), 'exact minimum strict slack')
    need(margin_name == 'main_transform' and m - K == Q(2097809947, 980000000000000000),
         'exact limiting row slack')
    actual = result['functional_checks']['actual_new_BIT_stock_sublinear']
    legacy = result['functional_checks']['new_BIT_row_stock_sublinear_in_active_group']
    need(beta - actual == beta / 250 and beta - legacy == 3 * beta / 1000,
         'distinct exact stock gaps')
    return encode({
        'schema': 'p104-outer-rational-audit/1', 'status': 'PASS',
        'source_sha256': {path: hashlib.sha256(raw).hexdigest() for path, raw in sorted(sources.items())},
        'matched_counts': GROUP_COUNTS, 'strict_inventory': {'base': 45, 'row_slacks': 9, 'total': 54},
        'reconstructed_outer': result,
        'minimum_strict': {'name': strict_name, 'value': result['strict_checks'][strict_name]},
        'minimum_functional': {'name': functional_name, 'value': result['functional_checks'][functional_name]},
        'limiting_row': {'name': margin_name, 'saving': m, 'slack_above_kappa': m - K},
        'stock': {
            'admitted_BIT_saving': ADMITTED_BIT, 'actual_atom': ACTUAL_ATOM,
            'legacy_atom': LEGACY_ATOM, 'active_group_beta': beta,
            'actual_exponent': actual, 'legacy_exponent': legacy,
            'actual_gap_below_beta': beta - actual, 'legacy_gap_below_beta': beta - legacy,
            'both_satisfy_zero_less_exponent_less_beta_less_one': True,
        },
        'controls': controls(receipt['complete_cost']['outer'], result),
        'scope': {
            'predecessor_code_executed': False,
            'all_named_values_reproduced_exactly': True,
            'conditional_outer_arithmetic_only': True,
            'word_native_compiler_precision_or_full_theorem_replayed': False,
            'framework_assumptions_or_supplier_admission_discharged': False,
            'selected_frontier_changed': False,
        },
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the deterministic exact audit receipt')
    args = parser.parse_args()
    result = verify()
    destination = HERE / 'RESULT.json'
    if args.write:
        destination.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    else:
        need(strict_json(destination.read_bytes()) == result, 'committed audit receipt differs')
    print(json.dumps({key: result[key] for key in (
        'status', 'matched_counts', 'minimum_strict', 'limiting_row', 'controls')}, sort_keys=True))


if __name__ == '__main__':
    main()
