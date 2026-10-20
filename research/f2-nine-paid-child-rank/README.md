# Paid child rank on the selected word is at most 8

**Scoped negative result. No new κ. The selected record is unchanged.**

Discussion #1166 comment 19021222 asks for the largest child rank a physical
local word on the selected template can emit, counting copies, frames and
restoration, for one fixed support alphabet. The rank-cap relaxation in open
PR #3701 says a target saving `a ≥ 1/99` needs some paid local child of rank
at least 44, and it records that question as blocked because no itinerary
carried a child-rank inventory.

The retained frame contract is that inventory. On the selected complex word,
every paid child is either one strict nested climb or one fixed centre
descent, and every frame is a subspace of `F_2^9`.

## Result

For every legal frame assignment in the unrestricted-terminal model of
`research/selected-k8-unrestricted-ends`:

- every positive-multiplicity edge has climb rank at most **6**
  (`dim(hi_dst) − dim(lo_src)` over all 10,222 paid edges);
- the eight centre descents are rank **8** and are fixed by the word;
- cone restoration is **106** zero-charge edges and creates no child;
- therefore the largest paid child rank is **8**, attained by those centre
  descents.

The selected baseline profile is `{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}`
(local mass 5,586). Copies are the edge multiplicities plus one copy of each
centre descent. The same cap holds for every enumerated frame in the 39,711
domain choices, not only for the baseline assignment: a legal source frame
contains `lo_src` and a legal destination frame is contained in `hi_dst`, so
the climb dimension cannot exceed the recorded gap.

Ideal delivery of the same local mass at rank 8 or at the absolute dimension
cap 9 still misses `a = 1/99`. The first integer histogram in this ceiling
model that clears the target remains the rank-44 greedy shape, which this
alphabet cannot emit.

| Local histogram | Certified ceiling | Against `1/99` |
|---|---:|---|
| Selected profile, max rank 8 | `a < 0.001690054109089` | below |
| All local mass at rank 8 | `a < 0.002739504384567` | below |
| All local mass at rank 9 | `a < 0.002886279317505` | below |
| All local mass at rank 43 | `a < 0.009999732016905` | below |
| `{44:126, 42:1}` | `a > 0.010369575355575` | clears |

The ceilings use `research/complex-local-word-ceiling` unchanged: width 73,
896 families, nine stages, centre charge 64, idle rank at most 51. The
selected bracket matches that package's published ceiling exactly.

## What this does not establish

- It is not a new decoder, supplier, or κ. The acceptance gate for a profile
  that beats the selected word by 5% is not met.
- Idle remainder children may still have rank up to 51. Those are not paid
  local children of this word.
- A scalar rewrite, a non-nested transport, or a bill that adds several climb
  dimensions into one child rank is outside this contract. So is any support
  alphabet larger than `F_2^9`.
- The rank-44 row is an arithmetic screen. It is not a word.
- Selected-k8's LP, duals, and cold replay were not rerun. This package uses
  the word, the frame model, and the unrestricted event graph only.

## Reproduce

Python 3.12, standard library, from the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/f2-nine-paid-child-rank
```

Expected marker:

```text
PASS_F2_NINE_PAID_CHILD_RANK H=9 graph_climb_cap=6 centre=8x8 paid_rank_cap=8 positive_edges=10222 cone_edges=106 domain_frames=39711 selected_hi=0.0016900541090890 cap8_hi=0.0027395043845670 cap9_hi=0.0028862793175050 cap43_hi=0.0099997320169050 cap44_lo=0.0103695753555750 target=1/99 cleared_by_physical_cap=no no_new_kappa
```

The direct run of `verify.py` finished in about 8 seconds on CPython 3.12.3.

## Open next questions

1. **Can a changed bill reach rank 44?** A contract that charges one child for
   the sum of several `F_2^9` climbs, or that leaves this alphabet, could
   escape the cap. First step: write one such identity with its frames,
   copies and restoration, then screen the resulting histogram with
   `ceiling.ceiling` before any search. Blocked until that contract exists.
2. **Does the cap survive a scalar rewrite?** Terminal-frame changes inside
   the fixed word are the model already bounded here. A new scalar program
   needs its own frame space and climb rule. Blocked on that program.

## Credit

The frame contract, centre-descent rule and unrestricted-end graph are
Gareth Davidson's, with OpenAI Codex assistance, in
`research/selected-k8-unrestricted-ends` (PR #2013 / PR #1995 lineage) and
the retained `complex-x4-frame-bound` model. The packing ceiling is Douglas
Colkitt's `research/complex-local-word-ceiling`, with Claude (Anthropic)
assistance. The rank-44 planning threshold and the blocked physical question
are Nick Petalas's open PR #3701 and discussion comment 19021222. This rank
extraction and the ceiling comparison are by unpaidmoon, with substantial
Cursor Grok assistance. Apache-2.0. No independent human or formal-kernel
review is claimed.
