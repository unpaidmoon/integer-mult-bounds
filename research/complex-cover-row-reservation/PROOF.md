# The #4100 common-cover row reservation does not fit

Audited text: `research/unconditional-batched-crt/COMPLEX.md`, section
"Common cover, fresh rows and fixed tapes", bytes identical at base
`fbc9ea0249746acca4f504d4fda2b84e0e36cf0d` and at the retained #4100 head
`337d04939571a637aeab54a0f58f54fde811663a`. The obligation named in that
package's `AUDIT.md` is the arbitrary-`f` complete-cover execution. This note
audits the row-bit reservation and the group order that execution cites. It
does not accept #4100 and does not change the selected frontier.

## Statement

Let `W = 322560` and let

```text
Gamma = 2^1296 * product_{i=1}^{36} (2^{2i} - 1).
```

`COMPLEX.md` says `Gamma = |O(73,2)|`, reserves

```text
q = ceil(log2((W Gamma)^{D(h)}))
```

row bits, and pads the complete range to

```text
R = ceil(2^q / (W Gamma)^{D(h)}) * (W Gamma)^{D(h)},
```

"a factor less than two."

For every integer `D >= 1`, that `R` equals `2N` with `N = (W Gamma)^D`, so
the factor `R/N` equals 2, and `R` is strictly larger than the reserved
`2^q` addresses. The same `q` does hold exactly one copy of `N`, and
`1 < 2^q/N < 2`. The group order itself is the integer `Gamma`.

## The dot-product group has order Gamma

Let `n = 2m + 1` and let `V = F_2^n` with `B(x,y) = sum_i x_i y_i`. The matrix
of `B` is the identity, so `B` is nondegenerate. Let `1` be the all-ones
vector. Then `B(1,1) = n mod 2 = 1`, and `B(x,x) = B(x,1)`.

Let `U = 1^perp`. Then `dim U = 2m`. Every `x in U` has `B(x,x) = 0`, so `B`
restricted to `U` is alternating. It is nondegenerate: a vector of `U` orthogonal
to all of `U` is orthogonal to `V = U ⊕ <1>`, hence is zero.

Let `O` be the group of linear automorphisms of `V` that preserve `B`.
Every `g in O` fixes `1`. Indeed `B(gx,gx) = B(x,x)` gives `B(gx,1) = B(x,1)`,
so `g^T 1 = 1`. Preservation of `B` is `g^T g = I`, so `g^T = g^{-1}` and
therefore `g 1 = 1`.

Restriction to `U` is an isomorphism `O → Sp(U,B)`. It is a homomorphism into
the symplectic group. It is injective because a map that fixes `1` and fixes
`U` is the identity. It is surjective: for `S in Sp(U)` the rule
`g(u + a 1) = S(u) + a 1` is linear, and

```text
B(Su + a 1, Sw + b 1) = B(Su, Sw) + ab B(1,1) = B(u,w) + ab,
```

since `Su` and `Sw` lie in `U`. The right-hand side is `B(u + a 1, w + b 1)`.

An ordered symplectic basis of a `2m`-dimensional space is chosen one hyperbolic
pair at a time. In dimension `2k` there are `2^{2k} - 1` choices for the next
nonzero vector and `2^{2k-1}` vectors pairing with it to `1`. The stabilizer of
a full basis is trivial, so

```text
|Sp(2m,2)| = product_{k=1}^{m} (2^{2k} - 1) 2^{2k-1}
          = 2^{m^2} product_{i=1}^{m} (2^{2i} - 1).
```

At `m = 36` the right-hand side is `Gamma`. The prose sentence that the all-ones
vector has norm 1, that its perpendicular space is symplectic of dimension 72,
and that one counts successive symplectic pairs, is this identification.
Thus `Gamma = |O(73,2)|` for the standard dot product. The integer has 2628
bits. Its decimal SHA-256 is
`50b58aaac98e621e9917d6c3bced5e276398b68918bbd57ac8d784d3d58db00b`.

The verifier enumerates both groups for `n = 1, 3, 5` (so `m = 0, 1, 2` on the
symplectic side, with the `m = 0` orthogonal count equal to 1) and checks that
every orthonormal basis sums to the all-ones vector. It also checks that the
two product writings agree for every `m <= 36`.

## The displayed pad does not fit

Factor `W = 2^{10} * 315` with `315 = 3^2 * 5 * 7`. Every term `2^{2i} - 1` is
odd, and `2^2 - 1 = 3`, so the odd part `Odd` of `Gamma` is an odd multiple of
`3`. Hence

```text
W Gamma = 2^{1306} * M_1,    M_1 = 315 * Odd,
```

with `M_1` odd and `M_1 >= 945`. For an integer `D >= 1`,

```text
N = (W Gamma)^D = 2^{1306 D} * M_1^D.
```

The odd part `M = M_1^D` satisfies `M >= 945 > 1`, so `N` is not a power of two.
Let `q = ceil(log2 N)`. Then `2^{q-1} < N < 2^q`, so `1 < 2^q / N < 2` and

```text
ceil(2^q / N) = 2,    R = 2N.
```

In particular `R/N = 2`, which is not strictly less than two, and
`R = 2N > 2^q`, so `R` is not a subset of the `q` reserved bits.

The repair inside the same bit budget replaces `ceil` by `floor`. Then
`floor(2^q / N) = 1`, and the only positive multiple of `N` that fits in
`2^q` addresses is `N` itself. The reservation factor `2^q / N` lies in the
open interval `(1, 2)`. Holding the written range `R = 2N` instead would take
`q + 1` bits, because `2^q < 2N < 2^{q+1}`. Either repair leaves the row-bit
count at `log2(N) + O(1) = O(D log(W Gamma))`. The sentence as written describes
neither a fitting range nor a factor strictly less than two.

`D(h) >= 1` for every width `h >= 73`, by the recurrence in the same paragraph,
so the failure applies at every recursive node that reserves row bits.

## The depth recurrence does halve

The same paragraph defines `D(e) = 0` for `e < 73` and
`D(e) = 1 + D(48 floor(e/73))` otherwise, and says that every child of rank
`r <= 48` decreases `D` and that two levels halve `e`.

`D` is nondecreasing. For the inductive step at `f >= 73`, the argument
`48 floor(f/73)` is strictly smaller than `f`, and `t(e) = 48 floor(e/73)` is
nondecreasing, so the claim reduces to the inductive hypothesis on that
smaller argument.

For `e >= 73` and `1 <= r <= 48` the child width
`c = r floor(e/73)` is at most `48 floor(e/73)`, hence
`D(c) <= D(48 floor(e/73)) = D(e) - 1`.

Let `e1 = 48 floor(e/73)` and `e2 = 48 floor(e1/73)`. Then
`e2 <= 48^2 e / 73^2`. Since `2 * 48^2 = 4608 < 5329 = 73^2`,
`(48/73)^2 < 1/2`, so `2 e2 < e`. Two maximum-rank steps more than halve the
width. This half of the paragraph stands. It is not the padding claim.

## What this does not establish

The fitting copy `N` is still one `W` by `Gamma` by remaining-stock product.
This note does not bound the parked ancestor volumes, does not build the
depth-first tapes, and does not execute a transversal of `O(73,2)`. The
free-word cancellation audited in #4184, the rank-`r f` moment sign in #4375,
and the common-grid height defect in #4178 are different sentences.
No selected-frontier change is claimed.
