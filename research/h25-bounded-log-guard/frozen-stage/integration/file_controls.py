"""Parent-executed real-file controls; all fixtures are finite and retained."""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import tracemalloc


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def write_pattern(path, size):
    block = bytes(range(256)) * 128
    expected = hashlib.sha256()
    with path.open('xb') as stream:
        remaining = size
        while remaining:
            chunk = block[:min(len(block), remaining)]
            stream.write(chunk)
            expected.update(chunk)
            remaining -= len(chunk)
    return expected.hexdigest()


def run_controls(runner_path, output):
    spec = importlib.util.spec_from_file_location('reviewed_runner_control', runner_path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    root = output / 'real-files'
    root.mkdir()
    rows = []
    # Independent expected hashes are produced by the writer before tracing.
    # The largest fixture is32MiB, and all fixtures together are below44MiB.
    for name, size in [('empty', 0), ('binary', 4352),
                       ('cap-boundary', 2 * 1024 ** 2),
                       ('oversize-small', 4 * 1024 ** 2),
                       ('oversize-large', 32 * 1024 ** 2)]:
        folder = root / name
        folder.mkdir()
        expected_hash = write_pattern(folder / 'stdout.txt', size)
        (folder / 'stderr.txt').write_bytes(b'')
        rss_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        tracemalloc.start()
        tracemalloc.reset_peak()
        stdout, stderr, stop, observed = runner.finalize_logs(folder, None)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rss_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        require(stdout['sha256'] == expected_hash, name + ': full hash mismatch')
        require(stdout['bytes'] == size == stdout['final_bytes'], name + ': count mismatch')
        require(stdout['stable'] and stderr['stable'] and stderr['bytes'] == 0,
                name + ': unstable retained logs')
        oversized = size > runner.OUTPUT_CAP
        require(stop == ('output_cap' if oversized else None), name + ': STOP mismatch')
        require(observed == ('before_stream_hash' if oversized else None), name + ': cap location mismatch')
        require(peak <= 512 * 1024, name + ': traced hashing memory exceeded512KiB')
        require((rss_after - rss_before) * 1024 <= 8 * 1024 ** 2,
                name + ': process peak RSS increment exceeded8MiB')
        rows.append({'case': name, 'bytes': size, 'sha256': expected_hash,
                     'termination': stop, 'output_cap_observed_at': observed,
                     'tracemalloc_peak_bytes': peak,
                     'process_lifetime_max_rss_kib_before': rss_before,
                     'process_lifetime_max_rss_kib_after': rss_after})

    # Mutate actual retained bytes after the first hash. This directly exercises
    # the final cross-file size check without a race or a background writer.
    mutation = root / 'final-size-growth'
    mutation.mkdir()
    (mutation / 'stdout.txt').write_bytes(b'initial')
    (mutation / 'stderr.txt').write_bytes(b'')
    literal_stream = runner.stream_log

    def grow_after_stream(path):
        record = literal_stream(path)
        if path.name == 'stderr.txt':
            with (mutation / 'stdout.txt').open('ab') as stream:
                stream.write(b'growth')
        return record

    runner.stream_log = grow_after_stream
    try:
        stdout, stderr, stop, _ = runner.finalize_logs(mutation, None)
    finally:
        runner.stream_log = literal_stream
    require(stop == 'output_changed_during_hash' and not stdout['stable'],
            'Final growth was admitted')
    require(stdout['bytes'] == 7 and stdout['final_bytes'] == 13,
            'Mutation did not distinguish hashed count and final file size')
    rows.append({'case': 'final-size-growth', 'termination': stop,
                 'bytes_hashed': stdout['bytes'], 'final_bytes': stdout['final_bytes']})

    # Cross the cap only after hashing: both the final cap and count gates must
    # reject it, with the pre-existing output-cap reason retaining precedence.
    mutation = root / 'final-size-cap-growth'
    mutation.mkdir()
    write_pattern(mutation / 'stdout.txt', runner.OUTPUT_CAP)
    (mutation / 'stderr.txt').write_bytes(b'')

    def grow_past_cap_after_stream(path):
        record = literal_stream(path)
        if path.name == 'stderr.txt':
            with (mutation / 'stdout.txt').open('ab') as stream:
                stream.write(b'x')
        return record

    runner.stream_log = grow_past_cap_after_stream
    try:
        stdout, _, stop, observed = runner.finalize_logs(mutation, None)
    finally:
        runner.stream_log = literal_stream
    require(stop == 'output_cap' and observed == 'after_stream_hash' and not stdout['stable'],
            'Final post-hash cap growth was admitted or mislabeled')
    require(stdout['bytes'] == runner.OUTPUT_CAP and stdout['final_bytes'] == runner.OUTPUT_CAP + 1,
            'Final cap-growth counts did not reflect distinct snapshots')
    rows.append({'case': 'final-size-cap-growth', 'termination': stop,
                 'bytes_hashed': stdout['bytes'], 'final_bytes': stdout['final_bytes'],
                 'output_cap_observed_at': observed})

    # Existing primary STOP reasons survive final oversized log inspection.
    large = root / 'oversize-large'
    _, _, stop, _ = runner.finalize_logs(large, 'sampled_group_rss_cap')
    require(stop == 'sampled_group_rss_cap', 'Primary resource STOP was replaced')
    rows.append({'case': 'stop-precedence', 'termination': stop})
    result = {'status': 'PASS', 'scientific_execution': False,
              'runner_sha256': hashlib.sha256(runner_path.read_bytes()).hexdigest(),
              'log_read_chunk_bytes': runner.LOG_CHUNK_BYTES, 'controls': rows}
    (output / 'file-control-results.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    return result
