# L561 has no tape interval at event 9895; the kernel-shaped copy costs \(8NW-12\) moves

**Scoped certificate. No new κ.** The selected conditional exponent stays
`605457647/200000000000` (`0.003027288235`).

## Result

On the pinned forward word, event 9895 is `L546 -= L561` in frame 4. The only
earlier record of register 561 is the entrance adapter at event 7963. Neither
record, and no other event kind in that word, names a tape origin or a cell
length. The cleared `C0`–`C7` windows are a different token family and are
still zero, so they are not a stored image of L561.

In the six-tape model, the only complex-register entrance is two owned tapes
of length \(NW\). Copying that entrance onto the four half-length scratch
windows used by the subtraction, with heads returned to cell 0 and no free
relocation, has the sharp bill

| | count |
| --- | ---: |
| READ | \(2NW\) |
| WRITE | \(2NW\) |
| MOVE | \(8NW-12\) |

The axis kernel's own packing habit, which steps one past the last cell, costs
12 moves more. Adding the already proved subtraction bill gives a conditional
pair total of READ \(6NW\), WRITE \(4NW\) and MOVE \(16NW-24\). That total
starts from the kernel entrance. It is not an embedding extracted from the
word.

The argument is in [PROOF.md](PROOF.md).

## Scope

Task card `joint-query-controller`, priority revision 7, base
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. Scope status is **refined**.

This is item 2 of the eligible list below. It answers open question 1 of
`research/qq16-l546-head-move`: the copy onto scratch that the head-move bill
does not charge. It is the distinct remainder of discussion comment 19030049
after event 9894 was bound and the in-place subtraction was priced. It does
not price the matched park/restore comparison, and it does not invent a native
window the word does not contain.

Ordered eligible list for session r34, rebuilt on 2026-10-25 against
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. The order is the one recorded in
`research/f2-six-difference-basis`: open handoffs from the 19 October index
(discussion comment 19029944) come first, a closed smallest task is removed,
and a still-open remainder is kept when it is distinct. Priority-table rows
whose stated next decision is still open come next, one row at a time.
Catalogue cards that are not already those rows follow. Dropped before the
cut: work this account already delivered, results on current main, questions
covered by an open pull request, and topics already on a fork `cursor/*`
branch.

1. A caller that accepts `(w, q, v_N)` without restoring the original source
   slots (comment 19030045). The q-field cleanup in
   `research/p104-residual-consumer` and the caller audit in
   `research/p104-role-exchange-caller-audit` leave that caller open.
   Distinct from the encoded-exit standard-Y consumer and from `(N-P)⊗M`.
2. **This package.**
3. Whether the PR2809 continuation serializer parks the ancestor chain or one
   root-sized stream per cut (open question 1 of
   `research/pr2809-continuation-stack-space`). The \(O_q(V)\) reading is
   already proved. This is the `uniform-transfer-audit` row.
4. The fixed-tape visit count of one blank-return on the 9475-row R437 parent
   (open question 1 of `research/r437-parent-spectator-blank`). The 972-bit
   payload comparison is already proved. This is the
   `r437-carrier-integration` row.
5. One explicit up, down, up frame trace for the three-step rank-8 comparison
   (open question 1 of `research/rank8-u2-entrance-obstruction`). Catalogue
   card `complex-new-helper-inventory`. The monotone entrance obstruction is
   already proved.
6. A 14-point difference basis of \(\mathbb{F}_2^6\), other than the displayed
   witness, with a simple closed walk of step weight at most 3 (open question
   1 of `research/f2-six-difference-basis`, after
   `research/fixed-fourteen-basis-walk`). Catalogue card
   `connector-alphabet-change`.

Excluded before this cut: the fresh T385 wrapper (comment 19030047), closed
by `research/t385-r437-copy-audit`; the retiming handoff (comment 19030053),
covered by #4122, #4128 and merged #4567; the four-provider rebind, on main in
`research/mixed-provider-admission`; the matched park/restore bill, covered by
open #4167's complete-root source-action comparison (open #4172 is the
allocator follow-up); `p104-side-correction` as its own row, because item 1 is
that consumer and the slot, chart, encoding, fiber and standard-Y pieces are
certified; `independent-moment`, because `research/fourth-entry-ceiling-transfer`
and the 1090-call record already compare the #4091 ceiling with the later
fill; `formal-interface-lemma`, because #4321 audited the compact-switch
contract and a fork branch holds the sharp-window density. Centre-path,
coverage, stock, census, replay, packing and scalar-itinerary cards stay
dropped for the reasons recorded on `research/f2-six-difference-basis`, plus
this account's later deliveries through #5281. A second #4100 successor, such
as the two excluded `p = 2` CRT corners, is the same uniform-transfer row as
item 3 and is not a new item ahead of the later rows.

## Reproduce

From the repository root, CPython 3.12, standard library only:

```sh
python3 scripts/research_package.py --package research/qq16-l561-scratch-placement --check-only
python3 -B research/qq16-l561-scratch-placement/verify.py
```

The verifier prints

```text
PASS_QQ16_L561_SCRATCH_PLACEMENT event=9895 intervals=absent prior_records=1 mentions=27 scratch_clear=C0-C7 move=8*N*W-12 read=2*N*W write=2*N*W sharp=yes one_past_extra=12 combined_read=6*N*W combined_write=4*N*W combined_move=16*N*W-24 no_new_kappa
```

It checks the forward-word schemas and the 27 register-561 mentions, the eight
terminal clears, the canonical entrance frames, the sharp copy and the
one-past copy on nine \((N,W)\) pairs through \(N=512\), \(W=5\), dirty-scratch
overwrite, home-bit visibility, and the sum with a re-meter of the pinned
subtraction schedule.

Not run: Lean, Docker, the selected cold replay, and any search for a native
tape program outside this word.

## Open next questions

1. If the next kernel needs these scratch windows empty, what does it cost to
   copy L561 out before that clear? The first step is to name the next
   tape-using event after 9895 that requires the four windows. No such event
   is bound here. The subtraction leaves L561's bits in scratch, so a later
   destructive kernel cannot treat those bits as free dirt.
2. Does any published native tape program, outside this scalar word, assign
   L561 a home other than the two-tape kernel entrance? The first step is one
   source whose event or memory map carries an origin and a length for
   register 561. This word does not. A different home can change the copy
   bill; the \(8NW-12\) count is not a lower bound for every encoding.

## Credit

The six-tape rules are Clear1nsight's `research/qq16-gaussian-axis-tapes`.
The unbound-interval statement and the zero `C0`/`C1` candidate are
`research/qq16-f0-first-caller` (PR #3932). The same-frame scalar price is
unpaidmoon's #4162. The conditional subtraction bill, and the question this
package answers, are unpaidmoon's `research/qq16-l546-head-move`
([finding](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19146840)).
Both schedules have move count \(8NW-12\) because they use the same six
lengths; the copy reads \(2NW\) cells and writes \(2NW\), while that
subtraction reads \(4NW\) and writes \(2NW\). Ali
Romman's QQ16 lineage and Nick Petalas's numerical formats are the retained
background; they are not re-proved.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human or formal-kernel review.
