# Frontier compression: 22,821 to 17,445 events, no new kappa

This package shortens the merged word of
[PR6167](https://github.com/CrocSwap/integer-mult-bounds/pull/6167)
(conditional kappa 0.003128645) from **22,821 to 17,445 events** (-5,376, -23.6%).
**No kappa is claimed.** The complete invoice (13,444 productive fields,
66,762 paid calls, rank surplus 760), the paid profile, the storage and the raw
crossing (between 0.00312865201590 and 0.00312865201591) are identical to PR6167's.

Builds on PR6285 (22,821 to 18,083 events), which uses the first two rewrites below.

## The edit

Only ADD and SCALE events change: 18,423 to 13,088 ADD and 861 to 820 SCALE.
All 3,449 MOVE events and all INIT, COPY and CLEAR events are kept, in order.

- **Shared partial sums.** The 104 Y registers each receive about 78 helper terms, and
  pairs of rows overlap in about 79 of 85 terms with the same coefficient ratio. A row
  that needs many terms that another, already complete row holds now adds that row's
  final value and folds the donor's other columns into its own initial-value reads.
- **Window resynthesis.** Within each stretch of ADD and SCALE events between MOVE
  events at one frame, the register update is re-solved exactly (Gauss/LU on the
  read graph, readers first). A new column is accepted only if it creates no cycle.
- **Shortest-linear-program partial sums.** On blocks of co-located Y rows, shared
  partial sums are synthesised as a short linear program (greedy pair sharing with
  ratio-normalised pairs), realised in place in registers that already exist.
- **Cycle-merging row sharing.** A donor that would close a cycle among the rows is
  accepted when the rows of that cycle form one small group (at most 8 rows) and the
  gain exceeds the cost of the extra rows; the group is rewritten as one block.

ADD and SCALE events do not enter the price, so the paid profile cannot change. The
event and scalar slack of the word grows (scalar allowance is recomputed in RESULT.json).

## Evidence

`verify.py` authenticates PR6167's word, price and the pinned PR5827 checker chain
(read from the merged package `research/p104-retained-operand-descent`, pinned in
[SOURCES.json](SOURCES.json)), checks that only ADD and SCALE events changed, then
replays the compressed word through the unmodified chain: identical productive targets,
paid profile and storage, all 799 input columns with 638,401 coefficients, the 2,922
native maps, the physical caller and the complete price. [RESULT.json](RESULT.json)
records the outcome.

```sh
python3.12 -I -O -B research/p104-frontier-compression-2/test_portability.py
python3.12 -I -B research/p104-frontier-compression-2/verify.py
python3.12 scripts/research_package.py --package research/p104-frontier-compression-2
```

These are author checks. Independent review is pending and the inherited framework
assumptions remain.

## Coordination and credit

Base word and checker: PR6167 by Ali Romman. Precedent: PR6169 (exact multi-gate
resynthesis, no kappa). The compression tool is `tk compress` from PR6170.
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.
See [NOTICE](NOTICE).

## Open next questions

- Does an independent reviewer confirm the replay? Start with `verify.py`.
- Can the rewrite be combined with the next merged word? Run it on that word and
  compare the replayed price. Details are in [TASK.json](TASK.json).
