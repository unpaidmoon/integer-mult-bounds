# A shared-chart terminal still loses its incremental moment

**Claim type: explicit word in a fixed alphabet, plus a written moment bound,
with an exhaustive finite chart census. No new κ.** This is not a proof that
every heterogeneous producer loses, and it is not a supplier or a selected-frontier
change.

The predecessor strip-all terminal in
[research/center-chain-terminal-feasibility](../center-chain-terminal-feasibility/PROOF.md)
pays `112 H8 + 114 H9` to clean one centre. The word below uses the same source,
the same 379+379 normalization, and the same add/scale/nested-transport alphabet.
It pays `112 H1 + 2 H9` for one centre, `176 H1 + 4 H9` for every pair, and
`224 H1 + 16 H9` for all eight centres together. Each bill is strictly cheaper
than that centre set's strip-all bill, and each is still strictly above the
optimistic new reward of one rank-8 job per selected centre, for every saving
`C in [0,1]`.

## Chart census

After the retained source word, every one of the eight centres has:

- its 56 data registers and its pivot on one common chart, chart 1, whose
  frame has length 9 and whose xor-span is all 512 addresses;
- 56 distinct Y registers, each on its own length-8 chart, each span a proper
  subspace of chart 1, and no two of those 56 subspaces nested.

The domain is finite: eight centres, 56 charts each, and all `C(56,2)` pairs.
`verify.py` reads those charts from the pinned ABI and frame table and checks
every subspace comparison. A direct transport between two Y charts is therefore
illegal in this alphabet. A transport between chart 1 and one Y chart has width
`9-8 = 1`. A transport between the empty chart and chart 1 has width 9.

## The word

Fix a nonempty set `S` of centres. Write `u` for the number of distinct Y
registers whose `B` column meets `S`. The suffix is:

1. At chart 1, add each selected data block into that centre's pivot.
2. Transport each selected centre from chart 0 to chart 1.
3. Subtract the pivot from the centre, then subtract the same data block back
   out of the pivot.
4. For each of the `u` Y registers, transport it to chart 1, subtract
   `B` times each selected centre that meets it, and transport it back.
5. Transport each selected centre from chart 1 back to chart 0.

No new register is created. X registers are not moved. Every pivot is restored
before any Y move. The predecessor evaluator accepts the suffix, reproduces the
predecessor's target matrix on all 640 inputs, and reproduces the gatewise raw
inverse transpose. That check is done for every singleton, every pair, and the
full set of eight centres. Four controls reject an omitted Y correction, an
unrestored pivot, a width shortened by one, and one direct Y-to-Y transport.

The resulting extra paid profile is exactly

```text
2u transports of width 1, and 2|S| transports of width 9.
```

The measured shapes are `u = 56` for each singleton, `u = 88` for each pair,
and `u = 112` for all eight centres.

## Moment bound

Let `t = 1-C`, with `t in [0,1]`. For an integer `w >= 1`, `w^t` is increasing
in the exponent and `1 <= w^t <= w`. The new reward is `|S|` rank-8 jobs, so
its moment is at most `8|S|`. The paid moment is

```text
2u · 1^t + 2|S| · 9^t >= 2u + 2|S|.
```

The deficit is therefore at least

```text
2u + 2|S| - 8|S| = 2u - 6|S|,
```

which equals 106, 164, and 176 on the three shapes above. The same arithmetic
at the endpoints is exact: at `t = 0` the deficit is `2u + |S|`, and at
`t = 1` it is `2u + 10|S|`. Scalar adds, the retained 758 normalization gates,
routing, precision, and storage are omitted from this screen, so charging them
would only make the deficit larger. The bound does not use a one-point sample.

## Comparison with the strip-all bill

Let the strip-all word for the same `S` pay `S8` width-8 transports and `S9`
width-9 transports, as counted by the predecessor `terminal` constructor. The
checker requires `S9 >= 2|S|` and

```text
Diff(0) = S8 + (S9 - 2|S|) - 2u >= 1.
```

For every `t in [0,1]`,

```text
Diff(t) = S8·8^t + (S9 - 2|S|)·9^t - 2u >= Diff(0) >= 1,
```

because both `8^t` and `9^t` are at least 1. The shared-chart word is strictly
cheaper than the strip-all word on the whole interval, and the moment section
still places it strictly above the optimistic reward.

## What this does not say

The census covers the charts of this pinned word. It does not enumerate every
suffix. A route through some other frame in the 4429-chart table, a new
register, a warp, or a change to the source word is outside the claim. The
width of each transport is the predecessor evaluator's nested-chart width.
Those relative operators are not run through a fresh Clifford lowering or an
all-column native phase replay. The 379+379 normalization remains charged, and
no compiler or outer transfer is attempted. Selected κ stays
`781451/250000000`.
