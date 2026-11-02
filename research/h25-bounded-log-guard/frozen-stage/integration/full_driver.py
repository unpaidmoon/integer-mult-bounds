"""Bounded process-only controls; no scientific imports or arithmetic work."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time


def write_bytes(fd, value):
    view = memoryview(value)
    while view:
        view = view[os.write(fd, view):]


def repeated_output(fd, size):
    block = bytes(range(256)) * 256
    while size:
        current = block[:min(size, len(block))]
        write_bytes(fd, current)
        size -= len(current)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--lanes', required=True)
    parser.add_argument('--finite-only', action='store_true')
    args = parser.parse_args()
    args.output.mkdir()
    (args.output / 'fixture.json').write_text(json.dumps({
        'case': args.lanes, 'scientific_execution': False,
        'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, sort_keys=True) + '\n')
    if args.lanes == 'normal':
        write_bytes(1, b'normal control\n')
    elif args.lanes == 'binary':
        write_bytes(1, bytes(range(256)) * 17)
    elif args.lanes == 'stderr':
        write_bytes(1, b'stderr control stdout\n')
        write_bytes(2, b'expected stderr\x00\xff\n')
    elif args.lanes == 'nonzero':
        write_bytes(1, b'nonzero control\n')
        raise SystemExit(7)
    elif args.lanes == 'oversize-live':
        repeated_output(1, 4 * 1024 ** 2)
        time.sleep(1)
    elif args.lanes == 'oversize-fast':
        repeated_output(1, 2 * 1024 ** 2 + 1)
    elif args.lanes == 'stderr-oversize-fast':
        repeated_output(2, 2 * 1024 ** 2 + 1)
    elif args.lanes == 'files':
        # Parent puts exact reviewed source copies in this immutable stage.
        from file_controls import run_controls
        result = run_controls(Path(__file__).resolve().parents[1] / 'runner_under_test.py', args.output)
        write_bytes(1, (json.dumps(result, sort_keys=True) + '\n').encode())
    else:
        raise ValueError('Unknown frozen process control')


if __name__ == '__main__':
    main()
