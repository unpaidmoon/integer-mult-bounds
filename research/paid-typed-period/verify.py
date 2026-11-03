"""Bounded exact corroboration, independent word and child-count oracles."""

import hashlib
import itertools
import json
import platform
from fractions import Fraction
from pathlib import Path

from model import contractive, invoice, minimum_word, reserves, stages


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def literal_product(n: int, h: int, word: str) -> tuple[Fraction, Fraction]:
    """Multiply matrices and adapters directly, without the model's stage builder."""
    matrices = {
        "A": ((Fraction(2), 0), (0, Fraction(1, 2))),
        "B": ((Fraction(1, 2**n), 0), (0, Fraction(2 ** (n - 1)))),
    }
    result = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    for j in range(len(word)):
        matrix = matrices[word[j]]
        result = tuple(tuple(sum(result[i][k] * matrix[k][l] for k in range(2))
                             for l in range(2)) for i in range(2))
        if word[j] != word[(j + 1) % len(word)]:
            result = tuple(tuple(entry * 2**h for entry in row) for row in result)
    check(result[0][1] == result[1][0] == 0, "oracle lost diagonality")
    return result[0][0], result[1][1]


def word_census() -> dict:
    digest = hashlib.sha256()
    checked = 0
    minima = {}
    for n, h in itertools.product(range(2, 5), range(2)):
        first = None
        for length in range(1, 13):
            for letters in itertools.product("AB", repeat=length):
                word = "".join(letters)
                direct = literal_product(n, h, word)
                check(invoice(n, h, word) == direct, "literal word invoice mismatch")
                passed = max(direct) < 1
                check(contractive(direct) == passed, "strict decision mismatch")
                if passed and first is None:
                    first = length
                digest.update(f"{n},{h},{word}:{direct}:{passed}\n".encode())
                checked += 1
        expected = (2 * h + 1) * (2 * n + 1)
        check(first == (expected if expected <= 12 else None), "short-word minimum mismatch")
        minima[f"{n},{h}"] = first
    return {"words": checked, "maximum_length": 12, "first_passing_lengths": minima,
            "sha256": digest.hexdigest()}


def child_count_census() -> dict:
    """Enumerate realizable cyclic run counts using integer children at s=1/2."""
    checked = 0
    digest = hashlib.sha256()
    for n, h in itertools.product(range(2, 9), range(4)):
        predicted = (2 * h + 1) * (2 * n + 1)
        first = None
        a = (2 ** (n + 1), 2 ** (n - 1))
        b = (1, 2 ** (2 * n - 1))
        g = 2 ** (n + h)
        for length in range(1, predicted + 1):
            for x in range(length + 1):
                y = length - x
                switches = (0,) if min(x, y) == 0 else range(2, 2 * min(x, y) + 1, 2)
                for count in switches:
                    numerator = (a[0]**x * b[0]**y * g**count,
                                 a[1]**x * b[1]**y * g**count)
                    denominator = 2 ** (n * (length + count))
                    passed = max(numerator) < denominator
                    if passed and first is None:
                        first = length
                    digest.update(f"{n},{h},{x},{y},{count}:{passed}\n".encode())
                    checked += 1
        check(first == predicted, "integer child-count minimum mismatch")
    return {"realizable_count_triples": checked, "parameter_pairs": 28,
            "sha256": digest.hexdigest()}


def witnesses() -> dict:
    checked = 0
    for n, h in itertools.product(range(2, 33), range(5)):
        word = minimum_word(n, h)
        check(len(word) == (2 * h + 1) * (2 * n + 1), "witness length mismatch")
        check(invoice(n, h, word) == (Fraction(1, 2), Fraction(1, 2)),
              "witness does not pay every switch")
        checked += 1
    phase_rows = 0
    for n, h in itertools.product(range(2, 6), range(2)):
        word = minimum_word(n, h)
        factors = stages(n, h, word)
        values = reserves(n, h, word)
        for j, stage in enumerate(factors):
            after = values[(j + 1) % len(values)]
            for coordinate in range(2):
                check(values[j][coordinate] > 0, "nonpositive phase reserve")
                check(values[j][coordinate] == 1 + stage[coordinate] * after[coordinate],
                      "unit forcing or phase return missing")
                phase_rows += 1
    return {"optimal_words": checked, "positive_phase_rows_with_unit_forcing": phase_rows}


def rank_realizations() -> dict:
    checked = 0
    for n, h, pq in itertools.product(range(2, 9), range(4), ((1, 2), (2, 3), (3, 5), (7, 8))):
        p, q = pq
        t = (n + p - 1) // p
        parent = 2 ** (q * t)
        check(parent > 1, "child does not descend")
        for e in (1, -1, -n, n - 1, h, h):
            count = 2 ** (p * t + e)
            coefficient = Fraction(2**e) if e >= 0 else Fraction(1, 2**-e)
            check(type(count) is int and count >= 1, "nonintegral child multiplicity")
            check(Fraction(count**q, parent**p) == coefficient**q,
                  "exact rational-power child moment mismatch")
            checked += 1
    n, h, t, p, q = 2, 1, 2, 1, 2
    word = minimum_word(n, h)
    exponents = {"A": (1, -1), "B": (-n, n - 1)}
    descendants = [1, 1]
    depth = 0
    for j, letter in enumerate(word):
        for i in range(2):
            descendants[i] *= 2 ** (p * t + exponents[letter][i])
        depth += 1
        if letter != word[(j + 1) % len(word)]:
            descendants = [value * 2 ** (p * t + h) for value in descendants]
            depth += 1
    check(descendants == [2**33, 2**33] and q * t * depth == 68,
          "complete example child invoice mismatch")
    return {"stage_realizations": checked, "example_supplier_layers": len(word),
            "example_total_recursive_stages": depth, "example_descendants": descendants,
            "example_size_ratio": "1/2^68", "example_exponent": "33/68"}


def controls() -> int:
    cases = [
        (lambda: minimum_word(1, 0), "N must be an integer in 2..64"),
        (lambda: minimum_word(True, 0), "N must be an integer in 2..64"),
        (lambda: minimum_word(65, 0), "N must be an integer in 2..64"),
        (lambda: minimum_word(2, -1), "h must be an integer in 0..8"),
        (lambda: minimum_word(2, 9), "h must be an integer in 0..8"),
        (lambda: invoice(2, 0, ""), "word length must be in 1..4096"),
        (lambda: invoice(2, 0, "A" * 4097), "word length must be in 1..4096"),
        (lambda: invoice(2, 0, "AC"), "word alphabet must be A,B"),
        (lambda: reserves(2, 0, "A"), "reserve requires a strict cyclic contraction"),
        (lambda: reserves(32, 4, minimum_word(32, 4)), "reserve phase count exceeds 128"),
        (lambda: contractive((Fraction(0), Fraction(1))),
         "invoice must contain two positive rational coefficients"),
    ]
    for action, message in cases:
        try:
            action()
        except ValueError as error:
            check(str(error) == message, "wrong rejection reason")
        else:
            raise ValueError("invalid input accepted")
    check(invoice(2, 1, "A" * 6 + "B" * 4) == (1, 1), "wrap control is not critical")
    check(not contractive(invoice(2, 1, "A" * 6 + "B" * 4)), "nonstrict cycle accepted")
    check(literal_product(2, 0, "A" * 6 + "B" * 4) == (Fraction(1, 4),) * 2,
          "fee omission control changed")
    check(not contractive(invoice(2, 1, minimum_word(2, 0))), "uncharged witness accepted")
    check(not contractive(invoice(2, 0, "AB")), "critical short word accepted")
    check(not contractive(invoice(2, 0, "AAAA")), "pure A accepted")
    check(not contractive(invoice(2, 0, "BBBB")), "pure B accepted")
    return len(cases) + 7


def package_hashes() -> dict:
    package = Path(__file__).resolve().parent
    result = {}
    names = ("PROOF.md", "README.md", "SOURCES.json", "TASK.json", "VERIFY.json", "model.py", "verify.py")
    for name in names:
        path = package / name
        check(path.is_file() and not path.is_symlink(), "unexpected package entry")
        check(path.stat().st_size <= 1024 * 1024, "package file exceeds one MiB")
        result[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main() -> None:
    result = {"schema": "paid-typed-period-receipt/v1", "python": platform.python_version(),
              "word_census": word_census(), "child_count_census": child_count_census(),
              "witnesses": witnesses(), "rank_realizations": rank_realizations(),
              "rejection_and_mathematical_controls": controls(),
              "package_sha256": package_hashes(),
              "claim_type": "scoped proof with finite exact corroboration",
              "status": "PASS_PAID_TYPED_PERIOD"}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
