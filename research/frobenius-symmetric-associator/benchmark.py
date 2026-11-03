"""Time the complete primary caller; produced by Nick Petalas. Apache-2.0."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def execute(engine):
    command = [sys.executable, '-I', '-B', '-W', 'error',
               str(HERE / 'adapter.py'), '--engine', engine, '--caller', 'main']
    start = time.perf_counter()
    result = subprocess.run(command, capture_output=True, check=True, timeout=120)
    elapsed = time.perf_counter() - start
    if result.stderr:
        raise ValueError('unexpected caller stderr: ' + result.stderr.decode())
    report = json.loads(result.stdout)
    if report.get('status') != 'PASS_FROBENIUS_ALGEBRA_RECOGNITION':
        raise ValueError('caller did not complete')
    return elapsed, result.stdout


def run(samples):
    if not 5 <= samples <= 15:
        raise ValueError('samples must be between five and fifteen')
    values = {'baseline': [], 'symmetric': []}
    expected = None
    order = []
    for trial in range(samples):
        engines = ('baseline', 'symmetric') if trial % 2 == 0 else ('symmetric', 'baseline')
        for engine in engines:
            elapsed, output = execute(engine)
            if expected is None:
                expected = output
            if output != expected:
                raise ValueError('complete caller bytes changed')
            values[engine].append(elapsed)
            order.append(engine)
    medians = {key: statistics.median(value) for key, value in values.items()}
    code = {name: sha256((HERE / name).read_bytes()).hexdigest()
            for name in ('adapter.py', 'verify.py', 'benchmark.py', 'SOURCES.json')}
    return {'status': 'PASS_COMPLETE_FROBENIUS_TIMING', 'errors': 0,
            'samples_per_engine': samples, 'order': order, 'seconds': values,
            'median_seconds': medians,
            'range_seconds': {key: [min(value), max(value)] for key, value in values.items()},
            'wall_time_reduction_fraction': 1 - medians['symmetric'] / medians['baseline'],
            'complete_report_sha256': sha256(expected).hexdigest(),
            'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
            'cpu_count': os.cpu_count(), 'load_average_at_finish': os.getloadavg(),
            'code_sha256': code,
            'timed_scope': 'Fresh process, source authentication, full primary run, JSON stdout; oracle companion not timed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run(args.samples), sort_keys=True, indent=2))
