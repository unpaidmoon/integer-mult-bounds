# Exact counts for the physical Gaussian carve

This contribution was produced by Nick Petalas. Apache-2.0.

## Contract and source

Let s,k,w be positive integers, k<s, t=s+k, and assume

    floor(s/(2k)) > 4w.                                      (1)

For each integer x, let j be its residue in [0,s), p=floor(x/s), and

    q_j=floor(tj/s+1/2),     h_j=q_j-j=floor(kj/s+1/2).

A physical cell is a maximal interval on which the pair (p,h_j) is
constant. The source cuts at physical period seams even if the unwrapped
phase does not change there. For a nonempty window [a,a+m), intersect it
with these cells. A piece of length L contributes

    f(L) = L  if L<=4w,
           2w if L>4w,                                      (2)

boundary rows. A piece is called long exactly when L>4w.

This is the carve in Jose Manuel / jmbarrancoml's PR3851,
`gaussian_axis.py:prepare_weights` and
`gaussian_window.py:prepare_positions,emit_cell`, retained at
`7ab67b4a84d28cd562b9711aa315ca5b47822b37`. Its numerical and physical
correctness are cited premises, not rechecked results. The construction
and credit of its Gaussian, RaD, PR481/486/489 and physical-word predecessors
remain with their sources. Dugongue's PR5566 already uses complete Beatty
runs for another inverse algorithm; the floor identity and general run
viewpoint are credited, rather than claimed as new mathematics.

The new result is the exact count for this physical-period carve, its
long-piece count and a smaller allowance for the unchanged caller.

## Every complete cell is long

In one physical period the phases are 0,...,k. Define their cuts

    A_0=0,  A_(k+1)=s,
    A_c=ceil(s(2c-1)/(2k)) for 1<=c<=k.

The phase-c cell is exactly [A_c,A_(c+1)). This follows by solving
c<=kj/s+1/2<c+1 for the integer j, including the half-open right
endpoint. The first cell has length ceil(s/(2k)), the last has length
floor(s/(2k)), and each other length is floor(s/k) or ceil(s/k).
Consequently every complete physical cell has length at least
floor(s/(2k)), and is long by (1). There are k+1 complete physical cells
per period. The two half-runs at the ends must not be merged.

The source production hypotheses include integer d with

    k/s < 1/(2d-1),       d-2 > 4w.

They imply s/(2k)>d-1/2, hence floor(s/(2k))>=d-1>4w.
Thus (1) follows in that domain. Other production, locality and numerical
hypotheses are not needed for this counting lemma and are not discharged.

## Exact constant-size formula

The cell containing x has ordinal

    g(x)=floor(x/s)+floor(kx/s+1/2).                         (3)

Indeed, writing x=ps+j gives g(x)=p(k+1)+h_j. Consecutive physical cells
increase this ordinal by one, including negative periods and physical
seams. If c=h_j, its left and right endpoints are

    ell(x)=ps+A_c,          r(x)=ps+A_(c+1).                (4)

Set b=a+m and C=g(b-1)-g(a)+1. This is exactly the number of nonempty
pieces meeting the window. If C=1, then

    n_B=f(m),             c_long=[m>4w].                   (5)

Otherwise let L=r(a)-a and R=b-ell(b-1). Then

    n_B = 2w(C-2)+f(L)+f(R),
    c_long = C-2+[L>4w]+[R>4w].                            (6)

Only the first and last pieces can be clipped. Each of the other C-2
pieces is a complete long cell, proving both equations. The interior-row
count is exactly m-n_B. The formulas hold for any positive window length,
including multiple periods and arbitrary signed starts.

The formula uses a fixed number of exact integer operations, independent
of the number of rows or cells. This is an arithmetic-operation statement,
not a constant bit-time claim or an encoded tape implementation. Integer
division and descriptor access still need their physical charges.

## A smaller source-domain allowance

For 1<=m<=s, each floor difference in (3) is bounded above by the ceiling
of its argument increment. The period difference is at most one. Hence

    C <= 2+ceil(k(m-1)/s).

For C>=2, f(L),f(R)<=4w, so (6) gives n_B<=2w(C+2). For C=1,
f(m)<=4w also obeys the following bound. Since n_B<=m in every case,

    n_B <= min(m, 2w ceil(k(m-1)/s)+8w).                  (7)

The source's actual window satisfies s-m>w and therefore m<s, so it is
covered. With theta=k/s and the source inequality theta<1/(2d-1),

    2w ceil(theta(m-1))+8w
        < 2theta mw+10w
        < 2mw/(2d-1)+10w
        < 4mw/d+12w.                                    (8)

The last inequality uses d>=1 and w,m>0. Thus the new untrivialized
allowance is strictly smaller than the published allowance; capping both
allowances by m can make them equal on short windows. No new carve,
word, numerical output or recursive paid profile is asserted.

## Exact strict example and complete invoice substitution

Take s=480,t=485,k=5,w=3,d=48 and [a,b)=[0,384). The phase-piece
lengths are

    48, 96, 96, 96, 48.

They are all long. Equations (5)-(6) give n_B=30, c_long=5 and n_I=354.
The published allowance is 4*384*3/48+12*3=132. Equation (7) is
6*ceil(5*383/480)+24=48. This is a strict improvement of an upper bound
for the same carve, not a changed execution. The ratio/spacing hypotheses
hold; this small fixture is not an asymptotic production payload.

The source's word-API count is

    20 n_I + 16w^2 c_long + 2 n_B(4w+1)
        + 2m + 2n_target + 2n_core + 32 c_long.

Substitute n_I=m-n_B to obtain

    22m+(8w-18)n_B+(16w^2+32)c_long+2n_target+2n_core.       (9)

At fixed c_long=5, the old n_B allowance gives 10120 plus the last two
terms, (7) gives 9616, and the exact count gives 9508. These totals are
derived solely from the displayed source tariff. They do not claim fewer
calls in the unchanged program. For w>=3 the n_B coefficient is positive,
so an upper bound can be substituted in (9); for w=1,2 it is negative
and that substitution would be invalid. Exact equations (5)-(6) remain
valid for every w. The full tensor/setup/native invoice and all inherited
numerical premises remain separate.
