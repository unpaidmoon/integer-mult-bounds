# #4470 monotone rooms miss the rank-8/u2 cell

**Negative result. No new κ.** The selected conditional exponent stays
`605457647/200000000000` (`0.003027288235`). This package does not touch that
record, and it does not read the selected k8 word.

The integer cell in ToikY's `research/lever-integer-twins` puts paid mass
5586 at `{8:698, 2:1}` on a call. Open question 2 of
`research/rank8-u2-entrance-obstruction` asks whether the #4470
productive-helper frames supply at least 698 monotone rank-8 slots. They do
not. This count uses only the #4470 endpoint frames.

## Contract

There are 632 persistent fields: 224 main fields and 408 helpers. Frames are
subspaces of \(\mathbb{F}_2^9\). A monotone chain on a field climbs from its
pinned entrance to its pinned exit, so its parts are positive integers summing
to at most \(\dim(\mathrm{exit}) - \dim(\mathrm{entrance})\). One such chain
holds at most one part of size 8, because every room has size at most 9.

The census applies the parent helper-boundary edits and the #4470 entrance/exit
edits to the pinned canonical frames. Scalar-contact edits, including the
missing-join B/480 patch, retarget events and do not change these 632 endpoint
indices. Every exit contains its entrance. The room histogram is

```text
{9:326, 8:271, 7:7, 4:28}.
```

| Fields | Count | Entrance | Exit | Room |
|---|---:|---|---|---:|
| Main fields | 112 | dimension 1 | dimension 9 | 8 |
| Main fields | 112 | dimension 0 | dimension 8 | 8 |
| Helpers | 326 | | | 9 |
| Helpers | 47 | | | 8 |
| Helpers | 7 | | | 7 |
| Helpers | 28 | | | 4 |

The helper rows are the published profile `{4:28, 7:7, 8:47, 9:326}`, and
their rank mass is the published 3471. Main boundaries stay the original 224
indices. There are `224 + 326 + 47 = 597` rooms of size at least 8.

## Result

597 is strictly less than 698, so the cell `{8:698, 2:1}` is not a monotone
histogram on these endpoints. The same rooms sum to

```text
9·326 + 8·271 + 7·7 + 4·28 = 5263,
```

which is strictly less than 5586. No assignment of mass 5586 fits, with or
without the rank-8 cap. The feasible set priced by the k8 checker is empty
here, so this package does not recompute that moment.

Replacing every pinned exit by the whole space, and keeping these entrances,
is a larger model. Entrance dimensions are `{0:470, 1:159, 2:1, 5:2}`, so the
rooms become `{9:470, 8:159, 7:1, 4:2}`. That model has 629 rank-8 slots and
capacity 5517. Both are still short: 629 < 698 and 5517 < 5586. The 32 slots
gained by the enlargement are exactly the fields whose pinned room is 4 or 7
and whose entrance dimension is 0 or 1. The three fields with entrance
dimension 2 or 5 already exit at dimension 9 and stay below 8.

The pinned native word, which these patches do not edit, has eight fused
rank-8 center jobs on owned register 0 in each orientation (a 3+5 pair, fused).
Charging those eight jobs as eight extra rooms of size 8 raises the two slot
counts to 605 and 637, and the two capacities to 5327 and 5581. All four
numbers remain strictly below the cell. One owned register would add at most
one room; the eight-job reading is the looser upper bound.

## What was not shown

Non-monotone paths, extra registers, and the selected #5413 frames are outside
this certificate. The k8 file's 648 slots are a different entrance table; this
checker rejects that number. Unknown restoration, precision and consumer costs
are not zero. No producer, consumer, or new exponent is claimed.

The predecessor's three-step centre comparison and its 16/17 moment control
stay on the k8 word. They are not rerun.

## Scope

Card `complex-new-helper-inventory`, priority revision 7, base
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. Scope status is **refined**. The
card asks for a new helper inventory with a favorable full bill. The bounded
question here is the open #4470 transfer of the monotone rank-8 obstruction.
The answer is that these frames do not host the cell.

Ordered eligible list for session r39, rebuilt on 2026-10-25 against
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. The order is the one recorded in
`research/f2-six-difference-basis`: open handoffs from the 19 October index,
then priority-table rows whose stated next decision is still open, then
catalogue cards that are not already one of those rows. Dropped before the
cut: work this account already delivered, questions closed on current main,
questions covered by an open pull request, and topics already on a fork
`cursor/*` branch.

1. Caller that accepts `(w, q, v_N)` without restoring the original source
   slots (discussion comment 19030045). Distinct from the encoded-exit
   consumer, the `(N-P)⊗M` consumer, and open #5517.
2. Cost to place `L561` onto the four scratch windows before `L546 −= L561`.
   The delivered move bill starts after placement.
3. PR2809 serializer reading: an ancestor chain, or one root-sized stream per
   cut. The `O_q(V)` arithmetic does not bind that reading.
4. Matched parent park/restore versus the external-call bill for the #4166
   caller. Open #4167 and #4172 do not state that comparison.
5. Fixed-tape visit count of one blank-return of the 9475-row parent,
   including cursor motion across the 124 omitted coordinates. The delivered
   factor `9475·3^124` is the payload, not that invoice.
6. Whether the idle `{3:22783, 5:1625, 48:138492}` is a feasible pattern
   vector of the 841-pattern program. The delivered moment comparison does
   not enumerate patterns.
7. This package.

A cached overlap search on 2026-10-25 (393 open pull requests, 4819 discussion
records, local notes at this base) found the predecessor histogram and its
#1166 handoff. Both say that certificate does not read the #4470 word. No
note stated the histograms `{9:326, 8:271, 7:7, 4:28}` or
`{9:470, 8:159, 7:1, 4:2}`. Coverage is not a novelty proof.

## Reproduce

Python 3.12, standard library only, from the repository root:

```sh
python3 -B research/rank8-4470-entrance-count/verify.py
python3 -B scripts/research_package.py --package research/rank8-4470-entrance-count
```

Expected line:

```text
PASS_RANK8_4470_ENTRANCE_COUNT slots=597/629 capacity=5263/5517 with_centers=605/637/5327/5581 ideal=698 mass=5586 helpers=4:28,7:7,8:47,9:326 no_new_kappa
```

The two slot numbers are the pinned exits and the full-space exits. The four
`with_centers` numbers are those counts and capacities after adding eight
rooms of size 8. The checker hashes the canonical frames, the native word,
both boundary patches, the join patch, and the selected record. It rebuilds
the rooms by elimination, locks the published helper profile and the
predecessor profile obtained by skipping the #4470 boundary edits, and rejects
a dependent basis, a non-nested exit, and an unpaired center event. Not run:
Lean, Docker, the selected cold replay, column replay, and any non-monotone
search.

## Open next questions

1. Do the selected #5413 frames have at least 698 monotone rank-8 slots?
   This obstruction is about the #4470 endpoints. The selected frontier has
   since moved, and a short count there would say whether the same cell is
   still blocked. The first step is this same
   `dim(exit) − dim(entrance)` census on that word's own persistent fields.
   The blocker is that those frames are a different file; substituting 597
   or 629 would mix two templates.
2. Can one #4470 field emit two rank-8 parts by leaving its pinned exit and
   returning? The full-space reading is still 69 slots short of 698, so
   another part has to come from a changed path law. The first step is one
   explicit climb, descent, and second climb, with the paid histogram of
   that trace alone. The blocker is the nested-transport contract: a descent
   is not a monotone room and needs its own restoration bill.

## Credit

The cell `{8:698, 2:1}` and the mass 5586 are ToikY's
`research/lever-integer-twins`, following Nick Petalas's PR #3874. The #4470
frames, the helper profile `{4:28, 7:7, 8:47, 9:326}`, and the predecessor
profile `{4:26, 5:2, 7:29, 8:42, 9:309}` are Cinna Davis's joint helper
lattice, on zxv's native word and the PR4441/PR4447 boundary lineage. The
question is open question 2 of unpaidmoon's
`research/rank8-u2-entrance-obstruction`. This note does not reuse that
package's entrance table.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human review and no formal-kernel acceptance are claimed.
