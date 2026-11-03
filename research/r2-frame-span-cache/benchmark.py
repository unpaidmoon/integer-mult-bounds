"""Measure complete fresh callers, never profiler times. Nick Petalas, Apache-2.0."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def measure(directory, index, mode):
    output = directory / f'run-{index:02d}-{mode}.json'
    cmd = [sys.executable, '-I', '-W', 'error', '-B', str(PACKAGE / 'replay.py'),
           '--mode', mode, '--output', str(output)]
    start = time.perf_counter()
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=True)
    elapsed = time.perf_counter() - start
    result = json.loads(output.read_bytes())
    need('PASS_R2_SPAN_REPLAY' in done.stdout, 'complete caller marker')
    need(result['scientific']['decisions'] == {'calls': 253, 'accepted': 244, 'rejected': 9},
         'complete operator decisions')
    for row in result['scientific']['providers'].values():
        need(len(row['mutants']) == 16 and row['original_unchanged'], 'complete mutant execution')
    return {'mode': mode, 'elapsed_seconds': elapsed, 'result': result}


def benchmark(directory, pairs):
    need(type(pairs) is int and 5 <= pairs <= 10, 'five to ten complete pairs')
    directory.mkdir()
    rows = []
    for i in range(pairs):
        for mode in ('source', 'cached'):
            rows.append(measure(directory, i, mode))
    first = rows[0]['result']
    for row in rows:
        result = row['result']
        need(result['scientific'] == first['scientific'], 'full scientific payload mismatch')
        need(result['source_sha256'] == first['source_sha256'], 'source mismatch')
        need(result['implementation_sha256'] == first['implementation_sha256'], 'implementation mismatch')
    summary = {}
    for mode in ('source', 'cached'):
        times = [r['elapsed_seconds'] for r in rows if r['mode'] == mode]
        summary[mode] = {'median_seconds': statistics.median(times),
                         'min_seconds': min(times), 'max_seconds': max(times)}
    a, b = (summary[m]['median_seconds'] for m in ('source', 'cached'))
    return {'schema_version': 1, 'pairs': pairs, 'failures': 0, 'summary': summary,
            'median_reduction_fraction': 1 - b / a, 'runs': rows,
            'python': sys.version, 'platform': platform.platform(), 'cpu_count': os.cpu_count(),
            'load_average': os.getloadavg(), 'interpreter': sys.executable,
            'benchmark_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'Fresh serial complete PR3240 path-copy callers; source authentication, '
                     'snapshots, all original controls, output serialization and process startup included. '
                     'Native artifact generation is excluded. Shared-host local measurement.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--pairs', type=int, default=5)
    args = parser.parse_args()
    result = benchmark(args.directory, args.pairs)
    with (args.directory / 'BENCHMARK.json').open('x') as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(json.dumps(result['summary'], sort_keys=True))
    print('PASS_R2_SPAN_BENCHMARK', 'failures=0', 'reduction=' +
          str(result['median_reduction_fraction']))


if __name__ == '__main__':
    main()
