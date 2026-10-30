# New-low commit and cache retirement at the port9 leaf

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No new κ. The selected conditional exponent stays `781451/250000000`.

## Statement

Fix the port9 inverse column-1 leaf of `research/port9-low-cache-carry`: `q = 5`,
row 0, quarter weights `(-1, 0, -2, 0, -1, 0, 0, 0)`, and a supplied 64-digit
cache. Both compile-time orientations are the unchanged frontend, generic
rotation and descriptor erasure linked by that package.

At leaf halt the cache on tape 17 is byte-for-byte the entry cache, including
bits 24 through 191, and tape 18 holds exactly three raw new-low bits. Two
successor facts follow.

1. **Commit.** An eight-transition straight-line program on tape 18 writes
   `RIGHT` three cells past the new-low origin and returns that head. The three
   bits and every other tape stay put. The marked word is a later owner
   protocol: it falsifies the leaf's raw-exit equality, so it is not a silent
   rewrite of the leaf.
2. **Retirement obstruction.** A 551-transition straight-line program blanks
   cache bits 24 through 191 and returns the cache head. It leaves bits 0
   through 23 and the endpoint marker. On every input this leaf accepts, that
   program falsifies the leaf exit contract. In particular the published
   witness row `(2, 3, 2, 1, 1, 1, 0, 0)` and the same cache with digit 8
   changed from 0 to 4 produce the same owner permutation and the same new-low
   digit 2, while their preserved caches differ on bits 24 through 26. Blanking
   the tail deletes that difference.

The low-type and ROW consumers named by the port9 handoff are still absent, so
this leaf is not a legal last consumer of the 64-digit cache.

## Why the tail is invisible to the output

The compiled frontend parameters are `positions = 0..7` and `cells = 64`.
The quarter numerator uses only the weighted row:

```text
N = -l_0 - 2 l_2 - l_4,    t = 4^{-1} N mod 5,    k = (N - 4t)/5.
```

Digit 8 is outside that row. For the published witness, `t = 2`, `k = -3`
and, at modulus 125, the carry offset is 93. Replacing digit 8 by 4 leaves
`(t, k)` unchanged. The machine agrees: both orientations of the witness, and
the forward mutant, satisfy the predecessor's full exit equality, and the
mutant differs from the witness only on tape 17.

The forward leaf reads every cache offset `0, ..., 192` and writes none of
them. Its only tape-18 writes are offsets 0, 1 and 2.

## Why later components cannot retire the cache

In both orientations the generic component's branch, write and move tapes are

```text
{0, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15}
```

and the cleanup component names only tape 14. Neither names tape 17 or 18.
The frontend does name both. Therefore every cache and new-low change is
confined to the frontend, and the measured exit state has no cache writes.

## The two straight-line successors

The commit program, entered at the leaf's new-low head, is

```text
move +1, move +1, move +1, write RIGHT, move -1, move -1, move -1, halt.
```

Eight transitions, visited offsets `{0, 1, 2, 3}`. The data symbols are not
rewritten. Re-checking the predecessor exit equality fails with
`every cell, head, borrowed input and declared output`.

The retirement program is

```text
24 right moves to offset 24,
write blank at each of offsets 24..191, moving right between writes,
191 left moves back to the origin,
halt.
```

The instruction count is `24 + 168 + 167 + 191 + 1 = 551`. Offsets 0 through 23
and the endpoint at 192 stay. The same exit check fails. Applied to both
caches above, the blanked tails are identical, so the digit-8 information the
leaf had preserved is gone.

## What this does not prove

It does not implement a low-type consumer, a ROW installer, a whole-T cache
layout, or a profitable supplier change. A later protocol may copy the tail to
a named consumer and only then erase it. No such consumer is present, and
erasing at this halt is not that protocol. The selected frontier is unchanged.
