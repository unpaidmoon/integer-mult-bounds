# Profile (2,1,1,0)/(1,1,1) fails support or a character

**Proof. No new κ and no word.** The selected conditional exponent stays
`363005817/100000000000`.

## Claim

In the PR2085/2112 register model, every decomposition of the seven-call
profile `(a,b,p,q)/(m1,m2,m3) = (2,1,1,0)/(1,1,1)` fails target support or
admits an additive character that detects two calls and four targets. Under
the cited premises (P1)–(P3), the profile admits no word.

This is one profile. It does not exclude the other open three-frame profiles,
and it does not change κ.

## 1. Premises and notation

Addresses are rational symmetric 2-by-2 matrices. Write

```
A = diag(1,0),  B = diag(0,1),
P = [[1,1],[1,1]]/2,  Q = [[1,-1],[-1,1]]/2.
```

Coefficient vector `(a,b,c)` means `aA + bB + cP`, with matrix

```
[[a + c/2, c/2], [c/2, b + c/2]].
```

The determinant is `ab + c(a+b)/2`. The matrix is nonzero of rank one exactly
when `(a,b,c) ≠ 0` and `2ab + c(a+b) = 0`. In these coordinates
`A = (1,0,0)`, `B = (0,1,0)`, `P = (0,0,1)` and `Q = (1,1,-1)`.

The targets are `A+P = (1,0,1)`, `A+Q = (2,1,-1)`, `B+P = (0,1,1)` and
`B+Q = (1,2,-1)`. The profile's residual is

```
M = 4I - 2A - B - P = (2,3,-1).
```

A decomposition is three nonzero rank-one frames `R,S,T` with `R+S+T = M`.
The paid multiset is two copies of `A`, one `B`, one `P`, and `R,S,T` once
each. There is no old `Q` call.

Three premises are cited and not reproved. They are the statements of
`research/bit-two-signed-frame-floor/PROOF.md`, Section 1, used for three
added labels in the same way as the merged all-old-once argument.

- **(P1) Determinant.** The labels of a word form a decomposition.
- **(P2) Characters.** For the labels of a word, every additive character of
  the label lattice has `calls(χ) ≥ targets(χ)`.
- **(P3) Support.** For the labels of a word, each target is a sum of a
  sub-multiset of the paid labels.

By (P1)–(P3), a profile whose every decomposition fails (P3) or has a
character with `calls(χ) < targets(χ)` admits no word.

## 2. Support of B+Q forces a frame equal to Q

**Lemma 1.** A decomposition meets (P3) if and only if one frame equals `Q`.
When it does, the other two frames are nonzero, rank one, and sum to
`A+2B = (1,2,0)`.

**Proof.** The old calls already contain `A` and `P`, and they contain `B`
and `P`. So `A+P` and `B+P` are subset sums of every paid multiset of this
profile.

The `b`-coordinate of `M` is 3. An old combination used in a subset sum is
`O = (α,β,γ)` with `α ∈ {0,1,2}`, `β ∈ {0,1}` and `γ ∈ {0,1}`. For
`B+Q = (1,2,-1)`, the complementary frame sum `Σ = B+Q - O` has
`b`-coordinate `2-β ∈ {1,2}` and `c`-coordinate `-1-γ ∈ {-1,-2}`.

- `Σ = 0` would have `b`-coordinate 0.
- `Σ = M` would have `b`-coordinate 3.
- If `Σ` is one frame, that frame equals `Σ` and is rank one.
- If `Σ` is two frames, the omitted frame equals `M-Σ` and is rank one.

There are twelve legal `O`. The rank-one equation `2ab+c(a+b) = 0` holds
for `Σ = B+Q-O` only at `O = (0,1,0)`, where `Σ = (1,1,-1) = Q`. It holds
for `M-Σ` at none of the twelve. Both finite checks are exhaustive and are
repeated in `verify.py`. Therefore `B+Q` is a subset sum if and only if one
frame equals `Q`, and the subset is that frame together with the old `B`.

If one frame is `Q`, then `A+Q` is that frame together with one old `A`.
The other two frames sum to `M-Q = (1,2,0)` and are nonzero of rank one.
Exactly one frame can be `Q`: two copies would leave `M-2Q = (0,1,1)`, and
`2·0·1 + 1·(0+1) = 1 ≠ 0`. ∎

## 3. The rank-one pairs that sum to A+2B

**Lemma 2.** The nonzero rank-one pairs with sum `(1,2,0)` are the ordered
pair `(A, 2B)`, the ordered pair `(2B, A)`, and every ordered pair

```
R = (a,b,c),  S = (1-a, 2-b, -c)
```

where `a,b,c` are rational, `c = -2ab/(a+b)` when `a+b ≠ 0`, both vectors
are nonzero and rank one, and

```
2a(1-a) = b(b-2).
```

The case `a = b = 0` forces `c = 4/3` on the first vector, which is the pair
`((4/3)P, (1,2,-4/3))` up to order.

**Proof.** A rank-one vector with `c = 0` has `ab = 0`, so it is a multiple
of `A` or of `B`. Two such vectors sum to `(1,2,0)` only as `A+2B`.

Otherwise both `c`-coordinates are nonzero and opposite. The rank-one
equations are

```
2ab + c(a+b) = 0,
2(1-a)(2-b) - c(3-a-b) = 0.
```

If `a+b = 0`, the first equation forces `ab = 0`, hence `a = b = 0`. The
second equation then reads `4 - 3c = 0`, so `c = 4/3`. If `a+b = 3`, the
second equation forces `a = 1` and `b = 2`, and the first gives `c = -4/3`,
the same pair swapped. If `a+b ≠ 0`, substitute `c = -2ab/(a+b)` into the
second equation and clear the denominator `a+b`. The resulting polynomial

```
(1-a)(2-b)(a+b) + ab(3-a-b)
```

expands to `2a + 2b - 2a^2 - b^2 = 2a(1-a) + b(2-b)`. Setting it to zero is
`2a(1-a) = b(b-2)`. `verify.py` expands the polynomial and checks that every
monomial outside `2a+2b-2a^2-b^2` cancels. ∎

## 4. Denominator parity

Take a pair from Lemma 2 and write the first vector as `(A1/d, B1/d, C1/d)`
with `d > 0` and `gcd(|A1|,|B1|,|C1|,d) = 1`. The second vector is then
`((d-A1)/d, (2d-B1)/d, -C1/d)`.

**Lemma 3.** `B1` is even, `d` is odd and `C1` is even.

**Proof.** The cleared rank-one and sum equations give

```
2 A1 (d - A1) = B1 (B1 - 2d).     (E)
```

Modulo 2 the left side vanishes and the right side is `B1^2`, so `B1` is
even. Write `B1 = 2 B2`.

Suppose `d` is even. The 2-valuation of the left side of (E) is
`1 + v(A1) + v(d-A1)`. If `A1` is odd then `d-A1` is odd, so the left side
has valuation 1. The right side has valuation at least 2 because both `B1`
and `B1-2d` are even. This is impossible, so `A1` is even. Then `A1`, `B1` and `d` are even,
and `v(d) ≥ 1`. The rearranged form of (E) is still

```
d (A1 + B1) = A1^2 + 2 B2^2.
```

If `A1 + B1 = 0`, the right side vanishes, so `A1 = B2 = 0`. That is
`a = b = 0`, and Lemma 2 forces reduced denominator 3, which is odd. If
`B1 = 0` and `A1 ≠ 0`, then (E) forces `A1 = d` and `c = 0`, so
`gcd(d,0,0,d) = d ≥ 2`. If `A1 = 0` and `B1 ≠ 0`, then (E) forces
`B1 = 2d` and `c = 0`, so the gcd is at least `d ≥ 2`.

The remaining subcase is `A1 ≠ 0` and `B1 ≠ 0`, hence `A1 + B1 ≠ 0` by the
previous paragraph and `c = -2ab/(a+b)`. Clearing gives
`C1 (A1+B1) = -2 A1 B1`, so

```
v(C1) = 1 + v(A1) + v(B1) - v(A1 + B1).
```

From the rearranged equation and `v(d) ≥ 1`,

```
v(A1 + B1) = v(A1^2 + 2 B2^2) - v(d),
v(C1) = 2 + v(A1) + v(B2) - v(A1^2 + 2 B2^2) + v(d).
```

Here `v(A1^2) = 2 v(A1)` is even and `v(2 B2^2) = 1 + 2 v(B2)` is odd, so
the two valuations differ and there is no cancellation. If
`2 v(A1) < 1 + 2 v(B2)`, then `v(A1) ≤ v(B2)` and
`v(C1) = 2 + v(B2) - v(A1) + v(d) ≥ 3`. If
`2 v(A1) > 1 + 2 v(B2)`, then `v(A1) ≥ v(B2) + 1` and
`v(C1) = 1 + v(A1) - v(B2) + v(d) ≥ 3`. Thus `C1` is even. All four
integers are even, contradicting the gcd. Thus `d` is odd.

Rearrange (E):

```
d (A1 + B1) = A1^2 + B1^2 / 2 = A1^2 + 2 B2^2.
```

The right side is an integer, and since `d` is odd,

```
v(A1 + B1) = v(A1^2 + 2 B2^2).
```

If `A1 = 0`, then `a = 0`. Lemma 2 forces `b ∈ {0,2}`. If `b = 2`, then
`B1 = 2d` and `B2 = d`, so `v(B2) = 0` and `C1 = 0` because `c = 0`. If
`b = 0`, Lemma 2 forces `c = 4/3`, so the reduced denominator is 3 and
`C1 = ±4` according to sign. Both are even.

If `A1 + B1 = 0`, the displayed equation gives `A1^2 + 2 B2^2 = 0`, hence
`A1 = 0`, already treated. Thus `A1 ≠ 0` implies `A1 + B1 ≠ 0`.

If `B2 = 0`, then `b = 0`, so Lemma 2 forces `a ∈ {0,1}`. The value `a = 0`
has `A1 = 0`. The value `a = 1` is the frame `A`, with `C1 = 0`, which is
even.

If `A1 ≠ 0` and `B2 ≠ 0`, then `a+b ≠ 0`, so the same clearing gives
`C1 (A1+B1) = -4 A1 B2` and

```
v(C1) = 2 + v(A1) + v(B2) - v(A1 + B1).
```

The valuations `v(A1^2) = 2 v(A1)` and `v(2 B2^2) = 1 + 2 v(B2)` have
opposite parity, so they differ and the sum has valuation equal to the
minimum.

- If `2 v(A1) < 1 + 2 v(B2)`, then `v(A1) ≤ v(B2)` and
  `v(C1) = 2 + v(B2) - v(A1) ≥ 2`.
- If `2 v(A1) > 1 + 2 v(B2)`, then `v(A1) ≥ v(B2) + 1` and
  `v(C1) = 1 + v(A1) - v(B2) ≥ 2`.

In every case `v(C1) ≥ 1`. ∎

## 5. The character

**Lemma 4.** Every decomposition that meets (P3) has a character with
`calls = 2` and `targets = 4`.

**Proof.** By Lemma 1 one frame is `Q` and the other two are a pair from
Lemma 2. Let `R = (A1/d, B1/d, C1/d)` be the reduced form of Lemma 3, and
let `S` be the other frame of the pair. The label lattice is contained in
the group of vectors whose `c`-coordinate lies in `(1/d)Z`. On that group
define `φ` by writing the `c`-coordinate as `Z/d` with `Z ∈ Z` and setting
`φ = Z mod 2`. The numerator is unique, and `φ` is a homomorphism to `F2`.
It kills `2Λ`.

Since `d` is odd, `φ(P) = φ(0,0,1) = 1` and `φ(Q) = φ(1,1,-1) = 1`.
Since `C1` is even, `φ(R) = 0` and `φ(S) = 0`. Also `φ(A) = φ(B) = 0`.
The paid calls therefore contribute

```
calls(φ) = 2·0 + 0 + 1 + 0 + 0 + 1 = 2.
```

Each target has `c`-coordinate `±1`, so each has numerator `±d`, which is
odd. Thus `targets(φ) = 4`. ∎

## 6. Theorem

**Theorem.** Every decomposition of `(2,1,1,0)/(1,1,1)` either fails (P3)
or has a character with `calls(χ) < targets(χ)`. Under (P1)–(P3) the
profile admits no word.

**Proof.** If the decomposition fails (P3), there is nothing to prove. If
it meets (P3), Lemma 4 supplies the character. ∎

## 7. What this does not prove

- It does not reprove (P1), (P2) or (P3).
- It does not exclude orbit `O4`, the profile `(0,1,1,1)/(1,1,2)`, or any
  profile outside `(2,1,1,0)/(1,1,1)`.
- The eight symmetries of PR #7128 would carry a no-word statement across
  orbit `O3` only if that transport lemma is granted. This file does not
  prove the lemma. The checker confirms that those eight maps permute a
  fixed list of eight profiles; that finite check is not the transport
  argument.
- No word is exhibited, and the selected exponent is unchanged.
- The finite solution sample in `verify.py` is corroboration of Lemma 3 and
  Lemma 4 on that sample. The quantifiers in the lemmas are the valuation
  argument above, not the sample.
