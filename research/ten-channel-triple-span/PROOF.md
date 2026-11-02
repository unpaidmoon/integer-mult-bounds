# Three low-grade frames do not meet the clean mode

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
This is a scoped exact certificate. It is not independent human review, a
supplier admission, or a change to the selected frontier
κ = 781451/250000000.

## 1. Contract

Fix the source, canonical ground-to-frame delivery, immutable original-mode
payloads and common-fixed-vector scalar quotient used by Ali Romman's
nine-channel certificate in `research/nine-channel-monotone-bound`, which
audits the PR #5745 delivery claim on the PR #5720 word. The original mode
matrix R satisfies RR^T = 56 I_8. For each frame g of transport grade below
8, S_g is the span over Q of its endpoint impulse responses. D is the
eight-dimensional clean-mode subspace. The nine-channel argument shows that
(S_g + S_h) ∩ D = {0} for every such pair, and therefore every completion
with at most nine channels costs at least 8 H_8 under any positive
nondecreasing canonical transport tariff. Its abstract ten-channel control
uses three low-grade responses whose pairwise sums miss D while the triple
sum meets D. This package decides whether that pattern occurs on the source.

Write γ for the smallest number of grade-below-8 frames whose response
spaces sum to a subspace meeting D. The pair theorem is γ ≥ 3. A positive
nondecreasing ten-channel bound of 8 H_8 would follow from γ ≥ 11 by the
same rank count, because a kernel vector supported only on low-grade
channels would then need at least 11 channels. This package does not prove
that inequality.

## 2. Census

The verifier replays the all-event orthogonal census. It does not import the
predecessor program. It checks 15,752 nonzero low-frame contacts, 14,816
distinct frame/column pairs, 12,240 projected columns and 879 frames. No
individual basis acquires a mode pivot, so S_g ∩ D = {0} and the nuisance
projection is injective on each S_g. The response dimensions are

| Dimension | 1 | 2 | 3 | 4 | 5 | 8 | 24 | 28 | 50 | 112 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frames | 119 | 480 | 136 | 116 | 1 | 23 | 1 | 1 | 1 | 1 |

Those bases have 2,354 rows and use 274 nuisance coordinates. Every
denominator is at most 629.

## 3. An explicit 41-frame relation

Restrict to the 119 dimension-1 frames. Their nuisance images have rank 105,
so the relation space has dimension 14. Its reduced basis has pivots

    (0, 6, 12, 1, 2, 3, 4, 5, 17, 13, 19, 18, 35, 23).

The coefficient vector

    (0, -1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0)

has frame support 41 and clean mode (0, 0, 0, 0, 14, -14, -14, 14). The
verifier rebuilds that combination from the original generators and checks
that every nuisance coordinate cancels. Therefore γ ≤ 41.

## 4. No triple meets D

### Leading coordinates

Suppose a nonzero nuisance vector lies in two images. In either RREF its
leading coordinate is a pivot, so the pivot sets meet. Equivalently, frames
with disjoint pivot sets have trivial nuisance intersection. There are
280,364 unordered pairs that do share a pivot. The verifier retains a pair
only when the stacked nuisance rank over Q is strictly smaller than the sum
of the dimensions and the stacked space does not meet D. Exactly 3,782 pairs
survive. Every pair that meets in nuisance is therefore mode-free, which
reproves the pair theorem on the pairs that need an explicit reduction.
Disjoint-pivot pairs are covered by the leading-coordinate lemma; forty
uniform samples are an additional control, not the proof.

### Nonzero minors

Work in F_631. The prime is larger than every denominator, so each basis
entry reduces. A square minor that is nonzero modulo 631 is nonzero over Q,
and those rows are linearly independent over Q.

### Frames of dimension at most 5

There are 852 such frames and 102,715,700 triples. For each triple the
verifier forms two disjoint random projections of order equal to the total
dimension, with the fixed seed 20261030. A nonzero determinant rejects the
triple. If both vanish and the triple contains none of the 3,782 pairs, a
full row rank modulo 631 also rejects it, because that rank is a lower bound
on the rational rank. Only a genuinely rank-deficient matrix is reduced over
Q, and that reduction is required not to meet D. Triples that contain one of
those pairs are certified in the extension step.

### Frames of dimension at least 8

Every remaining triple has a unique frame of largest dimension, breaking
ties by the greatest frame index. Reduce the other rows against that frame's
RREF modulo 631. If the two companions leave a residual of full companion
rank, the triple has full nuisance rank and no kernel. Full residual rank is
certified by a nonzero minor or, above order 40, by a direct modular rank.
Vanishing residuals that do not contain a known intersecting pair are
reduced exactly over Q.

### Extensions

For each of the 3,782 pairs, let ι be its exact nullity. The modular rank of
the pair equals its exact rank. Every third frame is reduced against the
pair. A residual of order equal to the third dimension proves that the
triple kernel has dimension exactly ι, hence equals the pair kernel, which
has mode zero. The verifier applies that reduction in a fixed 128-column
projection (seed 20261031) and treats a nonzero minor as full residual rank.
A modular residual rank equal to the third dimension is the same certificate
and is computed on the unprojected residual rows whenever the minor vanishes.
Only a residual that stays short modulo 631 is reduced over Q, and that
reduction is required not to meet D.

These three passes cover every unordered triple once in the direct sweep and
every intersecting-pair extension in the last pass. Disjoint batches of one
pass may run concurrently. The verifier requires the recorded batch sizes to
add up to every unordered triple and every intersecting-pair extension, so a
batch is not a sample. No clean triple remains, so γ ≥ 4.

## 5. Consequence and boundary

Thus 4 ≤ γ ≤ 41. Three low-grade channels cannot reproduce the abstract
ten-channel control on this source. Four through ten low-grade frames are
not ruled out, so this does not raise the nine-channel monotone floor to
ten channels. The separate power-tariff claim for every finite channel count
is not replayed. No schedule, restoration bill, or selected-frontier change
is claimed.

## References

- Ali Romman, nine-channel certificate, `research/nine-channel-monotone-bound`
- Ali Romman, PR #5745, and flyingviper, PR #5720
- Ali Romman, PR #5823, the separate concave power-tariff claim
- Retained source authors named by the nine-channel certificate
