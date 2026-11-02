"""Check that the compressed word is a lossless rewrite of PR6167's word.

Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code. Apache-2.0.
The word, price and checker chain are PR6167's (Ali Romman) over PR6144 and PR5827; they are read
from the merged package research/p104-retained-operand-descent, authenticated by SOURCES.json pins.
"""
from collections import Counter
from contextlib import ExitStack
from pathlib import Path
import gzip
import json
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'p104-retained-operand-descent'
sys.path.insert(0, str(HERE))
from construct import matches_shipped

STATUS = 'PASS_P104_FRONTIER_COMPRESSION_NO_NEW_KAPPA'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def authenticate(path, pin):
    from hashlib import sha1, sha256
    raw = Path(path).read_bytes()
    need(sha256(raw).hexdigest() == pin['sha256'], 'Exact SHA256: ' + pin['path'])
    need(sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == pin['git_blob'],
         'Exact Git blob: ' + pin['path'])
    return raw


def run():
    pins = {r['path']: r for r in json.loads((HERE / 'SOURCES.json').read_text())['files']}
    root_dir = HERE.parent.parent
    for name, pin in pins.items():
        if pin['usage'] == 'input':
            authenticate(root_dir / name, pin)
    base_raw = (BASE / 'WORD.json.gz').read_bytes()
    source = json.loads(gzip.decompress(base_raw))
    shipped = (HERE / 'WORD.json.gz').read_bytes()
    word = json.loads(gzip.decompress(shipped))
    need(matches_shipped(word, shipped), 'Canonical payload')
    old, new = source['program'], word['program']
    need({k: v for k, v in word.items() if k != 'program'} == {k: v for k, v in source.items() if k != 'program'},
         'Header unchanged')
    need((len(old), len(new)) == (22821, 18083), 'Exact event counts')
    for kind in ('MOVE', 'INIT', 'CLEAR', 'COPY'):
        need([e for e in old if e[0] == kind] == [e for e in new if e[0] == kind],
             kind + ' events unchanged and in order')
    need(all(type(e[4]) is bool for e in new if e[0] == 'MOVE'), 'Boolean ownership flags')
    print('PASS only ADD and SCALE events changed: 22,821 -> 18,083 events', flush=True)
    with ExitStack() as contexts:
        S = load(BASE / 'sources.py', 'base_sources')
        parent = contexts.enter_context(S.sources())
        cursor = contexts.enter_context(load(parent / 'sources.py', 'base_source_top').sources())
        for depth in range(7):
            module = load(cursor / 'sources.py', 'base_source_' + str(depth))
            cursor, root = contexts.enter_context(module.sources())
        L = load(parent / 'local.py', 'local')
        L.ROOT = root
        baseline, local = L.replay(source), L.replay(word)
        for key in ('helpers', 'paid', 'public_inputs', 'owned_fields', 'owned_lifetimes', 'peak_owned_fields'):
            need(local[key] == baseline[key], 'Unchanged replay field: ' + key)
        print('PASS replay: productive targets, paid profile and storage identical', flush=True)
        columns = L.reverse_columns(word)
        need(columns == L.reverse_columns(source), 'Identical endpoint columns')
        need(columns['columns'] == 799 and columns['coefficients'] == 638401, 'All input columns')
        print('PASS separate transpose: 799 columns, 638,401 coefficients identical', flush=True)
        native = L.native(word)
        C = load(root / 'research/p104-productive-controller/caller.py', 'base_caller')
        caller = C.construct()
        physical = C.physical(caller, word)
        P = load(BASE / 'pricing.py', 'retained_operand_price')
        price = P.run(local, native, caller, physical)
        ref = json.loads((BASE / 'RESULT.json').read_text())
        need(price['raw_root_interval'] == ref['complete_cost']['raw_root_interval'], 'Same raw crossing')
        for key in ('paid', 'targets'):
            need(price[key] == ref['complete_cost'][key], 'Same complete invoice: ' + key)
        rt = lambda v: json.loads(json.dumps(v))
        need(rt(physical) == ref['physical_caller'], 'Same physical caller')
        need(rt(native) == ref['native'], 'Same native maps')
        print('PASS native maps, physical caller and complete price identical to PR6167', flush=True)
        return dict(status=STATUS, events_before=len(old), events_after=len(new),
                    removed={k: Counter(e[0] for e in old)[k] - Counter(e[0] for e in new)[k]
                             for k in ('ADD', 'SCALE')},
                    raw_root_interval=price['raw_root_interval'], paid=price['paid'], targets=price['targets'],
                    scalar_allowance_before=baseline['real_scalar_allowance'],
                    scalar_allowance_after=local['real_scalar_allowance'])


def main():
    with tempfile.TemporaryDirectory(prefix='frontier-compression-') as cache:
        sys.pycache_prefix = cache
        result = run()
    if '--write' in sys.argv:
        (HERE / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    else:
        need(json.loads((HERE / 'RESULT.json').read_text()) == result, 'Exact retained result')
    print(STATUS, flush=True)


if __name__ == '__main__':
    main()
