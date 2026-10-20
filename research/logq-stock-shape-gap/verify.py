#!/usr/bin/env python3
"""Log_q shape coefficient for the selected m=73 finite stock.

The shape note substitutes bit length 2642 into a log_q composition slot.
On every integer q > 2^80 the same stock satisfies the log_q inequality with
B = 34, and B = 33 fails at the proved prime q = 2^80 + 13.
"""

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent

SHAPE = "research/selected-stock-shape-a-zero/PROOF.md"
COARSE = "research/selected-coarse-depth-stock/PROOF.md"
M73 = "research/selected-stock-envelope-m73/README.md"

F_COFACTOR = 8908647580887961
Q_WITNESS = (1 << 80) + 13


def fail(message):
    raise SystemExit("FAIL_LOGQ_STOCK_SHAPE_GAP " + message)


def need(condition, message):
    if not condition:
        fail(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pins():
    sources = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    pinned = {}
    for row in sources["files"]:
        if row["usage"] != "input":
            continue
        path = ROOT / row["path"]
        digest = sha256(path)
        need(digest == row["sha256"], "sha256 mismatch " + row["path"])
        pinned[row["path"]] = path.read_text(encoding="utf-8")
    return pinned


def trial_prime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    divisor = 3
    limit = math.isqrt(number)
    while divisor <= limit:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def pocklington(number, multiplicity, witness, proved):
    """Complete factorization of number-1, one witness for every prime factor."""
    product = 1
    distinct = []
    for prime, power in multiplicity:
        if prime not in proved:
            need(trial_prime(prime), "unproved factor " + str(prime))
            proved.add(prime)
        need(power > 0, "bad power")
        product *= prime ** power
        if prime not in distinct:
            distinct.append(prime)
    need(product == number - 1, "factorization does not rebuild n-1")
    need(product * product >= number, "factored part is below sqrt(n)")
    need(pow(witness, number - 1, number) == 1, "Fermat witness failed")
    for prime in distinct:
        residue = pow(witness, (number - 1) // prime, number)
        need(0 < residue < number, "zero residue")
        need(math.gcd(residue - 1, number) == 1, "Pocklington gcd failed for " + str(prime))
    proved.add(number)
    return True


def symplectic_order(rank_parameter):
    order = 1 << (rank_parameter * rank_parameter)
    for index in range(1, rank_parameter + 1):
        order *= (1 << (2 * index)) - 1
    return order


def stock_integer():
    families = 14336 + 480 + 8 + 2
    need(families == 14826, "family split")
    return symplectic_order(36) * families


def prove_primes():
    proved = set()
    for prime in (2, 3, 5, 3529, 69467, 302831, 1093, 31039):
        need(trial_prime(prime), "trial prime failed " + str(prime))
        proved.add(prime)
    cofactor_factors = ((2, 3), (3, 1), (5, 1), (3529, 1), (69467, 1), (302831, 1))
    need(pocklington(F_COFACTOR, cofactor_factors, 29, proved), "cofactor primality")
    witness_factors = ((2, 2), (1093, 1), (31039, 1), (F_COFACTOR, 1))
    need(pocklington(Q_WITNESS, witness_factors, 2, proved), "witness primality")


def evaluate():
    pinned = load_pins()
    need("sigma <= (43/26) * (1 - s) * 2642 + rho" in pinned[SHAPE],
         "shape composition sentence missing")
    need("log_q C(w)<=A*w+B" in pinned[COARSE], "coarse log_q slot missing")
    need("2^1296 * prod_{j=1..36} (2^(2j) - 1)" in pinned[M73], "symplectic formula missing")
    order = symplectic_order(36)
    need(order.bit_length() == 2628, "order bit length")
    stock = stock_integer()
    need(stock.bit_length() == 2642, "product bit length")
    need(1 << 2641 <= stock < 1 << 2642, "log2 band")
    prove_primes()
    floor_q = 1 << 80
    need((floor_q + 1) ** 34 > stock, "B=34 fails just above 2^80")
    need(Q_WITNESS ** 33 < stock <= Q_WITNESS ** 34, "witness exponent bracket")
    # Every integer q > 2^80 is at least 2^80+1, so q^34 is larger still.
    need(math.gcd(2642, 34) == 2, "ratio reduction")
    need(2642 // 2 == 1321 and 34 // 2 == 17, "1321/17")
    return {
        "stock_bit_length": 2642,
        "log2_band": [2641, 2642],
        "log_q_coefficient_sufficient": 34,
        "log_q_coefficient_failure": 33,
        "witness_prime": str(Q_WITNESS),
        "bit_length_plug_in": 2642,
        "plug_in_over_sufficient": "1321/17",
        "rho": "unbound",
        "new_kappa": False,
    }


def main():
    receipt = evaluate()
    need(receipt["log_q_coefficient_sufficient"] == 34, "receipt")
    print(
        "PASS_LOGQ_STOCK_SHAPE_GAP "
        "C_bits=2642 log_q_B=34 bit_plug_in=2642 "
        "witness=2^80+13 ratio=1321/17 rho=unbound no_new_kappa"
    )
    result_path = PACKAGE / "RESULT.json"
    if result_path.exists():
        recorded = json.loads(result_path.read_text(encoding="utf-8"))
        need(recorded == receipt, "RESULT.json drift")


if __name__ == "__main__":
    main()
