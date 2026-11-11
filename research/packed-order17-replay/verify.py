"""Check the new kernel and retain the original complete replay coverage."""

from contextlib import redirect_stdout
import hashlib
import io
from itertools import product
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from packed import middle, multiply, pack
from run_replay import ROOT, authenticate, load_primary


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rejected(function):
    try:
        function()
    except (ValueError, TypeError):
        return
    raise ValueError("invalid arithmetic/source input survived")


def vector_cases():
    count = 0
    for size in range(1, 4):
        vectors = list(product(range(-2, 3), repeat=size))
        bits = 4 + (2 * size).bit_length()
        for left in vectors:
            a = pack([(value, 0) for value in left], bits)[0]
            for right in vectors:
                b = pack([(value, 0) for value in right[::-1]], bits)[0]
                actual = middle(a * b, bits, size)
                need(actual == sum(x * y for x, y in zip(left, right, strict=True)),
                     "signed middle coefficient")
                count += 1
    raw = pack([(-1, 0), (0, 0)], 4)[0]
    need(((raw >> 4) % 16) == 15 and middle(raw, 4, 2) == 0,
         "negative lower-tail borrow control")
    return count


def matrix_cases(source):
    rng = random.Random(1706208)
    count = 0
    for size in range(1, 17):
        for unused in range(4):
            matrices = [source.canonical(
                [[(rng.randrange(-64, 65), rng.randrange(-64, 65))
                  for j in range(size)] for i in range(size)], rng.randrange(1, 65))
                for side in range(2)]
            need(multiply(*matrices) == source.multiply(*matrices), "full matrix product")
            count += 1
    for exponent in (0, 1, 63, 255, 4095):
        value = (1 << exponent) - 1
        a = ((((value, -value),),), 1)
        b = ((((-value, value),),), 1)
        need(multiply(a, b) == source.multiply(a, b), "large signed integer product")
        count += 1
    zero = (((0, 0),),)
    need(multiply((zero, 7), (zero, 11)) == (zero, 1), "canonical zero denominator")
    need(multiply(((((1, 0),),), 1 << 4095),
                  ((((-1, 0),),), 1 << 4095))[1] == 1 << 8190,
         "denominator capacity edge")
    return count + 2


def input_controls():
    one = ((((1, 0),),), 1)
    invalid = [([], 1), ([[[1, 0]]] * 17, 1), ([[[1, 0], [0, 0]]], 1),
               ([[[1]]], 1), ([[["x", 0]]], 1), ([[[1 << 4096, 0]]], 1),
               (one[0], 0), (one[0], -1), (one[0], True), (one[0], 1 << 4096)]
    for matrix in invalid:
        rejected(lambda: multiply(matrix, one))
    two = ((((1, 0), (0, 0)), ((0, 0), (1, 0))), 1)
    rejected(lambda: multiply(one, two))
    return len(invalid) + 1


def coverage(source):
    original = source.multiply
    with redirect_stdout(io.StringIO()) as expected:
        source.main()
    counts = {"matrix_products": 0, "output_entries": 0}

    def shadow(left, right):
        wanted = original(left, right)
        actual = multiply(left, right)
        need(actual == wanted, "literal replay product equality")
        counts["matrix_products"] += 1
        counts["output_entries"] += len(actual[0]) ** 2
        return actual

    source.multiply = shadow
    with redirect_stdout(io.StringIO()) as observed:
        source.main()
    need(observed.getvalue() == expected.getvalue(), "complete primary stdout equality")
    need(counts == {"matrix_products": 85, "output_entries": 21760}, "literal coverage")
    counts["primary_stdout_sha256"] = hashlib.sha256(observed.getvalue().encode()).hexdigest()
    source.multiply = original
    return counts


def source_controls():
    rows = [row for row in json.loads((HERE / "SOURCES.json").read_text())["files"]
            if row["usage"] == "input"]
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for row in rows:
            dest = root / row["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT / row["path"]).read_bytes())
        authenticate(root)
        for row in rows:
            dest = root / row["path"]
            raw = dest.read_bytes()
            dest.write_bytes(raw + b" ")
            rejected(lambda: authenticate(root))
            dest.write_bytes(raw)
    return len(rows)


def main():
    need(not sys.argv[1:], "unexpected arguments")
    source = load_primary()
    result = {"signed_vector_pairs": vector_cases(), "matrix_cases": matrix_cases(source),
              "input_rejections": input_controls(), "literal_primary": coverage(source),
              "source_byte_rejections": source_controls()}
    mode = ["-O"] if sys.flags.optimize else []
    direct = subprocess.run([sys.executable, "-I", "-B", "-W", "error", *mode,
                             str(HERE / "run_replay.py")], capture_output=True,
                            check=True, timeout=60)
    need(not direct.stderr and hashlib.sha256(direct.stdout).hexdigest() ==
         result["literal_primary"]["primary_stdout_sha256"], "actual packed CLI output")
    independent = ROOT / "research/order-seventeen-clifford/independent.py"
    done = subprocess.run([sys.executable, "-I", "-B", "-W", "error", *mode,
                           str(independent)], capture_output=True, check=True, timeout=60)
    need(not done.stderr, "independent stderr")
    result["independent_stdout_sha256"] = hashlib.sha256(done.stdout).hexdigest()
    need(result["independent_stdout_sha256"] ==
         "5145f6d662dd33b23352a5458087203f7e08d504c5ed01be72200ac2fd8619e0",
         "unchanged complete independent output")
    print(json.dumps(result, sort_keys=True))
    print("PASS_PACKED_ORDER17_REPLAY")


if __name__ == "__main__":
    main()
