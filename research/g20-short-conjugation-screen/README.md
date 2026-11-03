# One-to-three-contact conjugations do not lower the emitted G20 word

**Negative result. No new κ.** The selected conditional exponent stays
`781451/250000000` (`0.003125804`) in
[certificates/selected-result.json](../../certificates/selected-result.json).
That record is the frontier pin. The revision-8 priority page still names
the older #5599 value. The baseline binding check on this base returned
`PASS_RESEARCH_BASELINE_BINDINGS_ONLY` with admitted BIT saving `17/5000`.
That command is not a supplier replay.

On the emitted local word of
[PR #5708](https://github.com/CrocSwap/integer-mult-bounds/pull/5708),
every A2 conjugation with one, two, or three noncommuting contacts either
fails to emit on the published route table or does not strictly lower the
paid query moment for any exponent in `(0, 1)`. All 765 candidates preserve
the scalar endpoint. The argument is in [PROOF.md](PROOF.md).

## Task and overlap

Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. Card
`bit-helper-contract`, scope **refined**. The card asks for one uncovered
cut on the #5679/#5708 chain and says to stop when the paid moment does not
improve. The #5708 README reports 765 one-to-three-contact conjugations as
local-only discovery. This package is the replayed certificate for that
count on the emitted word.

Ordered eligible list for session r59, rebuilt on 2026-10-30 against that
main. Open handoffs from the 19 October index (discussion comments
19030045, 19030047, 19030049, and 19030053) come first and are dropped: the
`(w, q, v_N)` consumer, the fresh T385 wrapper, the L546 six-tape bill, and
the single-ADD retiming class are already delivered by this account or
closed on main. Discussion #1166 from 2026-10-26 through 2026-10-30 has no
newer finite handoff index; the new posts are claims, progress notes,
completions, or released handoffs. The priority table is the revision-8
"Next bounded decisions" table in `docs/research/current-priorities.md`.
A row stays while its stated next decision is still open. Catalogue cards
not named by that table were not reached. Dropped before the cut: work this
account already delivered, results closed on current main, and topics
already on a fork `cursor/*` branch, including the port-0 G20 tariff.

1. Complex helpers (`p104-side-correction`, `coverage-law-change`): one
   uncovered helper group and causal cut with a complete caller bill.
2. **This package.** BIT (`bit-helper-contract`): the #5708 one-to-three-contact
   conjugation screen, the local-only clause left after #5679/#5708.
3. New decoders and interfaces: one complete changed producer/consumer
   contract with an optimistic full signed bill.
4. Supplier audit of a latest candidate's uncovered caller gap.
5. All-size audit (`uniform-transfer-audit`): one selected assumption at its
   actual caller.
6. Verification tooling (`replay-runtime`).

Overlap refresh at 2026-10-30T13:28:54Z covered 333 open PR bodies and 6,037
discussion records, with complete reported pagination, plus local notes at
this base. The phrase "one-to-three-contact" appears in the #5708 README,
its vendored copy under `research/g20-four-role-resynthesis/source/`, and
[discussion 5696](https://github.com/CrocSwap/integer-mult-bounds/discussions/5696).
None of those sources is a replayed census of the 765 words. Closed-PR
bodies were not fetched beyond local notes and the ledger.

## Census

| Contacts | Missing route | Loss `2H1−H2` | Loss `H1+H2+H4` | Neutral | Endpoint failure |
|---:|---:|---:|---:|---:|---:|
| 1 | 184 | 0 | 0 | 0 | 0 |
| 2 | 220 | 109 | 0 | 2 | 0 |
| 3 | 201 | 44 | 1 | 4 | 0 |
| Total | 605 | 153 | 1 | 6 | 0 |

`2 − 2^t` and `1 + 2^t + 4^t` are strictly positive on `(0, 1)`. The empty
change is zero. The saving shape `1 + 3^t − 2·2^t` from the two conjugations
already applied in #5708 does not occur. Every length-1 candidate is missing
a route edge.

## Reproduce

Python 3.12 and the standard library, from the repository root:

```sh
python3.12 -I -B research/g20-short-conjugation-screen/verify.py
python3.12 -I -O -B research/g20-short-conjugation-screen/verify.py
python3.12 -B scripts/research_package.py --package research/g20-short-conjugation-screen
```

Both direct runs print

```text
PASS_G20_SHORT_CONJUGATION_SCREEN candidates=765 missing_edge=605 emitted=160 loss_2h1_minus_h2=153 loss_h1_h2_h4=1 neutral=6 savings=0 k1_emitted=0 endpoint_failures=0
```

The verifier hashes the six live inputs, checks that every route is one
edge, recomputes the published local histogram
`1281 H1 + 1338 H2 + 58 H3 + 57 H4 + 102 H5 + 10 H6`, and classifies every
candidate. Controls: the known saving shape is still named as a saving; a
route used by the base word is required for emission; changing one ADD
source changes the base result. Checks raise exceptions, so `-O` does not
disable them.

Not run: the #5708 integration replay, the 18-call caller, adjoint columns,
moduli 101 and 10201, ordinary admission, Lean, and Docker.

## Open next questions

1. Do the six neutral one-step neighbors and the 645 common-frame expansions
   in the same #5708 sentence have a replayed certificate? This matters
   because that sentence treats three searches as one local-only claim, and
   only the 765 conjugations are certified here. The first step is to write
   those two rules from a retained search record, or to show they are not
   the six paid-neutral words above. The blocker is that the published
   package does not contain the search.
2. Can a conjugation with four or more contacts, or one correction moved
   off its contact frame, strictly lower `Σ δ_r r^t` on `(0, 1)`? This
   matters because both restrictions are part of the screened identity. The
   first step is one explicit four-contact word, or one contact moved to a
   frame the route table already contains, with its paid histogram. The
   blocker is that every one-contact candidate already has no route, and no
   favorable longer witness is supplied.

## Credit

The emitted word, route table, A2 relation, and the local-only 765 count are
Ali Romman's `research/g20-conjugation-admission`, following Dugongue,
ai-nanachi, and the retained G20 lineage named there. The predecessor proof
already shows that `H1 − 2H2 + H3` is a strict saving. This package only
classifies the remaining length-1..3 contact-frame conjugations on that
emitted word. No predecessor file is modified.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
