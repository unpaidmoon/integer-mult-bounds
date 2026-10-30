# MOVE absolute phase on the selected word scales as i^{p f}

**Scoped partial result; no new κ.** Assumption ID `native_all_columns`, one implication. The selected conditional exponent stays κ = 781451/250000000.

On the selected #6030 word, a `MOVE` from frame `a` to frame `b` is the width-1 operator `U = chart(a)^† chart(b)`. Its global phase is `i^p` with `p ∈ {0,1,2,3}`. At column multiplicity `f ≥ 1`,

```text
U^{(⊗)f} = i^{p f} U_0^{(⊗)f}.
```

That joint phase equals the width-1 factor `i^p` for every `f ≥ 1` exactly when `p = 0`. Exhaustive compilation of this word gives 1,077 phase-zero operators (1,336 events) and 1,809 operators with `p ≠ 0` (2,117 events). Width 2 already separates the two readings: `i^{2} = -1`, `i^{4} = 1`, and `i^{6} = -1`.

Per-column execution of the width-1 circuit is the tensor power, so it is consistent with the identity. The obstructed reading is a joint recipe that copies the width-1 phase integer unchanged.

#5974 already records the factor `i^{p f}` for monomials of the older #5599 word. That word has 3,447 `MOVE`s and 2,887 endpoint pairs. The selected word shares 2,808 of those pairs, drops 79, and adds 78. The added pairs have phases 23 / 17 / 20 / 18 and occur as 103 events. #5974's payload hash does not cover them.

This is not a paid-profile change, a κ improvement, or a discharge of `native_all_columns`.

## Scope and evidence

Original card: `uniform-transfer-audit`. Scope status: **refined**. The card asks for one assumption and one quantified implication at the actual caller. The implication is Lemma B of [PROOF.md](PROOF.md), bound to `research/p104-helper470-twin-rung-removal/WORD.json.gz`.

| `p` | distinct pairs | events |
|---:|---:|---:|
| 0 | 1077 | 1336 |
| 1 | 994 | 1255 |
| 2 | 239 | 246 |
| 3 | 576 | 616 |

The chart walk accepts 3,453 `MOVE`s only along recorded frames. A wrong source frame and a non-nested destination are rejected. One operator of each residue matches `native_verify.state` after a global rotation by `p`, and fails after a rotation by `p+1`.

Pins are in [SOURCES.json](SOURCES.json). The catalogue and selected record are provenance at `2485805a6d47f36ea83ddde6327d453ac82d44dc`.

## Reproduce

```sh
python3 -B research/move-chart-phase-power/verify.py
python3 -B scripts/research_package.py --package research/move-chart-phase-power
```

Observed marker:

```text
PASS_MOVE_CHART_PHASE_POWER pairs=2886 events=3453 phase0_pairs=1077 phase0_events=1336 nontrivial_pairs=1809 nontrivial_events=2117 only_new_pairs=78 only_new_events=103
```

The Clifford census takes about two minutes on CPython 3.12. Lemmas B and C are the written argument. The four state comparisons are controls, not a substitute for those lemmas.

Not run: the #6030 primary native replay, `make` frontier verification, Lean, and Docker.

## Credit

DreamingOfClouds supplied the selected #6030 word. Ali Romman supplied the #5599 word used as the predecessor pair set. The chart compiler is the retained `clifford_exact.py` / `native_verify.py` native channel. #5837 (unpaidmoon) lifted `SCALE`, `ADD` and `COPY` on that #5599 word. #5974 (Mark / Matarener) certifies factorwise all-width lift for the #5599 native layer, including the monomial factor `i^{p f}`. #5442 (Mark / Matarener) is the group-algebra lift for the older #5413 caller. The selected review is Douglas Colkitt's `docs/research/pr-intake-evidence/pr6030-audit/PROOF-REVIEW.md`.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.

## Open next questions

Does any joint recipe in the #6030 primary copy a nontrivial width-1 phase integer `p` instead of `p f`? The first step is to compare one lowered recipe with `p ≠ 0` against the `f`-column operator. The primary payload is not a live input here.

Separately, does the predecessor #5907 word, which has 3,454 `MOVE`s, carry the same phase histogram? The first step is the same census on `research/p104-helper470-twin-rung-removal/inputs/pr5907-WORD.json.gz`.

## Ordered eligible list

Session r62, item 5. Recent #1166 comments in the fetched window are claims and released results, not an open request for this implication. The 19 October handoff index is already delivered or closed by later work, including unpaidmoon #4123/#4127 on the typed actual-width handoff. The revision-8 "Next bounded decisions" table then orders the open rows:

1. Complex helpers (`p104-side-correction`, `coverage-law-change`)
2. BIT `bit-helper-contract`
3. New decoders and interfaces
4. Supplier audit (`#5717` / `#5719`, with `#5718` left uncovered)
5. All-size assumption formalization — this item
6. Verification tooling

#5837 already proved the scalar half of `native_all_columns` for the older #5599 word. This item stays open for a different implication on the current selected caller. Rows 1–4 and 6 were left to the other sessions. Catalogue cards after the table were not reached.
