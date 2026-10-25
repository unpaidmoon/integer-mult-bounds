# One shared ordinary terminal still loses

The complementary B/C word of
[research/complementary-consumer-feasibility](../complementary-consumer-feasibility/README.md)
(PR #4848, discussion #4853) is exact, and every serial `n>=2` consumer on its
fixed 224 owners has a strictly negative optimistic moment on `(0,1]`. This
package prices one change outside that serial family.

Premise S keeps the word, the 224 owners, and both helper multisets. The 56
ordinary `L(-2 Q^{-1})` terminals share one rank-one `Q^{-1}` child. Finite
broadcast is free under the predecessor's optimistic finite-work grant.
Exceptional terminals stay `L(-2)`. Paid rank-one count falls from 4023 to
3968, and the rank-mass deficit falls from 176 to 121. The moment
`M(t) = sum_r c_r r^t` satisfies `M(1) = -121`, and `M'(t) > 0` on `[0,1]` by
rational bounds, so `M(t) < -121` for every `t` in `[0,1)`. The serial envelope
`224 - 112n` does not contain those 56 terminals, so deleting 55 of them cannot
raise it. Synthesis is not authorized. This is not a new kappa and does not
change the selected frontier.

[PROOF.md](PROOF.md) states the census, the derivative certificate, and the
subadditivity argument. `verify.py` is the replay. The predecessor native and
phase audit is inherited, not rerun. Single-call maps are not diagonal, so they
are not extra targets. Helper output ranks are not the paid ranks that produce
them, so this note does not claim a moment cancellation from sharing a helper
multiset.

Original card: `complex-new-helper-inventory`. Scope is **changed**: discussion
#1166 comment 19133514 asked for a shared producer beyond the losing serial
model, and the incumbent packing ceiling does not apply inside the predecessor's
replacement bound. Base commit `32890bc5de034ab8fc93ac88ead7279a6a416d04`.
Pins are in [SOURCES.json](SOURCES.json). The selected record and catalogue are
historical provenance.

## Reproduce

From the repository root, Python 3.12, standard library only:

```sh
python3 scripts/research_package.py --package research/complementary-shared-terminal-bill --check-only
python3.12 scripts/research_package.py --package research/complementary-shared-terminal-bill
```

Directly:

```sh
python3 -B research/complementary-shared-terminal-bill/verify.py
```

Expected line: `PASS_SHARED_ORDINARY_TERMINAL_STILL_LOSES`.

Not run: the predecessor native/phase suite, Lean, `ceiling.ceiling()` on this
word, and any search over other shared producers.

## Open next questions

The structured question in [TASK.json](TASK.json) is the only follow-up this
bill justifies:

Can a later premise delete part of the per-call direct primitive, or emit a
legal target whose central rank exceeds the mod-2 cap of one odd power of `Q`,
and still clear a positive complete bill?

It matters because the 55 saved rank-one jobs sit outside the serial envelope,
which is already strictly negative on `(0,1]`. The first step is to write the
new paid histogram and ownership-disjoint census and check that moment before
any native emission. It is blocked while each odd port addition is still charged
one rank-one child and fresh diagonal factors stay independent. Sharing all 112
direct rank-one jobs is not that premise.

## Credit

The complementary word, the 224-owner serial screen, and the direct-primitive
gaps are Chris R / Clear1nsight's. Dugongue's B/C suppliers, Cao Yifan /
intqwq's refreshed audit, and Cinna Davis's direct-price method keep the credit
recorded in the predecessor package. Prepared by unpaidmoon with substantial
Cursor Grok assistance. No independent human review is claimed. Apache-2.0.
