# E8 label-pairing child-rank cap

**Scoped negative result. No new κ. The selected conditional κ stays
0.001672660197076918.**

Card `complex-rank-shape-decoder`, method “bound the best effective child rank
achievable for one fixed support alphabet, including copies, frames and
restoration.” The alphabet is the E8 root-line label pairing used by the
eight-term decoder model. This does not construct a block-climb word, and it
does not meet the card’s positive 5% gate.

## Scope

The fixed support alphabet is the label pairing on the 120 root lines of E8:

```text
N_ij = (<r_i, r_j> + 1) mod 2.
```

Representatives are the doubled-coordinate roots from the same enumeration as
the retained frame-pair checker: 112 vectors of type `±2e_i ± 2e_j` and 128
vectors of type `(±1)^8` with an even number of minuses. Lines are unordered
pairs `{r, −r}`.

A complete invoice in this alphabet has three child kinds:

| Kind | Rank charged |
|---|---|
| Paid term whose nonzero supports are sets of these lines | the F2 rank of `N` on those supports |
| Frame transport of such a term | that same rank |
| Dirty-slot restoration | 1 |

The transport and restoration charges are the ones named by the block-climb
obstruction for this cost alphabet: a transported object is a recursive child
of its own rank, and overwriting a dirty gather slot costs one rank-1 save.
An external frame that is not one of these children is outside the alphabet.

## Result

The 120×120 pairing has F2 rank **9**. Every row reduces to zero against a
9-element basis, so every set of rows has rank at most 9. Deleting columns
cannot raise rank, and `N` is symmetric, so every support pair has pairing
rank at most 9. The same basis is itself a rank-9 minor, so the cap is
attained by one term supported on all 120 lines. A synthetic extra row
outside those 120 columns has rank 10 and is rejected; it is not a term of
this alphabet.

Therefore every paid term and every frame transport has rank at most 9, and
every restoration has rank 1. **No complete invoice in this alphabet has a
paid child of rank 10 or more.**

The selected local profile `{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}` has
mass 5586 and maximum rank 8, so it sits inside the cap. That check does not
rederive the profile.

Under the hosted nine-stage template (width 73, 896 families, centre 64,
idle rank at most 51), cost per unit of mass is nonincreasing in the child
rank for a saving `a ≥ 0`. The favorable local histogram of mass 5586 with
ranks at most 9 is therefore the fractional histogram `{9: 5586/9}`. Its
certified ceiling, recomputed with the pinned `ceiling.py` enclosure, is

```text
a < 577255863501/200000000000000 = 0.002886279317505.
```

The integer histogram `{9:620, 6:1}` has

```text
a < 1442853651953/500000000000000 = 0.002885707303906.
```

Both are strictly below `1/99`. At `a = 1/99` both relaxations have certified
lower bound greater than 1, so neither certifies that saving. The selected
word’s own ceiling remains `a < 1690054109089/10^15`. The rank-9 screen lies
above that selected ceiling, so the cap does not explain the selected word.
It does exclude the target-scale saving `a = 1/99` for every local word whose
paid children stay in this alphabet, even after ideal rank-51 idle packing.

Rank 44 is not available here. Further moment arithmetic that needs a paid
child of rank greater than 9 cannot be realized by this alphabet.

## What this does not establish

- No realizing rank-9 word, no block-climb identity, and no profile that
  passes the card’s 5% gate. The rank-9 histogram is an upper screen.
- Masked E-graph costs, where odd pairs are free, are a different alphabet.
  The one-sided tetrad-local sub-alphabet already has the sharper term cap 4.
- Idle children of rank up to 51 remain in the ceiling model. This note caps
  paid local children, transports and restorations, not that idle packing.
- A caller that imports a frame from outside the three invoice kinds is not
  covered. Zero-charge co-frame groups inside the selected word’s 2,412
  rank-1 children were not read from the gauge44 archives.
- No supplier admission, no selected-frontier change, and no new κ.

## Reproduce

From the repository root, Python 3.12, standard library only:

```sh
python3.12 -B research/e8-label-child-rank-cap/verify.py
python3.12 -B scripts/research_package.py --package research/e8-label-child-rank-cap
```

Expected final line of the package verifier:

```text
PASS_E8_LABEL_CHILD_RANK_CAP lines=120 pairing_rank=9 minor_rank=9 selected_max_rank=8 invoice_max_rank=9 rank9_ceiling_hi=577255863501/200000000000000 integer_ceiling_hi=1442853651953/500000000000000 selected_ceiling_hi=1690054109089/1000000000000000 below_1/99=true rank10_rejected=true controls=10 no_new_kappa=true
```

The registered package command then prints
`PASS_REGISTERED_RESEARCH_PACKAGE research/e8-label-child-rank-cap outcome=negative-result`.

## Open next questions

- **Which other support alphabet on this template can emit a paid child of
  rank at least 10 after copies, frames and restoration?** The label-pairing
  alphabet cannot. A first step is to name the alphabet and its invoice kinds
  before another ceiling screen. Blocked if the alphabet is not source-bound.
- **Do the selected word’s 2,412 rank-1 payload children already share a frame
  of rank greater than 9?** That would be an external frame, outside the
  invoice above. A first step is to partition the pinned gauge44 operand
  frames into co-frame groups. Blocked: that extraction is a separate pass
  over the word archive.

## Credit

The label pairing and the rank-9 fact for the full matrix are the model of
PR717 and the retained frame-pair proof
(`research/complex-frame-pair-decoders`). The ceiling enclosure and the
selected local profile are `research/complex-local-word-ceiling` (Douglas
Colkitt, with substantial Claude/Anthropic assistance). The transport and
restoration charges are the contract stated for the block-climb obstruction.
The tetrad-local cap 4 is a different alphabet and is not re-proved here.
Nick Petalas’s rank-cap curve posed the missing physical rank bound; this
package answers it only for the label-pairing alphabet.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human or formal-kernel review.
