"""Verify the bounded product adapter and its complete retained caller.

Produced by Nick Petalas. Apache-2.0.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import products
import runner


def need(condition, message):
    if not condition:
        raise ValueError(message)


def reference(a, b):
    size = len(a)
    result = [[(F(0), F(0)) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            real, imaginary = F(0), F(0)
            for k in range(size):
                ar, ai = a[i][k]
                br, bi = b[k][j]
                real += ar * br - ai * bi
                imaginary += ar * bi + ai * br
            result[i][j] = real, imaginary
    return result


def fixtures():
    zero = products.ZERO
    values = ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)),
              (F(-1, 2), F(3, 4)), (F(5, 8), F(-1, 16)))
    matrices = []
    for shift in range(12):
        matrices.append([[values[(shift + i * 2 + j * 3) % len(values)]
                          for j in range(2)] for i in range(2)])
    for a in matrices:
        for b in matrices:
            need(products.product(a, b) == reference(a, b), "mixed dyadic product")
    boundary = (F((1 << 256) - 1, 1 << 64), F(-1, 1 << 64))
    need(products.product([[boundary]], [[boundary]]) ==
         reference([[boundary]], [[boundary]]), "capacity-boundary product")
    diagonal = [[zero for _ in range(16)] for _ in range(16)]
    for i in range(16):
        diagonal[i][i] = values[1 + i % 4]
    need(products.product(diagonal, diagonal) == reference(diagonal, diagonal),
         "maximum-dimension product")
    return 146


def boundaries():
    zero = products.ZERO
    cases = [([], [], zero), ([[zero]] * 17, [[zero]], zero),
             ([[zero, zero]], [[zero]], zero), ([[()]], [[zero]], zero),
             ([[(0, 0)]], [[zero]], zero),
             ([[(F(1, 3), F(0))]], [[zero]], zero),
             ([[(F(1, 1 << 65), F(0))]], [[zero]], zero),
             ([[(F(1 << 256), F(0))]], [[zero]], zero),
             ([[zero]], [[zero, zero], [zero, zero]], zero),
             ([[zero]], [[zero]], (F(1), F(0)))]
    for left, right, canonical_zero in cases:
        try:
            products.product(left, right, canonical_zero)
        except (TypeError, ValueError):
            continue
        raise ValueError("invalid product accepted")
    return len(cases)


def mutation_controls():
    with tempfile.TemporaryDirectory(prefix="integer-controls-") as temporary:
        root = Path(temporary)
        package = root / "research" / HERE.name
        source = root / "research" / runner.SOURCE.name
        shutil.copytree(HERE, package)
        shutil.copytree(runner.SOURCE, source)
        checker = source / "evidence/finite-check/check_support.py"
        checker.chmod(checker.stat().st_mode | 0o200)
        original = checker.read_bytes()
        checker.write_bytes(original + b"\n")
        command = [sys.executable, "-I", "-W", "error", "-B", str(package / "runner.py")]
        if sys.flags.optimize:
            command.insert(2, "-O")
        changed = subprocess.run(command, capture_output=True, timeout=30)
        need(changed.returncode != 0 and b"Source pin mismatch" in changed.stderr,
             "changed source was not invalidated")
        checker.write_bytes(original)
        adapter = package / "products.py"
        adapter.chmod(adapter.stat().st_mode | 0o200)
        original_adapter = adapter.read_text()
        needle = "real[j] += ar * br - ai * bi"
        need(original_adapter.count(needle) == 1, "mutation site changed")
        adapter.write_text(original_adapter.replace(needle, "real[j] += ar * br + ai * bi"))
        changed = subprocess.run(command, capture_output=True, timeout=30)
        need(changed.returncode != 0 and b"Q inverse is actual adjoint" in changed.stderr,
             "wrong Gaussian product sign was not rejected by retained control")
    return 2


def main():
    products_checked = fixtures()
    invalid = boundaries()
    report, counts = runner.run("differential")
    need(counts == {"products": 277, "compared_entries": 70912}, "complete work count")
    command = [sys.executable, "-I", "-W", "error", "-B", str(runner.SOURCE / "verify.py")]
    if sys.flags.optimize:
        command.insert(2, "-O")
    original = subprocess.run(command, capture_output=True, timeout=30, check=True)
    need(json.loads(original.stdout) == report, "unchanged complete wrapper report")
    mutations = mutation_controls()
    hashes = {p.name: sha256(p.read_bytes()).hexdigest()
              for p in sorted(HERE.iterdir()) if p.is_file()}
    print(json.dumps({"status": "PASS_NONLINEAR_SUPPORT_INTEGER_PRODUCTS",
                      **counts, "additional_products": products_checked,
                      "invalid_inputs_rejected": invalid, "mutations_rejected": mutations,
                      "complete_report": report, "package_sha256": hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
