# Cut58 local-16 native floor

**Partial lower bound, superseded for sharpness.** PR #4086 (head
`cd0f22abce2b74d7d080a2e640c0f495d3d2c3aa`) already proves that the q2 event58
separable suffix costs at least `22f` for every `f ≥ 2`, and that the existing
word attains `22f`. A suffix of `16f` is impossible in that class, and there is
no open gap between 20 and 22.

This package gives a weaker independent count: with paid natives restricted to
`K`, `T`, `W` and their inverses, the native mass is at least **20**. That
already excludes 16. It misses the third `K`, which #4086 charges through the
`chi_KW` defect. The mass-22 neutral rewrite is replayed here. No new κ.
Selected κ stays `0.001672660197076918`.

## Scope and evidence

Card `joint-query-controller`, scope **changed**. The card asks for a literal
producer magnitude ledger. Discussion #1166 comment 19039339, quoting PR
#4082, left a local16 suffix open. PR #4086 later closed that target at a sharp
`22f`. A later address-swap menu prices the rank-0 source swap `P` and does not
undercut `22f`. This package does not reopen either result.

[PROOF.md](PROOF.md) is the argument. `verify.py` checks the finite facts it
uses: the pool splits into 128 even monomials and their `T` translates, `T` is
central, the output entry `-KWK T` lies outside the one-`K` bimodule, `K` and
`T` never create `W`'s address rows, the low-bit phase map is a representation
of all 128 even monomials, and the six even cores have representation rank 96
on bits 0-3 (a five-generator factorization would have rank at most 80). It also replays the mass-22 neutral gate list and checks that it equals
`T` on those cores. The resulting count is `6·2 + 2·2 + 4 = 20`, strictly
weaker than the sharp `22f` tariff.

The operators in [operators.json](operators.json) are the `K`, `T`, and `W`
monomials from PR #4082 head `ff277e8a958829954f371c85bdc447672266edbd`, file
`research/coupled-tail-support-floor/source/early-cut58-planning/CUT58.json`.
That head is not an object of this checkout, so there is no Git pin. The
verifier checks SHA-256 `057a8d5de8c64e63d37db78b26d83164fe1b64d71ce322b1d2cecadcccffd079`
of the vendored JSON. The monomial multiplication is the predecessor's
quadratic-chart rule, trimmed in [monomials.py](monomials.py).

Rank-0 fresh-plane swaps are outside this gate set. The mass-22 replay does
not use them. Owners, scans, and a supplier moment are not priced.

## Reproduce

```sh
python3.12 -B scripts/research_package.py --package research/cut58-local16-native-floor
```

Expected marker:

```text
PASS_CUT58_LOCAL16_NATIVE_FLOOR lower_bound=20 replayed_rewrite=22 target16=impossible_by_this_bound sharp_floor_not_reproved=pr4086 fresh_queries=6 k_queries=2 w_queries=1 group=256 no_new_kappa
```

## Open next questions

None justified from this package. The sharp separable tariff is PR #4086, and
the source ADDRESS swap was priced afterward without lowering `22f`. A new
adapter would be a different premise, not a tightening of this 20-count.

## Credit

The entrance, the matrix, the mass-22 rewrite, and the open local16 target are
Ross Richardson's, PR #4082, with the caller-run lineage in discussion #3606.
The quadratic-chart multiplication is from that package's pinned chart code.
Prepared by unpaidmoon with substantial Cursor Grok 4.7 assistance. Apache-2.0.
No independent human review is claimed.
