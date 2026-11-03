# One permutation on both Fourier indices

This contribution was produced by Nick Petalas. Apache-2.0.

## Contract and theorem

Let `D >= 1`, and let `s_1,...,s_D >= 2` be pairwise-coprime integers.
Put `N = product_i s_i`, `M_i = N/s_i`, and
`G = product_i Z/(s_i)`. Representatives are canonical integers.
Use the standard positive-exponent, unnormalized Fourier kernels

```text
K_N(a,b) = exp(2 pi i a b / N),
K_G(x,y) = exp(2 pi i sum_i x_i y_i / s_i).
```

The same statements hold with both exponent signs reversed, or with the
usual unitary normalization on both sides. Normalizing just one side does
not give the displayed identity.

A bijection `f: G -> Z/(N)` satisfies

```text
K_N(f(x), f(y)) = K_G(x,y)                  for every x,y in G       (1)
```

if and only if it has the form

```text
f(x) = sum_i M_i v_i x_i mod N,
M_i v_i^2 = 1 mod s_i                     for every i.             (2)
```

Consequently, such an `f` exists exactly when every `M_i` is a square
unit modulo `s_i`. The number of such bijections is the product of the
numbers of solutions to the local congruences in (2). These are all the
solutions, even when the initial search allows arbitrary nonlinear
permutations.

This is an exact interface classification. Local roots are fixed to the
standard roots in the displayed kernels. There are no extra diagonal
phases, changes of local primitive root, different permutations on the two
indices, or arbitrary linear input/output transforms.

## Necessity, including arbitrary bijections

Equality of the two roots of unity in (1) is equivalent to

```text
f(x) f(y) = sum_i M_i x_i y_i mod N.                                (3)
```

Since `f` is onto, there is a `y_*` with `f(y_*) = 1`. Taking `x=0` in
(3) gives `f(0)=0`. For any `x,x',y`, subtract the three instances of (3)
at `(x+x',y)`, `(x,y)` and `(x',y)`. The right sides cancel modulo `N`,
including any coordinate wrap, because `M_i s_i=N`. Thus

```text
(f(x+x') - f(x) - f(x')) f(y) = 0 mod N.
```

Take `y=y_*`. It follows that `f` is a group homomorphism. Nonlinear
bijections cannot evade this conclusion.

Let `e_i` be the unit vector in factor `i`. Since `s_i e_i=0`, additivity
gives `s_i f(e_i)=0 mod N`. Hence `M_i` divides the canonical integer
`f(e_i)`, and `f(e_i)=M_i v_i` for a unique `0<=v_i<s_i`. Every group
homomorphism is determined by these images, so `f` has the stated form.
Taking `x=y=e_i` in (3) gives

```text
M_i^2 v_i^2 = M_i mod N.
```

Divide the integer divisibility statement by `M_i` to obtain
`M_i v_i^2=1 mod s_i`. In particular `v_i` and `M_i` are units modulo
`s_i`. Then `M_i=(v_i^-1)^2 mod s_i`, proving the square-unit condition.

## Sufficiency and exact count

Suppose (2) holds. Modulo `s_i`, all terms of `f` except its `i`th term
vanish. The surviving coefficient `M_i v_i` is a unit. Thus the reductions
of `f` are independent invertible rescalings on the factors. The Chinese
remainder theorem proves that `f` is a bijection.

For distinct indices `i,j`, `N` divides `M_i M_j`. Expanding `f(x)f(y)`
therefore removes every cross term modulo `N`. Each remaining diagonal
term is `M_i^2 v_i^2 x_i y_i = M_i x_i y_i mod N`, by (2). This proves
(3), and hence (1).

If `M_i=w_i^2 mod s_i` for a unit `w_i`, take `v_i=w_i^-1`. This proves
existence from the square-unit condition. Finally, independent choices of
the `v_i` give distinct images of the generators `e_i`, so their product
counts all maps without duplication. QED.

## Explicit positive and negative instances

For axes `(13,17)`, all four coefficient tuples `f(e_1),f(e_2)` are

```text
(102,26), (102,195), (119,26), (119,195).
```

For example `102^2=17 mod 221`, `26^2=13 mod 221`, and `102*26=0 mod 221`.
The map `f(x,y)=102x+26y mod 221` is a bijection and identifies every one
of the `221^2` Fourier phases. The verifier checks each of the four maps.

For `(3,5)`, the complementary product `5=2 mod 3` is a nonsquare, so no
common permutation exists. For `(3,7)`, the first local test passes but
`3 mod 7` is a nonsquare, so the second test excludes every permutation.
This illustrates why testing just one axis is insufficient.

These exclusions do not forbid ordinary Good–Thomas tensorization. With
`u_i=M_i^-1 mod s_i`, its two address maps are

```text
a(x)=sum_i M_i u_i x_i mod N,
b(y)=sum_i M_i y_i mod N.
```

They satisfy the two-map Fourier identity for every pairwise-coprime grid,
including the two excluded shapes. This is the predecessor interface of
David Ganz / Dugongue's PR5564, not a new result here. The new question is
whether its two indices can share a single permutation while preserving
standard local roots. No criticism of its distinct-map convention is implied.

## Proof and execution boundaries

The universal theorem is the written argument above. The exact Python
reference enumerates local roots and independently enumerates cyclic
homomorphisms through their generator images, then compares the resulting
maps using integer phase congruences. Complete tiny permutation domains
also include every nonlinear bijection and every translation. These finite
checks corroborate the theorem; they do not establish its quantifiers by
extrapolation. Neither floating-point Fourier matrices nor approximate
phase equality are used.

The constructor is an offline bounded reference, not an efficient modular
square-root algorithm or a native physical program. Root testing can take
linear time in an axis value, and emitting a permutation takes `N` entries.
No reduced head movement, storage, coefficient-generation cost, rounded
resampling, complete paid recurrence, supplier admission or new kappa is
inferred. Standard-root phase conventions must be matched before applying
the theorem to a particular physical caller. The five selected framework
assumptions are unchanged.
