# Staged544 new-gap reduction audit

**Finite audit of an obstruction. No new κ.** Selected κ stays
`0.001672660197076918`.

## Scope and evidence

Original card: `scalar-to-moment`, scope **refined**. The card asks whether a
scalar simplification changes a paid histogram. This package does not offer a
new simplification. It answers the independent-challenge request in
[discussion #1166, comment 19032637](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19032637):
the interaction and new-gap reductions in
[PR #3942](https://github.com/CrocSwap/integer-mult-bounds/pull/3942)
`PROOF.md` §§2–4, at head `1416f8cd6bfb2f2eb9aa5cc22f0388a85fdbac91`.

The price oracle is that package's pinned `search.py` / `vendor/retiming.py`.
`bridge_census` is not called. The 11,917,718-row shared-register census is
not replayed. Gap rows are priced from gate frames and the segment's entry and
exit frames, without a fresh trace. On each provider the replay checks those
rows against `candidates()` for 47 pairs: 24 evenly spaced pairs and further
pairs that sit on a segment edge or beside a non-ADD. A separate local check,
not part of the registered replay, compared 159 pairs on the base provider,
including 120 edge pairs, and found no row mismatch.

On each pinned PR3734 provider (`BORROW-WORD-43base` and `BORROW-WORD-43extra`):

| Check | Count |
|---|---:|
| Fixed-frame adjacent pairs | 4,709 |
| Non-bridge gap prices, all found in the original local corridor | 1,354,687 |
| Bridge gap prices, all curvature-nonnegative | 14,693 |
| Changed first frames | 1,047 |
| Same-ADD second placements matching a direct move | 2,609,832 |
| First-frame intervals, quotient rank at most 3 | 1,559 |
| Pairs whose gap rows match `candidates()` exactly | 47 |

The bridge count equals PR #3942's published `candidate_dimensions` (14,693)
on each provider. The two provider receipts match each other; the gzip inputs
do not. No unlocalized non-bridge price, negative bridge price, disjoint-register
frame change, or composition mismatch appeared.

What this does not show: a universal two-gate barrier, a replay of the
shared-register census, uniform coefficient or precision costs, native hosting,
or a change to the selected frontier.

## Reproduce

From the repository root, CPython 3.12, standard library only. The run uses up
to four processes. Both providers finished in 180 seconds on a 4-core host.
One provider is the 600-second command unit, so a one-core replay stays inside
that cap.

```sh
python3.12 -B scripts/research_package.py --package research/staged544-new-gap-audit
```

Expected status: `PASS_STAGED544_NEW_GAP_AUDIT`.

## Credit

The move rules, price engine, and both provider words are Chris R /
Clear1nsight, PR #3942, reusing the PR #3886 retiming engine and the PR #3734
providers (dataisfire). PR #3964 (Clear1nsight) closed the stationary
illegal-intermediate gap and is not re-audited here. New work is the
exhaustive localisation, composition, and lattice comparison. Prepared by
unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.

## Open next questions

1. Replay `variable_census` for one provider, at least on the 29
   `frame_only_neutral` first words, against the published RESULT rows. This
   audit never enters that loop.
2. For one changed first frame, compare `candidates()` for a disjoint-register
   second ADD before and after the move. This audit only shows that those
   frame sequences stay put. Open PRs #4122 and #4128 already address moved
   illegal intermediates and are not repeated here.
