#!/usr/bin/env python3
"""Degree gaps of the selected row and the two earlier reserves.

The checker evaluates the published 51/25 formulas. It does not recompute
the fourteen stage headrooms.
"""

import hashlib
import json
import tarfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
MARKER = "PASS_DEGREE_GAP_CLEARANCE selected=23971789/25 no_new_kappa"
ASSEMBLY = "research/community-frontier1094-audit/ASSEMBLY.json"
THREE = "notes/three-stage-cover-assembly.tex"
PAIRED = "notes/paired-cube-assembly.tex"
TARBALL = "research/complex-t16-rare-pattern-exchanges/upstream1087.tar.gz"


def fail(message):
    raise SystemExit("FAIL_DEGREE_GAP_CLEARANCE " + message)


def require(condition, message):
    if not condition:
        fail(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def gap(degree, coefficient):
    return Fraction(degree) - Fraction(51 * coefficient, 25)


def evaluate():
    require(sha256(ROOT / "certificates/selected-result.json") == "bb2eaa58647b353f88d0aec2eafb9d30df1be53589231b23e12ceef3e4bad129", "selected record drift")
    require(sha256(ROOT / ASSEMBLY) == "1122cb3a575f8c788345fc1bf4c108ac7c3250fb81a5988671f5eb04b3ab3045", "assembly drift")
    require(sha256(ROOT / THREE) == "ccf34a6d37c4af14bebeab15be50ab204eb1caebe546385520050ec30089441d", "three-stage note drift")
    require(sha256(ROOT / PAIRED) == "45f28775ebf36338df9312957fd09af3c635690acc02ae3d60431ccd16fb46c3", "paired-cube note drift")
    require(sha256(ROOT / TARBALL) == "d4acf04daef85d4514f80ec5fcd2492d0c60e5d6c49fa71b3e6523f8db2dea86", "assembler archive drift")
    selected = json.loads((ROOT / "certificates/selected-result.json").read_text(encoding="utf-8"))
    require(Fraction(selected["kappa"]) == Fraction(836330098538459, 500000000000000000), "the selected kappa moved")
    with tarfile.open(ROOT / TARBALL) as archive:
        assembler = archive.extractfile("code/assemble.py").read().decode("utf-8")
    require("'degree_gap':Q(10**6)-Q(51*20161,25)" in assembler, "the selected formula moved")
    stored = json.loads((ROOT / ASSEMBLY).read_text(encoding="utf-8"))["outer"]["row_product_gap"]
    selected_gap = gap(10 ** 6, 20161)
    require(Fraction(stored) == selected_gap == Fraction(23971789, 25) > 0, "the selected gap moved")
    three = (ROOT / THREE).read_text(encoding="utf-8")
    paired = (ROOT / PAIRED).read_text(encoding="utf-8")
    require("58344+9909+252=68505" in three and "160000-\\frac{51}{25}\\,68505=20249.8>0" in three, "the three-stage reserve moved")
    require("10284+9909+252=20445" in paired and "\\frac{141461}{5}>0" in paired, "the paired-cube reserve moved")
    require(58344 + 9909 + 252 == 68505 and 10284 + 9909 + 252 == 20445, "a carried sum moved")
    three_gap = gap(160000, 68505)
    paired_gap = gap(70000, 20445)
    require(three_gap == Fraction(506245, 25) == Fraction("20249.8") > 0, "the three-stage gap moved")
    require(paired_gap == Fraction(141461, 5) > 0, "the paired-cube gap moved")
    return {
        "selected_gap": "23971789/25",
        "three_stage_gap": "506245/25",
        "paired_gap": "141461/5",
        "no_new_kappa": True,
    }


def main():
    observed = evaluate()
    expected = json.loads((PACKAGE / "RESULT.json").read_text(encoding="utf-8"))
    require(observed == expected, "RESULT.json does not match the execution")
    print(MARKER)


if __name__ == "__main__":
    main()
