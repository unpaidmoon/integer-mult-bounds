# The fixed E8 label alphabet stops at pairing rank 9

**Negative screen. No new κ.** Selected κ stays `836330098538459/500000000000000000`.

Discussion #1166 comment 19021222 asks for the largest child rank a physical
local word on the selected template can emit, for one fixed support alphabet.
This package takes the E8 label alphabet already used by the frame-pair
decoder: 120 lines, pairing `(⟨ℓ_i, ℓ_j⟩ + 1) mod 2`. It does not build a
block-climb word.

## Result

Every support-pairing term on this alphabet has `F_2` rank at most 9, and 9 is
attained. The `120 × 120` pairing has rank 9, so every submatrix does too. The
nine lines

```text
e1±e2, e1+e3, …, e1+e8, (1/2)(e1+···+e8)
```

(witness indices `0, 1, 2, 4, 6, 8, 10, 12, 56` in doubled coordinates) have a
rank-9 principal minor. Deleting any one line drops it to 8.

The selected per-call local profile, read from the pinned assembly, is
`{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}` (mass 5586, maximum rank 8). At
`a = 1/99`, cost per unit of paid mass is strictly decreasing from rank 1
through rank 9 in the pinned ceiling enclosures. The cheapest same-mass shape
whose children have pairing rank at most 9 is therefore the fractional profile
`{9: 5586/9}`, with idle mass at the halving cap 51 and with no frame or
restoration charge. Its relaxation at `a = 1/99` lies strictly above 1. The
ceiling bracket ends at `1443139659/500000000000`, below `1/99`. The integer
shape `{9:620, 6:1}` fails the same way.

In this same calculator the pure fractional cap 43 still fails `a = 1/99` and
the pure cap 44 still clears it. Rank 9 is on the failing side of that
threshold. Nonnegative copy, frame and restoration charges cannot repair a
moment that is already above 1.

The argument is in `PROOF.md`. The rank-9 minor is an algebraic support, not a
hosted decoder term and not a supplier.

## What this does not bound

A recursive child formed by grouping rank-1 scalar payload into one wider call
is not a support-pairing term. PR #3039 and
`research/mixed-block-climb-overhead` price charged groups of that kind; a
zero-transport group is not ruled out here. PR #3895 reaches pairing rank 16
by tensoring two roots into a larger ambient space. That is a different
alphabet. Neither route is given a new κ.

## Reproduce

From the repository root, Python 3.12, standard library only:

```sh
python3.12 -B research/e8-label-alphabet-child-rank/verify.py
python3.12 -B scripts/research_package.py --package research/e8-label-alphabet-child-rank
```

Expected marker:

```text
PASS_E8_LABEL_ALPHABET_CHILD_RANK pairing_rank=9 ideal_ceiling=1443139659/500000000000 below_1/99 cap44_clears selected_max_rank=8 no_new_kappa
```

The run is a few seconds. `--write` regenerates `RESULT.json`.

## Open next questions

1. Can one zero-transport grouping of the 2412 rank-1 local children emit a
   recursive child of rank at least 44, with copies, frames and restoration
   counted? The first step is one source-bound itinerary and its child-rank
   inventory. The blocker is that this package only caps support-pairing terms.
   A charged transport is already the wrong side of the PR #3039 test for
   `a ≤ 1/99`; a free grouping is not given that price.

2. Does any legal decoder identity on this same alphabet use a rank-9 term, or
   do the eight-term and masked hypotheses keep every costly term at rank at
   most 8? The first step is one admissible support whose pairing minor has
   rank 9 inside a stated term budget. The blocker is that the witness above
   is only a minor, not a hosted term.

## Credit

The root enumeration and pairing formula are the PR717 adapter retained in
`research/complex-frame-pair-decoders` (themilkman216, and the complex extension
recorded in the decoder scope map). The ceiling enclosures and the selected
local-profile split are Douglas Colkitt's
`research/complex-local-word-ceiling`, with Claude assistance. The rank-cap
threshold that makes rank 9 the wrong side of `a = 1/99` was measured for the
fractional and joint-integer packings in open PRs #3701 and #3811; this
package recomputes the pure fractional caps 43 and 44 in the pinned ceiling
engine instead of importing those trees. PR #3895 records the rank-16 climb
that leaves this alphabet.

Prepared by unpaidmoon with substantial Cursor Grok assistance. No independent
human or formal-kernel review is claimed. Apache-2.0.
