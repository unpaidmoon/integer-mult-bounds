"""Complete PR3240 caller with one opt-in span hook. Nick Petalas, Apache-2.0."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import types

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
PRIOR = 'research/r2-mutation-path-copy/'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def load(raw, name, path):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def capture(root=ROOT):
    rows = json.loads((PACKAGE / 'SOURCES.json').read_bytes())['files']
    need(len(rows) <= 64, 'source inventory capacity')
    captured = {}
    for row in rows:
        if row['usage'] != 'input':
            continue
        raw = (root / row['path']).read_bytes()
        need(len(raw) <= 16 * 1024 * 1024, 'input byte capacity')
        need(digest(raw) == row['sha256'], 'source drift: ' + row['path'])
        need(row['path'] not in captured, 'duplicate input')
        captured[row['path']] = raw
    need(len(captured) == 45, 'complete input inventory')
    return captured


def replace_once(raw, old, new):
    need(raw.count(old) == 1, 'unique span hook anchor')
    return raw.replace(old, new)


def install(prior, cache_class, caches):
    original_load = prior.load

    def install_span(original):
        need(not caches, 'one audit cache per invocation')
        cache = cache_class(original)
        caches.append(cache)
        return cache

    def hooked_load(raw, name, path, extra=None):
        namespace = dict(extra or {})
        if name == 'retained_anchor_replay':
            namespace['_install_span_cache'] = install_span
        module = original_load(raw, name, path, namespace)
        if name == 'mutation_adapter':
            transform_audit = module.transform_audit
            transform_replay = module.transform_replay

            def audit_hook(source):
                return transform_audit(source) + b'\nspan = _install_span_cache(span)\n'

            def replay_hook(source):
                anchor = b'        verifier._install_comparator = install'
                return replace_once(transform_replay(source), anchor, anchor +
                                    b'\n        verifier._install_span_cache = _install_span_cache')

            module.transform_audit = audit_hook
            module.transform_replay = replay_hook
        return module

    prior.load = hooked_load


def scientific(result):
    # Timing and executed-source hashes legitimately differ. Retain the full
    # theorem payload, decisions, mutant identities, footprints and immutability.
    names = ('reference_result', 'reference_result_sha256', 'call_multiset_sha256',
             'decisions', 'providers', 'source_sha256', 'mode', 'differential')
    return {name: result[name] for name in names}


def run(mode='cached', differential=False):
    need(mode in ('source', 'cached'), 'span mode')
    start = time.perf_counter()
    sources = capture()
    cache_raw = (PACKAGE / 'cache.py').read_bytes()
    cache_module = load(cache_raw, 'bounded_span_cache', PACKAGE / 'cache.py')
    prior = load(sources[PRIOR + 'replay.py'], 'complete_r2_caller', ROOT / PRIOR / 'replay.py')
    caches = []
    if mode == 'cached':
        install(prior, cache_module.SpanCache, caches)
    result = prior.run('paths', differential)
    need(len(caches) == int(mode == 'cached'), 'span hook executed')
    need(capture() == sources, 'input mutation during replay')
    return {'mode': mode, 'scientific': scientific(result),
            'scientific_sha256': digest(canonical(scientific(result))),
            'span_cache': caches[0].report() if caches else None,
            'executed_audit_sha256': result['executed_audit_sha256'],
            'wall_seconds': time.perf_counter() - start,
            'source_sha256': {p: digest(raw) for p, raw in sorted(sources.items())},
            'implementation_sha256': {'cache.py': digest(cache_raw),
                                       'replay.py': digest(Path(__file__).read_bytes())}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('source', 'cached'), default='cached')
    parser.add_argument('--differential', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), 'fresh output required')
    result = run(args.mode, args.differential)
    with args.output.open('x') as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print('PASS_R2_SPAN_REPLAY', args.mode, result['scientific_sha256'], result['span_cache'])


if __name__ == '__main__':
    main()
