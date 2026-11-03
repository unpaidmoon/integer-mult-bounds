#!/usr/bin/env python3
"""Replay only the unchanged finite log controls in a fresh external workspace."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

PACKAGE = Path(__file__).resolve().parent
RUNNER_SHA256 = '32633e40364d824c9f942af1ad2934da9701117328364c7c3f418b21b2e8054a'
CASES = ('normal', 'binary', 'stderr', 'nonzero', 'oversize-live',
         'oversize-fast', 'stderr-oversize-fast', 'files')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while True:
            block = stream.read(65536)
            if not block:
                return digest.hexdigest()
            digest.update(block)


def authenticate_package():
    manifest = json.loads((PACKAGE / 'MANIFEST.json').read_text())
    expected = manifest['files']
    actual = set()
    for path in PACKAGE.rglob('*'):
        require(not path.is_symlink(), 'Package symlink: ' + str(path))
        if path.is_file() and path.relative_to(PACKAGE).as_posix() != 'MANIFEST.json':
            name = path.relative_to(PACKAGE).as_posix()
            actual.add(name)
            require(name in expected, 'Unlisted shipped file: ' + name)
            row = expected[name]
            require(path.stat().st_size == row['bytes'] and sha256(path) == row['sha256'],
                    'Shipped bytes changed: ' + name)
    require(actual == set(expected), 'Shipped file inventory differs')
    provenance = json.loads((PACKAGE / 'PROVENANCE.json').read_text())
    for row in provenance['files']:
        path = PACKAGE / row['package_path']
        require(path.stat().st_size == row['bytes'] and sha256(path) == row['sha256'],
                'Original source conservation failed: ' + row['package_path'])
    require(sha256(PACKAGE / 'run_guarded.py') == RUNNER_SHA256,
            'Runner is not the reviewed version')
    frozen = PACKAGE / 'frozen-stage'
    stage = json.loads((frozen / 'STAGE.json').read_text())
    require(stage['runner_sha256'] == RUNNER_SHA256, 'Historical runner pin mismatch')
    for name, row in stage['files'].items():
        require(sha256(frozen / name) == row['sha256'], 'Frozen stage hash mismatch: ' + name)
    return manifest


def pattern_control(path):
    """Independent byte oracle for the finite fixture's repeating 0..255 bytes."""
    offset = 0
    with path.open('rb') as stream:
        while True:
            raw = stream.read(65536)
            if not raw:
                return
            expected = (bytes(range(256)) * 257)[offset % 256:offset % 256 + len(raw)]
            require(raw == expected, 'Unexpected fixture byte at offset ' + str(offset))
            offset += len(raw)


def check_receipt(folder, case, code, spent, stage_hash):
    receipt = json.loads((folder / 'receipt.json').read_text())
    start = json.loads((folder / 'START.json').read_text())
    require(receipt['job'] == case and receipt['label'] == case, case + ': identity')
    require(receipt['runner_sha256'] == RUNNER_SHA256 and
            receipt['stage_sha256'] == stage_hash and
            receipt['stage_sha256'] == start['stage_sha256'], case + ': source binding')
    require(receipt['source_bytes_and_modes_unchanged'] is True, case + ': source drift')
    require(receipt['retained_log_bytes_stable'] is True, case + ': unstable retained log')
    require(abs(receipt['spent_before_seconds'] - spent) <= 1e-8, case + ': ledger discontinuity')
    require(receipt['runner_wall_seconds'] >= receipt['wall_seconds'] >= 0,
            case + ': envelope accounting')
    require(receipt['phase_cap_seconds'] == 600 and receipt['log_read_chunk_bytes'] == 65536,
            case + ': changed resource contract')
    for channel in ('stdout', 'stderr'):
        path = folder / (channel + '.txt')
        require(receipt[channel + '_sha256'] == sha256(path), case + ': raw hash mismatch')
        require(receipt[channel + '_bytes'] == receipt[channel + '_final_bytes'] == path.stat().st_size,
                case + ': raw byte-count mismatch')
    expected_status = 'PASS' if case in ('normal', 'binary', 'files') else 'STOP'
    require(receipt['status'] == expected_status, case + ': unexpected admission')
    require(code == (0 if expected_status == 'PASS' else 1), case + ': runner exit mismatch')
    oversize = 'oversize' in case
    require(receipt['termination'] == ('output_cap' if oversize else None), case + ': STOP reason')
    fixed = {'normal': (b'normal control\n', b'', 0),
             'binary': (bytes(range(256)) * 17, b'', 0),
             'stderr': (b'stderr control stdout\n', b'expected stderr\x00\xff\n', 0),
             'nonzero': (b'nonzero control\n', b'', 7)}
    if case in fixed:
        stdout, stderr, exit_code = fixed[case]
        require((folder / 'stdout.txt').read_bytes() == stdout and
                (folder / 'stderr.txt').read_bytes() == stderr and
                receipt['exit'] == exit_code, case + ': literal fixture mismatch')
    elif oversize:
        channel = 'stderr' if case == 'stderr-oversize-fast' else 'stdout'
        other = 'stdout' if channel == 'stderr' else 'stderr'
        size = receipt[channel + '_bytes']
        require(receipt[other + '_bytes'] == 0, case + ': unexpected other channel')
        require(2097152 < size <= (4194304 if case == 'oversize-live' else 2097153),
                case + ': finite output bound')
        require(receipt['output_cap_observed_at'] in
                ('process_monitor', 'before_stream_hash', 'after_stream_hash'),
                case + ': cap observation missing')
        pattern_control(folder / (channel + '.txt'))
    else:
        require(receipt['exit'] == 0 and receipt['stderr_bytes'] == 0, 'files: child failure')
        result = json.loads((folder / 'science/file-control-results.json').read_text())
        require(json.loads((folder / 'stdout.txt').read_text()) == result, 'files: result/output mismatch')
        require(result['status'] == 'PASS' and result['runner_sha256'] == RUNNER_SHA256 and
                result['scientific_execution'] is False, 'files: incomplete result')
        rows = result['controls']
        require([row['case'] for row in rows] ==
                ['empty', 'binary', 'cap-boundary', 'oversize-small', 'oversize-large',
                 'final-size-growth', 'final-size-cap-growth', 'stop-precedence'],
                'files: control inventory mismatch')
        for row in rows[:5]:
            path = folder / 'science/real-files' / row['case'] / 'stdout.txt'
            require(path.stat().st_size == row['bytes'] and sha256(path) == row['sha256'],
                    'files: retained fixture mismatch')
            require(row['tracemalloc_peak_bytes'] <= 512 * 1024 and
                    (row['process_lifetime_max_rss_kib_after'] -
                     row['process_lifetime_max_rss_kib_before']) * 1024 <= 8 * 1024 ** 2,
                    'files: hashing memory gate failed')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-root', type=Path,
                        help='New external directory; retained on success and failure (default: fresh /tmp directory).')
    args = parser.parse_args()
    authenticate_package()
    require(sys.implementation.name == 'cpython' and sys.version_info[:2] == (3, 12),
            'Requires CPython 3.12, matching the unchanged tested runner')
    require(platform.system() == 'Linux', 'Requires Linux /proc and flock')
    for name in ('/usr/bin/python3.12', '/usr/bin/time', '/usr/lib/python3.12/fractions.py'):
        require(Path(name).is_file(), 'Missing unchanged runner dependency: ' + name)
    if args.work_root is None:
        root = Path(tempfile.mkdtemp(prefix='h25-bounded-log-guard-', dir='/tmp')).resolve()
    else:
        root = args.work_root.expanduser().resolve()
        require(root != PACKAGE and PACKAGE not in root.parents, 'Runtime output must be external to package')
        root.mkdir(parents=True, exist_ok=False)
    print(json.dumps({'status': 'START', 'external_workspace': str(root),
                      'optimized': bool(sys.flags.optimize)}), flush=True)
    shutil.copyfile(PACKAGE / 'run_guarded.py', root / 'run_guarded.py')
    stage = root / 'stages/log-v1'
    shutil.copytree(PACKAGE / 'frozen-stage', stage)
    # copytree preserves read-only modes; rewrite only our private metadata copies.
    for name in ('JOBS.json', 'STAGE.json'):
        (stage / name).chmod(0o644)
    jobs = json.loads((stage / 'JOBS.json').read_text())
    for job in jobs.values():
        job['optimized'] = bool(sys.flags.optimize)
    (stage / 'JOBS.json').write_text(json.dumps(jobs, indent=2, sort_keys=True) + '\n')
    rows = {}
    for path in sorted(stage.rglob('*')):
        if path.is_file() and path.name != 'STAGE.json':
            path.chmod(0o444)
            rows[path.relative_to(stage).as_posix()] = {'mode': 0o444, 'sha256': sha256(path)}
    stage_metadata = {'schema': 'h25-log-guard-portable-stage-v1', 'files': rows,
                      'runner_sha256': RUNNER_SHA256, 'scientific_execution': False}
    (stage / 'STAGE.json').write_text(json.dumps(stage_metadata, indent=2, sort_keys=True) + '\n')
    (stage / 'STAGE.json').chmod(0o444)
    (root / 'control').mkdir()
    (root / 'control/EXECUTION-PHASE.json').write_text(
        json.dumps({'aggregate_cap_seconds': 600}, sort_keys=True) + '\n')
    env = os.environ.copy()
    for name in ('PYTHONPATH', 'PYTHONOPTIMIZE', 'PYTHONINSPECT', 'PYTHONSTARTUP', 'PYTHONPYCACHEPREFIX'):
        env.pop(name, None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    deadline = time.monotonic() + 170
    receipts = []
    spent = 0.0
    try:
        for case in CASES:
            remaining = deadline - time.monotonic()
            require(remaining > 0, 'Adapter total 170-second envelope expired')
            command = [sys.executable, '-B', str(root / 'run_guarded.py'), 'log-v1', case, case]
            with (root / (case + '-runner-stdout.txt')).open('wb') as out, \
                    (root / (case + '-runner-stderr.txt')).open('wb') as err:
                completed = subprocess.run(command, cwd=root, env=env, stdout=out, stderr=err,
                                           timeout=remaining, check=False)
            require((root / (case + '-runner-stderr.txt')).stat().st_size == 0,
                    case + ': unexpected runner diagnostic')
            receipt = check_receipt(root / 'runtime/runs' / case, case, completed.returncode,
                                    spent, sha256(stage / 'STAGE.json'))
            receipts.append(receipt)
            spent += receipt['runner_wall_seconds']
        authenticate_package()
        result = {'status': 'PASS', 'scope': 'original finite log controls only',
                  'scientific_execution': False, 'optimized': bool(sys.flags.optimize),
                  'external_workspace': str(root), 'process_controls': len(receipts),
                  'real_file_controls': 8, 'runner_wall_seconds_sum': spent,
                  'receipt_tail_excluded_from_runner_wall_seconds': True,
                  'raw_attempts_and_expected_stops_retained': True,
                  'runner_sha256': RUNNER_SHA256}
        (root / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
        print(json.dumps(result, sort_keys=True), flush=True)
    except BaseException as error:
        (root / 'FAILURE.json').write_text(json.dumps({'status': 'FAIL', 'error': repr(error),
                                                      'completed_controls': len(receipts),
                                                      'external_workspace': str(root)},
                                                     sort_keys=True, indent=2) + '\n')
        raise


if __name__ == '__main__':
    main()
