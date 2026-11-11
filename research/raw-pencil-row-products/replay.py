"""Authenticate and execute the unchanged complete raw-pencil caller."""
import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from kernel import row_product

REPOSITORY = ROOT.parents[1]
SOURCE = REPOSITORY / 'research/raw-pencil-decomposition'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticated_bytes(repository=REPOSITORY):
    manifest = json.loads((ROOT / 'SOURCES.json').read_text())
    payloads = {}
    for entry in manifest['files']:
        if entry['usage'] == 'input':
            data = (repository / entry['path']).read_bytes()
            require(hashlib.sha256(data).hexdigest() == entry['sha256'],
                    'source hash: ' + entry['path'])
            payloads[entry['path']] = data
    return payloads


def execute_module(name, filename, payloads):
    path = SOURCE / filename
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    data = payloads[path.relative_to(REPOSITORY).as_posix()]
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module


@contextmanager
def source_modules():
    payloads = authenticated_bytes()
    names = ('field_source', 'decompose', 'raw_pencil_complete_caller')
    previous = {name: sys.modules.get(name) for name in names}
    old_path = sys.path[:]
    try:
        field = execute_module(names[0], 'field_source.py', payloads)
        decomposition = execute_module(names[1], 'decompose.py', payloads)
        caller = execute_module(names[2], 'verify.py', payloads)
        require(decomposition.a is field and caller.d is decomposition,
                'unexpected source module binding')
        yield decomposition, caller
    finally:
        sys.path[:] = old_path
        for name, module in previous.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def run(mode):
    require(mode in ('reference', 'fast', 'audit'), 'unknown mode')
    with source_modules() as (decomposition, caller):
        reference = decomposition.mm
        calls = 0
        maximum = [0, 0, 0]

        def audit(left, right, width, field):
            nonlocal calls
            expected = reference(left, right, width, field)
            actual = row_product(left, right, width, field)
            require(actual == expected, 'matrix product differs')
            calls += 1
            maximum[:] = [max(maximum[0], len(left)),
                          max(maximum[1], len(right)), max(maximum[2], width)]
            return actual

        if mode == 'fast':
            decomposition.mm = row_product
        elif mode == 'audit':
            decomposition.mm = audit
        caller.main()
        if mode == 'audit':
            print(json.dumps({'product_comparisons': calls, 'maximum_dimensions': maximum},
                             sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('reference', 'fast', 'audit'))
    run(parser.parse_args().mode)


if __name__ == '__main__':
    main()
