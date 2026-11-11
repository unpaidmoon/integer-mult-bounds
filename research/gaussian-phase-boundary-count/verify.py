#!/usr/bin/env python3
"""Exact phase-window census. Produced by Nick Petalas. Apache-2.0."""
import argparse
import hashlib
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def ceiling(numerator, denominator):
    return -(-numerator // denominator)


def validate(s, k, w, start, length):
    for value in (s, k, w, start, length):
        need(type(value) is int and value.bit_length() <= 4096,
             "integer argument with at most 4096 bits")
    need(0 < k < s and w > 0 and length > 0, "positive phase/window domain")
    need(s // (2 * k) > 4 * w, "every complete physical cell must be long")


def cell(s, k, position):
    period, residue = divmod(position, s)
    phase = (2 * k * residue + s) // (2 * s)
    left = 0 if phase == 0 else ceiling(s * (2 * phase - 1), 2 * k)
    right = s if phase == k else ceiling(s * (2 * phase + 1), 2 * k)
    return period * (k + 1) + phase, period * s + left, period * s + right


def piece(length, w):
    return (length, 0) if length <= 4 * w else (2 * w, 1)


def count(s, k, w, start, length):
    """Return boundary rows, long pieces and total pieces, without a row scan."""
    validate(s, k, w, start, length)
    first, _, right = cell(s, k, start)
    last, left, _ = cell(s, k, start + length - 1)
    pieces = last - first + 1
    if pieces == 1:
        boundary, long = piece(length, w)
        return boundary, long, 1
    first_boundary, first_long = piece(right - start, w)
    last_boundary, last_long = piece(start + length - left, w)
    boundary = 2 * w * (pieces - 2) + first_boundary + last_boundary
    long = pieces - 2 + first_long + last_long
    need(0 <= boundary <= length and 0 <= long <= pieces, "count invariants")
    return boundary, long, pieces


def short_window_bound(s, k, w, length):
    need(1 <= length <= s, "bound is for at most one period")
    return min(length, 2 * w * ceiling(k * (length - 1), s) + 8 * w)


def literal_prefixes(s, k, w, start, limit):
    """Independent append-only scan of the source's (period, q_j-j) keys."""
    need(0 < limit <= 1024, "literal scan capacity")
    previous, run_length = None, 0
    boundary = long = cells = 0
    for position in range(start, start + limit):
        period, residue = divmod(position, s)
        nearest = ((s + k) * residue * 2 + s) // (2 * s)
        key = period, nearest - residue
        if key != previous:
            cells += 1
            run_length = 0
        old_boundary = run_length if run_length <= 4 * w else 2 * w
        old_long = int(run_length > 4 * w)
        run_length += 1
        new_boundary = run_length if run_length <= 4 * w else 2 * w
        new_long = int(run_length > 4 * w)
        boundary += new_boundary - old_boundary
        long += new_long - old_long
        previous = key
        yield boundary, long, cells


def complete_census():
    configurations = windows = bounded = 0
    digest = hashlib.sha256()
    for s in range(10, 65):
        for w in range(1, 4):
            for k in range(1, s // (2 * (4 * w + 1)) + 1):
                if s // (2 * k) <= 4 * w:
                    continue
                configurations += 1
                for residue in range(s):
                    start = residue - (s if residue % 2 else 0)
                    scans = literal_prefixes(s, k, w, start, 2 * s + 1)
                    for length, expected in enumerate(scans, 1):
                        actual = count(s, k, w, start, length)
                        need(actual == expected, f"literal mismatch {s,k,w,start,length}")
                        if length <= s:
                            need(actual[0] <= short_window_bound(s, k, w, length),
                                 "one-period upper bound")
                            bounded += 1
                        digest.update(f"{s},{k},{w},{start},{length}:{actual};".encode())
                        windows += 1
    return {"configurations": configurations, "windows": windows,
            "bounded_windows": bounded, "transcript_sha256": digest.hexdigest()}


def boundary_fixtures():
    checks = 0
    for s, k, w in ((100, 2, 1), (211, 6, 2), (480, 5, 3)):
        for start in (-2*s-1, -s, -1, 0, 1, s-1, s, 2*s+1):
            for length in (1, 4*w, 4*w+1, s-1, s, 2*s+1):
                expected = list(literal_prefixes(s, k, w, start, length))
                need(count(s, k, w, start, length) == expected[-1], "seam fixture")
                a = count(s, k, w, start, length)
                need(a == count(s, k, w, start + 19*s, length), "translation")
                checks += 1
    huge = 1 << 4095
    need(count(huge, 1, 1, -huge, huge) == (4, 2, 2), "capacity boundary")
    need(count(480, 5, 3, 0, 384) == (30, 5, 5), "strict witness")
    need(short_window_bound(480, 5, 3, 384) == 48, "new witness allowance")
    need(4 * 384 * 3 // 48 + 12 * 3 == 132, "old witness allowance")
    return {"seam_translation_fixtures": checks, "witness": {
        "s": 480, "t": 485, "w": 3, "d": 48, "start": 0, "length": 384,
        "piece_lengths": [48, 96, 96, 96, 48], "boundary": 30,
        "long_pieces": 5, "new_allowance": 48, "old_allowance": 132}}


def controls():
    need(count(100, 2, 1, 90, 20) == (4, 2, 2), "period seam must split")
    need(cell(100, 2, -1) == (-1, -25, 0), "signed floor, not truncation")
    need(count(100, 2, 1, 0, 25)[2] == 1, "half-open right endpoint")
    need(count(100, 2, 1, 0, 4)[0] == 4, "4w is entirely boundary")
    need(count(100, 2, 1, 0, 5)[0] == 2, "4w+1 is long")
    need(count(480, 5, 3, 0, 9)[0] == 9, "short piece is not capped at 2w")
    invalid = ((0, 1, 1, 0, 1), (10, 0, 1, 0, 1), (10, 10, 1, 0, 1),
               (100, 2, 0, 0, 1), (100, 2, 1, 0, 0), (100, 2, 1, 0, -1),
               (True, 1, 1, 0, 1), (100, 2, 1, 0.0, 1),
               (8, 1, 1, 0, 1), (1 << 4096, 1, 1, 0, 1))
    for args in invalid:
        try:
            count(*args)
        except ValueError:
            continue
        raise ValueError("invalid input was accepted")
    try:
        short_window_bound(100, 2, 1, 101)
    except ValueError:
        return {"semantic": 6, "domain_rejections": len(invalid) + 1}
    raise ValueError("multi-period bound was accepted")


def invoice_fixture():
    lengths, previous = [], None
    for position in range(384):
        period, residue = divmod(position, 480)
        nearest = (2 * 485 * residue + 480) // 960
        key = period, nearest - residue
        if key != previous:
            lengths.append(0)
        lengths[-1] += 1
        previous = key
    need(lengths == [48, 96, 96, 96, 48], "literal witness pieces")
    w = 3
    units = 0
    for length in lengths:
        long = length > 4 * w
        for offset in range(length):
            boundary = not long or offset < w or offset >= length - w
            fee = 2 * (4 * w + 1) if boundary else 20
            units += sum(1 for _ in range(fee))
            units += 2
        if long:
            units += sum(1 for _ in range(16 * w * w + 32))
    totals = [22 * 384 + (8*w-18) * b + (16*w*w+32) * 5 for b in (132, 48, 30)]
    need(totals[-1] == units == 9508, "complete source tariff substitution")
    need(totals == [10120, 9616, 9508], "old, new and exact invoice allowances")
    return {"literal_units": units, "allowances": totals,
            "common_addend": "2*n_target+2*n_core", "old_to_new_reduction": 504}


def source_hashes(package):
    root = package.parents[1]
    with (package / "SOURCES.json").open("rb") as stream:
        metadata = stream.read(262145)
    need(len(metadata) <= 262144, "manifest capacity")
    sources = json.loads(metadata)
    need(len(sources["files"]) <= 16, "source-pin count capacity")
    hashes = {}
    for entry in sources["files"]:
        if entry["usage"] != "input":
            continue
        path = root / entry["path"]
        with path.open("rb") as stream:
            data = stream.read(262145)
        need(len(data) <= 262144, "source capacity")
        digest = hashlib.sha256(data).hexdigest()
        need(digest == entry["sha256"], "source byte pin: " + entry["path"])
        hashes[entry["path"]] = digest
    for name in ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py"):
        path = package / name
        with path.open("rb") as stream:
            data = stream.read(262145)
        need(len(data) <= 262144, "package capacity")
        hashes[name] = hashlib.sha256(data).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    hashes = source_hashes(package)
    result = {"status": "PASS_GAUSSIAN_PHASE_BOUNDARY_COUNT", "claim_type": "scoped-proof",
              "census": complete_census(), "fixtures": boundary_fixtures(),
              "controls": controls(), "invoice": invoice_fixture(), "sha256": hashes}
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt is not None:
        need(not args.receipt.resolve().is_relative_to(package.parents[1]),
             "receipt must remain outside the checkout")
        with args.receipt.open("x") as stream:
            stream.write(output)
    print(output, end="")


if __name__ == "__main__":
    main()
