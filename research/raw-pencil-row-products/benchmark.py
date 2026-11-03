"""Five alternating fresh-process comparisons of the complete retained caller."""
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[1]


def main():
    expected = json.loads((ROOT.parent / 'raw-pencil-decomposition/RESULT.json').read_text())
    samples = {'reference': [], 'fast': []}
    output_hashes = set()
    for pair in range(5):
        for mode in ('reference', 'fast'):
            command = [sys.executable, '-I', '-W', 'error', '-B', str(ROOT / 'replay.py'), mode]
            started = time.perf_counter()
            result = subprocess.run(command, cwd=REPOSITORY, capture_output=True,
                                    check=True, timeout=240)
            elapsed = time.perf_counter() - started
            lines = result.stdout.splitlines()
            if result.stderr or len(lines) != 6 or json.loads(lines[-1]) != expected:
                raise ValueError('complete scientific output differs or stderr is nonempty')
            samples[mode].append(elapsed)
            output_hashes.add(hashlib.sha256(result.stdout).hexdigest())
            print(json.dumps({'pair': pair, 'mode': mode, 'seconds': elapsed}),
                  file=sys.stderr, flush=True)
    if len(output_hashes) != 1:
        raise ValueError('scientific output bytes differ')
    medians = {mode: statistics.median(values) for mode, values in samples.items()}
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(ROOT.iterdir()) if path.is_file()}
    print(json.dumps({'status': 'PASS_RAW_PENCIL_BENCHMARK', 'failures': 0,
                      'python': sys.version, 'platform': platform.platform(),
                      'samples_seconds': samples, 'median_seconds': medians,
                      'fraction_wall_time_saved': 1 - medians['fast'] / medians['reference'],
                      'complete_output_sha256': sorted(output_hashes),
                      'package_sha256': hashes}, sort_keys=True))


if __name__ == '__main__':
    main()
