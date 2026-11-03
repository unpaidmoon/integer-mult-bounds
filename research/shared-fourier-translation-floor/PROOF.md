# Sharp error for a shared translated Fourier routine

This proof and its application were produced by Nick Petalas. Apache-2.0.

## Contract and result

Let G be any finite product of cyclic groups, N=|G|, with its standard
symmetric nondegenerate character pairing chi. Write

    (F± u)(x) = (1/N) sum_y chi(x,y)^±1 u(y).

Both signs have the factor 1/N. Convolution has no normalization. Let
b be a nonzero element of order two, let P_b f(x)=f(x+b), and let w(x)
be an arbitrary complex function with |w(x)|=1. Use exactly the same
routine A=D_w P_b F− for the two forward passes, and conjugate its
coefficients for the final pass. Thus

    B_w(u,v) = D_conj(w) P_b F+ [(D_w P_b F−u)(D_w P_b F−v)],
    B(u,v)   = (u*v)/N².

For a bilinear map L, define its coefficient Frobenius norm by

    ||L||_F² = sum_(s,t in G) ||L(e_s,e_t)||_2².

The normalization gives ||B||_F=1/N. Define

    E(w) = N ||B_w-B||_F,
    R(w) = N² max_(s,t in G) ||B_w(e_s,e_t)-B(e_s,e_t)||_2.

These are respectively a relative coefficient norm and the largest
relative output error among the basis-input pairs. No relative error
claim for arbitrary inputs with possibly zero convolution is intended.

**Theorem.** For every such G and b,

    min_(|w|=1) E(w) = min_(|w|=1) R(w)
                    = sqrt(2 - 8/(3 sqrt(3))).                 (1)

The same explicit weights attain both minima:

    c(x) = chi(b,x),
    w(x) = 1/sqrt(3) - i sqrt(2/3) c(x).                       (2)

Moreover, every basis-input pair has the same normalized error in (1)
for these weights. The constant is independent of N and of chi(b,b).

The new claim is this quantitative optimum for the shared translated
contract. Hanson Sun / bbMisk's PR1477 supplies the predecessor exact
weighted-layout classification and normalization, extending Ross
Richardson's PR940. It already excludes exact convolution here. No part
of that classification or its census is claimed as new.

## Reduction to two scalar moments

The character c takes values +1 and −1. It is nontrivial by
nondegeneracy and b!=0. Consequently the two signs each occupy N/2
points. Set f=F−u, g=F−v and compare the coefficient of
f(y+b)g(y+b) in output x before substituting f,g. The implemented and
desired coefficients are respectively

    (1/N) conj(w(x)) w(y)² chi(x+b,y),
    (1/N) chi(x,y+b).

Their ratio is

    rho(x,y) = conj(w(x)) w(y)² c(x)c(y).                      (3)

There are no off-diagonal input products because the two forward read
maps agree. Each of the N² desired coefficients has modulus 1/N.
The matrices sqrt(N) F− are unitary. Substitution of F− in each of
the two input indices therefore multiplies the squared coefficient
norm by 1/N². It follows that

    E(w)² = (1/N²) sum_(x,y) |rho(x,y)-1|².

Define a(x)=c(x)w(x), with |a|=1, and use uniform expectations on G:

    m = E a,              n = E c a².

The average of rho is conj(m)n. Thus

    E(w)² = 2 - 2 Re(conj(m)n).                               (4)

This identity is exact. In particular, the normalization does not hide
an error that decays with N relative to the desired basis output.

## The scalar inequality

We prove |m n| <= 4/(3 sqrt(3)) for every unit-valued a on a
balanced two-class probability space. Write

    u = E[a | c=+1],       v = E[a | c=−1],
    p = E[a² | c=+1],      q = E[a² | c=−1],
    d = (u-v)/2,           r=|m|,      s=|d|.

Since m=(u+v)/2, n=(p-q)/2, and |u|,|v|<=1, we have
r²+s²=(|u|²+|v|²)/2<=1. The conditional variance identity gives

    |p-u²| = |E[(a-u)² | c=+1]| <= 1-|u|²,
    |q-v²| <= 1-|v|².

Taking the triangle inequality and using u²-v²=4md yields

    |n| <= 2rs + 1-r²-s² = 1-(r-s)².                         (5)

If r<=1/sqrt(2), the elementary |n|<=1 gives
|mn|<=1/sqrt(2)<4/(3 sqrt(3)). If r>=1/sqrt(2), then
s<=sqrt(1-r²)<=r. The right side of (5) increases with s throughout
this interval. Hence

    |mn| <= 2r² sqrt(1-r²).

For x=r², the following polynomial identity proves the required
maximum on [1/2,1], without a numerical optimization:

    16/27 - 4x²(1-x) = (4/27)(3x-2)²(3x+1) >= 0.             (6)

Equations (4) and (6) imply E(w)²>=2-8/(3 sqrt(3)). Also

    R(w)² = N⁴ max_(s,t) ||(B_w-B)(e_s,e_t)||²
          >= N² sum_(s,t) ||(B_w-B)(e_s,e_t)||² = E(w)².

This proves both lower bounds in (1).

## Equality on every basis pair

Set h=1/sqrt(3), r=sqrt(2/3), and choose w=h-i r c. These weights
have modulus one. Then a=h c-i r, so

    m = -i r,             n = -2i h r,
    conj(m)n = 2h r² = 4/(3 sqrt(3)).

This proves equality for E. To establish equality for R as well,
calculate the actual three-pass output on e_s,e_t. Let k=s+t and note

    w(y)² = -1/3 - (2i sqrt(2)/3)c(y).

Character orthogonality leaves only two output coordinates, k and k+b.
They are distinct since b!=0. Their values, multiplied by N², are

    at k:     4/(3 sqrt(3)) - (2i sqrt(2)/(3 sqrt(3))) c(k),
    at k+b:   -(1/3)c(k) conj(w(k+b)).                         (7)

The second has modulus 1/3 regardless of chi(b,b). The desired
normalized output is one at k and zero elsewhere. Its squared error is

    (4/(3 sqrt(3))-1)² + 8/27 + 1/9
      = 2 - 8/(3 sqrt(3)).

It is the same for every s,t. This proves (1) and (2).

## Scope

The argument covers every unit complex phase function, every product of
cyclic groups, and every nonzero order-two translation under the stated
shared-routine contract. The finite checker covers only its listed tiny
groups and phases. The universal assertion comes from this written proof.

Separate forward/final phases escape the theorem. For example, the same
translation with forward weights alpha=1, beta=c and final weight omega=c
gives exact convolution, as in the predecessor affine criterion. This is
an explicit control of the hypothesis, not a new construction claim.

The optimum uses algebraic phases, and their preparation or application is
not priced. Other-order translations, arbitrary affine maps, general
unit-norm-input operator error and rounded implementations are not settled.
No physical caller, recursive saving, supplier admission, selected-frontier
change or complete multiplication theorem follows. Independent human and
formal proof-kernel review are unclaimed.
