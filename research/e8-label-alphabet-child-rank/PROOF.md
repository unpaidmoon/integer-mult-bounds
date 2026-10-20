# Support-pairing rank on the fixed E8 label alphabet

## Alphabet

Take the 240 roots of E8 in doubled coordinates: the vectors with two coordinates
`±2` and the rest `0`, and the vectors in `{±1}^8` with an even number of minus
signs. A line is an unordered pair `{r, −r}`. There are 120 lines. The same
enumeration, and the same inner product `dot/4`, is the adapter in
`research/complex-frame-pair-decoders/verify.py`.

The label pairing of lines `i` and `j` is `(⟨ℓ_i, ℓ_j⟩ + 1) mod 2`. A decoder
term with row support `A` and column support `B` costs the rank over `F_2` of
that pairing restricted to `A × B`. This is the term cost in that package, not
a new cost model.

## Rank is exactly 9

Let `N` be the `120 × 120` pairing matrix. Gaussian elimination on its rows
produces nine pivots, and every row reduces to zero against that basis. So
`rank N = 9`, and every row lies in a fixed 9-dimensional space.

Any term support is a submatrix of `N`. The rows of a submatrix are projections
of vectors from a 9-dimensional space, so the submatrix has rank at most 9.
No term on this alphabet costs more than 9.

The bound is sharp for a single support. The nine lines

```text
e1+e2, e1−e2, e1+e3, e1+e4, e1+e5, e1+e6, e1+e7, e1+e8,
(1/2)(e1+···+e8)
```

written in doubled coordinates as the verifier's witness lines
`0, 1, 2, 4, 6, 8, 10, 12, 56`, have pairing submatrix of rank 9. Deleting any
one of them drops that minor to rank 8. This minor is an algebraic support. It
is not a claim that an eight-term all-pairs decoder, or the selected word, uses
a rank-9 term.

A one-bit row outside the 120 columns has rank 10 against `N`. The rank routine
can see a larger matrix; the alphabet itself does not contain one.

## What this says about child rank

In the selected complex profile, the eight rank-8 local children are the shape
of eight costly pairing terms. On this alphabet a pairing term cannot be a
child of rank 10 or more, and rank 9 is the largest such term. A block climb
that leaves the alphabet, including the product-root frames of PR #3895, is not
a term of this pairing.

This does not bound a different object: a recursive child made by grouping
rank-1 scalar payload into one wider call. That child need not be a
support-pairing term. PR #3039 and `research/mixed-block-climb-overhead` price
charged groups of that kind. They are outside this rank.

## Screen at the alphabet cap

The selected per-call local profile, split from the pinned assembly and idle
ledger by the same identity as `research/complex-local-word-ceiling`, is

```text
{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8},
```

mass `5586`, maximum rank 8. The coverage check is `mass = 72W + 64N` on the
pinned complex profile.

At `a = 1/99` the pinned `child_cost` enclosures satisfy

```text
up(c(9)/9) < down(c(s)/s)    for every s = 1..8.
```

Cost per unit of paid mass therefore falls as the rank rises, up through 9.
Among profiles that spend local mass `5586` only on ranks at most 9, the moment
is minimized by the fractional shape `{9: 5586/9}`, with idle mass left at the
halving cap `R = 51`. Its relaxation at `a = 1/99` has lower enclosure strictly
above 1. Every other same-mass shape with ranks at most 9 is at least that
large. The integer shape `{9:620, 6:1}` is one of them; its ceiling is also
below `1/99`.

The same calculator puts the pure fractional cap-43 ceiling below `1/99` and
the pure cap-44 ceiling above it. Rank 9 is on the failing side of that
threshold. Copies, frames and restoration are not given a zero price here.
They are nonnegative charges, so they cannot pull a moment that is already
above 1 back under 1.

The ideal rank-9 ceiling is the fraction `1443139659/500000000000`. The
planning cap `a/(1+a)` at that upper endpoint is `1443139659/501443139659`,
about `0.002878`, above the selected `836330098538459/500000000000000000` and
below `1/99`. This is not a new selected exponent.

## Controls

The verifier rejects a witness whose minor is not rank 9, a witness line whose
doubled coordinates move, a selected local profile other than the one above, an
ideal rank-9 moment that does not exceed 1 at `a = 1/99`, and a pure rank-44
shape that has already exhausted its relaxation at that target. A rank-10
extension of the pairing is accepted by the rank routine and rejected as a
member of the label span.
