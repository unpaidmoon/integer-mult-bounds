"""Check the changed kernel and complete callers; produced by Nick Petalas."""

import argparse
import copy
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adapter


def tables(p, n):
    positions = list(combinations_with_replacement(range(n), 2))
    for values in product(range(p), repeat=n * len(positions)):
        table = [[[0] * n for _ in range(n)] for _ in range(n)]
        for offset, (i, j) in enumerate(positions):
            row = list(values[n * offset:n * (offset + 1)])
            table[i][j] = list(row)
            table[j][i] = list(row)
        yield table


def kernel_checks():
    original = adapter.load('recognize')
    counts = {}
    for p in (2, 3, 5):
        count = 0
        for table in tables(p, 2):
            before = copy.deepcopy(table)
            expected = original._algebra_error(table, p)
            adapter.require(adapter.algebra_error(table, p) == expected,
                            'complete two-dimensional kernel mismatch')
            adapter.require(table == before, 'kernel changed input')
            count += 1
        counts[str(p)] = count
    api = adapter.load('recognize')
    api._algebra_error = adapter.algebra_error
    complete_results = 0
    for table in tables(2, 2):
        adapter.require(api.recognize(2, table) == original.recognize(2, table),
                        'complete API result mismatch')
        complete_results += 1
    return counts, complete_results


def broad_checks():
    original = adapter.load('recognize')
    count = noncommutative = 0
    for p in (2, 3, 5, 7):
        for n in range(1, 7):
            for seed in range(24):
                table = [[[((i + 1) * (j + 1) + k * seed + (i ^ j) * k
                             + seed * (i + j)) % p for k in range(n)]
                          for j in range(n)] for i in range(n)]
                adapter.require(adapter.algebra_error(table, p)
                                == original._algebra_error(table, p), 'broad kernel mismatch')
                count += 1
                if n > 1:
                    table[0][1][0] = (table[0][1][0] + 1) % p
                    adapter.require(adapter.algebra_error(table, p)
                                    == original._algebra_error(table, p)
                                    == 'table is not commutative', 'commutativity precedence')
                    noncommutative += 1
    return count, noncommutative


def contraction_checks():
    original = adapter.bracket
    counts = []
    try:
        for n in range(1, 17):
            calls = []

            def counted(coefficients, table, index, p):
                calls.append(1)
                return original(coefficients, table, index, p)

            adapter.bracket = counted
            table = [[[0] * n for _ in range(n)] for _ in range(n)]
            adapter.require(adapter.algebra_error(table, 2) is None, 'zero algebra failed')
            expected = n * (n - 1) * (n + 2) // 2
            adapter.require(len(calls) == expected, 'wrong contraction coverage')
            counts.append([n, 2 * n ** 3, expected])
    finally:
        adapter.bracket = original
    return counts


def branch_controls():
    repeated_left = [[[0] * 2 for _ in range(2)] for _ in range(2)]
    repeated_left[0][0][1] = 1
    repeated_left[0][1][0] = repeated_left[1][0][0] = 1
    repeated_right = [[[0] * 2 for _ in range(2)] for _ in range(2)]
    repeated_right[1][1][0] = 1
    repeated_right[0][1][1] = repeated_right[1][0][1] = 1
    middle = [[[0] * 5 for _ in range(5)] for _ in range(5)]
    middle[0][2][3] = middle[2][0][3] = 1
    middle[1][3][4] = middle[3][1][4] = 1
    for table in (repeated_left, repeated_right, middle):
        adapter.require(adapter.algebra_error(table, 2) == 'table is not associative',
                        'missing associator branch')
    for engine, caller in (('missing', 'main'), ('symmetric', 'missing')):
        try:
            adapter.run(engine, caller)
        except ValueError:
            continue
        raise ValueError('invalid adapter selector accepted')
    return 5


def run(caller):
    adapter.authenticate()
    counts, results = kernel_checks()
    broad, noncomm = broad_checks()
    contractions = contraction_checks()
    controls = branch_controls()
    baseline = adapter.run('baseline', caller)
    symmetric = adapter.run('symmetric', caller)
    adapter.require(baseline == symmetric, 'complete caller report mismatch')
    encoded = json.dumps(symmetric, sort_keys=True).encode()
    files = {path.name: sha256(path.read_bytes()).hexdigest()
             for path in sorted(adapter.HERE.iterdir()) if path.is_file()}
    return {'status': 'PASS_FROBENIUS_SYMMETRIC_ASSOCIATOR', 'caller': caller,
            'complete_2d_commutative_tables': counts, 'complete_api_results': results,
            'broad_tables': broad, 'noncommutative_controls': noncomm,
            'branch_and_selector_controls': controls,
            'contractions_by_dimension': contractions, 'caller_report': symmetric,
            'caller_report_sha256': sha256(encoded).hexdigest(), 'package_sha256': files}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--caller', choices=('main', 'oracle'), default='main')
    args = parser.parse_args()
    print(json.dumps(run(args.caller), sort_keys=True))
