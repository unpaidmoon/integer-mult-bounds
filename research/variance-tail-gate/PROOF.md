# A variance-sensitive compiler tail screen

This contribution was produced by Nick Petalas. Apache-2.0.

The two-moment exponential majorant below is classical. In particular, it is
Seneta and Weber's 1982 Corollary 1(ii), after centering, which credits Brook
for the nonnegative-variable case. The new contribution is the optimized
strict compiler-gate criterion, its equality scope and the integer histogram
separation in section 5. No priority for the probability inequality is claimed.

## 1. Contract and cited gate implication

For nonempty positive finite target and paid histograms, fix 0<t<1 and write

```text
T(t) = sum_k W_k k^t,       P(t) = sum_r P_r r^t,
q = T(t)/P(t) >= 1,        mu_P = P'(t)/P(t).
```

Take a declared containing interval [A,B] for target log ranks, with B>A.
For a target rank sampled with probability W_k k^t/T(t), set

```text
Z = (log k-A)/(B-A),       p = E Z,       v = Var Z,
x = (mu_P-A)/(B-A),        h = lambda (B-A).
```

Assume 0<x<p<1 and 0<v<=p(1-p). The source's scalar criterion is

```text
F(lambda) = T(t-lambda) exp(lambda mu_P)/P(t)
          = q E exp[-h(Z-x)] < 1, for some lambda>0.            (1)
```

Dillon Amburgey's PR4532 supplies the implication from a strict passing
point to positive integer compiler heights and rational tail parameters
for the three tail/ordering gates. Nick Petalas's PR5254 states that
contract and its range-and-mean specialization. Those results are cited
premises, not independently rechecked here. Mirror coverage, recurrence
funding and native realizability are separate obligations.

A containing interval need not be the exact range. This distinction
matters to sharpness and equality below.

## 2. The sharp statistical screen

Define

```text
b = p+v/p,       theta = p/b,       alpha = x/b,
D(alpha||theta) = alpha log(alpha/theta)
                 +(1-alpha) log((1-alpha)/(1-theta)).
```

Then 0<alpha<theta<1 and p<b<=1. For every h>0,

```text
E exp[-h(Z-x)] <= exp(hx) [1-theta+theta exp(-hb)].             (2)
```

Equality at any h>0 holds exactly for the law with masses 1-theta at
0 and theta at b. This law has the specified mean and variance. The right
side of (2) has a unique positive minimum, at

```text
h* = (1/b) log[theta(1-alpha)/(alpha(1-theta))],
minimum = exp[-D(alpha||theta)].                              (3)
```

Consequently every law on the containing interval with these moments has
a strict passing point if and only if

```text
q exp[-D(x/b || p/b)] < 1.                                   (4)
```

This is an exact worst-case guarantee from these statistics. It is not a
necessary test for an individual law. At equality in (4), the two-point
law fails, while every other law with those moments passes at h*. In
particular, when [A,B] is the actual target range and v<p(1-p), equality
passes: the target has positive mass at Z=1>b and is not the extremizer.
For that smaller exact-range class the two-point attainment claim is not
made. Above the threshold, failure of this sufficient screen is inconclusive
for an individual histogram.

## 3. Proof of the transform bound and equality

For h>0 put f(z)=exp(-hz). Let Q(z)=1+c z+d z^2, where

```text
c = ((2+hb) exp(-hb)-2)/b,
d = (1-(1+hb) exp(-hb))/b^2.
```

These coefficients give Q(0)=f(0), Q(b)=f(b), Q'(b)=f'(b).
The Hermite remainder at z>=0 is

```text
f(z)-Q(z) = f'''(xi) z(z-b)^2/6 <= 0.                        (5)
```

For z distinct from 0,b, xi lies in the interval spanned by 0,b,z.
The repeated-node remainder follows by applying Rolle's theorem three
times to f-Q-C z(z-b)^2, with C chosen to give its additional zero at z.
Since f''' is strictly negative, (5) is strict except at 0,b.
Thus the classical bound applies on the whole nonnegative half-line,
including z>b. No unjustified restriction of z to [0,b] is used.

The identity E Z^2=p^2+v=p b yields

```text
E Q(Z) = 1+c p+d p b = 1-p/b+(p/b) exp(-hb).
```

Multiplication by exp(hx) proves (2). Its equality condition follows from
the strict pointwise remainder. The mean forces mass p/b at b, and direct
calculation gives variance p b-p^2=v. The extremal law is therefore unique.

With u=hb, differentiate

```text
G(u) = (1-theta) exp(alpha u)+theta exp(-(1-alpha)u).
```

Its second derivative is positive, its derivative at zero is alpha-theta<0,
and its derivative eventually becomes positive. Solving G'(u)=0 gives
exp(u)=theta(1-alpha)/(alpha(1-theta)). Substitution proves (3).
The extremal law attains this entire envelope, so sufficiency and necessity
of the worst-case statement (4) follow without a minimax interchange.
At equality the strict remainder proves the assertion for every other law.

If v=0, Z=p almost surely and the criterion passes for every finite q>=1
because x<p. This degenerate case is separate from formulas containing
theta=1. Cases outside 0<x<p<1 are not part of this screen.

## 4. Strict improvement over the mean-only guarantee

Suppose 0<v<p(1-p), so b<1. The extremal law in section 2 assigns positive
mass to the strict interior point b of [0,1]. Strict convexity therefore
puts its transform strictly below the endpoint chord

```text
exp(hx) [1-p+p exp(-h)]
```

at every h>0. Evaluate at the positive minimizer of that older chord and
then minimize the new envelope. This proves

```text
exp[-D(x/b||p/b)] < exp[-D(x||p)],
D(x/b||p/b) > D(x||p).
```

At the maximum variance v=p(1-p), b=1 and the screens coincide. Thus the
new statistic gives a strict threshold gain at every nonmaximal positive
variance, while preserving the old screen at its endpoint case.

## 5. A new exact integer histogram separation

Take t=1/2 and the abstract histograms

```text
W_4=32, W_64=16, W_1024=2,       P_32=43.
```

Choose an ambient m>1024 if needed by the source gate contract. The tilted
target weights are 64,128,64, so T(t)=256. P(t)=172 sqrt(2), and
q=32 sqrt(2)/43>1. The normalized log-rank positions are 0,1/2,1;
therefore

```text
p=1/2, v=1/8, x=3/8, b=3/4, theta=2/3, alpha=1/2.
```

The new guaranteed minimum is exactly

```text
q exp[-D(1/2||2/3)] = (32 sqrt(2)/43)(2 sqrt(2)/3)
                           = 128/129 < 1.
```

Its h* corresponds to the rational lambda=1/6. For the actual histogram,
write a=2^(1/3). Its literal scalar criterion at that lambda is

```text
F(1/6) = (16+16a+4a^2)/43 < 1.
```

The rational bound a<63/50 proves this last inequality exactly, since
(63/50)^3>2 and 16+16(63/50)+4(63/50)^2<43.
The bound 128/129 is a statistical guarantee, not the actual minimum of
this three-rank histogram. No optimality of lambda for that histogram
is asserted.

The older range-and-mean screen fails. The eighth power of its optimized
criterion is

```text
[q exp(-D(3/8||1/2))]^8 = 2^60/(3^3 5^5 43^8) > 1.
```

This is an exact integer comparison. The new histogram therefore passes
the cited scalar-to-gate implication where the older statistical screen
cannot certify it. It is not claimed to fail the actual older gate
criterion: that criterion is the same (1).

These are abstract integer histograms. No native supplier, mirror coverage,
recurrence funding, physically owned/restored caller, precision/stock bound,
outer multiplication theorem or new kappa follows. No selected artifact is
changed.

## References and credit

- E. Seneta and N. C. Weber, *Attainable bounds for expectations*, Journal of
  the Australian Mathematical Society A 33 (1982), 411-420, Lemma 2,
  Theorem 1(ii), Corollary 1(ii),
  [original paper](https://doi.org/10.1017/S144678870001884X).
  Their quadratic bound and two-point equality classification are classical
  premises, rederived here to make the application self-contained.
- Nick Petalas, [PR5254](https://github.com/CrocSwap/integer-mult-bounds/pull/5254),
  normalized gate criterion and the older range-and-mean screen.
- Ali Romman, [PR5345](https://github.com/CrocSwap/integer-mult-bounds/pull/5345),
  the distinct prescribed-interior-mass screen. No interior-mass theorem is
  reverified or claimed here.
- Dillon Amburgey, [PR4532](https://github.com/CrocSwap/integer-mult-bounds/pull/4532),
  the scalar-to-gate equivalence; zxv PR4436/4483, Jacob Alan Sussman,
  Ryanson Jonathan PR4459 and their retained compiler/native/outer lineage.

The classical bound and relative-entropy calculation retain their classical
credit. Only this optimized compiler application and histogram separation
are claimed as the contribution. Independent human and formal proof-kernel
review are unclaimed.
