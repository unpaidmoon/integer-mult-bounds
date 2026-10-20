# The bit length 2642 is not the log_q shape coefficient

## Claim

Let `C` be the selected m=73 finite stock integer from
`research/selected-stock-envelope-m73`: `C = |Sp(72,2)| * 14826`, with

```text
|Sp(72,2)| = 2^1296 * prod_{j=1..36} (2^(2j) - 1)
14826 = 14336 + 480 + 8 + 2.
```

Then `2^2641 <= C < 2^2642`. For every integer `q > 2^80`,

```text
log_q C < 34,
```

so `A = 0` and `B = 34` satisfy the coarse-depth slot

```text
log_q C(w) <= A*w + B
```

at every atom width `w >= 1`. The integer `B = 33` does not: the prime
`q = 2^80 + 13` has `C > q^33`.

`research/selected-stock-shape-a-zero/PROOF.md` substitutes the bit length
`2642` into that same log_q composition and writes

```text
sigma <= (43/26) * (1 - s) * 2642 + rho.
```

`2642` is a valid log_q upper bound, because `log_q C < log2(C) < 2642` for
every integer `q > 2`. It is not a necessary coefficient on the selected
prime domain `q > 2^80`. The C-part of the composition, before the unbound
leaf constant `rho`, is smaller by exactly `2642/34 = 1321/17` when `34`
replaces `2642`.

## Primality

`2^80 + 13` is prime by Pocklington's criterion. Its predecessor factors as

```text
(2^80 + 13) - 1 = 2^2 * 1093 * 31039 * 8908647580887961.
```

The cofactor `F = 8908647580887961` is itself prime. Its predecessor is

```text
F - 1 = 2^3 * 3 * 5 * 3529 * 69467 * 302831,
```

and each of those six primes is proved by trial division through its square
root. The witness `29` satisfies `29^(F-1) ≡ 1 (mod F)` and
`gcd(29^((F-1)/p) - 1, F) = 1` for every prime `p` dividing `F - 1`. The
factored part is all of `F - 1`, which is larger than `sqrt(F)`.

The witness `2` then satisfies the same two conditions for every prime
divisor of `(2^80 + 13) - 1`, including `F`. That factored part is the whole
predecessor and is larger than `sqrt(2^80 + 13)`.

## Exponent comparison

`C < 2^2642` and `(2^80 + 1)^34 > 2^2720 > 2^2642`, so every integer
`q >= 2^80 + 1` has `q^34 > C`. The separate comparison `C > (2^80 + 13)^33`
is an integer power, not a floating logarithm. Together they give

```text
33 < log_q C <= 34
```

at that prime, and `log_q C < 34` for every larger integer base.

## What this does not say

`rho` stays unbound, so this note does not produce a numerical `sigma` and
does not change the selected conditional kappa `0.001672660197076918`. It
does not rerun cutoff margins, and it does not adopt the finite stock as a
physical caller. The historical coefficients `57604` and `252` are not used.
The ordinary BIT coefficients `8194`, `6748` and `6741` are a different
producer.
