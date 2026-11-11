# An integer shortening obstruction

## Contract and theorem

Let `a,b,p` be arbitrary elements of `Z^w`, where `w>=1`. The source p is
preserved. Exactly two dirty working rows A and B start at a and b. Allowed
gates have arbitrary integer coefficients and are only

```text
P0(t): A += t p       P1(t): B += t p       price mu each
E0(t): A += t B       E1(t): B += t A       price c each.
```

Prices mu and c are positive, stationary and coefficient-independent. All
gates, including inverses, are paid. There are no extra rows, free scales,
free swaps, observers, branching or free basis changes. A word is finite
and independent of its input values. Its endpoint must be

```text
A = a + 5p, B = b + 12p, with p unchanged.
```

**Theorem.** The exact minimum price over all such words is
`min(2 mu, mu+6c)`. In particular it is 16 when mu=10 and c=1.

This is a scoped algebraic tariff. The assumption of coefficient-independent
prices is a declared interface, not a claim about actual fixed-tape costs.

## Lower bound

With no source insertion, both source coefficients stay zero, so the word
cannot attain the endpoint. A word with at least two insertions costs at least
2 mu. This bound does not limit their placement or their coefficients.

Consider a word with exactly one insertion `Pi(beta)`. Let L be the 2-by-2
integer matrix of all row additions before it and C the matrix of all row
additions after it, in their chronological action order. Dirt restoration
requires `CL=I`. The source column is `beta C e_i = (5,12)^T`.

Every elementary row-addition matrix has determinant one. Each column of
C is therefore primitive. Equivalently, its coordinates have gcd one,
because the corresponding row of C inverse is an integral Bezout witness.
The source equation gives `|beta|=gcd(5,12)=1`. Thus
`C e_i` is either `(5,12)^T` or `(-5,-12)^T`.

Neither signed column can be obtained from either coordinate vector with
at most two integer row additions. Consecutive additions in one direction
combine into one. Of the two alternating orders, one has an initially
inactive first gate. The only remaining possibilities, including shorter
words, are

```text
from e0: (1,t) or (1+s t,t),
from e1: (t,1) or (t,1+s t),        s,t in Z.
```

For e0, the latter form would require t=12 or t=-12. Its first coordinate
is 1 modulo 12, whereas 5 and -5 are not. The former form has first
coordinate one. For e1 the latter form would require t=5 or t=-5. Its
second coordinate is 1 modulo 5, whereas 12 and -12 are not. The former
form has second coordinate one. All possibilities fail.

Consequently every suffix C uses at least three row additions. Every
prefix L uses at least three as well. Otherwise reversing its at-most-two
gates and negating their coefficients would express `L^-1=C` with at most
two gates, contradicting the same column obstruction. Exactly one insertion
therefore costs at least `mu+6c`. Together with the insertion-count split
this proves the lower envelope. Arbitrarily large integer coefficients and
arbitrarily long interleavings have not been bounded or omitted.

## Attainment

Let C be the following three row additions in chronological order

```text
E1(2), E0(2), E1(2).
```

Their matrix is `[[5,2],[12,5]]`, with determinant one and first column
(5,12). Perform C inverse, then `P0(1)`, then C. In literal order this is

```text
E1(-2), E0(-2), E1(-2), P0(1), E1(2), E0(2), E1(2).
```

Every dirt column returns and the source contribution is exactly (5,12).
The price is `mu+6c`. Direct insertions `P0(5),P1(12)` cost 2 mu. These
two words attain both branches of the envelope, including their tie at
mu=6c. Since equality of the full integer coefficient matrices implies
equality on each coordinate, both constructions work for every w>=1.

## Why finiteness matters

Ali Romman's PR5312 extends lee-phys's finite-commutative formula to finite
associative rings. Its shortening step is expressly finite; this package
does not dispute that theorem. Formally applying its five-term formula over
Z to demand (5,12), with equal directional prices, would give
`min(2mu,mu+4c)`: the demand ideal is principal and neither demand divides
the other. At mu=10,c=1 this is 14, strictly below the proved optimum 16.

Thus principality alone does not justify that finite-length tariff over
integer coefficients. This example does admit one insertion; its extra
restoration cost, rather than infeasibility, is the obstruction. The result
does not exclude a different integer formula, extra dirty rows, rational or
dyadic coefficients, coefficient-dependent pricing or a different caller.

## Finite evidence

The new verifier checks the complete 3-by-3 operators, literal dirty inputs,
both attaining costs and semantic mutations. It also enumerates every
column reachable in at most two shears over Z/60Z, with all sixty residue
coefficients in each direction. Both signed target columns are absent from
both origins. A separate direct normal-form set gives the identical result.
Every integer two-shear word maps into this finite quotient, so this is
also an independently rerunnable finite certificate of that local step.
It does not replace the written insertion-count and restoration argument.

Elementary matrices, primitivity and Bezout identities are classical. The
new repository result is this exact integer tariff and its finite-ring
extension discriminator; global literature priority is unclaimed.
