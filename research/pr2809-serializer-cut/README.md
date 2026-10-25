# One PR2809 recursive cut parks the child capsule

**Scoped serializer comparison. No new κ.** The selected conditional exponent
stays `605457647/200000000000`. The GL64 macroprogram is not run.

## Result

`RoleParking.park`, taken from the pinned archive
`research/physical-ordinary-interchange/inputs/pr2809.tar`, parks the bodies
present on the canonical roles. It writes four bits per current symbol, blanks
that symbol, and pushes once per role. The method does not name a root stream.

On a three-role schedule with a fixed 8-symbol control role and one empty
role, the data records are:

```text
root data bits        = 4000    (1000 symbols)
child data bits       = 28      (7 symbols)
grandchild data bits  = 4       (1 symbol)
```

The child cut is shorter than the root cut, so it did not recopy the root
packet. The 7-symbol and 1-symbol bodies are the adopted-capsule schedule for
this comparison. They are not a live GL64 measurement. Park does not compute
`V/(WN)`; the predecessor's geometric model supplies that identification, and
`PROOF.md` §§6–7 of the archive say the child adopts the capsule prepared
before parking.

The pinned nested fixture charges `depth * (5 * 132 + 7 * 5 + 3 * 2)` steps.
Those 132 bits are `4 * (4 + 13 + 12) + (1 + 3 + 12)`, a constant per level.
The depth-1500 loop is not run.

The other reading, one fresh root-sized stream at every cut, is outside the
geometric constant 26041 already proved in
`research/pr2809-continuation-stack-space`. Here `D(2^26050) = 42857`, which
is greater than 26041. This package does not re-prove that constant.

The argument is [PROOF.md](PROOF.md).

## Scope

Task card `uniform-transfer-audit`, priority revision 7, base
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. Scope status is **refined**.

The card asks whether one quantified step of the #4100 construction holds at
its caller. This package takes only the serializer question left open by
`research/pr2809-continuation-stack-space` after that package proved the
geometric `O_q(V)` reading. It does not audit another #4100 sentence and it
does not change the selected record.

This is item 3 of the eligible list below. Fewer than eight items remained,
so the assigned index is `(8 - 1) mod 5 = 2`.

Ordered eligible list for session r40, rebuilt on 2026-10-25 against
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. Open handoffs from the 19 October
index (Discussion #1166 comment 19029944) come first, with a closed smallest
task removed. Priority-table rows whose stated next decision is still open
come next, one concrete successor each. Catalogue cards that are not already
those rows follow. Dropped before the cut: work this account already
delivered, results on current main, questions covered by an open pull request,
and topics already on a fork `cursor/*` branch.

1. A caller that accepts `(w, q, v_N)` without restoring the original source
   slots (discussion comment 19030045; open question 1 of
   `research/p104-role-exchange-caller-audit`). The cleanup consumer in
   `research/p104-residual-consumer` leaves that caller open.
2. Unbound L561 intervals before the L546 subtraction (the unfinished bind
   from comment 19030049). `research/qq16-l546-head-move` priced the head
   move and left placement open.
3. **This package.** Whether the pinned PR2809 serializer parks the ancestor
   chain or one root-sized stream per cut.
4. The exact fixed-tape visit count of one R437 parent blank-return (open
   question 1 of `research/r437-parent-spectator-blank`). The payload
   comparison is already on main.
5. A 14-point difference basis of `F_2^6` with a simple closed walk of step
   weight at most 3 (open question 1 of `research/f2-six-difference-basis`).
   The displayed witness in `research/fixed-fourteen-basis-walk` needs weight
   4 and does not exclude another basis.

Excluded before this cut: the fresh T385 wrapper, closed by
`research/t385-r437-copy-audit`; the retiming handoff, covered by #4122 and
#4128; the four-provider rebind, on main in
`research/mixed-provider-admission`; the matched park/restore bill, covered
by open #4167 and #4172; the #4091 1090-call equivalence, on main in
`research/fourth-entry-ceiling-transfer`; the rank-8/u2 producer, closed by
`research/rank8-u2-entrance-obstruction`; and the centre-path card, stopped
by `research/centre-sharing-overhead-budget`.

Overlap refresh at 2026-10-25T07:18:32Z, cache `/tmp/overlap-r40.json` during
the session: local head `32890bc5` with a complete inventory of 7402 notes,
393 open pull requests, and 4817 discussion records. Terms were `RoleParking`,
`root-sized stream`, `serializer cut`, `continuation serializer`, and
`PR2809`. The predecessor package is the open question answered here. GitHub
search of open pull requests found no hit for `RoleParking`, `root-sized
stream`, or `serializer cut`. Historical PR2809 threads are the source
construction. No matches is not a novelty certificate. The fork had
`cursor/pr2809-stack-space-6e4c` and no serializer branch.

## Reproduce

Python 3.12, standard library only, from the repository root:

```sh
python3 scripts/research_package.py --package research/pr2809-serializer-cut --check-only
python3.12 -B scripts/research_package.py --package research/pr2809-serializer-cut
```

`verify.py` prints

```text
PASS_PR2809_SERIALIZER_CUT root_data_bits=4000 child_data_bits=28 grandchild_data_bits=4 child_is_capsule=true child_recopies_root=false full_copy_depth=42857 no_new_kappa=true
```

`test_verify.py` prints `PASS_PR2809_SERIALIZER_CUT_CONTROLS`.

Not run: the GL64 macroprogram, numerical PARK, the depth-1500 nested loop,
Lean, Docker, and the selected cold replay.

## Open next questions

1. Are the marker, template, and erased-backing cells inside the `26041 V`
   budget? `BIT.md` §2 includes them in the `O_q(V)` sentence, and each parked
   role emits one `$` mark that this comparison does not charge. First charge
   one fixed template per live role against `V/(G-1)`. Blocked here because
   §2 does not give the live role count.
2. Does numerical PARK of the live Word slots also avoid recopying the root
   templates? The archive proof says intermediate calls retain those templates
   and do not rebuild them per child. First meter `numerical_frame.py` at one
   cut. Blocked here because this package does not execute the numerical codec.

## Credit

The `O_q(V)` sentence is Cinna Davis's #4100
(`research/unconditional-batched-crt/BIT.md`). The serializer and §§6–7 of
its proof are Jose Manuel's PR2809 archive. Mark (Matarener), with Claude
Code assistance, checked `BIT.md` §§1–4 in
`research/bit-stock-recurrence-audit`. The geometric constant 26041 and the
open serializer question are unpaidmoon's
`research/pr2809-continuation-stack-space`.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human review and no formal-kernel acceptance are claimed.
