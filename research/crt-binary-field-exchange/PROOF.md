# Direct binary exchanges and the ordinary-interchange bill

**No new κ.** The selected conditional exponent stays `605457647/200000000000`.
BIT.md's theorem is not reproved. The #4174 constructor is executed, not rewritten.

## Two readings

`research/crt-reservoir-interchange-bill` leaves this question open: does a
direct exchange of `H` single-bit swaps meet `O(V H^{1-a2} + V)` on fixed
tapes, without the volume factor `(q^E/2^H)^2`? BIT.md's machine exchanges
two equal address fields and moves the record at address `x` to the swapped
address. A pass that rewrites bits inside one stored word does not do that.
The two readings are priced separately. Here `a2 = c(1-c^2)` with
`c = 8667/5000000`, as in BIT.md.

## 1. In-record pass

A record is a binary tape of length `L`. A second tape has two cells and
starts blank. An action is one read, one write, or a one-cell head move.
Finite control holds no data bit.

For `0 ≤ i < j < L` the schedule in `verify.py` copies bit `i` onto buffer
cell 0, copies bit `j` onto buffer cell 1, writes cell 0 onto position `j`
and cell 1 onto position `i`, blanks both buffer cells, and returns both
heads to cell 0. Every other bit stays. The action count is exactly

```text
moves = 2j + 6,   reads = 4,   writes = 6,   total = 2j + 16.
```

The data head travels `i + (j-i) + (j-i) + i = 2j` cells. The buffer head
makes six one-cell moves. The four reads and six writes are the two saves,
the two restores, and the two blanking writes.

An exchange of the disjoint fields `[α, α+H)` and `[β, β+H)`, with
`α+H ≤ β`, is these `H` passes on the pairs `(α+t, β+t)`. The passes
commute. The total is

```text
sum_{t<H} (2(β+t) + 16) = H (2β + H + 15).
```

There is no embedding into `q^E`. The volume factor is 1.

## 2. The in-record bill

Let `M` be the number of records and set `V = M L`, one scan of every
address bit. For `L ≥ 15` and `β ≤ L-H`,

```text
H (2β + H + 15) ≤ H (2(L-H) + H + 15) ≤ H (2L + 15) ≤ 3 H L.
```

Six such exchanges, the placement and the restoration in the predecessor,
therefore cost at most `18 V H` actions. For `1 ≤ H < 2^25`,

```text
25 a2 < 1/20,
```

because `500 · 8667 · (5000000^2 - 8667^2) < 5000000^3`. Thus
`H^{a2} < 2^{25 a2} < 2^{1/20}`, and

```text
18 V H < 18 · 2^{1/20} V H^{1-a2}.
```

Both #4174 layouts below have `H < 2^25` and `L ≥ 15`, so the in-record
reading meets the bill with constant `18 · 2^{1/20}` and with volume
factor 1. The same constant covers one exchange with `3` in place of `18`.

This is not BIT.md's operation. On two-bit labels `[0,1,2,3]` with
payloads `[10,11,12,13]`, swapping the two stored bits rewrites the labels
to `[0,2,1,3]` and leaves every payload in its slot.

## 3. Payload transport

Index records in address order. Position `0` is the most significant bit,
so position `p` has place value `2^{L-1-p}`. Swapping place values `2^A` and
`2^B`, `A > B`, moves every address whose bits differ. There are `M/4`
such pairs, and each pair is distance `2^A - 2^B` apart. The small cases
`L ≤ 6` are exhaustive in `verify.py`.

Assume one action carries at most one payload across one record boundary.
Those `M/4` payloads each cross `2^A - 2^B` boundaries, so the schedule
uses at least

```text
M (2^A - 2^B) / 4
```

record-boundary crossings. One full scan supplies `M` crossings.

On every plan produced by the #4174 allocator, one destination is
`[0, H)` and its source starts at an index `s ≥ 2H`. The exchanged MSB
has place `2^{L-1}` and its partner has place `2^{L-1-s}`. The distance is

```text
D = 2^{L-1} - 2^{L-1-s} > 2^{L-2},
```

so the crossing count is greater than `M · 2^{L-4}` and the scan count is
greater than `2^{L-4}`. The in-record allowance of §2 is less than
`18 H` scans. The executed minimal and production plans satisfy

| layout | `L` | `H` | scans | `18 H` |
|---|---:|---:|---:|---:|
| `p = 1310720`, `ell = 21`, widths 20 | 1310720 | 10752 | `> 2^{1310716}` | 193536 |
| `p = 9240576`, `ell = 24` | 1540096 | 15360 | `> 2^{1540092}` | 276480 |

`2^{L-4}` grows faster than every constant multiple of `H ≤ L/100`. No
constant that is independent of the layout, in the sense BIT.md requires
of its `O` (dependence on `q` and the fixed source only), bounds this
transport on every layout the constructor accepts.

The minimal padding factor recomputed here lies strictly between `2^{33}`
and `2^{34}`. The transport lower bound is larger than that padding. A
direct single-bit payload swap does not remove it.

## 4. Answer

For the in-record rewrite, yes: six field exchanges cost at most
`18 · 2^{1/20} V H^{1-a2}` actions and do not pad the volume. For the
payload movement BIT.md states, no: already on the minimal #4174 layout
the front-field swap needs more than `2^{1310716}` scans, above the same
allowance. The selected exponent is unchanged.
