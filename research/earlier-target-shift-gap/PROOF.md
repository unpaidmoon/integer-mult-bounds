# Earlier-target frame506 shifts are the reversed-field conjugate

## Statement

Let `S` be the `8×8` matcher stored in the committed helper-462 / frame-506
program `research/bit-row-route-generator/PROGRAM.json.gz`. Write `N = 8f`
for a positive tensor width `f`. The route generator expands each additive
elimination factor once in each direction. Exactly four of the fourteen
factors per direction update an earlier matrix address from a later one.

Those sites are not calls of the proved later-target fixed-tape shear. On
the source stream layout they are `add_high(..., reversed_fields=True)`:
the forward shear conjugated by one swap of its two high axes. Each such
call records two `completed_swap_oracle` invocations. The forward shear
records none. No fixed-tape transition bill for that oracle is claimed.

The selected conditional exponent stays the value in
`certificates/selected-result.json`. This is not a P3 admission, a physical
transposition, or a new κ.

## Address census

Run the usual right-looking elimination on `S`, as a separate implementation
of the route generator's factor loop. For pivot column `j` and row `i ≠ j`,
an additive factor is the operation that replaces row `i` by
`row i - z * row j` and then emits

```text
ordered_shift(target = row*N + j*f + lane,
              source = row*N + i*f + lane,
              coefficient = z)
```

for every `row < N` and `lane < f`. The committed interpreter updates only
the target:

```text
high[target] = high[target] + z * high[source]    (mod R).
```

The same index pair is retained in the opposite direction, with coefficient
`-z` for an additive factor and `1/z` for a scale. Therefore the comparison
of the two addresses does not depend on direction, row, or lane:

```text
target - source = (j - i) * f.
```

Since `f > 0`, the target address is smaller than the source address exactly
when `j < i`. The elimination of this matcher has fourteen additive factors:
four with `j < i` and ten with `j > i`. None has `i = j`. Each factor
contributes `N f = 8 f²` sites in each direction, so the two directions give

```text
earlier-target sites = 2 * 4 * 8 f² = 64 f²,
later-target sites   = 2 * 10 * 8 f² = 160 f².
```

The committed `f = 1` program contains these 224 shifts in that order, 112
in each direction. The checker recomputes both directions and compares them
with the stored steps, then checks the closed formula at `f = 1, 2, 3`.

## Conjugation

Index a Boolean stream by `(p, x, g, y, z)`, where `x` and `y` are the two
high axes. Let `L_c` be the forward operation
`add_high(..., reversed_fields=False)` and let `E_c` be the same call with
`reversed_fields=True`. Let `τ` swap the two high axes, leaving `p`, `g`,
and `z` fixed.

The source implements `E_c` by calling `completed_swap_oracle`, then the
forward scale/rotate body, then `completed_swap_oracle` again. That oracle
exchanges the two high axes and restores the rectangular support. Hence

```text
E_c = τ ∘ L_c ∘ τ
```

on every stream whose length is `before * high * middle * high * suffix`.
The checker compares the two sides on three shapes, including coefficient
`1/2`, coefficient `-2` with carry `1`, and a nontrivial suffix. A single
application of `τ` does not satisfy the identity, and the forward image
differs from the reversed image on each of those shapes.

When `high = 1` the source returns before either swap. Both sides are the
identity and the oracle list is empty. The route's earlier-target sites are
not in that degenerate case: their block indices differ.

## What the two oracle records do not provide

`completed_swap_oracle` pads each high axis to the next power of two, appends
one ordinary-call record, performs the axis exchange by direct indexing, and
unpads. Its comment charges that body as `T_old`, not as one of the linear
stream primitives. The forward checker records two such objects for every
reversed call above and none for `L_c`.

The published fixed-tape ordered shear, affine shear, and original-owner
affine shear implement the forward axis order. Their own write-ups leave
`reversed_fields` and the earlier-target route outside the proved interface.
Signed-dyadic scaling prices the `80 f²` unit-scale sites and states the
same `64 f²` earlier-target remainder. This package proves that remainder is
exactly the reversed-field class, with two unpriced oracle calls per site.
It does not replace either call by a finite tape program.

## Stop

A useful successor is one fixed-tape axis transposition with an all-extent
transition and visited-cell bill. Multiplying that bill by two and by
`64 f²`, then adding the proved later-target bill, is the earlier-target
allowance. Owner-bank installation, low-cache lifetime, ROW padding, and P3
remain separate. Unknown oracle time is not zero, and it is not a reason to
continue inside the forward-only kernel.
