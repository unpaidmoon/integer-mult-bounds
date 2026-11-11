"""Parent-executed bounded retention controls; never imports scientific modules."""
import argparse
import errno
from contextlib import contextmanager
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import types


def load(path, name):
    raw = path.read_bytes()
    if len(raw) > 1048576:
        raise RuntimeError('control source cap')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def check(value, reason):
    if not value:
        raise RuntimeError(reason)


@contextmanager
def replacement(owner, name, value):
    original = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield original
    finally:
        setattr(owner, name, original)


class CaseJournal(list):
    """Bounded append-only ordered case prefix, retained on a later suite failure."""
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.written_bytes = 0
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            info = os.fstat(fd)
            self.identity = (info.st_dev, info.st_ino)
            os.fsync(fd)
        finally:
            os.close(fd)
        parent = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(parent)
        finally:
            os.close(parent)

    def append(self, row):
        record = {'ordinal': len(self) + 1, 'case': row}
        raw = (json.dumps(record, sort_keys=True, ensure_ascii=True,
                          separators=(',', ':')) + '\n').encode('ascii')
        check(len(self) < 128 and len(raw) <= 4096 and
              self.written_bytes + len(raw) <= 1048576, 'case journal bound')
        fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW)
        try:
            info = os.fstat(fd)
            check(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
                  (info.st_dev, info.st_ino) == self.identity and
                  info.st_size == self.written_bytes, 'case journal identity/length')
            view = memoryview(raw)
            while view:
                written = os.write(fd, view)
                check(written > 0, 'case journal short write')
                self.written_bytes += written
                view = view[written:]
            os.fsync(fd)
        finally:
            os.close(fd)
        super().append(row)


def run(root):
    root = Path(root)
    check(root.is_absolute() and not root.exists(), 'fresh absolute control output required')
    root.mkdir(mode=0o700)
    results = CaseJournal(root / 'CASE-PREFIX.jsonl')
    here = Path(__file__).absolute().parent
    archive, oracle = load(here / 'archive.py', '_archive_control'), load(here / 'oracle.py', '_oracle_control')
    source = root / 'source'
    source.mkdir(mode=0o750)
    for name in ('run-pass-a', 'run-pass-b', 'run-stop'):
        (source / name).mkdir(mode=0o750)
    (source / 'root-receipt.json').write_bytes(b'{"root":"receipt"}\n')
    (source / 'run-pass-a' / 'empty-directory').mkdir(mode=0o555)
    payloads = [b'', bytes(range(256)) + b'\x00\xff\n', b'witness-fixture\n' * 37]
    for run_name in ('run-pass-a', 'run-pass-b'):
        for i, payload in enumerate(payloads):
            (source / run_name / ('payload-%d.bin' % i)).write_bytes(payload)
        (source / run_name / 'receipt.json').write_bytes(b'{"status":"PASS","preserved":true}\n')
    (source / 'run-stop' / 'receipt.json').write_bytes(b'{"status":"STOP","reason":"retained fixture failure"}\n')
    (source / 'run-stop' / 'stderr.bin').write_bytes(b'\x00\xff retained failure\n')
    (source / 'run-pass-a' / 'unicode-é.txt').write_bytes(b'ASCII bytes under Unicode path\n')
    for size in (0, 1, 1023, 1024, 1025, 2048, 2049):
        (source / 'run-pass-a' / ('boundary-%d.bin' % size)).write_bytes(bytes([size % 251]) * size)
    (source / 'run-pass-a' / 'payload-0.bin').chmod(0o444)
    (source / 'run-pass-a' / 'payload-1.bin').chmod(0o755)
    (source / 'run-pass-b' / 'payload-1.bin').chmod(0o640)
    inventory_path = root / 'original.json'
    anchor = oracle.write_inventory(str(source), str(inventory_path))
    original_inventory = json.loads(inventory_path.read_bytes())
    check(original_inventory['counts']['bytes'] <= 65536 and len(original_inventory['entries']) <= 64,
          'fixture bill exceeded')
    limits = dict(chunk_bytes=1024)
    package = root / 'package'
    created = archive.create_archive(str(source), str(inventory_path), anchor['inventory_sha256'],
                                     str(package), str(root / 'create-positive'), limits=limits)
    pin = created['root_sha256']
    restored = root / 'restored'
    restoration = archive.restore_archive(str(package), pin, str(restored), str(root / 'restore-positive'), limits)
    compare = oracle.collect(str(restored), require_single_links=True)
    check(oracle.content_projection(compare) == oracle.content_projection(original_inventory),
          'independent full fixture restoration')
    package_root = json.loads((package / 'ROOT.json').read_bytes())
    expected_blobs = {row['sha256']: row['size'] for row in original_inventory['entries'] if row['kind'] == 'file'}
    check(package_root['blobs'] == expected_blobs, 'exact unique blob accounting')
    check((restored / 'run-stop' / 'receipt.json').read_bytes() ==
          (source / 'run-stop' / 'receipt.json').read_bytes(), 'failure receipt bytes lost')
    results.append(dict(id='P01-P04', outcome='PASS', source_bytes=original_inventory['counts']['bytes'],
                        archive_bytes=created['accounting']['archive_logical_bytes'],
                        restored_bytes=restoration['restored_logical_bytes']))
    # A separate bounded fixture proves old source/package locations are unavailable.
    offline_source = root / 'offline-source'
    shutil.copytree(source, offline_source, copy_function=shutil.copy2)
    offline_inventory = root / 'offline-original.json'
    offline_anchor = oracle.write_inventory(str(offline_source), str(offline_inventory))
    offline_package = root / 'offline-package'
    offline_created = archive.create_archive(str(offline_source), str(offline_inventory),
                                             offline_anchor['inventory_sha256'], str(offline_package),
                                             str(root / 'offline-create-attempt'), limits=limits)
    standalone = root / 'standalone-package'
    shutil.copytree(offline_package, standalone, copy_function=shutil.copy2)
    offline_source.rename(root / 'offline-source-preserved')
    offline_package.rename(root / 'offline-package-preserved')
    check(not offline_source.exists() and not offline_package.exists(), 'old fixture locations still available')
    separate_archive = load(standalone / 'tools/archive.py', '_standalone_archive_control')
    separate_archive.restore_archive(str(standalone), offline_created['root_sha256'],
                                     str(root / 'standalone-restored'), str(root / 'standalone-attempt'), limits)
    results.append(dict(id='P05', outcome='PASS', historical_source_and_package_unavailable=True,
                        original_fixture_bytes_preserved_at_new_locations=True))

    def clone(label):
        target = root / ('package-' + label)
        shutil.copytree(package, target, copy_function=shutil.copy2)
        return target

    def put(path, raw):
        path.chmod(0o600)
        path.write_bytes(raw)
        path.chmod(0o444)

    def repin(target, name=None, value=None, raw=None, root_mutation=None):
        data = json.loads((target / 'ROOT.json').read_bytes())
        if name is not None:
            content = raw if raw is not None else archive.canonical(value)
            put(target / name, content)
            data['metadata'][name] = dict(size=len(content), sha256=hashlib.sha256(content).hexdigest(), mode=0o444)
            if name == 'ORIGINAL.json':
                data['inventory_sha256'] = hashlib.sha256(content).hexdigest()
        if root_mutation:
            root_mutation(data)
        root_raw = archive.canonical(data)
        digest = hashlib.sha256(root_raw).hexdigest()
        put(target / 'ROOT.json', root_raw)
        put(target / 'COMPLETE.json', archive.canonical(dict(schema=archive.FORMAT, root_sha256=digest)))
        return digest

    def rejected(label, operation, reason=None, attempt=None):
        try:
            operation()
        except BaseException as error:
            check(not isinstance(error, (SystemExit, KeyboardInterrupt)), 'unexpected control interruption')
            check(reason is None or reason in str(error), label + ': unexpected rejection: ' + str(error))
            if attempt is not None:
                receipt = json.loads((attempt / 'RESULT.json').read_bytes())
                check(receipt['status'] == 'STOP', label + ': no retained STOP receipt')
            results.append(dict(id=label, outcome='EXPECTED_STOP', reason=str(error)[:240]))
            return
        raise RuntimeError(label + ': rejection absent')

    def bad_package(label, mutation, expected_reason=None, fresh_pin=False):
        target = clone(label)
        changed = mutation(target)
        chosen_pin = changed if fresh_pin else pin
        attempt = root / ('attempt-' + label)
        rejected(label, lambda: archive.verify_archive(str(target), chosen_pin, str(attempt), limits),
                 expected_reason, attempt)

    def stage_for(attempt):
        return Path(json.loads((attempt / 'START.json').read_bytes())['context']['staging'])

    # Authenticated malformed originals exercise parser/path admission, not only ROOT rejection.
    for index, path in enumerate(('/absolute', '../escape', './dot', 'a//b', 'a\\b', 'a\x00b', '', 'C:/escape')):
        def mutate(target, path=path):
            inv = json.loads((target / 'ORIGINAL.json').read_bytes())
            inv['entries'][0]['path'] = path
            return repin(target, 'ORIGINAL.json', inv)
        bad_package('N01-%d' % index, mutate, fresh_pin=True)
    def duplicate_key(target):
        raw = (target / 'runs/0000.json').read_bytes()
        return repin(target, 'runs/0000.json', raw=b'{"schema":"duplicate",' + raw[1:])
    bad_package('N03-key', duplicate_key, 'duplicate JSON key', True)
    def duplicate_path(target):
        inv = json.loads((target / 'ORIGINAL.json').read_bytes())
        inv['entries'].insert(1, dict(inv['entries'][0]))
        return repin(target, 'ORIGINAL.json', inv)
    bad_package('N03-path', duplicate_path, 'duplicate/unsorted', True)
    def file_parent(target):
        inv = json.loads((target / 'ORIGINAL.json').read_bytes())
        inv['entries'][0]['path'] = 'absent/child'
        return repin(target, 'ORIGINAL.json', inv)
    bad_package('N03-parent', file_parent, 'missing directory', True)
    def omit_manifest(target):
        data = json.loads((target / 'runs/0001.json').read_bytes())
        data['entries'].pop()
        repin(target, 'runs/0001.json', data)
    bad_package('N04', omit_manifest, 'ROOT authentication')
    def missing_blob(target):
        folder = target / 'blobs/sha256'
        folder.chmod(0o755)
        next(folder.iterdir()).rename(folder / 'missing-preserved')
        folder.chmod(0o555)
    bad_package('N06-missing', missing_blob, 'package complete membership')
    def missing_marker(target):
        target.chmod(0o755)
        (target / 'COMPLETE.json').rename(target / 'COMPLETE.saved')
        target.chmod(0o555)
    bad_package('N06-partial', missing_marker)
    nonempty_digest = next(d for d, size in expected_blobs.items() if size > 2)
    def corrupt_blob(target):
        file = target / 'blobs/sha256' / nonempty_digest
        raw = file.read_bytes()
        put(file, bytes([raw[0] ^ 1]) + raw[1:])
    bad_package('N07', corrupt_blob, 'payload hash/length mismatch')
    bad_package('N08', lambda t: (t / 'ROOT.json').chmod(0o644), 'package entry type/mode')
    def symlink_blob(target):
        folder = target / 'blobs/sha256'
        folder.chmod(0o755)
        file = folder / nonempty_digest
        file.rename(folder / 'retained-original')
        file.symlink_to(source / 'run-pass-a/payload-1.bin')
        folder.chmod(0o555)
    bad_package('N02', symlink_blob, 'symlink/special file')
    for index, value in enumerate((-1, True, 1.5, 2147483649)):
        bad_package('N11-%d' % index,
                    lambda t, value=value: repin(t, root_mutation=lambda r: r.update(source_bytes=value)),
                    'source_bytes bounds/type', True)
    bad_package('N11-schema', lambda t: repin(t, root_mutation=lambda r: r.update(schema='unknown')),
                'ROOT format', True)
    target = clone('N12')
    small = {**limits, 'max_root_bytes': 32}
    attempt = root / 'attempt-N12'
    rejected('N12', lambda: archive.verify_archive(str(target), pin, str(attempt), small),
             'metadata size/type cap', attempt)
    attempt = root / 'attempt-N13'
    rejected('N13', lambda: archive.restore_archive(str(package), pin, str(root / 'too-large-restore'),
             str(attempt), {**limits, 'max_total_bytes': 1}), 'source_bytes bounds/type', attempt)
    check(not stage_for(attempt).exists(), 'oversize preflight wrote output')
    exists = root / 'existing-destination'
    exists.mkdir()
    (exists / 'sentinel').write_bytes(b'preserve')
    attempt = root / 'attempt-N14-existing'
    rejected('N14-existing', lambda: archive.restore_archive(str(package), pin, str(exists), str(attempt), limits),
             'destination exists', attempt)
    check((exists / 'sentinel').read_bytes() == b'preserve', 'existing destination changed')
    attempt = root / 'attempt-N14-race'
    race_target = root / 'raced-destination'
    original_publish = archive.publish
    def raced_publish(stage, destination):
        Path(destination).mkdir()
        (Path(destination) / 'sentinel').write_bytes(b'race-preserved')
        original_publish(stage, destination)
    with replacement(archive, 'publish', raced_publish):
        rejected('N14-race', lambda: archive.restore_archive(str(package), pin, str(race_target), str(attempt), limits),
                 attempt=attempt)
    check((race_target / 'sentinel').read_bytes() == b'race-preserved', 'raced destination overwritten')
    rejected('N15', lambda: archive.restore_archive(str(package), pin, str(package / 'inside'),
             str(root / 'attempt-N15'), limits), 'overlapping')
    attempt = root / 'attempt-N21'
    rejected('N21', lambda: archive.verify_archive(str(package), '0' * 64, str(attempt), limits),
             'ROOT authentication', attempt)
    # Source drift and unsupported modes use fresh copies; original fixtures remain unchanged.
    changed_source = root / 'changed-source'
    shutil.copytree(source, changed_source)
    changed_inventory = root / 'changed-original.json'
    changed_anchor = oracle.write_inventory(str(changed_source), str(changed_inventory))
    (changed_source / 'new-file').write_bytes(b'not in inventory')
    attempt = root / 'attempt-N05'
    rejected('N05', lambda: archive.create_archive(str(changed_source), str(changed_inventory),
             changed_anchor['inventory_sha256'], str(root / 'archive-N05'), str(attempt), limits=limits),
             'source root changed', attempt)
    n05_receipt = json.loads((attempt / 'RESULT.json').read_bytes())
    check(n05_receipt['counters']['payload_write_bytes'] == 0 and not stage_for(attempt).exists(),
          'source-root drift must reject before snapshot payload creation')
    special = root / 'special-source'
    shutil.copytree(source, special)
    (special / 'run-stop/receipt.json').chmod(0o1644)
    rejected('N16', lambda: oracle.collect(str(special)), 'unsupported special permission')
    # A short-write return must be handled, while a write failure retains partial output.
    attempt = root / 'attempt-short-writes'
    original_stream = archive.stream
    real_write = os.write
    def short_stream(*args, **kwargs):
        target_fd = kwargs.get('target', args[6] if len(args) > 6 else None)
        if target_fd is None:
            return original_stream(*args, **kwargs)
        with replacement(os, 'write', lambda fd, data: real_write(fd, data[:7]) if fd == target_fd else real_write(fd, data)):
            return original_stream(*args, **kwargs)
    with replacement(archive, 'stream', short_stream):
        archive.restore_archive(str(package), pin, str(root / 'short-write-restored'), str(attempt), limits)
    results.append(dict(id='P06-short-write', outcome='PASS'))
    attempt = root / 'attempt-N17'
    def failed_stream(*args, **kwargs):
        target_fd = kwargs.get('target', args[6] if len(args) > 6 else None)
        if target_fd is not None:
            with replacement(os, 'write', lambda fd, data: 0 if fd == target_fd else real_write(fd, data)):
                return original_stream(*args, **kwargs)
        return original_stream(*args, **kwargs)
    with replacement(archive, 'stream', failed_stream):
        rejected('N17', lambda: archive.restore_archive(str(package), pin, str(root / 'failed-restore'),
                 str(attempt), limits), 'zero-length stream write', attempt)
    check(stage_for(attempt).exists() and not (root / 'failed-restore').exists(), 'partial write evidence lost')
    # Mutation after oracle computation invalidates the staged inode metadata before commit.
    attempt = root / 'attempt-N19'
    original_verify = archive._verify
    calls = [0]
    def mutate_before_commit(*args, **kwargs):
        value = original_verify(*args, **kwargs)
        calls[0] += 1
        if calls[0] == 2:
            file = stage_for(attempt) / 'run-stop/receipt.json'
            file.write_bytes(file.read_bytes() + b'changed')
        return value
    with replacement(archive, '_verify', mutate_before_commit):
        rejected('N19', lambda: archive.restore_archive(str(package), pin, str(root / 'mutated-restore'),
                 str(attempt), limits), 'restored tree changed before commit', attempt)
    # Unsupported no-replace publication must not use a replacement fallback.
    attempt = root / 'attempt-N22'
    def no_publish(*args):
        raise archive.Rejected('renameat2 unavailable (control)')
    with replacement(archive, 'publish', no_publish):
        rejected('N22', lambda: archive.restore_archive(str(package), pin, str(root / 'unsupported-restore'),
                 str(attempt), limits), 'renameat2 unavailable', attempt)
    # Aliased payload is rejected even though bytes and its digest remain correct.
    def hardlinked(target):
        folder = target / 'blobs/sha256'
        folder.chmod(0o755)
        leaf = folder / nonempty_digest
        external = root / ('external-alias-' + nonempty_digest)
        os.link(leaf, external)
        folder.chmod(0o555)
    bad_package('N20', hardlinked, 'file hardlink alias')
    # Fresh verification must not accept a previously verified but now-mutated package.
    stale = clone('N24')
    archive.verify_archive(str(stale), pin, str(root / 'attempt-N24-before'), limits)
    corrupt_blob(stale)
    attempt = root / 'attempt-N24-after'
    rejected('N24', lambda: archive.verify_archive(str(stale), pin, str(attempt), limits),
             'payload hash/length mismatch', attempt)
    def wrong_owner(target):
        manifest = json.loads((target / 'runs/0001.json').read_bytes())
        manifest['run'] = 'wrong-run'
        return repin(target, 'runs/0001.json', manifest)
    bad_package('N23', wrong_owner, 'run manifest ownership', True)
    # A reused blob is rehashed immediately before reuse; its address is insufficient.
    attempt = root / 'attempt-N09'
    corrupted = [False]
    def corrupt_reuse(*args, **kwargs):
        if (not corrupted[0] and args[0] == str(stage_for(attempt)) and
                args[4] == 'blob_read_bytes' and args[5]['size'] > 0):
            leaf = Path(args[0]) / args[1]
            value = leaf.read_bytes()
            put(leaf, bytes([value[0] ^ 1]) + value[1:])
            corrupted[0] = True
        return original_stream(*args, **kwargs)
    with replacement(archive, 'stream', corrupt_reuse):
        rejected('N09', lambda: archive.create_archive(str(source), str(inventory_path),
                 anchor['inventory_sha256'], str(root / 'archive-N09'), str(attempt), limits=limits),
                 'payload hash/length mismatch', attempt)
    check(corrupted[0], 'reuse corruption control not triggered')
    # Mutate only a separate fixture after the first read inside a source stream.
    drift_source = root / 'drift-source'
    shutil.copytree(source, drift_source)
    drift_inventory = root / 'drift-original.json'
    drift_anchor = oracle.write_inventory(str(drift_source), str(drift_inventory))
    attempt = root / 'attempt-N10'
    real_read = os.read
    drifted = [False]
    def drift_stream(*args, **kwargs):
        if args[0] != str(drift_source) or drifted[0]:
            return original_stream(*args, **kwargs)
        def read_and_drift(fd, length):
            value = real_read(fd, length)
            if value and not drifted[0]:
                leaf = drift_source / args[1]
                with leaf.open('ab') as out:
                    out.write(b'drift')
                drifted[0] = True
            return value
        with replacement(os, 'read', read_and_drift):
            return original_stream(*args, **kwargs)
    with replacement(archive, 'stream', drift_stream):
        rejected('N10', lambda: archive.create_archive(str(drift_source), str(drift_inventory),
                 drift_anchor['inventory_sha256'], str(root / 'archive-N10'), str(attempt), limits=limits),
                 attempt=attempt)
    check(drifted[0], 'mid-read drift control not triggered')
    # Interrupted publication preserves its partial tree and an explicit STOP.
    for phase in ('before-marker', 'before-rename', 'after-rename'):
        attempt = root / ('attempt-N18-' + phase)
        output = root / ('archive-N18-' + phase)
        real_new = archive.write_new
        def interrupted_new(path, *args, **kwargs):
            if path.endswith('/COMPLETE.json'):
                raise InterruptedError('control interrupted before marker')
            return real_new(path, *args, **kwargs)
        def interrupted_publish(stage, destination, phase=phase):
            if phase == 'after-rename':
                original_publish(stage, destination)
            raise InterruptedError('control interrupted ' + phase)
        owner, name, replacement_value = (archive, 'write_new', interrupted_new) if phase == 'before-marker' else (archive, 'publish', interrupted_publish)
        with replacement(owner, name, replacement_value):
            rejected('N18-' + phase, lambda: archive.create_archive(str(source), str(inventory_path),
                     anchor['inventory_sha256'], str(output), str(attempt), limits=limits),
                     'control interrupted', attempt)
        check(output.exists() == (phase == 'after-rename'), 'interrupted publication state')
    # Receipt-writing failure must not replace the first operation failure.
    attempt = root / 'attempt-secondary-receipt-failure'
    real_new = archive.write_new
    def result_write_failure(path, *args, **kwargs):
        if path.endswith('/RESULT.json'):
            raise OSError('secondary receipt failure control')
        return real_new(path, *args, **kwargs)
    with replacement(archive, 'write_new', result_write_failure):
        rejected('N17-secondary-receipt', lambda: archive.verify_archive(str(package), '0' * 64,
                 str(attempt), limits), 'ROOT authentication mismatch')
    check((attempt / 'START.json').is_file() and not (attempt / 'RESULT.json').exists(),
          'unclosed receipt failure attempt missing')
    # Unsupported owner access is rejected before payload creation/restoration.
    for index, (kind, mode) in enumerate((('file', 0o040), ('dir', 0o040), ('dir', 0o050))):
        mode_source = root / ('mode-source-%d' % index)
        mode_source.mkdir()
        target = mode_source / 'entry'
        if kind == 'file':
            target.write_bytes(b'owner-read required')
        else:
            target.mkdir()
        target.chmod(mode)
        rejected('N16-owner-mode-%d' % index, lambda mode_source=mode_source:
                 oracle.collect(str(mode_source)), 'unsupported owner access mode')
    # Source symlinks, including a root ancestor, never become traversal permissions.
    link = root / 'source-alias'
    link.symlink_to(source, target_is_directory=True)
    rejected('N02-ancestor', lambda: oracle.collect(str(link)))
    fifo = root / 'fifo-source'
    fifo.mkdir()
    os.mkfifo(fifo / 'pipe')
    rejected('N16-fifo', lambda: oracle.collect(str(fifo)), 'unsupported symlink or special file')
    attributes = root / 'xattr-source'
    attributes.mkdir()
    attribute_file = attributes / 'file'
    attribute_file.write_bytes(b'xattr fixture')
    os.setxattr(attribute_file, 'user.h25-control', b'present')
    rejected('N16-xattr', lambda: oracle.collect(str(attributes)), 'unsupported xattrs/ACLs')
    invalid = root / 'invalid-name-source'
    invalid.mkdir()
    descriptor = os.open(os.fsencode(invalid) + b'/invalid-\xff', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    rejected('N01-invalid-utf8', lambda: oracle.collect(str(invalid)))
    for field, value in (('max_manifest_bytes', 8), ('max_metadata_bytes', 64),
                         ('max_entries', 2), ('max_depth', 1), ('max_path_bytes', 8), ('max_runs', 1),
                         ('max_file_bytes', 1), ('max_unique_bytes', 1)):
        attempt = root / ('attempt-N12-' + field)
        rejected('N12-' + field, lambda field=field, value=value, attempt=attempt:
                 archive.verify_archive(str(package), pin, str(attempt), {**limits, field: value}),
                 attempt=attempt)
    # Independently vary source mode, inode and membership during a bounded read.
    for variant in ('mode', 'inode', 'membership'):
        mutable_source = root / ('source-drift-' + variant)
        shutil.copytree(source, mutable_source, copy_function=shutil.copy2)
        mutable_inventory = root / ('source-drift-' + variant + '.json')
        mutable_anchor = oracle.write_inventory(str(mutable_source), str(mutable_inventory))
        attempt = root / ('attempt-N10-' + variant)
        changed = [False]
        def source_change_stream(*args, variant=variant, mutable_source=mutable_source, **kwargs):
            if args[0] != str(mutable_source) or changed[0]:
                return original_stream(*args, **kwargs)
            def changing_read(fd, amount):
                value = real_read(fd, amount)
                if value and not changed[0]:
                    leaf = mutable_source / args[1]
                    if variant == 'mode':
                        leaf.chmod(0o444)
                    elif variant == 'inode':
                        kept = leaf.with_name(leaf.name + '.preserved')
                        leaf.rename(kept)
                        leaf.write_bytes(kept.read_bytes())
                    else:
                        (mutable_source / 'new-membership').write_bytes(b'changed during read')
                    changed[0] = True
                return value
            with replacement(os, 'read', changing_read):
                return original_stream(*args, **kwargs)
        with replacement(archive, 'stream', source_change_stream):
            rejected('N10-' + variant, lambda mutable_source=mutable_source, mutable_inventory=mutable_inventory,
                     mutable_anchor=mutable_anchor, attempt=attempt, variant=variant:
                     archive.create_archive(str(mutable_source), str(mutable_inventory),
                                            mutable_anchor['inventory_sha256'], str(root / ('archive-N10-' + variant)),
                                            str(attempt), limits=limits), attempt=attempt)
        check(changed[0], 'source drift variant did not trigger')
    leaf_source = root / 'symlink-leaf-source'
    leaf_source.mkdir()
    (leaf_source / 'link').symlink_to(source / 'root-receipt.json')
    rejected('N02-source-leaf', lambda: oracle.collect(str(leaf_source)), 'unsupported symlink or special file')
    bad_package('N08-root', lambda t: t.chmod(0o755), 'package root mode')
    bad_package('N08-dir', lambda t: (t / 'blobs').chmod(0o755), 'package entry type/mode')
    bad_package('N08-blob', lambda t: (t / 'blobs/sha256' / nonempty_digest).chmod(0o644),
                'package entry type/mode')
    # Explicit regression: readonly archive and readonly original root publish unchanged.
    readonly_source = root / 'readonly-source'
    shutil.copytree(source, readonly_source, copy_function=shutil.copy2)
    readonly_source.chmod(0o555)
    readonly_inventory = root / 'readonly-original.json'
    readonly_anchor = oracle.write_inventory(str(readonly_source), str(readonly_inventory))
    readonly_created = archive.create_archive(str(readonly_source), str(readonly_inventory),
                                              readonly_anchor['inventory_sha256'], str(root / 'readonly-package'),
                                              str(root / 'readonly-create-attempt'), limits=limits)
    check(stat.S_IMODE((root / 'readonly-package').stat().st_mode) == 0o555,
          'archive root changed from readonly during publication')
    archive.restore_archive(str(root / 'readonly-package'), readonly_created['root_sha256'],
                             str(root / 'readonly-restored'), str(root / 'readonly-restore-attempt'), limits)
    check(stat.S_IMODE((root / 'readonly-restored').stat().st_mode) == 0o555,
          'restored readonly root mode changed')
    for action in ('readonly-create-attempt', 'readonly-restore-attempt'):
        record = json.loads((root / action / 'RESULT.json').read_bytes())
        check(Path(record['context']['staging']).parent == Path(record['context']['destination']).parent,
              'publication staging crossed parents')
        check(not Path(record['context']['staging']).exists(), 'published sibling stage remains')
    results.append(dict(id='P07-readonly-publication', outcome='PASS'))
    # Truncation/extension are distinct from same-length corruption.
    for variant in ('truncated', 'extended'):
        def wrong_length(target, variant=variant):
            leaf = target / 'blobs/sha256' / nonempty_digest
            raw = leaf.read_bytes()
            put(leaf, raw[:-1] if variant == 'truncated' else raw + b'x')
        bad_package('N07-' + variant, wrong_length, 'payload hash/length mismatch')
    def extra_file(target):
        target.chmod(0o755)
        (target / 'extra.bin').write_bytes(b'undeclared')
        (target / 'extra.bin').chmod(0o444)
        target.chmod(0o555)
    bad_package('N06-extra', extra_file, 'package complete membership mismatch')
    def absent_manifest(target):
        folder = target / 'runs'
        folder.chmod(0o755)
        (folder / '0001.json').rename(folder / '0001.saved')
        folder.chmod(0o555)
    bad_package('N06-manifest', absent_manifest, 'package complete membership mismatch')
    def file_ancestor(target):
        inv = json.loads((target / 'ORIGINAL.json').read_bytes())
        row = next(r for r in inv['entries'] if r['path'] == 'run-pass-a')
        row.update(kind='file', size=0, sha256=hashlib.sha256(b'').hexdigest())
        return repin(target, 'ORIGINAL.json', inv)
    bad_package('N03-file-ancestor', file_ancestor, 'missing directory or file ancestor', True)
    bad_package('N11-unknown-root', lambda t: repin(t, root_mutation=lambda r: r.update(unknown=1)),
                'ROOT fields', True)
    def unknown_manifest(target):
        manifest = json.loads((target / 'runs/0000.json').read_bytes())
        manifest['unknown'] = 1
        return repin(target, 'runs/0000.json', manifest)
    bad_package('N11-unknown-manifest', unknown_manifest, 'run manifest fields', True)
    bad_package('N13-blob-sum', lambda t: repin(t, root_mutation=lambda r:
                r.update(unique_blob_bytes=r['unique_blob_bytes'] + 1)), 'blob total mismatch', True)
    bad_package('N13-source-sum', lambda t: repin(t, root_mutation=lambda r:
                r.update(source_files=r['source_files'] + 1)), 'source aggregate mismatch', True)
    def inventory_sum(target):
        inv = json.loads((target / 'ORIGINAL.json').read_bytes())
        inv['counts']['bytes'] += 1
        return repin(target, 'ORIGINAL.json', inv)
    bad_package('N13-inventory-sum', inventory_sum, 'inventory aggregate mismatch', True)
    for name, digest in (('missing', None), ('malformed', 'not-a-sha256')):
        attempt = root / ('attempt-N21-' + name)
        rejected('N21-' + name, lambda digest=digest, attempt=attempt:
                 archive.verify_archive(str(package), digest, str(attempt), limits),
                 'external expected ROOT hash required', attempt)
    # Fresh independent restoration must detect mode/path/alias drift, not just bytes.
    for variant in ('mode', 'path', 'alias'):
        attempt = root / ('attempt-N19-' + variant)
        count = [0]
        def drift_restored(*args, variant=variant, attempt=attempt, **kwargs):
            value = original_verify(*args, **kwargs)
            count[0] += 1
            if count[0] == 2:
                stage = stage_for(attempt)
                if variant == 'mode':
                    (stage / 'run-stop/receipt.json').chmod(0o600)
                elif variant == 'path':
                    (stage / 'run-stop/receipt.json').rename(stage / 'run-stop/receipt.moved')
                else:
                    leaf = stage / 'run-pass-a/payload-0.bin'
                    leaf.rename(stage / 'run-pass-a/payload-0.preserved')
                    os.link(stage / 'run-pass-a/boundary-0.bin', leaf)
            return value
        with replacement(archive, '_verify', drift_restored):
            rejected('N19-' + variant, lambda variant=variant, attempt=attempt:
                     archive.restore_archive(str(package), pin, str(root / ('drift-restored-' + variant)),
                                             str(attempt), limits),
                     'file hardlink alias' if variant == 'alias' else 'restored tree changed before commit', attempt)
    # Test destination privacy as an admission contract, without chmodding user parents.
    public_parent = root / 'public-parent'
    public_parent.mkdir(mode=0o755)
    public_parent.chmod(0o755)
    attempt = root / 'attempt-private-parent'
    rejected('N25-private-parent', lambda: archive.restore_archive(str(package), pin,
             str(public_parent / 'restored'), str(attempt), limits),
             'destination parent must be owned private mode 0700', attempt)
    destination_alias = root / 'destination-alias'
    destination_alias.symlink_to(root, target_is_directory=True)
    rejected('N02-destination-ancestor', lambda: archive.restore_archive(str(package), pin,
             str(destination_alias / 'restored'), str(root / 'attempt-destination-alias'), limits))
    # Copy faults occur during actual payload IO, after preflight and START writing.
    for fault in ('chmod', 'fsync', 'disk-full'):
        attempt = root / ('attempt-N17-' + fault)
        target_fd, fired, writes = [None], [False], [0]
        real_chmod, real_sync = os.fchmod, os.fsync
        def watched_stream(*args, **kwargs):
            fd = kwargs.get('target', args[6] if len(args) > 6 else None)
            if fd is not None and target_fd[0] is None:
                target_fd[0] = fd
            return original_stream(*args, **kwargs)
        def failed_chmod(fd, mode):
            if fd == target_fd[0] and not fired[0]:
                fired[0] = True
                raise OSError(errno.EIO, 'injected payload chmod failure')
            return real_chmod(fd, mode)
        def failed_sync(fd):
            if fd == target_fd[0] and not fired[0]:
                fired[0] = True
                raise OSError(errno.EIO, 'injected payload fsync failure')
            return real_sync(fd)
        def disk_full(fd, data):
            if fd == target_fd[0] and not fired[0]:
                writes[0] += 1
                if writes[0] == 1:
                    return real_write(fd, data[:7])
                fired[0] = True
                raise OSError(errno.ENOSPC, 'injected payload disk full')
            return real_write(fd, data)
        api, replacement_value = {'chmod': ('fchmod', failed_chmod), 'fsync': ('fsync', failed_sync),
                                  'disk-full': ('write', disk_full)}[fault]
        with replacement(archive, 'stream', watched_stream), replacement(os, api, replacement_value):
            rejected('N17-' + fault, lambda fault=fault, attempt=attempt:
                     archive.restore_archive(str(package), pin, str(root / ('fault-restored-' + fault)),
                                             str(attempt), limits), 'injected payload', attempt)
        check(fired[0] and stage_for(attempt).exists(), 'copy fault did not preserve sibling stage')
        if fault == 'disk-full':
            receipt = json.loads((attempt / 'RESULT.json').read_bytes())
            check(receipt['counters']['payload_write_bytes'] == 7, 'partial disk-full write count')
    attempt = root / 'attempt-publication-fsync'
    real_sync = os.fsync
    def publish_sync_fault(stage, destination):
        def reject_sync(fd):
            raise OSError(errno.EIO, 'injected publication fsync failure')
        with replacement(os, 'fsync', reject_sync):
            return original_publish(stage, destination)
    with replacement(archive, 'publish', publish_sync_fault):
        rejected('N22-publication-fsync', lambda: archive.restore_archive(str(package), pin,
                 str(root / 'published-but-unadmitted'), str(attempt), limits),
                 'injected publication fsync failure', attempt)
    check((root / 'published-but-unadmitted').exists(), 'post-rename fault state missing')
    # First error remains primary if final receipt writing also fails (N17-secondary above).
    # Allocation-only diagnosis must never erase a logical or identity custody check.
    original_encoding = oracle.canonical(original_inventory)
    allocation_only = copy.deepcopy(original_inventory)
    allocation_only['counts']['allocated_bytes'] += 4096
    changed_encoding = oracle.canonical(allocation_only)
    allocation_comparison = oracle.compare_custody(original_inventory, allocation_only)
    check(allocation_comparison['unchanged'] and allocation_comparison['allocated_bytes_delta'] == 4096 and
          allocation_comparison['excluded_field'] == 'counts.allocated_bytes', 'allocation-only custody comparison')
    check(oracle.canonical(original_inventory) == original_encoding and
          oracle.canonical(allocation_only) == changed_encoding, 'custody comparison mutated inputs')
    results.append(dict(id='P08-allocation-only', outcome='PASS', comparison=allocation_comparison))
    for variant in ('content', 'identity'):
        tiny = root / ('custody-real-' + variant)
        tiny.mkdir(mode=0o700)
        leaf = tiny / 'evidence.bin'
        leaf.write_bytes(b'aaaa')
        before_tiny = oracle.collect(str(tiny))
        if variant == 'content':
            leaf.write_bytes(b'bbbb')
        else:
            leaf.rename(root / 'custody-identity-original-preserved.bin')
            leaf.write_bytes(b'aaaa')
        after_tiny = oracle.collect(str(tiny))
        check((before_tiny['entries'][0]['sha256'] != after_tiny['entries'][0]['sha256']) if variant == 'content'
              else (before_tiny['entries'][0]['origin']['inode'] != after_tiny['entries'][0]['origin']['inode']),
              'real custody mutation fixture did not change intended field')
        (root / ('custody-real-' + variant + '-before.json')).write_bytes(oracle.canonical(before_tiny))
        (root / ('custody-real-' + variant + '-after.json')).write_bytes(oracle.canonical(after_tiny))
        rejected('N26-real-' + variant, lambda before_tiny=before_tiny, after_tiny=after_tiny:
                 check(oracle.compare_custody(before_tiny, after_tiny)['unchanged'], 'real custody mismatch'),
                 'real custody mismatch')
    for variant in ('hash', 'inode', 'root-origin', 'mode', 'logical-bytes', 'read-count'):
        changed = copy.deepcopy(original_inventory)
        leaf = next(row for row in changed['entries'] if row['kind'] == 'file')
        if variant == 'hash':
            leaf['sha256'] = '0' * 64
        elif variant == 'inode':
            leaf['origin']['inode'] += 1
        elif variant == 'root-origin':
            changed['root_origin']['ctime_ns'] += 1
        elif variant == 'mode':
            leaf['mode'] ^= 0o020
        elif variant == 'logical-bytes':
            changed['counts']['bytes'] += 1
        else:
            changed['counts']['read_bytes'] += 1
        rejected('N26-only-' + variant, lambda changed=changed:
                 check(oracle.compare_custody(original_inventory, changed)['unchanged'],
                       'isolated custody field mismatch'), 'isolated custody field mismatch')
    # Persist both full observations; only physical allocation is diagnostic.
    after = oracle.collect(str(source))
    (root / 'SOURCE-AFTER-INVENTORY.json').write_bytes(oracle.canonical(after))
    source_custody = oracle.compare_custody(original_inventory, after)
    (root / 'SOURCE-CUSTODY.json').write_bytes(oracle.canonical(source_custody))
    check(source_custody['unchanged'], 'original source custody changed during controls')
    all_bytes, all_files = 0, 0
    for directory, _, files in os.walk(root):
        for name in files:
            path = Path(directory) / name
            if path.is_symlink() or not stat.S_ISREG(path.lstat().st_mode):
                continue
            all_bytes += path.stat().st_size
            all_files += 1
    check(all_bytes <= 50331648, 'aggregate fixture storage bill exceeded')
    check(sum(r['outcome'] == 'EXPECTED_STOP' for r in results) <= 96, 'negative case count cap')
    coverage_raw = (here / 'COVERAGE-v5.json').read_bytes()
    check(len(coverage_raw) <= 65536 and hashlib.sha256(coverage_raw).hexdigest() == 'dfada24bd481a79048ac70eb0bcfcf4d7b43982051b24352401f2d80dd32369e',
          'source-bound concrete control coverage changed')
    coverage = json.loads(coverage_raw)
    actual_ids = [row['id'] for row in results]
    check(len(actual_ids) == len(set(actual_ids)) and sorted(actual_ids) == coverage['required_case_ids'],
          'concrete control case list incomplete or duplicated')
    check(sum(row['outcome'] == 'PASS' for row in results) == coverage['expected_positive_rows'] and
          sum(row['outcome'] == 'EXPECTED_STOP' for row in results) == coverage['expected_stop_rows'],
          'control outcome count mismatch')
    report = dict(status='PASS', cases=results, case_count=len(results),
                  retained_regular_file_bytes=all_bytes, retained_regular_file_count=all_files,
                  source_unchanged=True, source_custody=source_custody, no_scientific_imports=True,
                  case_prefix={'file': 'CASE-PREFIX.jsonl', 'rows': len(results),
                               'bytes': results.written_bytes, 'sha256': hashlib.sha256(results.path.read_bytes()).hexdigest(),
                               'max_rows': 128, 'max_line_bytes': 4096, 'max_bytes': 1048576,
                               'io_and_storage_included_in_parent_guard': True},
                  source_sha256={name: hashlib.sha256((here / name).read_bytes()).hexdigest()
                                 for name in ('archive.py', 'oracle.py', 'controls.py', 'USAGE.md', 'COVERAGE-v5.json')},
                  coverage_sha256=hashlib.sha256(coverage_raw).hexdigest(),
                  coverage_boundaries=coverage['declared_boundaries'],
                  pending_bill_cases=sorted(set(coverage['required_case_ids']) - set(actual_ids)))
    (root / 'CONTROL-RESULT.json').write_bytes(archive.canonical(report))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output')
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))
