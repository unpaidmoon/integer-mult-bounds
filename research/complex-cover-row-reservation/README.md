# Common-cover row reservation in #4100

**Negative result on one displayed formula. No new κ.** The selected frontier
stays `0.00302015`. #4100 is not accepted.

## Scope and evidence

Card `uniform-transfer-audit`, scope **refined**. The card asks for one
quantified implication of the proposed all-size construction at its actual
caller. This package takes the complete-cover execution named in
`AUDIT.md`: the row-bit reservation in `COMPLEX.md`, section "Common cover,
fresh rows and fixed tapes."

`COMPLEX.md` sets `W = 322560` and

```text
Gamma = 2^1296 * product_{i=1}^{36}(2^{2i}-1),
```

calls `Gamma` the order of `O(73,2)`, reserves `q = ceil(log2(N))` row bits for
`N = (W Gamma)^{D(h)}`, and pads to

```text
R = ceil(2^q / N) * N,
```

"a factor less than two."

For every integer `D >= 1`, `N` is not a power of two. The displayed `R` equals
`2N`, so the factor is 2, and `R` is strictly larger than the `2^q` reserved
addresses. Replacing `ceil` by `floor` leaves exactly one copy of `N` inside
those addresses, and the reservation factor `2^q/N` lies in `(1, 2)`. Holding
the written `2N` addresses would take one extra bit. Either repair stays in the
same `O(D log(W Gamma))` bit budget. The sentence as written does not.

The order claim is the other half of the same sentences, and it holds.
`Gamma` equals the order of the standard dot-product orthogonal group on
`F_2^{73}`: the all-ones vector has norm 1, its perpendicular space is
symplectic of dimension 72, and counting hyperbolic pairs gives
`|Sp(72,2)| = Gamma`. The integer has 2628 bits. The depth recurrence in the
same paragraph does decrease on every rank-`r <= 48` child, and two maximum-rank
steps halve the width.

The proof is `PROOF.md`. `verify.py` binds the audited sentences, checks the
2-adic failure for `D = 1..4`, enumerates the dot-product and perpendicular
groups at dimensions 1, 3 and 5, and checks the depth inequalities through
width `100000`.

This is not the free-word cancellation in #4184, the rank-`r f` moment sign in
#4375, the common-grid height defect in #4178, or the BIT.md stock audit in
#4432.

## Reproduce

From the repository root, with Python 3.12:

```sh
python3 -B research/complex-cover-row-reservation/verify.py
python3 -B scripts/research_package.py --package research/complex-cover-row-reservation
```

Expected verifier line:

```text
PASS_COMPLEX_COVER_ROW_RESERVATION gamma_bits=2628 gamma_sha256=50b58aaac98e621e9917d6c3bced5e276398b68918bbd57ac8d784d3d58db00b written_factor=2 written_fits=false repair_copy=1 repair_factor_lt_2=true depth_halves=true dot_orders=1,6,720 no_new_kappa
```

Pins are in `SOURCES.json`. Base `fbc9ea0249746acca4f504d4fda2b84e0e36cf0d`.
The audited `COMPLEX.md` blob is also the blob at retained head
`337d04939571a637aeab54a0f58f54fde811663a`.

## Open next questions

1. Once the fitting stock is the single copy `N`, do the depth-first parked
   ancestor volumes still form a geometric series bounded by a constant times
   the child payload `V/(W Gamma)`? The time section charges parking inside
   `O(V e^{1-a2} polylog(p))`. The first step is to write the parked volume at
   depth `k` from the product split into `W` families, one `Gamma` cover, and
   the remaining stock. This package does not replay the four provider words
   or the tape schedule.
2. `Gamma` is a finite cardinality, not an executed transversal. A constructive
   cover still needs an encoder that turns one symplectic basis of the
   72-dimensional perpendicular space into the fixed control `COMPLEX.md`
   allows. The integer has 2628 bits, so listing the group is not a next step.

## Credit

The construction and the audited sentences are Cinna Davis's #4100, with
OpenAI Codex assistance. The coverage map that left this execution unaudited
is Ryanson Jonathan's #4311. #4184 (ToikY), #4178 (Jose Manuel), #4375, and
#4432 (Mark / Matarener) are neighbouring audits of different sentences.
Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
