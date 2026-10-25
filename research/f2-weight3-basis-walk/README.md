# A 14-point difference basis admits a weight-at-most-3 closed walk

**Scoped existence proof. No new κ.** The selected conditional exponent stays
`605457647/200000000000` (`0.003027288235`, #5413).

## Result

The set

```text
P = {0, 1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 55, 56}
```

is a difference basis of \(\mathbb{F}_2^6\). The closed walk

```text
0-32-40-56-24-16-8-4-5-55-6-2-3-1-0
```

visits each point once and returns. Its fourteen steps have Hamming weights

```text
1, 1, 1, 1, 1, 2, 2, 1, 3, 3, 1, 1, 1, 1,
```

so the maximum is 3 and the sum is 20. The argument is in [PROOF.md](PROOF.md).

Among the 53,340 normalized bases that contain 0 and every weight-1 vector,
53,270 have some such walk and none has total weight below 20. The displayed
basis of `research/fixed-fourteen-basis-walk`, whose point 63 lies at distance
at least 4 from the rest, is one of the 70 that have none.

Under that note's paired-readout accounting this walk still costs 140 root
queries and 146 map applications. It does not beat the generic six-source DUO
bill, and it is not a physical connector program.

## Scope

Task card `connector-alphabet-change`, priority revision 7, base
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. Scope status is **refined**.

The card asks whether one added connector operation has a favorable completed
budget. This package does not add an operation. It answers the walk left open
by `research/f2-six-difference-basis` and by the displayed-witness theorem:
some other 14-point basis does have a simple closed walk of step weight at
most 3. The alphabet, source count and paired-readout contract stay fixed.

### Eligible list for session r46

Ordered as in `research/f2-six-difference-basis`: open handoffs from the
19 October index (discussion comment 19029944), then priority-table rows whose
stated next decision is still open, then catalogue cards that are not already
those rows. Dropped before the cut: work this account already delivered,
results on current main `32890bc5`, questions covered by an open pull request,
and topics already on a fork `cursor/*` branch.

1. A caller that accepts `(w, q, v_N)` without restoring the original source
   slots (comment 19030045; open question 1 of
   `research/p104-role-exchange-caller-audit`).
2. **This package.** A 14-point difference basis of \(\mathbb{F}_2^6\) with a
   simple closed walk of step weight at most 3. The displayed witness needs
   weight 4. Fewer than 14 items remained, so the assigned index is
   `(14-1) mod 2 = 1`.

Dropped on this rebuild: the fresh T385 wrapper
(`research/t385-r437-copy-audit`); the six-tape `L546` head-move bill
(`research/qq16-l546-head-move`); the retiming handoff (merged #4567); the
four-provider rebind (`research/mixed-provider-admission`); the matched
park/restore comparison (open #4167 and #4172); the R437 blank-return ratio
(`research/r437-parent-spectator-blank`); the #4100 continuation stack
(`research/pr2809-continuation-stack-space`) and ledger-boundary exponent
(`research/pr4100-ledger-boundary-exponent`); the #4091 word, capacity and
stock equivalence (`research/staged-fourth-ceiling-equivalence`); the rank-8
entrance obstruction (`research/rank8-u2-entrance-obstruction`); the
compact-switch contract; and the stock, census, replay, packing and
scalar-itinerary cards already closed on main or by this account's earlier
notes. The free-word tensor lift of #4100 is
`research/free-word-tensor-lift-audit`.

## Reproduce

Python 3.12 and a C11 compiler (`cc`), from the repository root:

```sh
python3 -B research/f2-weight3-basis-walk/verify.py
python3 -B scripts/research_package.py --package research/f2-weight3-basis-walk
```

`verify.py` prints

```text
PASS_F2_WEIGHT3_BASIS_WALK steps=14 max_weight=3 applications=20 normalized_hits=53340 normalized_cycles=53270 normalized_min=20 queries=140 map_applications=146 no_new_kappa=true
```

The compiled census is the slow part, about one minute. The Python checks of
the recorded cycle, the deleted-point control and the displayed distance
obstruction are immediate. Not run: Lean, Docker, the selected cold replay,
and any search outside the normalized slice.

## Open next questions

1. Does a 14-point difference basis that omits some weight-1 vector have a
   weight-at-most-3 closed walk with source-application total 16? That is the
   generic DUO application count. First drop the standard-basis requirement
   and search sets translated to contain 0. The blocker is that \(|\mathrm{GL}(6,2)|\)
   does not preserve Hamming weight, so the 53,340 normalized bases do not
   represent every weight pattern.
2. The length-10 five-source leaf question in
   `research/connector-triple-query-floor` stays open. This six-source walk
   does not decide it.

## Credit

The order-14 census and the walk question are unpaidmoon's
`research/f2-six-difference-basis`. The displayed weight-4 theorem and the
paired-readout accounting are Nick Petalas's
`research/fixed-fourteen-basis-walk`. The six-source interface is Ross
Richardson's `research/universal-connector-boundary`. Aaron Wang's #2128 and
Tairitsu-Aya's #2156 supply the generic DUO bill cited as a comparison, not
replayed here. Volodymyr Gavrylkiv's six-dimensional difference-basis value
is the one already credited in #2156.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human review and no formal-kernel acceptance are claimed.
