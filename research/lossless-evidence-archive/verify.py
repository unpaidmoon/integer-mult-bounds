"""Replay the exact retained finite controls; retain every fixture and STOP record.

Apache-2.0. Prepared with substantial OpenAI Codex assistance.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import sys
import tempfile
import types


PINS = {
    'archive.py': '5c60009c9ba1dd9eab5ba85b859ae3ca43b36ed1675100e824a801c9f04804f7',
    'oracle.py': '5617967782a34a142dad25f499f432e6c5736a670bec6db6192c143bb774d9f3',
    'controls.py': 'ece5c5a7f4282c783c7ccd274c5c130b1af12e5dc2cae8946dd9974ff7b66e89',
    'USAGE.md': '13edef89fe8aa68cd662ccc6b0c6fbac7026e08385303c605963594f77c9ba89',
    'COVERAGE-v5.json': 'dfada24bd481a79048ac70eb0bcfcf4d7b43982051b24352401f2d80dd32369e',
}


def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def source_bytes(package):
    result = {}
    for name, digest in PINS.items():
        path = package / name
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size <= 1048576,
                'unsupported or oversized source: ' + name)
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest, 'source pin mismatch: ' + name)
        result[name] = raw
    return result


def timeout(signum, frame):
    raise KeyboardInterrupt('175-second finite replay deadline; retained output requires review')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='fresh absolute external fixture directory, under an owned mode-0700 parent')
    args = parser.parse_args()
    require(sys.platform.startswith('linux'), 'Linux renameat2 and filesystem controls required')
    package = Path(__file__).absolute().parent
    raw = source_bytes(package)
    if args.output is None:
        output = Path(tempfile.mkdtemp(prefix='lossless-evidence-archive-', dir='/tmp')) / 'controls'
    else:
        output = Path(args.output)
        require(output.is_absolute() and os.path.normpath(str(output)) == str(output),
                'output must be a normalized absolute path')
    require(not output.exists() and not output.is_symlink(), 'output must be fresh')
    require(os.path.commonpath((str(package), str(output))) not in (str(package), str(output)),
            'output must be external and disjoint from package source')
    parent = output.parent.lstat()
    require(stat.S_ISDIR(parent.st_mode) and parent.st_uid == os.getuid()
            and stat.S_IMODE(parent.st_mode) == 0o700, 'output parent must be owned and mode 0700')
    print(json.dumps({'status': 'START', 'retained_output': str(output),
                      'optimized': sys.flags.optimize, 'deadline_seconds': 175,
                      'address_space_cap_bytes': 1073741824}), flush=True)
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = min(1073741824, hard) if hard != resource.RLIM_INFINITY else 1073741824
    if soft != resource.RLIM_INFINITY:
        cap = min(cap, soft)
    resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(175)
    try:
        # Read the authenticated .py directly: never import an implementation .pyc.
        controls = types.ModuleType('_retained_lossless_controls')
        controls.__file__ = str(package / 'controls.py')
        exec(compile(raw['controls.py'], controls.__file__, 'exec'), controls.__dict__)
        report = controls.run(str(output))
        require(source_bytes(package) == raw, 'source changed during finite replay')
        require(report['status'] == 'PASS' and report['case_count'] == 98,
                'finite control result incomplete')
        require(sum(row['outcome'] == 'PASS' for row in report['cases']) == 5
                and sum(row['outcome'] == 'EXPECTED_STOP' for row in report['cases']) == 93,
                'finite control outcome mismatch')
        require(report['pending_bill_cases'] == [] and report['source_unchanged'] is True
                and report['source_custody']['unchanged'] is True, 'coverage or custody incomplete')
        require(report['source_sha256'] == PINS, 'executed control source pins differ')
        journal = (output / 'CASE-PREFIX.jsonl').read_bytes()
        require(len(journal) <= 1048576 and journal.endswith(b'\n'), 'case journal incomplete')
        rows = [json.loads(line) for line in journal.splitlines()]
        require(len(rows) == 98 and rows == [dict(ordinal=i + 1, case=row)
                for i, row in enumerate(report['cases'])], 'case journal/report mismatch')
        require(hashlib.sha256(journal).hexdigest() == report['case_prefix']['sha256'],
                'case journal digest mismatch')
        print(json.dumps({'status': 'PASS', 'case_count': 98, 'positive': 5,
                          'expected_STOP': 93, 'retained_output': str(output),
                          'report': str(output / 'CONTROL-RESULT.json'),
                          'optimized': sys.flags.optimize,
                          'source_sha256': PINS,
                          'boundary': 'Finite fixture replay only; historical payload not replayed; no scientific or reclamation claim.'}, sort_keys=True))
    except BaseException as exc:
        print(json.dumps({'status': 'STOP', 'retained_output': str(output),
                          'reason': str(exc)[:2048], 'automatic_retry': False}), flush=True)
        raise
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
