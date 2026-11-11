"""Opt-in symmetric associativity kernel, produced by Nick Petalas.

Apache-2.0. The unmodified recognizer and callers are apoursh's PR5502.
"""

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'research/frobenius-algebra-recognition'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate(root=ROOT):
    manifest = json.loads((HERE / 'SOURCES.json').read_text())
    for item in manifest['files']:
        if item['usage'] == 'input':
            actual = sha256((root / item['path']).read_bytes()).hexdigest()
            require(actual == item['sha256'], 'source hash mismatch: ' + item['path'])


def load(name):
    path = ROOT / SOURCE / (name + '.py')
    spec = importlib.util.spec_from_file_location('symmetric_' + name, path)
    require(spec is not None and spec.loader is not None, 'source loader missing')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bracket(coefficients, table, index, p):
    n = len(table)
    return [sum(coefficients[r] * table[r][index][s] for r in range(n)) % p
            for s in range(n)]


def algebra_error(table, p):
    """Match the internal contract: a normalized nonempty table, prime p."""
    n = len(table)
    for i in range(n):
        for j in range(i):
            if table[i][j] != table[j][i]:
                return 'table is not commutative'
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                if i == k:
                    continue
                first = bracket(table[i][j], table, k, p)
                last = bracket(table[j][k], table, i, p)
                if first != last:
                    return 'table is not associative'
                if i < j < k and first != bracket(table[i][k], table, j, p):
                    return 'table is not associative'
    return None


def run(engine, caller):
    require(engine in ('baseline', 'symmetric'), 'unknown engine')
    require(caller in ('main', 'oracle'), 'unknown caller')
    authenticate()
    api = load('recognize')
    if engine == 'symmetric':
        api._algebra_error = algebra_error
    module = load('verify' if caller == 'main' else 'check_exhaustive')
    if caller == 'main':
        module.load_recognizer = lambda: api
    else:
        module.recognize = api.recognize
    return module.run() if caller == 'main' else module.run_checks()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', choices=('baseline', 'symmetric'), required=True)
    parser.add_argument('--caller', choices=('main', 'oracle'), default='main')
    arguments = parser.parse_args()
    print(json.dumps(run(arguments.engine, arguments.caller), sort_keys=True))
