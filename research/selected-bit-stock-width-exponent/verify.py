#!/usr/bin/env python3
"""Selected BIT stock width exponent at the #4470 joint-helper producer.

The selected ordinary BIT interface uses atom s = 1/250. Borrowed digits stay
O(w log e) for w = ceil(e^s). The inherited outer guard beta*(1 - 3/1000)
matches a different exponent, and that exponent fails the adapter test.
No new kappa is claimed.
"""
import hashlib
import json
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

S = Fraction(1, 250)
REJECTED = Fraction(3, 1000)
C1 = Fraction(69, 20000)
A_OLD = Fraction("0.0000384599")
ADMITTED = Fraction(17, 5000)
KAPPA = Fraction(60403, 20000000)
TESTED = Fraction(604031, 200000000)


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def read(rel):
    with open(os.path.join(ROOT, rel), "rb") as handle:
        return handle.read()


def load_json(rel):
    return json.loads(read(rel).decode("utf-8"))


def check_pins():
    sources = load_json(os.path.join(HERE, "SOURCES.json"))
    require(sources["base_commit"] == "fbc9ea0249746acca4f504d4fda2b84e0e36cf0d",
            "base commit")
    for row in sources["files"]:
        if row["usage"] != "input":
            continue
        digest = hashlib.sha256(read(row["path"])).hexdigest()
        require(digest == row["sha256"], "sha256 " + row["path"])


def ordinary_saving(atom):
    return (1 - atom) * C1 + atom * A_OLD


def slacks(atom, saving):
    return atom - saving, 1 - saving - atom


def beta():
    gap = (TESTED - KAPPA) / 7
    require(gap == Fraction(1, 1400000000), "compiler gap")
    return 1 - 3 * gap


def certificate(atom=S):
    """Return the exact stock identities for one candidate atom."""
    saving = ordinary_saving(atom)
    adapter, absorption = slacks(atom, saving)
    group = beta()
    return {
        "atom": atom,
        "ordinary": saving,
        "adapter": adapter,
        "absorption": absorption,
        "beta": group,
        "guard": group * (1 - atom),
    }


def main():
    check_pins()
    selected = load_json("certificates/selected-result.json")
    receipt = load_json("research/joint-helper-lattice/RESULT.json")
    source = load_json("research/query-thinned-controllers/RESULT.json")
    require(selected["kappa"] == str(KAPPA), "selected kappa")
    require(selected["source_certificate"] == "research/joint-helper-lattice/RESULT.json",
            "selected certificate path")
    require(4470 in selected["source_prs"], "selected source pr")
    require(receipt["kappa"] == str(KAPPA), "receipt kappa")
    require(receipt["ordinary_BIT"] == source["ordinary_BIT"], "rechecked BIT interface")
    bit = receipt["ordinary_BIT"]
    require(Fraction(bit["atom"]) == S, "receipt atom")
    require(Fraction(bit["after_cover"]) == C1, "receipt cover")
    require(Fraction(bit["admitted"]) == ADMITTED, "receipt admitted saving")
    require(Fraction(bit["ordinary_saving"]) == ordinary_saving(S), "receipt ordinary saving")

    joint_proof = read("research/joint-helper-lattice/PROOF.md").decode("utf-8")
    source_proof = read("research/query-thinned-controllers/PROOF.md").decode("utf-8")
    endpoint = read("research/pr4359-p7-padding/dependencies/compiler-refill/endpoint.py").decode("utf-8")
    checker = read("research/joint-helper-lattice/verify.py").decode("utf-8")
    require("atom exponent 0.004" in joint_proof, "selected proof atom sentence")
    require("w=ceil(e^0.004)" in source_proof, "width rule")
    require("The old delta=0.003 fails" in source_proof, "rejected atom sentence")
    require("beta*(1-Q(3, 1000))" in endpoint, "inherited guard formula")
    require("actual_new_BIT_stock_sublinear']=params['beta']*(1-atom)" in checker,
            "selected guard assignment")

    fact = certificate()
    rejected = certificate(REJECTED)
    recorded = receipt["outer"]["functional_checks"]
    parameters = receipt["outer"]["parameters"]
    require(Fraction(parameters["beta"]) == fact["beta"], "receipt beta")
    require(Fraction(parameters["d"]) == Fraction(1, 1400000000), "receipt gap")
    require(Fraction(recorded["actual_new_BIT_stock_sublinear"]) == fact["guard"],
            "selected guard value")
    require(Fraction(recorded["new_BIT_row_stock_sublinear_in_active_group"]) == rejected["guard"],
            "inherited guard value")
    require(fact["adapter"] > 0 and fact["absorption"] > 0, "selected atom fits both tests")
    require(fact["ordinary"] > ADMITTED, "ordinary saving clears the admitted BIT saving")
    require(rejected["adapter"] < 0, "rejected exponent fails the adapter test")
    require(rejected["absorption"] > 0, "rejected exponent is still sublinear")
    require(rejected["guard"] > fact["guard"] > 0, "inherited guard is the looser positive value")
    require(fact["ordinary"] == Fraction(8590884599, 2500000000000), "reduced ordinary saving")
    require(fact["adapter"] == Fraction(1409115401, 2500000000000), "reduced adapter slack")
    require(fact["absorption"] == Fraction(2481409115401, 2500000000000), "reduced absorption slack")
    # The m=73 envelope coefficient is a different object and stays unset here.
    require("actual_stock_coefficient" not in receipt, "no m=73 coefficient field is filled")
    print(
        "PASS_SELECTED_BIT_STOCK_WIDTH"
        " exponent=1/250"
        " ordinary=8590884599/2500000000000"
        " adapter=1409115401/2500000000000"
        " slack=2481409115401/2500000000000"
        " rejected_atom=3/1000"
        " inherited_guard=1395799997009/1400000000000"
        " selected_guard=348599999253/350000000000"
        " no_new_kappa"
    )


if __name__ == "__main__":
    main()
