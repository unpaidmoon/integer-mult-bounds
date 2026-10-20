# Cut58 local-16 native floor

**Negative result.** On the q2 event58 six-bank suffix, any circuit whose paid
natives are the selected operators `K`, `T`, `W` and their inverses has native
mass at least **20**. The hypothetical suffix of mass 16, which would put the
whole word at 70 against stock 72, is impossible. The predecessor's neutral
rewrite still has mass 22, and that gate list is replayed here. No new κ.
Selected κ stays `0.001672660197076918`.

## Scope and evidence

Card `joint-query-controller`, scope **changed**. The card asks for a literal
producer magnitude ledger. This package instead answers the still-open local16
target in discussion #1166 comment 19039339, recorded by PR #4082's cut58
appendix. The predecessor leaves prefix 54, suffix 22, total 76, stock 72, and
says a suffix of 16 is not constructed or excluded. Its own note says that the
matrix rank being 6 does not exclude 16.

[PROOF.md](PROOF.md) is the argument. `verify.py` checks the finite facts it
uses: the pool splits into 128 even monomials and their `T` translates, `T` is
central, the output entry `-KWK T` lies outside the one-`K` bimodule, `K` and
`T` never create `W`'s address rows, the low-bit phase map is a representation
of all 128 even monomials, and the six even cores have representation rank 96
on bits 0-3 (a five-generator factorization would have rank at most 80). It also replays the mass-22 neutral gate list and checks that it equals
`T` on those cores. The resulting floor is `6·2 + 2·2 + 4 = 20`.

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
PASS_CUT58_LOCAL16_NATIVE_FLOOR minimum=20 target16=impossible upper=22 fresh_queries=6 k_queries=2 w_queries=1 group=256 no_new_kappa
```

## Open next questions

Is the selected-pool minimum 20 or 22? The floor uses two `K` queries. The
replayed circuit uses three: one on `a`, one on `z`, and one outside `W`. A
six-bank circuit with only two `K` queries, six `T` queries, and one `W` would
match the floor.

## Credit

The entrance, the matrix, the mass-22 rewrite, and the open local16 target are
Ross Richardson's, PR #4082, with the caller-run lineage in discussion #3606.
The quadratic-chart multiplication is from that package's pinned chart code.
Prepared by unpaidmoon with substantial Cursor Grok 4.7 assistance. Apache-2.0.
No independent human review is claimed.
