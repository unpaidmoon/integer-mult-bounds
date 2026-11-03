# A grade that includes the final carry

Claim type: scoped constructive proof, with exact finite corroboration.
This contribution was produced by Nick Petalas. It builds on Chafik Boukhalfa's
PR524 mixed-radix carry filter and retains its four-product sign splitting.
It changes the grade weights and the horizontal index stride. It does not
replay or audit the predecessor's result.

## Construction

Let D >= 1, let n_0,...,n_(D-1) be positive integers, and put
N = product n_i. Coordinates satisfy 0 <= a_i < n_i. Write

    P_0 = 1, P_(i+1) = n_i P_i, I(a) = sum_i a_i P_i.

Choose an integer T > D with gcd(T,N) = 1. Such a T exists, for example any
integer congruent to 1 modulo N and larger than D. Define weights modulo T
backwards by

    w_(D-1) = 0,
    w_i = (w_(i+1) + 1) / n_i mod T,   i = D-2,...,0.

The divisions are modular inverses, which exist by coprimality. Define

    g(a) = sum_i w_i a_i mod T, with 0 <= g(a) < T,
    J(a) = I(a) + N g(a).

All input slots are distinct, since J(a) modulo N is I(a). The new stride is
N. The predecessor used 2N-1 to keep index overflow out of the grade digit.
The new weights make that overflow useful.

## All-carry identity

For any two box coordinates a,b, including those whose index sum reaches N,
let c be the mixed-radix coordinate of (I(a)+I(b)) mod N. Ordinary addition
has carries e_i satisfying

    a_i + b_i + e_(i-1) = c_i + n_i e_i,
    e_(-1) = 0, e_i in {0,1}, e_(D-1) = floor((I(a)+I(b))/N).

These statements also hold for singleton axes. The input digits then vanish,
and an incoming carry passes through that axis. Multiply the digit equations
by w_i and sum. Since n_i w_i - w_(i+1) = 1 modulo T and w_(D-1) = 0,

    g(a) + g(b) - g(c) = sum_(i=0)^(D-2) e_i mod T.

The physical addition of packed indices has one further carry:

    J(a)+J(b) = I(c) + N [g(a)+g(b)+e_(D-1)].

Consequently its grade differs from g(c), modulo T, by

    g(a)+g(b)+e_(D-1)-g(c) = sum_(i=0)^(D-1) e_i mod T.       (1)

The right side is an integer in [0,D]. Because T > D, it is zero modulo T
exactly when every carry is zero. That happens exactly when a+b=c
componentwise inside the box. Thus both internal overflow and final overflow
are rejected by the same grade test. This is the new step.

## Exact integer products and extraction

For coefficient arrays f,q, form the polynomials

    F(z) = sum_a f(a) z^J(a), Q(z) = sum_b q(b) z^J(b).

To obtain the truncated box-convolution coefficient h(c), sum coefficients of
FQ at positions

    I(c) + N g(c),
    I(c) + N [g(c)+T].

A position beyond the polynomial degree contributes zero. These are the only
possible positions with the required index and grade: each input slot is at
most NT-1, so each product slot is at most 2NT-2. Equation (1) proves that
precisely the valid componentwise sums contribute. No cancellation or
positivity assumption is needed for this polynomial identity.

To execute with signed integer coefficients, keep PR524's four nonnegative
products f+q+, f-q-, f+q-, f-q+ and combine them with signs +,+,-,- after
extraction. If |f| <= A and |q| <= B, any raw product coefficient is at most
NAB. For a fixed first coordinate and a fixed raw slot, the second coordinate
is uniquely determined by reducing the slot difference modulo N. Hence at
most N ordered pairs contribute. Evaluate each nonnegative polynomial at a
power-of-two base strictly larger than max(A,B,NAB). This also stores an
operand when the other is identically zero. No coefficient carry crosses a
slot, and exact integer digit extraction implements the polynomial proof.
The byte-aligned implementation can add up to seven alignment bits per slot;
this is explicit and is separate from the coefficient-slot claim.

Every operand has at most NT coefficient slots and every product has at most
2NT-1. The exact occupied extent for a given layout is 2 max_a J(a)+1.
Packing, extraction and four integer multiplications are paid operations;
this is a representation bound, not a noncircular multiplication-time theorem.

## Power-of-two boxes and the first improvement

When N is a power of two, choose the smallest odd T > D. It is D+1 for even D
and D+2 for odd D. The product-slot bound is therefore below 2N(D+2), compared
with PR524's below-4DN bound. In particular, for binary cubes with D >= 4 the
new bound 2NT-1 is strictly below the predecessor bound (2D-1)(2N-1).
The ratio of these two sufficient bounds tends to 1/2 as D grows.

For the same twelve-axis binary shape as PR524, N=4096, T=13 and

    w = (12,10,6,11,8,2,3,5,9,4,7,0).

The new maximum input slot is 53247, hence the product extent is 106495.
The predecessor's published recurrence and stride give extent 188391.
The exact saving is 81896 coefficient slots per product. The checker computes
these maxima over all 4096 coordinates. It also executes the four actual
integer products on the dense signed separable inputs

    f(a) = (-1)^sum(a), q(a) = 2^(12-sum(a)),
    h(c) = product_i (2 if c_i=0 else -1).

The expected output follows from the one-dimensional truncated convolution
(1,-1)*(2,1) = (2,-1), independently of grades or integer packing.
This corroborates all 4096 outputs. The written argument above gives the
all-shape theorem; finite cases alone do not.

## Scope and predecessor boundary

Ross Richardson's PR918 characterizes admissible moduli for the fixed PR524
weights and padded stride. It explicitly leaves changed weights outside its
negative result. Here T>D is sufficient, not claimed necessary or optimal.
For general radices, the smallest coprime T can be too large to improve the
old layout. No uniform advantage over all boxes is asserted. Singleton
compaction, different grade groups and modulus optimization are left open.

Rank-filtered convolution, mixed-radix addition, modular inverses and integer
polynomial packing are established techniques. The contribution is this
backward weight choice, final-carry extraction identity and its smaller
layout in the retained box-convolution interface. No literature-wide priority
for the underlying techniques is claimed.

The Gaussian recentering, analytic tables, weighted error bounds, tiling,
Schur boundaries, compiler, physical routing and caller costs from PR524's
lineage are not discharged. No new kappa, supplier admission, selected-result
change, complete multiplication theorem, independent human review or formal
proof-kernel acceptance is claimed.
