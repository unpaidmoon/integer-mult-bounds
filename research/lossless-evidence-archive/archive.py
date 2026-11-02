"""Standalone immutable evidence archive; post-run only. Apache-2.0."""
import argparse
from contextlib import contextmanager
import ctypes
import hashlib
import types
import json
import os
from pathlib import Path
import resource
import stat
import time
import uuid

FORMAT = 'h25-evidence-cas-v1'
LIMITS = dict(chunk_bytes=1048576, max_entries=4096, max_depth=32,
              max_path_bytes=4096, max_file_bytes=536870912,
              max_total_bytes=2147483648, max_unique_bytes=2147483648,
              max_runs=128, max_manifest_bytes=1048576,
              max_root_bytes=4194304, max_metadata_bytes=8388608)
HEX = set('0123456789abcdef')


class Rejected(ValueError):
    pass


def need(value, reason):
    if not value:
        raise Rejected(reason)


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(',', ':')) + '\n').encode('ascii')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def is_hash(value):
    return type(value) is str and len(value) == 64 and set(value) <= HEX


def exact(obj, fields, name):
    need(type(obj) is dict and set(obj) == set(fields), name + ' fields')


def number(value, maximum, name):
    need(type(value) is int and 0 <= value <= maximum, name + ' bounds/type')


def caps(overrides=None):
    out = dict(LIMITS)
    if overrides:
        need(type(overrides) is dict and set(overrides) <= set(out), 'unknown limits')
        out.update(overrides)
    need(all(type(v) is int and v > 0 for v in out.values()), 'positive integer limits')
    need(out['chunk_bytes'] <= 1048576, 'stream buffer cap')
    return out


def normalized(path):
    value = os.fspath(path)
    need(type(value) is str and value.startswith('/') and
         os.path.normpath(value) == value and '\x00' not in value,
         'normalized absolute path required')
    return value


def relative(value, limits):
    need(type(value) is str and value and not value.startswith('/') and
         '\\' not in value and '\x00' not in value and ':' not in value,
         'unsafe relative path')
    parts = value.split('/')
    need(all(part not in ('', '.', '..') for part in parts), 'noncanonical path')
    need(len(parts) <= limits['max_depth'] and
         len(value.encode('utf-8', 'strict')) <= limits['max_path_bytes'], 'path bounds')
    return parts


def signature(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_uid,
            info.st_gid, info.st_mtime_ns, info.st_ctime_ns, info.st_nlink)


def origin(info):
    return dict(device=info.st_dev, inode=info.st_ino, uid=info.st_uid, gid=info.st_gid,
                mtime_ns=info.st_mtime_ns, ctime_ns=info.st_ctime_ns, nlink=info.st_nlink)


def dirfd(path):
    path = normalized(path)
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.split('/')[1:]:
            if part:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


@contextmanager
def opened(root, name, flags=os.O_RDONLY):
    """Descriptor anchored traversal; intermediate and leaf links prohibited."""
    fd = dirfd(root)
    try:
        parts = name.split('/')
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        leaf = os.open(parts[-1], flags | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        try:
            yield leaf
        finally:
            os.close(leaf)
    finally:
        os.close(fd)


def absent(path):
    parent = dirfd(os.path.dirname(path))
    try:
        try:
            os.stat(os.path.basename(path), dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise Rejected('destination exists')
    finally:
        os.close(parent)


def disjoint(*paths):
    def ancestry(path):
        descriptor = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        info = os.fstat(descriptor)
        chain = {(info.st_dev, info.st_ino)}
        endpoint = (info.st_dev, info.st_ino)
        try:
            for part in path.split('/')[1:]:
                if not part:
                    continue
                try:
                    child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=descriptor)
                except FileNotFoundError:
                    return chain, None
                os.close(descriptor)
                descriptor = child
                info = os.fstat(descriptor)
                endpoint = (info.st_dev, info.st_ino)
                chain.add(endpoint)
            return chain, endpoint
        finally:
            os.close(descriptor)
    identities = [ancestry(path) for path in paths]
    for i, first in enumerate(paths):
        for j, second in enumerate(paths[i + 1:], i + 1):
            need(os.path.commonpath((first, second)) not in (first, second),
                 'overlapping source/package/output/attempt paths')
            first_chain, first_end = identities[i]
            second_chain, second_end = identities[j]
            need(not (first_end in second_chain or second_end in first_chain),
                 'filesystem alias overlaps source/package/output/attempt')


def sibling_stage(destination):
    return os.path.dirname(destination) + '/.h25-retention-' + uuid.uuid4().hex + '.stage'


def private_destination_parent(destination):
    fd = dirfd(os.path.dirname(destination))
    try:
        info = os.fstat(fd)
        need(info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o700,
             'destination parent must be owned private mode 0700')
        need(not os.listxattr(fd), 'destination parent xattrs/ACLs unsupported')
    finally:
        os.close(fd)


def new_dir(path):
    parent = dirfd(os.path.dirname(path))
    try:
        os.mkdir(os.path.basename(path), 0o700, dir_fd=parent)
        os.fsync(parent)
    finally:
        os.close(parent)


def write_new(path, raw, mode=0o600, counters=None):
    parent = dirfd(os.path.dirname(path))
    try:
        fd = os.open(os.path.basename(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     mode, dir_fd=parent)
        try:
            view = memoryview(raw)
            while view:
                count = os.write(fd, view)
                need(count > 0, 'zero-length write')
                if counters is not None:
                    counters['metadata_write_bytes'] += count
                view = view[count:]
            os.fchmod(fd, mode)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.fsync(parent)
    finally:
        os.close(parent)


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    obj = json.loads(raw, object_pairs_hook=pairs,
                     parse_constant=lambda value: (_ for _ in ()).throw(Rejected('nonfinite JSON')))
    need(canonical(obj) == raw, 'noncanonical JSON bytes')
    return obj


def read_small(root, name, limit, counters=None):
    with opened(root, name) as fd:
        info = os.fstat(fd)
        need(stat.S_ISREG(info.st_mode) and info.st_size <= limit, 'metadata size/type cap')
        raw = bytearray()
        while len(raw) <= limit:
            block = os.read(fd, min(65536, limit + 1 - len(raw)))
            if not block:
                break
            raw.extend(block)
            if counters is not None:
                counters['metadata_read_bytes'] += len(block)
        need(len(raw) == info.st_size and len(raw) <= limit, 'metadata length drift/cap')
        need(signature(info) == signature(os.fstat(fd)), 'metadata changed during read')
        return bytes(raw)


def stream(root, name, limits, counters, category, expected=None, target=None):
    with opened(root, name) as fd:
        info = os.fstat(fd)
        need(stat.S_ISREG(info.st_mode) and info.st_size <= limits['max_file_bytes'], 'file type/size')
        need(not os.listxattr(fd), 'unsupported xattrs/ACLs')
        h, size = hashlib.sha256(), 0
        while True:
            block = os.read(fd, limits['chunk_bytes'])
            if not block:
                break
            size += len(block)
            counters[category] += len(block)
            need(size <= info.st_size, 'file grew during read')
            h.update(block)
            if target is not None:
                view = memoryview(block)
                while view:
                    count = os.write(target, view)
                    need(count > 0, 'zero-length stream write')
                    counters['payload_write_bytes'] += count
                    view = view[count:]
        need(size == info.st_size and signature(info) == signature(os.fstat(fd)),
             'file changed during stream')
        result = dict(size=size, sha256=h.hexdigest())
        if expected:
            need(result == {k: expected[k] for k in ('size', 'sha256')}, 'payload hash/length mismatch')
        return result


def scan(root, limits, single_links=False):
    """Metadata-only bounded tree census, independent of the oracle code."""
    found, identities = {}, set()
    fd = dirfd(root)
    try:
        root_info = os.fstat(fd)
        need(not os.listxattr(fd), 'unsupported root xattrs/ACLs')
        need(stat.S_IMODE(root_info.st_mode) <= 0o777, 'unsupported root permission bits')
        need(stat.S_IMODE(root_info.st_mode) & 0o500 == 0o500, 'unsupported root owner access mode')
        def descend(parent, prefix, depth):
            need(depth <= limits['max_depth'], 'tree depth cap')
            before = os.fstat(parent)
            names = []
            with os.scandir(parent) as items:
                for item in items:
                    names.append(item.name)
                    need(len(names) <= limits['max_entries'], 'directory entry cap')
            for name in sorted(names):
                path = name if not prefix else prefix + '/' + name
                relative(path, limits)
                info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                need(stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), 'symlink/special file')
                mode = stat.S_IMODE(info.st_mode)
                need(mode <= 0o777, 'unsupported special mode')
                owner_access = 0o500 if stat.S_ISDIR(info.st_mode) else 0o400
                need(mode & owner_access == owner_access, 'unsupported owner access mode')
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if stat.S_ISDIR(info.st_mode):
                    flags |= os.O_DIRECTORY
                child = os.open(name, flags, dir_fd=parent)
                try:
                    need(signature(info) == signature(os.fstat(child)), 'entry changed during census')
                    need(not os.listxattr(child), 'unsupported xattrs/ACLs')
                    need(len(found) < limits['max_entries'], 'total entry cap')
                    row = dict(path=path, kind='dir' if stat.S_ISDIR(info.st_mode) else 'file',
                               mode=mode, origin=origin(info))
                    if row['kind'] == 'file':
                        number(info.st_size, limits['max_file_bytes'], 'file size')
                        row['size'] = info.st_size
                        row['allocated'] = info.st_blocks * 512
                        if single_links:
                            identity = (info.st_dev, info.st_ino)
                            need(info.st_nlink == 1 and identity not in identities, 'file hardlink alias')
                            identities.add(identity)
                    found[path] = row
                    if row['kind'] == 'dir':
                        descend(child, path, depth + 1)
                    need(signature(info) == signature(os.fstat(child)), 'entry changed during census')
                finally:
                    os.close(child)
            need(signature(before) == signature(os.fstat(parent)), 'directory changed during census')
        descend(fd, '', 0)
        return dict(root_mode=stat.S_IMODE(root_info.st_mode), root_origin=origin(root_info), entries=found)
    finally:
        os.close(fd)


def validate_inventory(value, limits):
    exact(value, ('schema', 'source_root', 'root_mode', 'root_origin', 'entries', 'counts'), 'inventory')
    need(value['schema'] == 'h25-tree-inventory-v1', 'inventory schema')
    normalized(value['source_root'])
    number(value['root_mode'], 0o777, 'root mode')
    need(value['root_mode'] & 0o500 == 0o500, 'unsupported root owner access mode')
    need(type(value['entries']) is list and len(value['entries']) <= limits['max_entries'], 'entry count')
    modes, total, files, dirs, previous = {}, 0, 0, 1, None
    for row in value['entries']:
        need(type(row) is dict and row.get('kind') in ('dir', 'file'), 'entry kind')
        fields = ('path', 'kind', 'mode', 'origin')
        if row['kind'] == 'file':
            fields += ('size', 'sha256')
        exact(row, fields, 'entry')
        parts = relative(row['path'], limits)
        need(previous is None or previous < row['path'], 'duplicate/unsorted paths')
        previous = row['path']
        number(row['mode'], 0o777, 'entry mode')
        owner_access = 0o500 if row['kind'] == 'dir' else 0o400
        need(row['mode'] & owner_access == owner_access, 'unsupported owner access mode')
        exact(row['origin'], ('device', 'inode', 'uid', 'gid', 'mtime_ns', 'ctime_ns', 'nlink'), 'origin')
        need(all(type(v) is int for v in row['origin'].values()), 'origin integers')
        if len(parts) > 1:
            need(modes.get('/'.join(parts[:-1])) == 'dir', 'missing directory or file ancestor')
        modes[row['path']] = row['kind']
        if row['kind'] == 'file':
            number(row['size'], limits['max_file_bytes'], 'file bytes')
            need(is_hash(row['sha256']), 'file digest')
            total += row['size']
            need(total <= limits['max_total_bytes'], 'total restored size cap')
            files += 1
        else:
            dirs += 1
    exact(value['root_origin'], ('device', 'inode', 'uid', 'gid', 'mtime_ns', 'ctime_ns', 'nlink'), 'root origin')
    need(all(type(v) is int for v in value['root_origin'].values()), 'root origin integers')
    exact(value['counts'], ('files', 'directories', 'bytes', 'read_bytes', 'allocated_bytes'), 'inventory counts')
    need(all(type(v) is int and v >= 0 for v in value['counts'].values()), 'count types')
    need(value['counts']['files'] == files and value['counts']['directories'] == dirs and
         value['counts']['bytes'] == total and value['counts']['read_bytes'] == total,
         'inventory aggregate mismatch')
    return value


def inventory_file(path, expected, limits, counters):
    path = normalized(path)
    need(is_hash(expected), 'expected inventory hash required')
    raw = read_small(os.path.dirname(path), os.path.basename(path), limits['max_metadata_bytes'], counters)
    need(sha(raw) == expected, 'independent inventory digest mismatch')
    return validate_inventory(parse(raw), limits), raw


def same_source(census, inventory):
    need(census['root_mode'] == inventory['root_mode'] and
         census['root_origin'] == inventory['root_origin'], 'source root changed')
    expected = {r['path']: {k: v for k, v in r.items() if k != 'sha256'} for r in inventory['entries']}
    actual = {p: {k: v for k, v in r.items() if k != 'allocated'}
              for p, r in census['entries'].items()}
    need(actual == expected, 'source complete census/metadata changed')


def publish(source, target):
    """Publish readonly roots within one parent using no-replace rename only."""
    old = dirfd(os.path.dirname(source))
    new = dirfd(os.path.dirname(target))
    try:
        old_info, new_info = os.fstat(old), os.fstat(new)
        need((old_info.st_dev, old_info.st_ino) == (new_info.st_dev, new_info.st_ino),
             'publication must stay within one parent')
        library = ctypes.CDLL(None, use_errno=True)
        function = getattr(library, 'renameat2', None)
        need(function is not None, 'renameat2 unavailable')
        function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        function.restype = ctypes.c_int
        result = function(old, os.fsencode(os.path.basename(source)), new,
                          os.fsencode(os.path.basename(target)), 1)
        if result != 0:
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error), target)
        os.fsync(old)
        os.fsync(new)
    finally:
        os.close(old)
        os.close(new)


def freeze_tree(root):
    # Private stage has no untrusted descendants; still use no-follow descriptors.
    fd = dirfd(root)
    try:
        def visit(parent):
            with os.scandir(parent) as items:
                names = [item.name for item in items]
            for name in names:
                info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if stat.S_ISDIR(info.st_mode):
                    flags |= os.O_DIRECTORY
                child = os.open(name, flags, dir_fd=parent)
                try:
                    if stat.S_ISDIR(info.st_mode):
                        visit(child)
                        os.fchmod(child, 0o555)
                    else:
                        need(stat.S_ISREG(info.st_mode), 'unexpected stage object')
                        os.fchmod(child, 0o444)
                    os.fsync(child)
                finally:
                    os.close(child)
            os.fsync(parent)
        visit(fd)
        os.fchmod(fd, 0o555)
        os.fsync(fd)
    finally:
        os.close(fd)


@contextmanager
def operation(kind, attempt, **context):
    attempt = normalized(attempt)
    new_dir(attempt)
    counters = dict(metadata_read_bytes=0, source_read_bytes=0, blob_read_bytes=0,
                    payload_write_bytes=0, metadata_write_bytes=0, independent_oracle_read_bytes=0)
    before = resource.getrusage(resource.RUSAGE_SELF)
    start = time.monotonic()
    result = {'operation': kind, 'status': 'INCOMPLETE', 'context': context, 'counters': counters,
              'accounting_exclusions': ['RESULT.json bytes and its final write/fsync/resource time are excluded from this self-metering receipt; parent wall/footprint includes them.']}
    primary = None
    try:
        write_new(attempt + '/START.json', canonical(dict(operation=kind, context=context)), counters=counters)
        yield result
        result['status'] = 'PASS'
    except BaseException as error:
        primary = error
        result.update(status='STOP', error_type=type(error).__name__, reason=str(error)[:2048])
        raise
    finally:
        after = resource.getrusage(resource.RUSAGE_SELF)
        result.update(wall_seconds=time.monotonic() - start,
                      cpu_seconds=after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                      process_peak_rss_bytes=after.ru_maxrss * 1024)
        try:
            write_new(attempt + '/RESULT.json', canonical(result))
        except BaseException as receipt_error:
            if primary is None:
                raise
            if hasattr(primary, 'add_note'):
                primary.add_note('Secondary RESULT receipt write failed; attempt remains incomplete: ' +
                                 type(receipt_error).__name__ + ': ' + str(receipt_error)[:1024])
            # Preserve the active original exception; parent captures its failure and the unclosed attempt.


def package_metadata(stage, name, raw, descriptors, counters, limits):
    need(len(raw) <= limits['max_manifest_bytes'], 'individual manifest/tool byte cap')
    descriptors[name] = dict(size=len(raw), sha256=sha(raw), mode=0o444)
    need(sum(row['size'] for row in descriptors.values()) <= limits['max_metadata_bytes'],
         'aggregate metadata cap')
    write_new(stage + '/' + name, raw, counters=counters)


def _verify(archive, expected_root, limits, counters):
    need(is_hash(expected_root), 'external expected ROOT hash required')
    raw = read_small(archive, 'ROOT.json', limits['max_root_bytes'], counters)
    need(sha(raw) == expected_root, 'ROOT authentication mismatch')
    root = parse(raw)
    exact(root, ('schema', 'metadata', 'blobs', 'inventory_sha256', 'source_files',
                 'source_directories', 'source_bytes', 'unique_blob_bytes', 'provenance'), 'ROOT')
    need(root['schema'] == FORMAT and is_hash(root['inventory_sha256']), 'ROOT format/inventory hash')
    need(type(root['metadata']) is dict and type(root['blobs']) is dict, 'ROOT tables')
    need(len(root['metadata']) <= limits['max_entries'] and len(root['blobs']) <= limits['max_entries'],
         'ROOT table count cap')
    total_meta = len(raw)
    for name, record in root['metadata'].items():
        relative(name, limits)
        need(name == 'ORIGINAL.json' or name in ('tools/archive.py', 'tools/oracle.py', 'tools/USAGE.md')
             or (name.startswith('runs/') and name.endswith('.json') and len(name.split('/')) == 2),
             'unknown metadata path')
        exact(record, ('size', 'sha256', 'mode'), 'metadata record')
        number(record['size'], limits['max_manifest_bytes'], 'manifest bytes')
        need(is_hash(record['sha256']) and record['mode'] == 0o444, 'metadata digest/mode')
        total_meta += record['size']
    need(total_meta <= limits['max_metadata_bytes'], 'aggregate metadata byte cap')
    required = {'ORIGINAL.json', 'tools/archive.py', 'tools/oracle.py', 'tools/USAGE.md', 'runs/0000.json'}
    need(required <= set(root['metadata']), 'missing required package metadata')
    run_names = sorted(n for n in root['metadata'] if n.startswith('runs/'))
    need(len(run_names) <= limits['max_runs'] + 1 and run_names ==
         ['runs/%04d.json' % n for n in range(len(run_names))], 'run manifest sequence/count')
    blob_total = 0
    for digest, size in root['blobs'].items():
        need(is_hash(digest), 'blob hash name')
        number(size, limits['max_file_bytes'], 'blob size')
        blob_total += size
        need(blob_total <= limits['max_unique_bytes'], 'unique payload byte cap')
    for key, maximum in (('source_files', limits['max_entries']),
                         ('source_directories', limits['max_entries'] + 1),
                         ('source_bytes', limits['max_total_bytes']),
                         ('unique_blob_bytes', limits['max_unique_bytes'])):
        number(root[key], maximum, key)
    need(blob_total == root['unique_blob_bytes'], 'blob total mismatch')
    need(type(root['provenance']) is dict, 'provenance shape')
    complete_raw = read_small(archive, 'COMPLETE.json', 1024, counters)
    complete = parse(complete_raw)
    exact(complete, ('schema', 'root_sha256'), 'completion')
    need(complete == dict(schema=FORMAT, root_sha256=expected_root), 'incomplete package')
    census = scan(archive, {**limits, 'max_entries': limits['max_entries'] * 3 + 32}, True)
    need(census['root_mode'] == 0o555, 'package root mode')
    wanted_dirs = {'blobs', 'blobs/sha256', 'runs', 'tools'}
    wanted_files = set(root['metadata']) | {'ROOT.json', 'COMPLETE.json'} | {
        'blobs/sha256/' + digest for digest in root['blobs']}
    need(set(census['entries']) == wanted_dirs | wanted_files, 'package complete membership mismatch')
    for name, row in census['entries'].items():
        need(row['kind'] == ('dir' if name in wanted_dirs else 'file') and
             row['mode'] == (0o555 if name in wanted_dirs else 0o444), 'package entry type/mode')
    metadata = {}
    for name, expected in root['metadata'].items():
        value = read_small(archive, name, limits['max_manifest_bytes'], counters)
        need(len(value) == expected['size'] and sha(value) == expected['sha256'], 'metadata digest mismatch')
        metadata[name] = value
    local_tools = os.path.dirname(os.path.abspath(__file__))
    for tool in ('archive.py', 'oracle.py'):
        local_raw = read_small(local_tools, tool, limits['max_manifest_bytes'], counters)
        need(sha(local_raw) == root['metadata']['tools/' + tool]['sha256'], 'local tool source mismatch')
    need(sha(metadata['ORIGINAL.json']) == root['inventory_sha256'], 'original inventory binding')
    inventory = validate_inventory(parse(metadata['ORIGINAL.json']), limits)
    merged, run_ids = [], []
    for name in run_names:
        manifest = parse(metadata[name])
        exact(manifest, ('schema', 'run', 'entries'), 'run manifest')
        need(manifest['schema'] == FORMAT and type(manifest['entries']) is list, 'run manifest shape')
        run = manifest['run']
        if name == 'runs/0000.json':
            need(run is None, 'root manifest identity')
        else:
            need(type(run) is str and len(relative(run, limits)) == 1 and run not in run_ids,
                 'run identity')
            run_ids.append(run)
        for row in manifest['entries']:
            need(type(row) is dict and type(row.get('path')) is str, 'run entry shape')
            if run is None:
                need('/' not in row['path'] and row.get('kind') == 'file', 'root manifest entry ownership')
            else:
                need(row['path'] == run or row['path'].startswith(run + '/'), 'run manifest ownership')
        merged.extend(manifest['entries'])
        need(len(merged) <= limits['max_entries'], 'merged manifest count cap')
    need(sorted(merged, key=lambda r: r['path']) == inventory['entries'], 'incomplete/duplicate run union')
    need(set(run_ids) == {r['path'] for r in inventory['entries']
                          if r['kind'] == 'dir' and '/' not in r['path']}, 'run root partition')
    expected_blobs = {}
    for row in inventory['entries']:
        if row['kind'] == 'file':
            if row['sha256'] in expected_blobs:
                need(expected_blobs[row['sha256']] == row['size'], 'digest/size collision')
            expected_blobs[row['sha256']] = row['size']
    need(root['blobs'] == expected_blobs, 'exact blob closure mismatch')
    need((root['source_files'], root['source_directories'], root['source_bytes']) ==
         tuple(inventory['counts'][k] for k in ('files', 'directories', 'bytes')), 'source aggregate mismatch')
    for digest, size in root['blobs'].items():
        stream(archive, 'blobs/sha256/' + digest, limits, counters, 'blob_read_bytes',
               dict(size=size, sha256=digest))
    # Fresh census rejects mode/membership/inode mutation after byte verification.
    need(scan(archive, {**limits, 'max_entries': limits['max_entries'] * 3 + 32}, True) == census,
         'package changed during verification')
    archive_bytes = sum(r['size'] for r in census['entries'].values() if r['kind'] == 'file')
    allocated = sum(r['allocated'] for r in census['entries'].values() if r['kind'] == 'file')
    return root, inventory, dict(archive_logical_bytes=archive_bytes, archive_allocated_bytes=allocated,
                                source_logical_bytes=root['source_bytes'], unique_blob_bytes=blob_total,
                                derived_bytes_avoided=root['source_bytes'] - archive_bytes)


def create_archive(source_root, original_inventory, expected_inventory_sha256,
                   destination, attempt_dir, provenance=None, limits=None):
    limits = caps(limits)
    source_root, destination, attempt_dir = map(normalized, (source_root, destination, attempt_dir))
    stage = sibling_stage(destination)
    disjoint(source_root, destination, attempt_dir, stage)
    with operation('create', attempt_dir, source=source_root, destination=destination, staging=stage,
                   expected_inventory_sha256=expected_inventory_sha256) as result:
        counts = result['counters']
        private_destination_parent(destination)
        absent(destination)
        inventory, original_raw = inventory_file(original_inventory, expected_inventory_sha256, limits, counts)
        need(inventory['source_root'] == source_root, 'inventory source root mismatch')
        same_source(scan(source_root, limits), inventory)
        new_dir(stage)
        for name in ('blobs', 'blobs/sha256', 'runs', 'tools'):
            new_dir(stage + '/' + name)
        descriptors, blobs = {}, {}
        package_metadata(stage, 'ORIGINAL.json', original_raw, descriptors, counts, limits)
        run_ids = sorted(r['path'] for r in inventory['entries'] if r['kind'] == 'dir' and '/' not in r['path'])
        need(len(run_ids) <= limits['max_runs'], 'run count cap')
        for index, run in enumerate([None] + run_ids):
            rows = [r for r in inventory['entries'] if
                    (r['kind'] == 'file' and '/' not in r['path'] if run is None else
                     r['path'] == run or r['path'].startswith(run + '/'))]
            package_metadata(stage, 'runs/%04d.json' % index,
                             canonical(dict(schema=FORMAT, run=run, entries=rows)), descriptors, counts, limits)
        tool_dir = os.path.dirname(os.path.abspath(__file__))
        for name in ('archive.py', 'oracle.py', 'USAGE.md'):
            raw = read_small(tool_dir, name, limits['max_manifest_bytes'], counts)
            package_metadata(stage, 'tools/' + name, raw, descriptors, counts, limits)
        for row in inventory['entries']:
            if row['kind'] != 'file':
                continue
            digest = row['sha256']
            if digest in blobs:
                need(blobs[digest] == row['size'], 'digest size collision')
                with opened(stage, 'blobs/sha256/' + digest) as fd:
                    need(stat.S_IMODE(os.fstat(fd).st_mode) == 0o444 and os.fstat(fd).st_nlink == 1,
                         'reused blob mode/alias')
                stream(stage, 'blobs/sha256/' + digest, limits, counts, 'blob_read_bytes', row)
                stream(source_root, row['path'], limits, counts, 'source_read_bytes', row)
            else:
                need(sum(blobs.values()) + row['size'] <= limits['max_unique_bytes'], 'unique byte cap')
                path = stage + '/blobs/sha256/' + digest
                parent = dirfd(os.path.dirname(path))
                try:
                    fd = os.open(digest, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=parent)
                    try:
                        stream(source_root, row['path'], limits, counts, 'source_read_bytes', row, fd)
                        os.fchmod(fd, 0o444)
                        os.fsync(fd)
                    finally:
                        os.close(fd)
                    os.fsync(parent)
                finally:
                    os.close(parent)
                blobs[digest] = row['size']
        same_source(scan(source_root, limits), inventory)
        root = dict(schema=FORMAT, metadata=descriptors, blobs=blobs,
                    inventory_sha256=expected_inventory_sha256,
                    source_files=inventory['counts']['files'], source_directories=inventory['counts']['directories'],
                    source_bytes=inventory['counts']['bytes'], unique_blob_bytes=sum(blobs.values()),
                    provenance=provenance or {})
        raw = canonical(root)
        need(len(raw) <= limits['max_root_bytes'] and len(raw) + sum(r['size'] for r in descriptors.values())
             <= limits['max_metadata_bytes'], 'ROOT/metadata byte cap')
        expected_root = sha(raw)
        write_new(stage + '/ROOT.json', raw, counters=counts)
        complete = canonical(dict(schema=FORMAT, root_sha256=expected_root))
        write_new(stage + '/COMPLETE.json', complete, counters=counts)
        freeze_tree(stage)
        _, _, accounting = _verify(stage, expected_root, limits, counts)
        same_source(scan(source_root, limits), inventory)
        publish(stage, destination)
        result.update(root_sha256=expected_root, inventory_sha256=expected_inventory_sha256,
                      accounting=accounting, raw_bytes_removed=0, destination=destination)
    return result


def verify_archive(archive, expected_root_sha256, attempt_dir, limits=None):
    archive, attempt_dir = map(normalized, (archive, attempt_dir))
    disjoint(archive, attempt_dir)
    with operation('verify', attempt_dir, archive=archive, expected_root_sha256=expected_root_sha256) as result:
        _, _, accounting = _verify(archive, expected_root_sha256, caps(limits), result['counters'])
        result.update(root_sha256=expected_root_sha256, accounting=accounting)
    return result


def load_oracle(expected_sha256, counters):
    directory = os.path.dirname(os.path.abspath(__file__))
    raw = read_small(directory, 'oracle.py', 1048576, counters)
    need(sha(raw) == expected_sha256, 'independent oracle source changed')
    module = types.ModuleType('_h25_retention_independent_oracle')
    module.__file__ = directory + '/oracle.py'
    exec(compile(raw, module.__file__, 'exec'), module.__dict__)
    return module


def restore_archive(archive, expected_root_sha256, destination, attempt_dir, limits=None):
    limits = caps(limits)
    archive, destination, attempt_dir = map(normalized, (archive, destination, attempt_dir))
    stage = sibling_stage(destination)
    disjoint(archive, destination, attempt_dir, stage)
    with operation('restore', attempt_dir, archive=archive, destination=destination, staging=stage,
                   expected_root_sha256=expected_root_sha256) as result:
        counters = result['counters']
        private_destination_parent(destination)
        absent(destination)
        root, inventory, accounting = _verify(archive, expected_root_sha256, limits, counters)
        # Historical source_root is provenance, never a live-location dependency.
        historical = inventory['source_root']
        for live in (archive, destination, attempt_dir):
            need(os.path.commonpath((historical, live)) not in (historical, live),
                 'historical source path overlaps restoration operation')
        new_dir(stage)
        for row in inventory['entries']:
            path = stage + '/' + row['path']
            if row['kind'] == 'dir':
                new_dir(path)
            else:
                parent = dirfd(os.path.dirname(path))
                try:
                    fd = os.open(os.path.basename(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=parent)
                    try:
                        stream(archive, 'blobs/sha256/' + row['sha256'], limits, counters,
                               'blob_read_bytes', row, fd)
                        os.fchmod(fd, row['mode'])
                        os.fsync(fd)
                    finally:
                        os.close(fd)
                    os.fsync(parent)
                finally:
                    os.close(parent)
        for row in sorted(inventory['entries'], key=lambda r: r['path'].count('/'), reverse=True):
            if row['kind'] == 'dir':
                fd = dirfd(stage + '/' + row['path'])
                try:
                    os.fchmod(fd, row['mode'])
                    os.fsync(fd)
                finally:
                    os.close(fd)
        fd = dirfd(stage)
        try:
            os.fchmod(fd, inventory['root_mode'])
            os.fsync(fd)
        finally:
            os.close(fd)
        oracle = load_oracle(root['metadata']['tools/oracle.py']['sha256'], counters)
        oracle_limits = {k: limits[k] for k in ('chunk_bytes', 'max_entries', 'max_depth',
                                               'max_path_bytes', 'max_file_bytes', 'max_total_bytes')}
        oracle_limits['max_inventory_bytes'] = limits['max_metadata_bytes']
        restored = oracle.collect(stage, oracle_limits, require_single_links=True, io_counters=counters)
        need(oracle.content_projection(restored) == oracle.content_projection(inventory),
             'independent restoration oracle mismatch')
        proof_raw = oracle.canonical(restored)
        write_new(attempt_dir + '/RESTORED-INVENTORY.json', proof_raw, counters=counters)
        proof_digest = sha(proof_raw)
        before_commit = scan(stage, limits, True)
        # Bind the oracle to the live staged inodes and all metadata, not a saved PASS.
        same_source(before_commit, restored)
        _verify(archive, expected_root_sha256, limits, counters)
        need(scan(stage, limits, True) == before_commit, 'restored tree changed before commit')
        publish(stage, destination)
        result.update(root_sha256=expected_root_sha256, inventory_sha256=root['inventory_sha256'],
                      restored_inventory_sha256=proof_digest, accounting=accounting,
                      restored_logical_bytes=restored['counts']['bytes'],
                      restored_allocated_bytes=restored['counts']['allocated_bytes'],
                      independent_oracle_read_bytes=restored['counts']['read_bytes'],
                      destination=destination, exact_restoration=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('create', 'verify', 'restore'))
    parser.add_argument('--source')
    parser.add_argument('--inventory')
    parser.add_argument('--inventory-sha256')
    parser.add_argument('--archive')
    parser.add_argument('--root-sha256')
    parser.add_argument('--destination')
    parser.add_argument('--attempt', required=True)
    args = parser.parse_args()
    if args.operation == 'create':
        result = create_archive(args.source, args.inventory, args.inventory_sha256,
                                args.destination, args.attempt)
    elif args.operation == 'verify':
        result = verify_archive(args.archive, args.root_sha256, args.attempt)
    else:
        result = restore_archive(args.archive, args.root_sha256, args.destination, args.attempt)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
