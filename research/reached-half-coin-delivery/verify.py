"""Bounded source-relative event52 coin-delivery audit; no full prefix replay.

Credits: zxv/PR6092 and PR6066, JoyboyBrian/PR6095, Nick Petalas/PR6026,
Ali Romman/PR5599 and their retained source lineage. New wrapper/audit:
AAAmirinu + OpenAI Codex. Apache-2.0.
"""
import argparse
import gzip
import hashlib
import io
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

from machine import TABLE, fetch_word, need, run, wrapped_word

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL = 'research/reversible-signed-half-kernel/kernel.py'
MARKER = 'research/signed-half-marker-audit/verify.py'
WORD = 'research/p104-helper-subspace-splits/WORD.json.gz'
INPUTS = {
    KERNEL, MARKER, WORD,
    'research/reversible-signed-half-kernel/PROOF.md',
    'research/signed-half-marker-audit/AUDIT.md',
    'research/p104-stochastic-prefix/PROOF.md',
    'research/reversible-stochastic-shears/verify.py',
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load_sources():
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    rows = [row for row in manifest['files'] if row['usage'] == 'input']
    need(len(rows) == 7 and {row['path'] for row in rows} == INPUTS,
         'exact seven input sources')
    data = {}
    for row in rows:
        raw = (ROOT / row['path']).read_bytes()
        need(digest(raw) == row['sha256'], 'source SHA256: ' + row['path'])
        blob = b'blob ' + str(len(raw)).encode() + b'\0' + raw
        need(hashlib.sha1(blob).hexdigest() == row['git_blob'],
             'source Git blob: ' + row['path'])
        data[row['path']] = raw
    modules = {}
    for path in (KERNEL, MARKER):
        namespace = {'__name__': 'authenticated_source', '__file__': str(ROOT / path)}
        # Authenticated bytes, with assertions enabled even under python -O.
        # No cached module/bytecode and no inherited main/verification run.
        exec(compile(data[path], path, 'exec', optimize=0), namespace)
        modules[path] = namespace
    return data, modules


def source_slice(raw):
    need(len(raw) <= 1 << 20, 'compressed source size')
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        unpacked = stream.read((1 << 22) + 1)
    need(len(unpacked) <= 1 << 22, 'unpacked source size')
    word = json.loads(unpacked)
    need(word['public'] == 748 and word['frames'][3] == [], 'source scalar chart')
    events = word['program'][:53]
    need(len(events) == 53 and all(e[0] in ('ADD', 'SCALE') and e[-1] == 3
                                 for e in events), 'actual event52 scalar prefix')
    need(events[52] == ['SCALE', 345, '1/2', 3], 'actual half event52')
    writes = [(i, e) for i, e in enumerate(events[:52]) if e[1] == 345]
    need(writes == [(40, ['ADD', 345, 93, '1', 3])], 'full prior target write slice')
    need(not any(e[1] == 93 for e in events[:40]), 'source93 untouched before read')
    need(events[51] == ['ADD', 93, 345, '-1', 3], 'event51 modifies93, not345')
    reservations = []
    for i, event in enumerate(events[:52]):
        denominator = Fraction(event[-2]).denominator
        need(denominator > 0 and denominator & (denominator - 1) == 0,
             'dyadic fixed-draw coefficient')
        if denominator > 1:
            reservations.append([i, denominator.bit_length() - 1])
    need(reservations == [[19, 1], [20, 1], [41, 2]] + [[i, 1] for i in range(42, 49)],
         'fixed-draw reservations before event52')
    need(sum(bits for _, bits in reservations) == 11, 'declared packed offset11')
    return {
        'event': events[52], 'index': 52, 'prior_target_writes': [[i, e] for i, e in writes],
        'reached_value': 'initial[345] + initial[93]',
        'original_signed_bits': 'B>=1', 'required_signed_width': 'W=B+1',
        'reached_range': '[-2^B, 2^B-2]', 'prior_fixed_draw_blocks': reservations,
        'coin_offset': 11, 'packing': 'new declared fixed-draw packing, not inherited tape ABI',
        'full_prefix_replayed': False,
    }


def check_table(marker):
    old = marker['transition_table']()
    need(len(old) == 256 and len(TABLE) == 704, 'literal table cardinalities')
    projections = 0
    for key, row in old.items():
        for coin in (0, 1):
            new = TABLE[key + (coin,)]
            need(new[:6] + new[7:] == row and new[6] == 0,
                 'unchanged old row projection')
            projections += 1
    new_rows = 0
    for mode, symbol, a, b, bit, coin in product(
            ('F', 'FR', 'I', 'IR'), 'NPJ', (0, 1), (0, 1), (0, 1), (0, 1)):
        row = TABLE[mode, symbol, a, b, bit, coin]
        active = mode in ('F', 'IR')
        expected_a = a ^ (coin if active and symbol == 'J' else 0)
        expected_move = (1 if symbol == 'N' else -1) if active and symbol != 'J' else 0
        if mode == 'IR':
            expected_move = -expected_move
        need(row == (mode, expected_a, b, bit, 0,
                     1 if mode in ('F', 'I') else -1, expected_move, False, False),
             'independent local new-symbol rule')
        new_rows += 1
    return {'rows': len(TABLE), 'old_rows': len(old), 'old_coin_projections': projections,
            'new_rows': new_rows,
            'sha256': digest(json.dumps([[list(k), list(v)] for k, v in sorted(TABLE.items())],
                                       separators=(',', ':')).encode())}


def signed_bits(value, width):
    need(-(1 << (width - 1)) <= value < (1 << (width - 1)), 'signed width insufficient')
    return [(value >> j) & 1 for j in range(width)]


def make_layout(x, width, word, coins, origins):
    d0, p0, r0 = origins
    need(len(coins) == 12 and set(coins) <= {0, 1}, 'twelve supplied random bits')
    data = {d0 + j: bit for j, bit in enumerate(signed_bits(x, width) + [0] * (width + 2))}
    data.update({d0 - 2: 1, d0 - 1: 0, d0 + 2 * width + 2: 1, d0 + 2 * width + 9: 0})
    program = {p0 + j: symbol for j, symbol in enumerate('<' + word + '>')}
    program.update({p0 - 1: '?', p0 + len(word) + 2: '#'})
    random_tape = {r0 + j: bit for j, bit in enumerate(coins)}
    random_tape.update({r0 - 2: 1, r0 - 1: 0, r0 + 12: 1, r0 + 19: 0})
    return data, program, random_tape


def clean_cut(data, width, d0):
    need(all(data[d0 + j] == 0 for j in range(width, 2 * width + 2)),
         'supplied clean cut premise violated')


def check_case(left, right, original_bits, coins, half, word, origins=(0, 0, 0),
               table=TABLE, dirty=False, inverse_coins=None):
    width = original_bits + 1
    signed_bits(left, original_bits)
    signed_bits(right, original_bits)
    x = left + right  # Independent source-slice arithmetic, not a prefix interpreter.
    data, program, random_tape = make_layout(x, width, word, coins, origins)
    d0, _, r0 = origins
    if dirty:
        data[d0 + width + 2] = 1
    clean_cut(data, width, d0)
    frozen_program, frozen_random = dict(program), dict(random_tape)
    output, stats = run(data, program, random_tape, width, len(word), origins, table=table)
    # Independent integer oracle; neither source expected() nor gate executor is used.
    parity = x % 2
    quotient = x // 2 + int(coins[11] == 0 and parity == 1)
    want = dict(data)
    want.update({d0 + j: bit for j, bit in enumerate(signed_bits(quotient, width))})
    want[d0 + width] = parity
    need(output == want, 'complete forward endpoint including owned cells/spectators')
    if inverse_coins is not None:
        random_tape = dict(random_tape)
        random_tape.update({r0 + j: bit for j, bit in enumerate(inverse_coins)})
    restored, inverse_stats = run(output, program, random_tape, width, len(word),
                                  origins, inverse=True, table=table)
    need(restored == data, 'complete inverse endpoint and residue cleanup')
    need(program == frozen_program and random_tape == frozen_random,
         'complete read-only tape preservation')
    need(inverse_stats == stats, 'complete direction invoice/write-support equality')
    need(stats['steps'] == 2 * len(half) + 8 * width + 110 and stats['marker_steps'] == 2,
         'complete transition invoice')
    need(stats['coin_moves'] == 44, 'literal coin-head walks')
    need(stats['data_moves'] == half.count('L') + half.count('R') + 4 * (width + 1),
         'literal data-head walks')
    need(stats['visited_data'] == list(range(2 * width + 2)) and
         stats['visited_program'] == list(range(len(word) + 2)) and
         stats['visited_coin'] == list(range(12)), 'exact visited intervals')
    need(set(stats['written']) <= set(range(2 * width + 2)) and
         width + 1 in stats['written'], 'owned write support includes resident coin')
    return stats['steps'] * 2


def patterns(index, coin):
    mode = index % 4
    if mode == 0: bits = [j % 2 for j in range(12)]
    elif mode == 1: bits = [1 - j % 2 for j in range(12)]
    elif mode == 2: bits = [int(j == index % 10) for j in range(12)]
    else: bits = [int(j != index % 10) for j in range(12)]
    bits[10], bits[11] = 1 - coin, coin
    return bits


def negative_controls(kernel):
    width, original_bits, left, right = 2, 1, -1, 0
    half = kernel['compile_tape'](kernel['compile_gates'](width, 1))
    word = wrapped_word(half, width)
    coins = patterns(0, 0)
    wrong_inverse = dict(TABLE)
    for key, row in list(wrong_inverse.items()):
        if key[0] == 'IR' and key[1] in 'NP':
            changed = list(row); changed[6] *= -1; wrong_inverse[key] = tuple(changed)
    no_rewind = dict(TABLE)
    for key, row in list(no_rewind.items()):
        if key[0] == 'F' and key[1] == '>':
            changed = list(row); changed[7] = True; no_rewind[key] = tuple(changed)
    retained_control = dict(TABLE)
    for key, row in list(retained_control.items()):
        if key[1] == '<':
            changed = list(row); changed[1] = 1; retained_control[key] = tuple(changed)
    changed_coin = list(coins); changed_coin[11] ^= 1
    controls = {
        'wrong_coin_offset10': lambda: check_case(left, right, original_bits, coins, half,
                                                wrapped_word(half, width, 10)),
        'omitted_unfetch': lambda: check_case(left, right, original_bits, patterns(0, 1), half,
                                             fetch_word(width) + half),
        'wrong_inverse_coin_walk': lambda: check_case(left, right, original_bits, coins,
                                                     half, word, table=wrong_inverse),
        'missing_marker_rewind': lambda: check_case(left, right, original_bits, coins,
                                                   half, word, table=no_rewind),
        'retained_accumulator': lambda: check_case(left, right, original_bits, coins,
                                                  half, word, table=retained_control),
        'changed_inverse_coin': lambda: check_case(left, right, original_bits, coins,
                                                  half, word, inverse_coins=changed_coin),
        'dirty_work_domain': lambda: check_case(left, right, original_bits, coins,
                                               half, word, dirty=True),
        'one_bit_short_extreme_domain': lambda: signed_bits(-2, 1),
    }
    expected_reasons = {
        'wrong_coin_offset10': 'complete forward endpoint including owned cells/spectators',
        'omitted_unfetch': 'complete forward endpoint including owned cells/spectators',
        'wrong_inverse_coin_walk': 'coin head escaped supplied interval',
        'missing_marker_rewind': 'heads or finite control did not return',
        'retained_accumulator': 'heads or finite control did not return',
        'changed_inverse_coin': 'complete inverse endpoint and residue cleanup',
        'dirty_work_domain': 'supplied clean cut premise violated',
        'one_bit_short_extreme_domain': 'signed width insufficient',
    }
    need(set(controls) == set(expected_reasons), 'fixed eight control discriminators')
    reasons = {}
    for name, control in controls.items():
        try:
            control()
        except ValueError as error:
            need(str(error) == expected_reasons[name], 'wrong control discriminator: ' + name)
            reasons[name] = str(error)
        else:
            raise ValueError('undetected control: ' + name)
    return reasons


def verify():
    sources, modules = load_sources()
    kernel = modules[KERNEL]
    source = source_slice(sources[WORD])
    table = check_table(modules[MARKER])
    fixtures = []
    exhaustive = endpoints = transitions = 0
    translated_origins = ((0, 0, 0), (-17, 29, -53), (101, -211, 307))
    for original_bits in (1, 2, 3, 4, 5, 7, 15, 31):
        width = original_bits + 1
        gates = kernel['compile_gates'](width, 1)
        half = kernel['compile_tape'](gates)
        word = wrapped_word(half, width)
        need(word == fetch_word(width) + half + fetch_word(width), 'unchanged contiguous kernel')
        length = len(half)
        need(length <= 64 * width * width + 64 * width + 8, 'source gate envelope')
        need(len(word) == length + 4 * width + 54, 'complete payload length')
        low, high = -(1 << (original_bits - 1)), (1 << (original_bits - 1)) - 1
        pairs = product(range(low, high + 1), repeat=2) if original_bits <= 4 else (
            (low, low), (high, high), (low, high), (high, low),
            (low, 0), (high, 0), (-1, 0), (0, 0))
        cases = 0
        for left, right in pairs:
            for coin in (0, 1):
                index = exhaustive + endpoints
                coins = patterns(index // 2, coin)
                transitions += check_case(left, right, original_bits, coins, half, word,
                                           translated_origins[index % 3])
                cases += 1
                if original_bits <= 4: exhaustive += 1
                else: endpoints += 1
        fixtures.append({
            'original_bits': original_bits, 'width': width, 'cases': cases,
            'half_symbols': length, 'half_sha256': digest(half.encode()),
            'payload_symbols': len(word), 'payload_sha256': digest(word.encode()),
            'steps_per_direction': 2 * length + 8 * width + 110,
            'program_cells': length + 4 * width + 56, 'data_cells': 2 * width + 2,
            'random_cells': 12, 'sum_visited_intervals': length + 6 * width + 70,
            'coin_moves_per_direction': 44,
            'data_moves_per_direction': half.count('L') + half.count('R') + 4 * (width + 1),
        })
    need(exhaustive == 680 and endpoints == 64, 'fixed bounded fixture count')
    return {
        'schema': 'reached-half-coin-delivery/1', 'status': 'PASS',
        'source_sha256': {path: digest(raw) for path, raw in sorted(sources.items())},
        'source_slice': source, 'local_table': table,
        'exhaustive_pair_coin_cases': exhaustive, 'larger_endpoint_cases': endpoints,
        'literal_round_trip_transitions': transitions, 'fixtures': fixtures,
        'origins': [list(origin) for origin in translated_origins],
        'controls': negative_controls(kernel),
        'scope': {
            'allocation_layout_program_setup_supplied': True,
            'random_tape_generation_supplied': True,
            'source_event40_or_full_prefix_implemented': False,
            'native_or_selected6030_transfer': False,
            'sampler_full_supplier_invoice_or_kappa_claim': False,
            'freshness': 'requires coin11 uniform conditional on past and input',
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the deterministic local receipt')
    args = parser.parse_args()
    result = verify()
    destination = HERE / 'RESULT.json'
    if args.write:
        destination.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    else:
        need(json.loads(destination.read_text(encoding='utf-8')) == result,
             'committed deterministic receipt differs')
    print(json.dumps({key: result[key] for key in (
        'status', 'exhaustive_pair_coin_cases', 'larger_endpoint_cases',
        'literal_round_trip_transitions', 'local_table', 'controls')}, sort_keys=True))


if __name__ == '__main__':
    main()
