# Division-free exchange of a dual pair

This scoped construction and its compiler application were produced by Nick
Petalas. Elementary block shears, stabilized unimodular completion and
compute/use/uncompute are classical. No general linear-algebra priority is
claimed. The contribution is a coefficient-preserving alternative for the
dyadic helper interface, its explicit scalar tariff and the emitted-program
improvement below.

## Boundary contract

Let D = Z[1/2], let a be a row in D^n and b a column in D^n with ab = 1.
There are n data fields x and one spare field z, all at one common linear
chart. Every incoming value, including z, is arbitrary. No zero initialization,
erasure, odd inverse or change of chart is available inside the exchange.

The desired basis map on these n+1 fields is

```text
S(x,z) = ((I-ba)x + bz, ax).
S = [[I-ba, b], [a, 0]].
```

The extended pair is (a,0), (b,0), and the pivot is the spare coordinate.
Then (a,0)S = e_z^T and S e_z = (b,0)^T, exactly the row/column equations
of Ali Romman's [PR5611](https://github.com/CrocSwap/integer-mult-bounds/pull/5611).
This changes the resource contract by requiring a spare coordinate. It does
not replace a no-spare completion and does not assert that the spare exists
in a particular P104 cut. During S alone, z becomes ax; it is not restored
at that intermediate boundary.

## Two literal factorizations

Define common-chart block shears and a sign operation by

```text
U_b(x,z) = (x+bz,z)
L_a(x,z) = (x,z+ax)
D(x,z)   = (x,-z).
```

Operations below are written in chronological order. The first program is

```text
U_b; L_(-a); U_b; D.
```

After the middle block, the spare is
z-a(x+bz) = -ax, using ab=1. After the last upper block and sign, the
result is ((I-ba)x+bz,ax). The second program is

```text
D; L_a; U_(-b); L_a.
```

Its first lower block gives ax-z. Its upper block gives (I-ba)x+bz.
Its last lower block gives ax-z+a(I-ba)x+abz = ax. Thus both programs
are S. Every upper block is one ADD per nonzero b_i; every lower block
is one ADD per nonzero a_i. Within each block the ADDs commute, but blocks
cannot be reordered freely. Only the sign SCALE is used. Every emitted
coefficient belongs to {+a_i,-a_i,+b_i,-b_i,-1}; no Euclidean quotient,
new denominator, native operation, INIT or CLEAR is introduced.

Put s_a=nnz(a), s_b=nnz(b). The two exact gate counts are
2s_b+s_a+1 and 2s_a+s_b+1. In particular a completion exists with
min(2s_b+s_a,2s_a+s_b)+1 gates. Selecting the cheaper scalar tariff can
select a different factorization than selecting the smaller gate count.

Because ab=1, (ba)^2=ba and (I-ba)b=0=a(I-ba). Direct multiplication
therefore gives S^2=I. S fixes ker(a) and swaps the directions (b,0) and
(0,1), so its determinant is -1. It uses no additional field beyond the
stated spare. Its n-dimensional top-left block is singular, with kernel
exactly Db.

## A sharp block count, within a stated alphabet

Three off-diagonal block shears are necessary for this S, even allowing
arbitrary invertible block-diagonal operations for free. This statement
counts entire U and L blocks, not individual ADDs, and is not a lower bound
for unrestricted scalar circuits.

Move each block-diagonal factor through an adjacent shear by conjugation.
Conjugation preserves whether the shear is upper or lower. The resulting
outer block-diagonal factors preserve invertibility of each principal
block. Two upper shears combine, as do two lower shears. A product UL has
invertible lower-right block; a product LU has invertible top-left block.
The same is true of zero or one shear. S has lower-right block zero and
singular top-left block I-ba. Hence at most two shears cannot realize S.
The displayed programs attain three. The argument applies over D by
embedding into Q. The constructive identities themselves hold over any
commutative ring with ab=1.

## Full scalar bill and intermediate growth

Use the retained PR5602 real scalar tariff, as defined in its pinned
`local.py`. For reduced nonzero q=u/2^v, define

```text
A(q) = 2(3 + bitlength(|u|)-1 + popcount(|u|) + v),
A_a = sum_(a_i != 0) A(a_i),
A_b = sum_(b_i != 0) A(b_i).
```

The sign SCALE costs 2. The cheaper of the two displayed factorizations
therefore has exact allowance

```text
B = 2 + min(2 A_a + A_b, A_a + 2 A_b).
```

This is an exact bill for emitted scalar work, not a proof of global scalar
optimality. The source caller additionally limits coefficient magnitudes;
that limit must still be checked for each installation. The named example
below satisfies it. The general bounded compiler is an algebraic tool and
does not widen the source caller's admissible coefficients.

For a magnitude bound put alpha=||a||_1 and beta=||b||_1. Every scalar
prefix of a lower block has infinity-operator norm at most 1+alpha, and
every scalar prefix of an upper block at most 1+beta. D has norm one.
Submultiplicativity bounds every intermediate by
(1+alpha)^2(1+beta) times the input infinity norm for the a-repeated
program, and (1+alpha)(1+beta)^2 for the b-repeated program. This includes
partial accumulation inside each block; cancellation only at the end of
a block is not used as an intermediate bound.

## An arbitrary dirty spare returns in the complete consumer

Let G be a D-linear endomorphism of the field value space. Scalar
coefficients commute with G. Apply S, then G on the spare alone, then S
again. Since S^2=I, the complete map is

```text
x -> x + b(G-I)ax
z -> z.
```

One direct calculation starts after the first S with
x'=(I-ba)x+bz and z'=ax. The last S sends the data to
(I-ba)x'+bGz'=(I-ba)x+bGax, and sends the spare to ax'=z.
There is no initial-zero premise or dirty-spare contribution to the data.
The fully charged displayed consumer uses two exchanges, allowance 2B,
and one application of G. G's own cost, representation, physical delivery,
any required chart changes and allocation are additional obligations.
This is not an independence certificate for new productive helper targets.

## First emitted-program improvement

For a=(3,5), b=(2,-1), ab=1 and neither entry of a is a dyadic unit.
Use the same three roles and spare pivot 2 in both constructions. The
unmodified PR5611 compiler, called on (3,5,0), (2,-1,0), pivot 2, emits
20 gates with scalar allowance 134. The new compiler emits

```text
x_0 += 2 z
x_1 -= z
z   -= 3 x_0
z   -= 5 x_1
x_0 += 2 z
x_1 -= z
z   *= -1.
```

This has seven gates and allowance 64. Both programs satisfy the same
dual-pair equations on the same three-role resource contract. Their full
matrices need not agree on the complementary subspace. The numerical
comparison concerns the predecessor's actual emitted program, not an
optimal predecessor algorithm or all possible three-role completions.
Only that one source invocation is used for the comparison. Its scientific
suite is not replayed or claimed as this contribution.

The corresponding displayed consumer has fourteen scalar gates and
allowance 128, plus G. No claim is made that this consumer bill or its sign
operations are minimal. This first small compiler improvement is the
deliverable; no larger physical search is included.

## Evidence and remaining obligations

The written algebra proves the quantified result. Exact finite replays
corroborate the emitted code, full matrices, all scalar prefixes, tariff,
and dirty-spare return for a nonscalar two-coordinate G. Deliberate
omission, sign, ordering and invalid-input controls must reject. Tests
alone are not an all-input proof or formal-kernel acceptance.

This package finds no actual P104 cut, physical native supplier, rounded
precision allocation, favorable complete paid/target invoice or new kappa.
All five selected framework assumptions remain. Classical stabilized
completion has a broad literature; for historical context see M. Roitman,
[Completing unimodular rows to invertible matrices, 1977](https://doi.org/10.1016/0021-8693(77)90280-0).
That citation is background, not a claim that this elementary block identity
or the notion of completion is new.
