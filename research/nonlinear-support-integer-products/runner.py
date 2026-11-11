"""Run the complete retained finite caller using either exact product engine.

The fixture, checks, outputs and frozen predecessor files remain unchanged.
Produced by Nick Petalas. Apache-2.0.
"""
import argparse
import contextlib
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research/nonlinear-monomial-control-ceiling"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError("Python module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    for row in manifest["files"]:
        if row["usage"] == "input":
            path = ROOT / row["path"]
            if path.is_symlink() or sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError("Source pin mismatch: " + row["path"])
    owner = load(SOURCE / "verify.py", "retained_portable_wrapper")
    return owner.authenticate()


def prepare(destination):
    review = SOURCE / "evidence/proof-review"
    logical = {
        "outputs/nonlinear-monomial-control-ceiling-20261023/PROOF.md": "REVIEWED-PROOF.md",
        "outputs/released-operator-intersection-20261023/PROOF.md": "PREDECESSOR-PROOF.md",
        "outputs/released-operator-intersection-20261023/SOURCES.json": "PREDECESSOR-SOURCES.json",
        "outputs/released-operator-intersection-20261023/frozen/PHYSICAL.md": "PHYSICAL.md",
    }
    for name, source in logical.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(review / "frozen" / source, target)
    work = destination / "outputs/nonlinear-monomial-support-check-20261023"
    work.mkdir()
    shutil.copyfile(SOURCE / "evidence/finite-check/check_support.py", work / "check_support.py")
    return work, logical


def execute(mode, work):
    checker = load(work / "check_support.py", "retained_finite_checker")
    integer = load(HERE / "products.py", "scaled_gaussian_products")
    reference = checker.product
    counts = {"products": 0, "compared_entries": 0}

    def observed(left, right):
        counts["products"] += 1
        result = reference(left, right) if mode == "reference" else integer.product(left, right, checker.ZERO)
        if mode == "differential":
            expected = reference(left, right)
            if result != expected:
                raise ValueError("Complete product disagreement")
            counts["compared_entries"] += checker.N * checker.N
        return result

    checker.product = observed
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        checker.main()
    return json.loads(printed.getvalue()), counts


def outputs(work, logical, destination):
    finite = SOURCE / "evidence/finite-check"
    for stem in ("RESULT", "MATRICES"):
        data = (work / (stem + ".json")).read_bytes()
        for suffix in ("", "-OPTIMIZED"):
            if data != (finite / (stem + suffix + ".json")).read_bytes():
                raise ValueError("Complete generated output differs: " + stem + suffix)
    review = SOURCE / "evidence/proof-review/frozen"
    for name, source in logical.items():
        if (destination / name).read_bytes() != (review / source).read_bytes():
            raise ValueError("Private source capture changed")
    return json.loads((work / "RESULT.json").read_text()), (work / "MATRICES.json").read_bytes()


def run(mode):
    manifest = authenticate()
    with tempfile.TemporaryDirectory(prefix="nonlinear-integer-") as temporary:
        destination = Path(temporary)
        work, logical = prepare(destination)
        compact, counts = execute(mode, work)
        result, matrices = outputs(work, logical, destination)
    review = SOURCE / "evidence/proof-review"
    finite = SOURCE / "evidence/finite-check"
    report = {
        "status": "PASS_PORTABLE_NONLINEAR_FINITE_SUPPORT_ONLY",
        "immutable_evidence_files": len(manifest["files"]),
        "written_proof_sha256": sha256((review / "frozen/REVIEWED-PROOF.md").read_bytes()).hexdigest(),
        "independent_review_sha256": sha256((review / "REVIEW.md").read_bytes()).hexdigest(),
        "finite_result_sha256": sha256((finite / "RESULT.json").read_bytes()).hexdigest(),
        "finite_matrices_sha256": sha256(matrices).hexdigest(),
        "positive_examples": compact["positive_examples"],
        "terminal_sandwiches": result["terminal_nonmonomial_count"],
        "scope": "Finite exact16x16 support examples and controls only. Independently reviewed written proof supplies sufficiently-large-width fixed finite complete-product support theorem. No17-axis/all-width phase/native/compiler/caller or kappa replay.",
    }
    return report, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("integer", "reference", "differential"), default="integer")
    args = parser.parse_args()
    report, counts = run(args.mode)
    print(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps(counts, sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    main()
