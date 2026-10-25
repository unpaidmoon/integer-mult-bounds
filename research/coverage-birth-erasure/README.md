# Erasing the line birth does not create a second unpaid coordinate

**Scoped obstruction. No new κ. The selected record is unchanged.**

Original card: `coverage-law-change`. The question answered here is open question 1
of [three-bank-restored-unpaid](../three-bank-restored-unpaid/README.md): can a
non-nested three-bank schedule erase the initial direction, rewrite it, and
leave two unpaid coordinates without becoming a plane port? Scope status is
**refined**. The card, the reason, and the bottleneck link are in [TASK.json](TASK.json).

## Result

No. For any finite sequence of subspaces `A_0, ..., A_t`, both of the counts
below are at most `dim(A_0)`:

- the surviving-birth count `dim(A_0 ∩ ... ∩ A_t)`, the extension of the nested
  unpaid count that still equals the initial dimension on a nested chain;
- the naive endpoint count `dim(A_0 ∩ A_t)`.

A one-dimensional birth, the selected `C_q` line, therefore never contributes
two unpaid coordinates. A second surviving direction would have to lie in that
line. The proof is the step lemma and the paid-rank induction in [PROOF.md](PROOF.md).

On the selected width `m = 73` the explicit erasure is `⟨e_0⟩`, then `⟨e_1⟩`,
then the whole space. The surviving-birth count is 0. The naive intersection
is 1, because `e_0` is rewritten into the endpoint. The dimension charge is
`2 + 72 = 74`, at least `73`. The nested climb `⟨e_0⟩ → F_2^73` still pays 72
and keeps unpaid count 1, which is the `72W` term of the coverage identity.
A side bank `⟨e_1, e_2⟩` inserted into the family history drops the surviving
birth to 0. Leaving that bank off the family frame keeps unpaid count 1.

Two unpaid coordinates do occur when the birth itself is the plane `⟨e_0, e_1⟩`.
That is the plane-port contract already screened by
[plane-port-copy-budgets](../plane-port-copy-budgets/README.md), not an erasure
of the selected line. This package does not reprice it.

The nested case of `rank(A, B) = dim(A + B) - dim(A ∩ B)` is the Fourier-rank
sentence in
[INHERITED-COMPLEX-GEOMETRY.txt](../split-centres-global/proofs/INHERITED-COMPLEX-GEOMETRY.txt).
The same formula is the charge used off that hypothesis. It is not a compiler
theorem for non-nested steps. A cheaper physical step would be a different
acquisition cost. It would not raise either intersection count above
`dim(A_0)`.

## Checks

`verify.py` enumerates every subspace history of length 3 on `F_2^3` (4096
histories, 16 subspaces) and every length-3 history on `F_2^4` whose birth is
a line (67335 histories, 15 lines, 67 subspaces). The maximum line-birth unpaid
count is 1. It also checks the step lemma for every host, every subspace of
that host, and every next frame: 1056 triples on `F_2^3` and 34371 on `F_2^4`.
There are 385 length-3 histories on `F_2^3`, and 12240 line histories on
`F_2^4`, where the naive endpoint intersection is strictly larger than the
surviving-birth count. Four hundred random length-6 histories on `F_2^8` obey
the same inequalities. Rejection controls: the explicit erasure is not counted
as unpaid 2, and a cleared source is not nested.

## Limitations

This is a dimension ledger for subspace histories. It does not replay Clifford
phases, the 946 local frames, or a native tape. It does not change the selected
frontier. The selected κ on this base is `605457647/200000000000`; it is
provenance only and is not an input of the checker.

## Reproduce

From the repository root, Python 3.12, standard library only:

```sh
python3 -B research/coverage-birth-erasure/verify.py
python3 scripts/research_package.py --package research/coverage-birth-erasure --check-only
python3.12 scripts/research_package.py --package research/coverage-birth-erasure
```

`verify.py` prints

`PASS_COVERAGE_BIRTH_ERASURE line_unpaid_at_most_1=true erasure_creates_second_unpaid=false no_new_kappa`

and checks [RESULT.json](RESULT.json) against a fresh run. Pins are in
[SOURCES.json](SOURCES.json).

## Open next questions

1. **Does any checked non-nested compiler step have Fourier rank strictly below `dim(A+B) - dim(A∩B)`?**
   The unpaid bound does not need that formula. The paid-rank lower bound does.
   A cheaper physical step would be an acquisition saving, not a second unpaid
   coordinate. First step: compare one directed transition in the geometry
   note's 3120 used transitions with this dimension formula. Blocker: this
   package does not replay `clifford_exact.py`.

2. **At the current selected κ, does the existing plane-port copy budget still
   fail the complex word?**
   That birth is the remaining way to get unpaid count 2 inside this ledger.
   First step: rerun the pinned plane-port budget at
   `κ = 605457647/200000000000`. Blocker: the budget package pins an older
   selected record, and this package does not reprice ceilings.

## Credit

- The erasure question and the nested third-bank obstruction are
  [three-bank-restored-unpaid](../three-bank-restored-unpaid/README.md),
  prepared by unpaidmoon with substantial Cursor Grok assistance.
- The third-bank question was left by themilkman216,
  [multipair-schedule-bound](../multipair-schedule-bound/README.md).
- The nested Fourier-rank sentence and `m = 73` are the inherited complex
  geometry note above.
- Plane-port copy budgets are a separate contract and are not recomputed.
- The selected record is historical provenance at base
  `32890bc5de034ab8fc93ac88ead7279a6a416d04`.

Prepared by unpaidmoon with substantial Cursor Grok assistance for the ledger
proof, the finite census, and the package text. New work is Apache-2.0.
