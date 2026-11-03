"""Independent bounded tree oracle; no archive implementation imports. Apache-2.0."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

SCHEMA = 'h25-tree-inventory-v1'
DEFAULTS = dict(chunk_bytes=1048576, max_entries=4096, max_depth=32,
                max_path_bytes=4096, max_file_bytes=536870912,
                max_total_bytes=2147483648, max_inventory_bytes=8388608)


def demand(value, reason):
    if not value:
        raise ValueError(reason)


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(',', ':')) + '\n').encode('ascii')


def absolute(path):
    value = os.fspath(path)
    demand(isinstance(value, str) and value.startswith('/') and
           os.path.normpath(value) == value and '\x00' not in value,
           'oracle requires normalized absolute path')
    return value


def directory(path):
    """Open every ancestor without following symlinks."""
    path = absolute(path)
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.split('/')[1:]:
            if part:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=fd)
                os.close(fd)
                fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def signature(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
            info.st_nlink)


def metadata(info):
    return {'device': info.st_dev, 'inode': info.st_ino, 'uid': info.st_uid,
            'gid': info.st_gid, 'mtime_ns': info.st_mtime_ns,
            'ctime_ns': info.st_ctime_ns, 'nlink': info.st_nlink}


def content_projection(inventory):
    return {'root_mode': inventory['root_mode'],
            'entries': [{k: v for k, v in row.items() if k != 'origin'}
                        for row in inventory['entries']]}


def compare_custody(before_inventory, after_inventory):
    """Exact oracle-inventory equality except physical block-allocation diagnosis."""
    fields = {'schema', 'source_root', 'root_mode', 'root_origin', 'entries', 'counts'}
    count_fields = {'files', 'directories', 'bytes', 'read_bytes', 'allocated_bytes'}
    projections, allocations = [], []
    for inventory in (before_inventory, after_inventory):
        demand(type(inventory) is dict and set(inventory) == fields and
               inventory['schema'] == SCHEMA, 'custody inventory shape/schema')
        counts = inventory['counts']
        demand(type(counts) is dict and set(counts) == count_fields and
               all(type(value) is int and value >= 0 for value in counts.values()),
               'custody count shape/type')
        allocations.append(counts['allocated_bytes'])
        # Copy only the two dictionaries being projected; never mutate either input.
        projected = dict(inventory)
        projected['counts'] = {key: value for key, value in counts.items()
                               if key != 'allocated_bytes'}
        projections.append(projected)
    return {'unchanged': projections[0] == projections[1],
            'allocated_bytes_before': allocations[0], 'allocated_bytes_after': allocations[1],
            'allocated_bytes_delta': allocations[1] - allocations[0],
            'excluded_field': 'counts.allocated_bytes'}


def collect(source, limits=None, require_single_links=False, io_counters=None):
    """All hashing is fresh; holds bounded metadata and one chunk at a time."""
    caps = dict(DEFAULTS)
    if limits:
        demand(set(limits) <= set(caps), 'unknown oracle limit')
        caps.update(limits)
    demand(all(type(v) is int and v > 0 for v in caps.values()), 'oracle limits')
    source = absolute(source)
    entries, snapshots, identities = [], {}, set()
    counts = {'files': 0, 'directories': 1, 'bytes': 0,
              'read_bytes': 0, 'allocated_bytes': 0}
    root = directory(source)
    try:
        root_stat = os.fstat(root)
        demand(not (stat.S_IMODE(root_stat.st_mode) & ~0o777), 'unsupported root mode')
        demand(stat.S_IMODE(root_stat.st_mode) & 0o500 == 0o500, 'unsupported root owner access mode')
        demand(not os.listxattr(root), 'unsupported root xattrs/ACLs')
        def walk(fd, prefix, depth, hashing):
            demand(depth <= caps['max_depth'], 'oracle depth cap')
            start = os.fstat(fd)
            names = []
            with os.scandir(fd) as listing:
                for item in listing:
                    names.append(item.name)
                    demand(len(names) <= caps['max_entries'], 'oracle directory count cap')
            if hashing:
                snapshots[prefix] = signature(start)
            else:
                demand(snapshots[prefix] == signature(start), 'source directory changed')
            for name in sorted(names):
                demand(name not in ('', '.', '..') and '\\' not in name and ':' not in name,
                       'unsupported path component')
                name.encode('utf-8', 'strict')
                relative = name if not prefix else prefix + '/' + name
                demand(len(relative.encode('utf-8')) <= caps['max_path_bytes'], 'oracle path cap')
                info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                demand(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),
                       'unsupported symlink or special file')
                needed = 0o500 if stat.S_ISDIR(info.st_mode) else 0o400
                demand(stat.S_IMODE(info.st_mode) & needed == needed, 'unsupported owner access mode')
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if stat.S_ISDIR(info.st_mode):
                    flags |= os.O_DIRECTORY
                child = os.open(name, flags, dir_fd=fd)
                try:
                    opened = os.fstat(child)
                    demand(signature(opened) == signature(info), 'entry changed while opening')
                    mode = stat.S_IMODE(opened.st_mode)
                    demand(not (mode & ~0o777), 'unsupported special permission bits')
                    demand(not os.listxattr(child), 'unsupported xattrs/ACLs')
                    if hashing:
                        demand(len(entries) < caps['max_entries'], 'oracle total entry cap')
                        row = {'path': relative, 'kind': 'dir' if stat.S_ISDIR(info.st_mode) else 'file',
                               'mode': mode, 'origin': metadata(opened)}
                        entries.append(row)
                    else:
                        demand(relative in snapshots and snapshots[relative] == signature(opened),
                               'source entry changed or added')
                    if stat.S_ISDIR(info.st_mode):
                        if hashing:
                            counts['directories'] += 1
                        walk(child, relative, depth + 1, hashing)
                    elif hashing:
                        demand(opened.st_size <= caps['max_file_bytes'], 'oracle file size cap')
                        demand(counts['bytes'] + opened.st_size <= caps['max_total_bytes'],
                               'oracle total byte cap')
                        if require_single_links:
                            identity = (opened.st_dev, opened.st_ino)
                            demand(opened.st_nlink == 1 and identity not in identities,
                                   'oracle file aliases')
                            identities.add(identity)
                        digest, length = hashlib.sha256(), 0
                        while True:
                            block = os.read(child, caps['chunk_bytes'])
                            if not block:
                                break
                            length += len(block)
                            counts['read_bytes'] += len(block)
                            if io_counters is not None:
                                io_counters['independent_oracle_read_bytes'] += len(block)
                            demand(length <= opened.st_size, 'source grew during oracle read')
                            digest.update(block)
                        demand(length == opened.st_size, 'source shortened during oracle read')
                        row.update(size=length, sha256=digest.hexdigest())
                        counts['files'] += 1
                        counts['bytes'] += length
                        counts['allocated_bytes'] += opened.st_blocks * 512
                    demand(signature(opened) == signature(os.fstat(child)), 'source changed during read')
                    if hashing:
                        snapshots[relative] = signature(opened)
                finally:
                    os.close(child)
            demand(signature(start) == signature(os.fstat(fd)), 'directory changed during oracle scan')
            return names
        walk(root, '', 0, True)
        expected_names = set(snapshots)
        # A second independent metadata traversal also detects missing entries.
        seen = {''}
        def census(fd, prefix):
            with os.scandir(fd) as listing:
                for item in listing:
                    name = item.name if not prefix else prefix + '/' + item.name
                    demand(len(seen) <= caps['max_entries'], 'oracle final census cap')
                    seen.add(name)
                    if item.is_dir(follow_symlinks=False):
                        child = os.open(item.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                        dir_fd=fd)
                        try:
                            census(child, name)
                        finally:
                            os.close(child)
        walk(root, '', 0, False)
        census(root, '')
        demand(seen == expected_names, 'source paths changed during oracle scan')
        result = {'schema': SCHEMA, 'source_root': source,
                  'root_mode': stat.S_IMODE(root_stat.st_mode),
                  'root_origin': metadata(root_stat),
                  'entries': sorted(entries, key=lambda r: r['path']), 'counts': counts}
        demand(len(canonical(result)) <= caps['max_inventory_bytes'], 'oracle inventory byte cap')
        return result
    finally:
        os.close(root)


def write_inventory(source, output, limits=None, require_single_links=False):
    output = absolute(output)
    source = absolute(source)
    demand(os.path.commonpath((source, output)) != source, 'oracle output inside source')
    parent = directory(os.path.dirname(output))
    try:
        inventory = collect(source, limits, require_single_links)
        raw = canonical(inventory)
        fd = os.open(os.path.basename(output), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent)
        try:
            view = memoryview(raw)
            while view:
                count = os.write(fd, view)
                demand(count > 0, 'oracle short write')
                view = view[count:]
            os.fsync(fd)
        finally:
            os.close(fd)
        os.fsync(parent)
        return {'inventory_sha256': hashlib.sha256(raw).hexdigest(),
                'inventory_path': output, 'counts': inventory['counts']}
    finally:
        os.close(parent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('output')
    parser.add_argument('--single-links', action='store_true')
    args = parser.parse_args()
    print(json.dumps(write_inventory(args.source, args.output,
                                    require_single_links=args.single_links), sort_keys=True))
