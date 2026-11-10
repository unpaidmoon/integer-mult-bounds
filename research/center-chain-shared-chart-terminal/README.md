# Shared-chart terminal for the heterogeneous centre offer

**One explicit suffix beats the strip-all bill and still loses. No new κ.**

Handoff
[discussion comment 19133212](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19133212)
asks for one physical entry/call/exit word that changes the costs of the
declared strip-all terminal while keeping every data observation, every Y
correction, and every helper return. This package supplies that word for every
singleton, every pair, and all eight centres.

```text
one centre:   112 H1 + 2 H9   against  1 H8    deficit at least 106
one pair:     176 H1 + 4 H9   against  2 H8    deficit at least 164
all eight:    224 H1 + 16 H9  against  8 H8    deficit at least 176
```

The predecessor strip-all profile for one centre is `112 H8 + 114 H9`. The new
word is strictly cheaper on the whole saving interval `C in [0,1]` and remains
strictly negative against the optimistic new reward. The 379+379 normalization
is unchanged and still charged.

The argument is in [PROOF.md](PROOF.md). The chart statement is an exhaustive
finite census of the eight centres' X and Y frames. The endpoint and raw-dual
statements are checks of those 37 finite words in the predecessor evaluator.
The moment comparison is a written bound, using `1 <= w^t <= w` for integer
`w >= 1` and `t in [0,1]`.

## Reproduce

Python 3.12, standard library, from the repository root:

```sh
python3 -I -W error -B research/center-chain-shared-chart-terminal/verify.py
python3 -I -O -W error -B research/center-chain-shared-chart-terminal/verify.py
```

Expected marker: `PASS_SHARED_CHART_TERMINAL_LOSES cases=37 deficit_floors=106,164,176 no_new_kappa`.
Allow about a minute. The checker pins its input bytes, rebuilds every suffix,
compares all 640 input columns with the predecessor target, checks the raw
inverse transpose, and rejects four bad suffixes.

Not run: a fresh Clifford lowering of the width-1 quotient, an all-column
native phase replay, a compiler or outer admission, and any search over the
other 4429 charts. No selected record is edited.

## Open next questions

1. Can one added register, or one chart outside `{0, 1}` and the selected Y
   charts, make this same endpoint's optimistic moment nonnegative? The word
   above does not. A useful first step is to name that register and chart and
   price its transports before any search. This package's own policy should
   not be enlarged: its favorable screen already fails.
2. The retained 758 normalization gates are still paid once per invocation.
   Cancelling any of them against this suffix is a different chronology, and
   this negative terminal bill does not fund that rewrite.

## Credit

The strip-all terminal, evaluator, and open producer question are Chris R /
Clear1nsight's
[PR #4839](https://github.com/CrocSwap/integer-mult-bounds/pull/4839) and
[discussion #4840](https://github.com/CrocSwap/integer-mult-bounds/discussions/4840).
The source word and ABI are the retained #4694/#4698 normal form. Selected κ
remains `781451/250000000` from #6030.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
