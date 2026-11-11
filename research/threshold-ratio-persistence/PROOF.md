# Persistence of the section-6 threshold comparison

Selected κ stays `363005817/100000000000`. This note proves one comparison.
It does not prove `precision_tape`, and it does not change the exponent.

## Statement

Let `C` and `d0` be integers with `C ≥ 1` and `d0 ≥ 0`, and let `a` and `b` be
positive integers. Write `δ = a/b`. For a nonnegative integer `j`, the
predicate `P(j)` means

```text
C^b (j+1)^{d0 b} ≤ 2^{a j}.
```

Both sides are positive integers, so `P(j)` is exactly

```text
C (j+1)^{d0} ≤ 2^{δ j}.
```

Let `s` be the bit length of `C`, so `2^{s-1} ≤ C < 2^s`. Set

```text
L = s b + a + d0 b,
u = ceil(log2 L),
T = 2 u + 2,
j* = 2^T - 1.
```

Since `s ≥ 1`, `a ≥ 1` and `b ≥ 1`, one has `L ≥ 2`, so `u` and `T` are
positive integers and `j*` is a nonnegative integer.

**Theorem.** `P(j*)` holds. If `d0 = 0`, then `P(k)` holds for every integer
`k ≥ j*`. If `d0 ≥ 1`, then `P(k)` holds for every integer `k ≥ j*`, and the
same persistence holds for any integer `j` that satisfies both `P(j)` and
`j + 1 ≥ ceil(8 d0 b / (5 a))`. In particular, every integer `j > 4 d0 / δ`
that satisfies `P(j)` also satisfies `P(k)` for every integer `k ≥ j`.

The last sentence is the comparison invoked by the #7000 application review,
section 6: choose `j` beyond `4 d0/δ` at which the inequality holds, and the
inequality continues. The factor `4` is sufficient. It is not claimed to be
the smallest possible factor.

## The binomial bound

For every integer `m ≥ 1`,

```text
(1 + 1/m)^m < 3.
```

Expand the left side by the binomial theorem. The summand of index `k` is
`C(m,k) / m^k = (1/k!) ∏_{i=1}^{k-1} (1 - i/m) ≤ 1/k!`. For `k ≥ 1`,
`1/k! ≤ 1/2^{k-1}`. Therefore

```text
(1 + 1/m)^m ≤ Σ_{k=0}^{m} 1/k! ≤ 1 + Σ_{j=0}^{m-1} 1/2^j
            = 1 + (2 - 2^{1-m}) < 3.
```

The last step is strict for every finite `m`. As an integer comparison,
`(m+1)^m < 3 m^m`.

## One-step persistence

Let `d0 ≥ 1` and let `m ≥ ceil(8 d0 b / (5 a))`. Then

```text
(1 + 1/m)^{d0} < 2^δ,
```

and consequently `(m+1)^{d0 b} < m^{d0 b} 2^a`.

Indeed `(1+1/m)^m < 3`, and the map `x ↦ x^{d0 b / m}` is increasing on the
positive reals, so

```text
(1 + 1/m)^{d0 b} < 3^{d0 b / m}.
```

The hypothesis on `m` says `d0 b / m ≤ 5 a / 8`, hence
`3^{d0 b / m} ≤ 3^{5 a / 8}`. From `3^5 = 243 < 256 = 2^8`,

```text
3^{5 a / 8} = (3^5)^{a/8} < (2^8)^{a/8} = 2^a.
```

Chaining these gives `(1+1/m)^{d0 b} < 2^a`, which is the integer comparison
above. The inequality is strict because `(1+1/m)^m < 3` is strict.

Now suppose `P(j)` and `m = j+1` meets the ceiling. Then

```text
C^b (j+2)^{d0 b} < C^b (j+1)^{d0 b} 2^a ≤ 2^{a j} 2^a = 2^{a(j+1)},
```

so `P(j+1)` holds. Induction gives `P(k)` for every integer `k ≥ j`.

If `d0 = 0`, the predicate is `C^b ≤ 2^{a j}`. The right side is nondecreasing
in `j` and strictly increasing for `a ≥ 1`, so one success persists for every
larger index. The step comparison is `1 ≤ 2^a`, which holds for every `j`.

## The ceiling cannot drop by one

For `(d0, a, b) = (1, 2, 5)`,

```text
ceil(8 · 1 · 5 / (5 · 2)) = ceil(4) = 4.
```

At `m = 3`, `(3+1)^5 = 1024` and `3^5 · 2^2 = 972`, so `1024 > 972` and the
step fails. At `m = 4`, `5^5 = 3125` and `4^5 · 4 = 4096`, so the step holds.
The hypothesis `m ≥ ceil(8 d0 b/(5 a))` is therefore sharp for this triple:
replacing it by one less is false. This does not say that every smaller
rational constant fails for every triple. It says that this ceiling cannot be
decreased by one inside the statement above.

## The explicit witness

Keep `L`, `u`, `T` and `j*` as in the statement. Then `2^u ≥ L` and

```text
2^T = 2^{2u+2} = 4 (2^u)^2 ≥ 4 L^2.
```

Also `u = ceil(log2 L) ≤ L - 1` for `L ≥ 2`: this is `2^{L-1} ≥ L`, true at
`L = 2`, and if it holds at `L` then `2^L = 2 · 2^{L-1} ≥ 2 L ≥ L + 1`.
Thus `2 L ≥ u + 1` and `4 L ≥ 2 u + 2 = T`. Hence `4 L^2 ≥ T L`. The
quantity to be bounded is

```text
s b + a + T d0 b = L + (T - 1) d0 b ≤ L + (T - 1) L = T L,
```

because `d0 b ≤ L`. Since `a ≥ 1`,

```text
a 2^T ≥ 4 L^2 ≥ T L ≥ s b + a + T d0 b.
```

Equivalently, `s b + T d0 b ≤ a (2^T - 1)`. Now `C < 2^s`, so `C ≤ 2^s - 1`
and `C^b ≤ (2^s - 1)^b`. For `b = 1` this is `2^s - 1`. For `b ≥ 2`,
`(2^s - 1)^b ≤ (2^s - 1) 2^{s(b-1)} = 2^{s b} - 2^{s(b-1)} ≤ 2^{s b} - 1`.
With `j* + 1 = 2^T`,

```text
C^b (j* + 1)^{d0 b} < 2^{s b + T d0 b} ≤ 2^{a (2^T - 1)} = 2^{a j*}.
```

The left side is an integer, so `P(j*)` holds.

It remains to check that `j*` lies in the persistence range. If `d0 = 0`,
the degree-zero paragraph applies. If `d0 ≥ 1`, the threshold is
`ceil(8 d0 b/(5 a))`. Here `L ≥ d0 b`, so `2^T ≥ 4 L^2 ≥ 4 (d0 b)^2`. For
every integer `z ≥ 1` and every integer `a ≥ 1`,

```text
20 a z^2 - 8 z - 5 a ≥ 0,
```

which is `4 z^2 ≥ 8 z/(5 a) + 1` after dividing by the positive number `5 a`.
The difference factors as `5 a (4 z^2 - 1) - 8 z`, and
`4 z^2 - 1 = (2 z - 1)(2 z + 1) ≥ 2 z + 1`, so
`5 a (4 z^2 - 1) ≥ 5 (2 z + 1) = 10 z + 5 ≥ 8 z`. Thus
`4 (d0 b)^2 ≥ 8 d0 b/(5 a) + 1`, and `2^T` is at least the ceiling.
Therefore `j* + 1` meets the one-step hypothesis, and `P(k)` holds for every
integer `k ≥ j*`.

## The review factor 4

Let `x = 4 d0 b / a` and suppose `d0 ≥ 1`. An integer `j > x` satisfies
`j ≥ floor(x) + 1`, hence `j + 1 ≥ floor(x) + 2`. The persistence ceiling is
`ceil(2 x / 5)`, because `8 d0 b/(5 a) = 2 x / 5`. If
`ceil(2 x / 5) ≥ floor(x) + 3`, then `2 x / 5 > floor(x) + 2`. Since
`floor(x) ≥ x - 1`, one has `floor(x) + 2 ≥ x + 1`, so `2 x / 5 > x + 1`,
hence `0 > 3 x / 5 + 1`, which is impossible for `x ≥ 0`. Therefore
`j + 1 ≥ ceil(8 d0 b/(5 a))`. Combined
with `P(j)`, the one-step paragraph gives persistence for every larger
integer. This is exactly the review's instruction to choose `j` beyond
`4 d0/δ` at which the displayed inequality holds.

The factor `4` does not by itself force `P(j)`. For `C = 1000`, `d0 = 1` and
`δ = 1`, the bound `4 d0/δ` is `4`, but `j = 5` gives
`1000 · 6 = 6000 > 2^5`. The review states both conditions, and both are
necessary for this argument.

## What is not proved

The five selected assumptions stay assumptions. The argument never reads a
selected outer predicate, a monomial recipe, or a tape alphabet. It does not
compute the least `j` for the constants in section 6, and it does not say
that freezing an input threshold at `2^{j*}` is the cutoff used by the
selected word. Open PR #7286 counts elimination records; that count is not
an input here. Finite rows in `verify.py` check the integer comparisons on
stated rectangles. They are not the proof, and a missed row would not be a
counterexample to the theorem.
