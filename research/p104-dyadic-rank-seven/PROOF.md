# An exact Gaussian-dyadic Hermitian projection below the real P104 floor

Jerry Chen (@CubeJerry), substantial OpenAI Codex assistance. Apache-2.0.

## Statement and scope

Let R contain one squared-norm-two representative from each of PR6211's
104 root lines: all 56 D8 lines and the 48 odd half-spin lines remaining
after the sixteen omissions in the pinned MISSING.json. Set S=2R and
K=RR^T/2=SS^T/8. There is a Hermitian orthogonal projector D over
Z[i,1/2] with complex rank seven such that

    C = R D R^T / 2,
    rank_C C = 7,       0 <= C <= K,
    max_(j,k) |K_jk-C_jk| = 16193/65536 < 1/4.

The modulus is the complex modulus. The contraction 0<=D<=I concerns the
eight-dimensional carrier, not C relative to the 104-dimensional identity.
This answers PR6211's first open question, the exact Gaussian-dyadic
Hermitian projector. It is not an optimality or physical-supplier theorem.

## Preserve the projection identity before approximating its coefficients

Take the Gaussian-integer vector

    z = (73-53i, 31+118i, 73-51i, 88+16i,
         73-51i, -15-51i, -87-15i, -88-17i).

Its squared norm is N=z* z=65536=2^16. Put P=zz*/N and D=I8-P.
Since P*=P and P^2=z(z*z)z*/N^2=P, P is a rank-one Hermitian orthogonal
projector. Thus D*=D, D^2=D, rank_C D=7 and 0<=D<=I. All its entries
are Gaussian-dyadic with common denominator 2^16. This exact identity
would not follow from entrywise dyadic rounding of an old matrix.

The eight retained roots e_0 +/- e_1, e_2 +/- e_3, e_4 +/- e_5 and
e_6 +/- e_7 form an orthogonal basis, so R has column rank eight.
Multiplication on the left by R and on the right by R^T preserves the
rank of D: these maps have left and right inverses respectively. Also
C=(RD)(RD)*/2 and K-C=(Rz)(Rz)*/(2N). Hence C has rank seven and
0<=C<=K. Since R is dyadic, every C coefficient is Gaussian-dyadic.
The sufficient common denominator is 8N; the largest reduced component
denominator is actually 2^17, as the complete certificate checks.

## Complete entry-error certificate

Write w=Sz. Then K-C=ww*/(8N). For any complex vector w,
max_(j,k)|w_j conjugate(w_k)|=max_j|w_j|^2: a diagonal entry attains
the product bound. Exact enumeration of every retained row gives:

| Root family | Rows | Maximum squared response |
| --- | ---: | ---: |
| D8 | 56 | 129544 |
| Odd half-spin | 48 | 128596 |
| Complete instance | 104 | 129544 |

Use PR6211's order: D8 pairs lexicographic, signs minus then plus,
followed by lexicographic half-spin tails. The unique maximum is row 24,
S_24=2(e_1-e_7), where (Sz)_24=238+270i. Therefore

    max |K-C| = (238^2+270^2)/(8*65536) = 16193/65536,
    1/4 - max |K-C| = 191/65536 > 0.

The primary verifier reconstructs the root set and checks all 10,816
entries of the literal product SDS^T/8 against the residual formula.
It does not trust the search maximum. Rational Gaussian elimination
separately checks the rank of D and an eight-root principal minor of C.

The second arithmetic path imports no primary or predecessor executable.
It uses separately ordered roots and Fraction arithmetic on the 16-by-16
realification, checking symmetry, idempotence and rank fourteen. It
independently evaluates every residual entry using real and imaginary
outer products. Both paths are by the same contributor with AI assistance;
this is not independent human or formal-kernel review.

## Real and operator-norm boundaries

Writing z=u+iv gives

    u^T u=40230, u^T v=-2683, v^T v=25306,
    det Gram(u,v)=1010861891 > 0.

The two nonzero eigenvalues of uu^T+vv^T are positive and sum to N,
so each is less than N. Thus Re(D)=I-(uu^T+vv^T)/N is positive
definite and Re(C) has real rank eight. This does not yield a
seven-real-mode approximation or contradict PR6191's real theorem.

For this root set S^T S=104 I, checked exactly. Thus ||w||_2^2=104N
and ||K-C||_2=104N/(8N)=13. The largest eigenvalue of K is also 13.
Smaller maximum coefficient error therefore does not supply vanishing
operator error: worst-case relative spectral error is one. This is a
scope calculation, not a new optimality result.

Exact reconstruction of K through a linear seven-dimensional intermediate
is impossible, since rank K=8. Retaining the lost scalar response gives
the elementary seven-plus-one reconstruction, with eight independent
pieces of information before acquisition, transport or restoration costs.
No free residual correction or completed recursive invoice is assumed.

## Bounded discovery

The guide is PR6211's stronger Gaussian-rational witness, written as
sixteen interleaved real coordinates:

    a=(14,-10,6,23,14,-10,17,3,14,-10,-3,-10,-17,-3,-17,-3),
    sum a_i^2=2456.

For k=4,...,9 in increasing order, let
q_i=floor(2^k a_i/sqrt(2456)), restrict y_i to {q_i-1,q_i,q_i+1},
and require sum y_i^2=4^k. Floors are calculated with integer square
roots and sign-aware exact comparisons. On that sphere, minimizing
squared distance from 2^k a/sqrt(2456) is equivalent to maximizing a dot y.

The DP keeps the largest dot product at each partial squared norm.
The remaining coordinate choices depend only on the norm and position,
so a lower-scoring prefix cannot produce a better completion. Remaining
minimum/maximum squared norms discard only infeasible completions.
The nonce 0b7fc9054fc70396e2d971f95342f0a4 rotates the coordinate order
by four; tied scores take the lexicographically largest tuple in that
order. One selected nearest vector at each scale is tested for its error.

| k | Error of the selected nearest vector | Strictly below 1/4? |
| ---: | --- | --- |
| 4 | 37/128 | no |
| 5 | 17/64 | no |
| 6 | 4121/16384 | no |
| 7 | 257/1024 | no |
| 8 | 16193/65536 | yes; stop |

The search stops at k=8, leaving k=9 unsearched. Each completed box has
3^16 possible tuples before the norm constraint; the DP compresses them
by exact sufficient state. WITNESS.json retains all five selected vectors,
scores, state counts and transitions. search.py reproduces this record.
The certificate's validity does not depend on DP completeness.

These are not error optima or smaller-denominator exclusions. Another
vector in the same box might have lower error. No larger search was run.
The initial exploratory root parser failed to canonicalize seven omitted
representatives and produced 111 rows; those outputs are invalid, not
search evidence. The corrected 104-row loader also reproduces PR6211's
exact guide maximum 4820 before any accepted search or verification.

## New result and inherited obligations

Armin Pourshafeie / apoursh's PR6211 already supplies complex Hermitian
rank-seven examples below 1/4. The present error lies between its
25/101 and 1205/4912 witnesses; the contribution is Gaussian-dyadic
coefficient feasibility, not a new best complex error. Nick Petalas's
PR6183 supplies the contractive question, real attaining projector and
omission data; apoursh's PR6191 supplies the sharp real comparison.
Matarener's PR6166 supplies the cited physical P104/root identification,
which is not independently audited here. Exact input pins and full
predecessor heads are recorded in SOURCES.json and README.md.

Dyadic entries are not a native implementation. Gate synthesis, a caller,
source access, correction, dirty restoration and the complete paid/target
bill remain open. No inverse for this singular projection is claimed.
No selected assumption is discharged, no full multiplication theorem is
proved, and no new kappa or literature priority is claimed.
