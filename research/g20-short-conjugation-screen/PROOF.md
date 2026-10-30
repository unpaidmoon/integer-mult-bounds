# One-to-three-contact conjugations on the emitted G20 word

## Setup

The word is the emitted local scalar program in
`research/g20-conjugation-admission/WORD.json.gz`, the output of PR #5708.
Its scalar skeleton is the record list with `Q` and `ZERO_Q` removed.
`ADD(a, b)` means the characteristic-2 update `x_a <- x_a + x_b` at the
record's frame. Two such maps fail to commute when one destination is the
other source.

An interval from one `ADD(a, b)` to a later equal `ADD(a, b)` is an
**A2 conjugation of length k** when the open interval contains no `ERASE`
or `INIT` of `a` or `b`, contains exactly `k` noncommuting `ADD` records,
and each of those records has an A2 correction:

- `ADD(b, s)` with `s ≠ a` contributes `ADD(a, s)` at the same frame;
- `ADD(d, a)` with `d ≠ b` contributes `ADD(d, b)` at the same frame.

`ADD(b, a)` has no correction of this form. The conjugation deletes both
outer records and inserts each correction beside its contact. Both the
contact and the correction keep the contact's original frame. This is the
relation implemented by `construct.conjugate` in the #5708 package, restricted
to the contact frame rather than a freely chosen frame.

The scalar endpoint is the same bit-mask identity used by that package:
every non-owned column `i` finishes as `e_i`, xor `e_{i-111}` when
`111 ≤ i < 222`, and every owned column finishes at zero. A conjugation
that misses this endpoint does not preserve arbitrary scalar inputs.

A wire moves from frame `u` to frame `v` only along an edge of
`PATHS.json`. Every published path is one edge. The edge's third component
is its query rank, an integer from 1 to 7. A missing edge means the
candidate does not emit. A nonzero scalar row pays one query of that rank;
a zero row pays nothing. The paid moment at exponent `t` is
`Σ_r n_r r^t`. Its change is `Σ_r δ_r r^t`.

## Census

There are 765 A2 conjugations with `k ∈ {1, 2, 3}`.

| Contacts | Missing route | Emitted loss `2H1 − H2` | Emitted loss `H1+H2+H4` | Emitted neutral | Endpoint failure |
|---:|---:|---:|---:|---:|---:|
| 1 | 184 | 0 | 0 | 0 | 0 |
| 2 | 220 | 109 | 0 | 2 | 0 |
| 3 | 201 | 44 | 1 | 4 | 0 |
| Total | 605 | 153 | 1 | 6 | 0 |

Another 324 equal-gate intervals meet a reversed contact `ADD(b, a)` before
they qualify. They are outside the identity. The verifier recomputes the
table from the pinned word and route file.

## Sign of each emitted shape

Write `H_r` for one paid query of rank `r`.

1. `δ = 2H1 − H2` gives `f(t) = 2 − 2^t`. The map `t ↦ 2^t` is strictly
   increasing because its derivative `ln(2) 2^t` is positive, and `2^1 = 2`.
   For `0 < t < 1`, `1 < 2^t < 2`, so `0 < f(t) < 1`.
2. `δ = H1 + H2 + H4` gives `f(t) = 1 + 2^t + 4^t > 0` for every real `t`.
3. The empty change gives `f(t) = 0`.

None of the 160 emitted words satisfies `f(t) < 0` for any `t ∈ (0, 1)`.
The 154 nonzero changes are strict losses on that whole interval. The six
neutral words preserve both the paid histogram and the scalar endpoint, so
they do not improve the moment either.

The one-step saving already used by #5708 is the different shape
`H1 − 2H2 + H3`. Its change is `1 + 3^t − 2·2^t`. Strict concavity of
`x^t` on `(0, ∞)` at the midpoint `2 = (1+3)/2` gives
`2^t > (1 + 3^t)/2`, hence `1 + 3^t − 2·2^t < 0`, for every `t ∈ (0, 1)`.
The census contains no copy of that shape. The classifier used by the
verifier still names it as a saving, so a later run that found one would
fail the `savings=0` check instead of folding it into a loss.

## What this does not say

The screen does not rebuild the 18-call caller, the adjoint, the moduli
101 and 10201, or the ordinary-admission arithmetic. It does not move a
correction to a different frame, and it does not accept an interval with
four or more noncommuting contacts. The six neutral one-step neighbors and
the 645 common-frame expansions named next to this count in the #5708
README are not given executable definitions by that README, so they remain
outside the certificate. No selected-frontier update follows.
