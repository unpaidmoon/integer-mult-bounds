"""Exact cache conformance and complete replay. Nick Petalas, Apache-2.0."""
import itertools
import json
from pathlib import Path
import statistics
import tempfile
import types

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name):
    path = PACKAGE / (name + '.py')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def outcome(fn, rows):
    try:
        return ('value', fn(rows))
    except (ValueError, TypeError) as exc:
        return ('exception', type(exc), str(exc))


def conformance(replay, cache_class):
    sources = replay.capture()
    key = replay.PRIOR + 'vendor/pr3218/vendor/pr3202/verify.py'
    original = replay.load(sources[key], 'exact_source_span', ROOT / key).span
    cache = cache_class(original)
    cases = 0
    # Every ordered frame of length <=4 over the 3-bit ambient space,
    # including zero, repeats and dependent bases. Only successes are cached.
    for length in range(5):
        for values in itertools.product(range(8), repeat=length):
            rows = list(values)
            expected = outcome(original, rows)
            need(outcome(cache, rows) == expected, 'ordered frame conformance')
            need(outcome(cache, tuple(rows)) == expected, 'immutable key conformance')
            cases += 1
    for rows in ([True], [1.0], [0], [-1], [512], [1, 2, 3], list(range(10)), [1, []]):
        need(outcome(cache, rows) == outcome(original, rows), 'invalid frame conformance')
        cases += 1
    rows = [1, 2]
    need(cache(rows) == frozenset((0, 1, 2, 3)), 'warm mutable frame')
    rows[1] = 4
    need(cache(rows) == frozenset((0, 1, 4, 5)), 'content mutation invalidation')
    rows[1] = 1
    need(outcome(cache, rows) == outcome(original, rows), 'warm invalid mutation')
    other = cache_class(original)
    need(other.report()['entries'] == 0 and other([1]) == frozenset((0, 1)), 'fresh lifetime')
    tiny = cache_class(original, capacity=1)
    need(tiny([1]) == original([1]) and tiny([2]) == original([2]), 'capacity fallback')
    need(tiny.report()['entries'] == 1 and tiny.report()['misses'] == 2, 'capacity bound')
    return cases


def rejection_controls(replay):
    # Capture authenticates before any predecessor code executes.
    rows = json.loads((PACKAGE / 'SOURCES.json').read_bytes())['files']
    inputs = [row['path'] for row in rows if row['usage'] == 'input']
    changed = (replay.PRIOR + 'replay.py', replay.PRIOR + 'adapter.py',
               replay.PRIOR + 'vendor/pr3218/vendor/pr3202/data/base/CANONICAL-WORD.json.gz')
    with tempfile.TemporaryDirectory(prefix='r2-span-controls-') as directory:
        root = Path(directory)
        for name in inputs:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / name).read_bytes())
        for name in changed:
            path = root / name
            raw = path.read_bytes()
            path.write_bytes(raw + b' ')
            try:
                replay.capture(root)
            except ValueError as exc:
                need(str(exc) == 'source drift: ' + name, 'source rejection reason')
            else:
                raise ValueError('source mutation accepted')
            path.write_bytes(raw)
    try:
        replay.replace_once(b'missing', b'anchor', b'new')
    except ValueError as exc:
        need(str(exc) == 'unique span hook anchor', 'hook rejection reason')
    else:
        raise ValueError('unknown hook accepted')
    return 4


def benchmark_binding(replay):
    receipt = json.loads((PACKAGE / 'BENCHMARK.json').read_bytes())
    need(receipt['failures'] == 0 and len(receipt['runs']) == 2 * receipt['pairs'], 'timing inventory')
    need(receipt['benchmark_sha256'] == replay.digest((PACKAGE / 'benchmark.py').read_bytes()),
         'timing harness binding')
    current = {name: replay.digest((PACKAGE / name).read_bytes()) for name in ('cache.py', 'replay.py')}
    inputs = {p: replay.digest(raw) for p, raw in replay.capture().items()}
    for row in receipt['runs']:
        need(row['result']['implementation_sha256'] == current, 'timing implementation binding')
        need(row['result']['source_sha256'] == inputs, 'timing input binding')
    need([row['mode'] for row in receipt['runs']] == ['source', 'cached'] * receipt['pairs'],
         'alternating complete process order')
    for mode in ('source', 'cached'):
        times = [row['elapsed_seconds'] for row in receipt['runs'] if row['mode'] == mode]
        need(all(type(t) is float and 0 < t < 120 for t in times), 'complete timing bounds')
        need(receipt['summary'][mode] == {'median_seconds': statistics.median(times),
                                        'min_seconds': min(times), 'max_seconds': max(times)},
             'timing summary arithmetic')
    a, b = (receipt['summary'][m]['median_seconds'] for m in ('source', 'cached'))
    need(receipt['median_reduction_fraction'] == 1 - b / a, 'timing percentage arithmetic')
    return receipt


def main():
    replay, cache = load('replay'), load('cache')
    cases = conformance(replay, cache.SpanCache)
    controls = rejection_controls(replay)
    source = replay.run('source')
    candidate = replay.run('cached', differential=True)
    # The differential flag changes observation work, never the scientific result.
    a, b = source['scientific'].copy(), candidate['scientific'].copy()
    a.pop('differential')
    b.pop('differential')
    need(a == b, 'complete scientific equality')
    need(candidate['span_cache'] == {'calls': 372952, 'hits': 371802, 'misses': 1150,
                                    'entries': 1150, 'capacity': 4096}, 'complete span work inventory')
    receipt = benchmark_binding(replay)
    need(all(row['result']['scientific'] == source['scientific'] for row in receipt['runs']),
         'timing full scientific payload')
    print('PASS_R2_FRAME_SPAN_CACHE', f'conformance={cases}', f'controls={controls}',
          'mutants=32', 'decisions=253', 'hits=371802')


if __name__ == '__main__':
    main()
