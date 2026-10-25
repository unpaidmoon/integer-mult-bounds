"""Exact corner certificate for the section-2 record inventory.

Standard library only. The written proof is the quantified argument; this
checker recomputes the same integers, a second polynomial expansion, the
comparison with the inherited majorant, and the stated rejection controls.
"""

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent.parent
LIMIT = 64

# Integers displayed in PROOF.md. The old batch values are the predecessor's
# published exhaustion, not outputs of this process.
CORNERS = {
    (1, 1): {
        "A": 62, "J": 10, "V": 1, "ops": 2481,
        "T_record": 5081088, "T_tape": 287541, "T_rot": 162, "T_crt": 4214784,
        "U": 25689948, "B": 822078336, "E": 68719476736,
        "old_B": 75548846976, "ratio": Fraction(6422487, 536870912),
    },
    (2, 1): {
        "A": 62, "J": 10, "V": 1, "ops": 2481,
        "T_record": 5081088, "T_tape": 287541, "T_rot": 288, "T_crt": 4243456,
        "U": 25719124, "B": 823011968, "E": 1099511627776,
        "old_B": 75549780608, "ratio": Fraction(6429781, 8589934592),
    },
    (2, 2): {
        "A": 252, "J": 44, "V": 8, "ops": 44360,
        "T_record": 90849280, "T_tape": 4734627, "T_rot": 576, "T_crt": 4243456,
        "U": 386581388, "B": 12370604416, "E": 1099511627776,
        "old_B": 1241895956864, "ratio": Fraction(96645347, 8589934592),
    },
}
CELL = {
    (1, 1): {"ops": 52153, "B": 13843295104},
    (2, 2): {"ops": 931696, "B": 244980412800},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parts(p, ell, h):
    if type(p) is not int or type(ell) is not int or type(h) is not int:
        raise ValueError("integer parameters required")
    if not (p >= 2 and 1 <= h <= ell <= p):
        raise ValueError("outside the admissible domain")
    q, n, w = p + 2, 2**h, 4 * (p + 2)
    accesses = n * n + 2 * n * h * h + 24 * n * h + 3 * n
    records = n * (h * h + 3 * h + 1)
    require(n * h % 2 == 0, "pairwise count must be an integer")
    pairs = n * n - n - (n * h) // 2
    tape = accesses * (26 * w * records + 25 * w) + 30 * w * records
    tape += 3 * n * h + 6 * (2 * h - 1) * n + 3
    rotation = 9 * (ell + 2)**2 * n
    crt = 65536 * q**3 + 1024 * q * ell**3 + 1024 * q * q
    return {
        "q": q, "n": n, "w": w, "A": accesses, "J": records, "V": pairs,
        "T_tape": tape, "T_rot": rotation, "T_crt": crt,
        "cap": 8 * w * w, "cells": 5 * w * records,
    }


def record_ops(row):
    return 4 * row["A"] * row["J"] + row["V"]


def cell_ops(row):
    return record_ops(row) + row["A"] + row["J"] + row["A"] * row["cells"]


def batch(row, operations):
    scalar = row["cap"] * operations
    axis = row["T_crt"] + 4 * (row["T_rot"] + row["T_tape"] + scalar)
    return 8 * row["q"] * axis, axis, scalar


def expanded_record_batch(p, ell, h):
    """Independent q-polynomial of the record-inventory batch."""
    q, n = p + 2, 2**h
    accesses = n * (n + 2 * h * h + 24 * h + 3)
    records = n * (h * h + 3 * h + 1)
    pairs = n * n - n - (n * h) // 2
    operations = 4 * accesses * records + pairs
    linear = accesses * (104 * records + 100) + 120 * records
    constant = n * (15 * h - 6) + 3
    return (524288 * q**4 + 8192 * ell**3 * q**2 + 8192 * q**3
            + 288 * q * n * (ell + 2)**2 + 32 * linear * q**2
            + 32 * constant * q + 4096 * operations * q**3)


def sources():
    manifest = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    phrases = {
        "research/crt-arena-root-axis/vendor/pr4192-crt-benes-scan-PROOF.md": (
            "four key words",
            "N²-N-Nh/2",
        ),
        "research/crt-arena-batch-threshold/PROOF.md": (
            "(2,1,1)",
            "(2,2,2)",
        ),
    }
    checked = 0
    for row in manifest["files"]:
        if row["usage"] != "input":
            continue
        data = (ROOT / row["path"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        require(digest == row["sha256"], "source SHA256 mismatch: " + row["path"])
        header = f"blob {len(data)}\0".encode()
        blob = hashlib.sha1(header + data).hexdigest()
        require(blob == row["git_blob"], "source Git blob mismatch: " + row["path"])
        text = data.decode("utf-8")
        for phrase in phrases.get(row["path"], ()):
            require(phrase in text, "pinned source lost " + phrase)
        checked += 1
    require(checked == 3, "three live inputs required")
    return checked


def corners():
    for (ell, h), expected in CORNERS.items():
        row = parts(2, ell, h)
        operations = record_ops(row)
        new_batch, axis, scalar = batch(row, operations)
        old_batch, _, _ = batch(row, row["T_tape"])
        allowance = 2**(4 * ell) * row["q"]**16
        require(row["A"] == expected["A"] and row["J"] == expected["J"], "census")
        require(row["V"] == expected["V"] and operations == expected["ops"], "operations")
        require(scalar == expected["T_record"], "record term")
        require(row["T_tape"] == expected["T_tape"], "tape invoice")
        require(row["T_rot"] == expected["T_rot"] and row["T_crt"] == expected["T_crt"],
                "crt or rotation tariff")
        require(axis == expected["U"] and new_batch == expected["B"], "new batch")
        require(allowance == expected["E"] and old_batch == expected["old_B"], "old batch")
        require(new_batch == expanded_record_batch(2, ell, h), "expanded batch")
        require(Fraction(new_batch, allowance) == expected["ratio"], "displayed ratio")
        require(new_batch < allowance, "record inventory must fit")
        if (ell, h) != (2, 1):
            require(old_batch > allowance, "inherited majorant must still exceed E")
        else:
            require(old_batch < allowance, "the non-exception must stay under E")
        omitted, _, _ = batch_without_tape(row, operations)
        require(omitted < new_batch, "dropping the tape invoice is a different bill")
    return len(CORNERS)


def batch_without_tape(row, operations):
    scalar = row["cap"] * operations
    axis = row["T_crt"] + 4 * (row["T_rot"] + scalar)
    return 8 * row["q"] * axis, axis, scalar


def cell_corners():
    for (ell, h), expected in CELL.items():
        row = parts(2, ell, h)
        operations = cell_ops(row)
        value, _, _ = batch(row, operations)
        allowance = 2**(4 * ell) * row["q"]**16
        require(operations == expected["ops"] and value == expected["B"], "cell batch")
        require(value < allowance, "coefficient-one cell enlargement must fit")
        require(operations < row["T_tape"], "cell enlargement must tighten the old scalar")
    return len(CELL)


def domain_comparison():
    """Corroborate T_record < T_scalar on a bounded box. The proof has no cap."""
    checked = 0
    for p in range(2, LIMIT + 1):
        for ell in range(1, p + 1):
            for h in range(1, ell + 1):
                row = parts(p, ell, h)
                operations = record_ops(row)
                require(expanded_record_batch(p, ell, h) == batch(row, operations)[0],
                        "expanded batch on the box")
                require(0 < row["V"] < row["n"] * row["n"] < row["A"], "pair bound")
                require(row["J"] >= 10 and row["A"] >= 4 and row["w"] >= 16, "width")
                require(4 * row["A"] * row["J"] + row["V"] < 5 * row["A"] * row["J"],
                        "record count")
                require(5 * row["A"] * row["J"] < 26 * row["A"] * row["w"] * row["J"]
                        <= row["T_tape"], "tape lower bound")
                require(cell_ops(row) < row["T_tape"], "cell count below tape")
                require(6 < 21 * row["w"], "cell coefficient comparison")
                checked += 1
    require(checked == 45759, "bounded box size")
    return checked


def controls():
    rejected = 0
    invalid = [(True, 1, 1), (2, 0, 1), (2, 1, 2), (1, 1, 1), (2, 3, 1)]
    for args in invalid:
        try:
            parts(*args)
        except ValueError:
            rejected += 1
            continue
        raise ValueError("invalid fixture accepted")
    row = parts(2, 2, 2)
    old_batch, _, _ = batch(row, row["T_tape"])
    allowance = 2**8 * row["q"]**16
    require(old_batch > allowance, "old constant-one claim must reject at (2,2,2)")
    mutant = expanded_record_batch(2, 2, 2) - 4096 * record_ops(row) * row["q"]**3
    require(mutant != batch(row, record_ops(row))[0], "dropped scalar term must disagree")
    require(mutant > 0, "mutant expansion")
    return rejected + 2


def result():
    source_count = sources()
    corner_count = corners()
    cell_count = cell_corners()
    box = domain_comparison()
    rejection_count = controls()
    names = ["PROOF.md", "verify.py", "SOURCES.json", "TASK.json", "VERIFY.json"]
    hashes = {name: hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest()
              for name in names}
    witnesses = []
    for ell, h in ((1, 1), (2, 1), (2, 2)):
        witnesses.append({"ell": ell, "h": h, "batch": CORNERS[(ell, h)]["B"],
                          "allowance": CORNERS[(ell, h)]["E"],
                          "ratio": str(CORNERS[(ell, h)]["ratio"])})
    return {
        "status": "PASS_CRT_P2_CORNER_RECORD_INVENTORY",
        "claim_type": "finite certificate with a cited domain corollary",
        "corners": witnesses,
        "corner_checks": corner_count,
        "cell_checks": cell_count,
        "box_triples": box,
        "live_inputs": source_count,
        "rejection_controls": rejection_count,
        "source_sha256": hashes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    actual = result()
    path = PACKAGE / "RESULT.json"
    if args.write_result:
        path.write_text(json.dumps(actual, indent=2) + "\n", encoding="utf-8")
    expected = json.loads(path.read_text(encoding="utf-8"))
    require(json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True),
            "receipt differs from exact replay")
    print(actual["status"])


if __name__ == "__main__":
    main()
