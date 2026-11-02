# The selected P104 orbit has sharp metric constant 75/2

Jerry Chen (@CubeJerry), with substantial OpenAI Codex assistance. Apache-2.0.

## 1. Exact object and result

Let Q be the ordered `ports` field of the selected PR6030
`research/p104-helper470-twin-rung-removal/WORD.json.gz`, at canonical commit
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. Its SHA256 is
`7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f`.
This is the selected word's own 104 labels, not an assumed equivalence with
another 104-root fixture. The word's complete endpoint/native/caller proof is
not replayed here.

Use the retained A8 root convention in the eight-dimensional subspace
V = {x in R^9 : sum x_i = 0}. For a weight-three label q with support T, put

    r(q) = sum_{i in T} e_i - (1/3) sum_{i=0}^8 e_i.

For a weight-seven q with omitted indices i < j, put r(q) = e_i - e_j.
Every root has norm squared two. Write u(q) = r(q)/sqrt(2), and use the
Euclidean structure on V. This convention is the one documented in
Matarener's PR6166 and the retained `p104-two-channel-support/PROOF.md`.
Our certificate independently checks its finite coordinates and Gram
isometry; the identification with the supplier's intended root geometry
retains that source attribution.

For any real symmetric operator A on V, define

    A0 = A - tr(A) I/8,
    E_Q(A) = sum (u(q)^T A u(r))^2,

where the sum is over **unordered**, distinct q,r in Q with u(q) perpendicular
to u(r). There are exactly 2,860 such pairs. The statement is

    E_Q(A) >= (75/2) ||A0||_F^2.                         (1)

The coefficient 75/2 is exact and sharp. Equality holds exactly when A0 is
in the six-dimensional space described in Section 4. The full spectrum of
this quadratic form relative to the Frobenius metric is

| Eigenvalue | Multiplicity |
| --- | ---: |
| 0 | 1 |
| 75/2 | 6 |
| 151/4 | 8 |
| 38 | 7 |
| 165/4 | 4 |
| 91/2 | 6 |
| 199/4 | 4 |

The statement also holds for any sign/permutation/orthogonal-coordinate image
of this fixed root set. It does not classify all pairs of deleted E8 frames.

Nick Petalas's PR6278 proves a sharp **uniform** coefficient 37 over all
two-disjoint-frame punctures, leaving the selected orbit as an explicit open
question. Its equality example is not assumed to be our selected orbit.
Equation (1), its complete spectrum and selected equality space resolve that
source-specific question. Our proof does not use PR6278's executable or its
sum-of-squares identity as a premise.

## 2. Rational coordinates without square roots

The full 120-line A8 realization consists of the 84 triple labels and 36
weight-seven labels. Its complement to Q is the disjoint union of frames

    F = (7, 25, 42, 52, 76, 82, 97, 127),
    G = (67, 104, 137, 162, 266, 289, 448, 491).

Each is an orthonormal frame after dividing r by sqrt(2); this is checked
from all 64 pairings in each frame. In the ordered orthonormal F basis set

    c(q)_i = r(F_i) . r(q) = 2 * coordinate_i(u(q)).

All c(q) entries are integers. The code first constructs the integer vectors
3r(q), takes their dot products, and divides exactly by nine. It then checks
all 14,400 Gram relations

    9 c(q).c(r) = 2 (3r(q)).(3r(r)).                    (2)

This establishes the complete coordinate isometry, not merely the orthogonality
mask. Every c(q) has norm squared four.

Represent A by its 36 independent entries a: first A_00,...,A_77, then A_ij
in lexicographic i<j order. Put

    W = diag(1,...,1,2,...,2),

with eight ones and 28 twos, so a^T W a = ||A||_F^2. For each retained
orthogonal pair let ell(q,r) be the integer coefficients of c(q)^T A c(r).
Its diagonal coordinates are c(q)_i c(r)_i; its off-diagonal coordinates are
c(q)_i c(r)_j + c(q)_j c(r)_i. Direct expansion gives the integer matrix

    H = sum ell(q,r) ell(q,r)^T,
    E_Q(A) = a^T H a / 16.                             (3)

The denominator is 16 because each unit-root vector is c/2. Pair signs or
the ordering of Q cannot change the sum of squares.

## 3. Complete exact spectral certificate

`CERTIFICATE.json` supplies 36 explicit integer column vectors v_j, grouped
by integers mu_j = 16 lambda_j. The direct checker reconstructs H from the
authenticated word's ports and verifies every coefficient of

    H v_j = mu_j W v_j.                                (4)

There are 1,296 exact integer scalar equations. It separately verifies that
the 36 columns have rank 36 modulo the prime 1009. Therefore their integer
determinant is nonzero, so they are a basis over Q and R. This use of modular
rank is a sufficient independence certificate, not a finite-field inference
about a rank-deficient rational matrix.

The null eigenvector is explicitly (1,...,1,0,...,0), representing I. Every
positive-eigenvalue column is checked to have zero trace. The supplied block
sizes are 1,6,8,7,4,6,4, totaling 36. Completeness follows from independent
columns and (4); numerical eigenvalue estimates are not used in acceptance.

Since H is symmetric and W is positive definite, the operator W^-1 H is
self-adjoint for the W inner product. Different eigenspaces are orthogonal:
subtract v^T H w = mu_w v^T W w and v^T H w = mu_v v^T W w.
Within each eigenspace the quadratic form is its eigenvalue times the
positive W metric. Removing the scalar component leaves precisely the six
positive eigenvalues in the table. The smallest is 600/16 = 75/2, proving
(1); equality is precisely its six-dimensional eigenspace.

`generate.py` obtains the integer vectors using exact rational row reduction
and denominator clearing. It is not imported by the verifier. The certificate
is checked by multiplication and modular elimination, so an error in the
nullspace generator does not bypass (4) or independence. Regeneration produces
the same canonical JSON. This is a finite exact certificate of a quadratic
identity holding for all real symmetric A, not a test on finitely many A.

## 4. Equality and rational common deformations

For i<j, let E_ij^+ have ones at (i,j) and (j,i), zero elsewhere. The six
following matrices J_k form an orthogonal basis of the equality eigenspace:

| k | Nonzero signed symmetric entries |
| --- | --- |
| 1 | +(0,6), -(1,7), +(2,4), +(3,5) |
| 2 | +(0,5), -(1,4), +(2,7), +(3,6) |
| 3 | +(0,4), -(1,5), +(2,6), +(3,7) |
| 4 | +(0,3), -(1,2), +(4,7), +(5,6) |
| 5 | +(0,2), -(1,3), +(4,6), +(5,7) |
| 6 | +(0,1), -(2,3), -(4,5), -(6,7) |

Coordinates here are in the F basis from Section 2, numbered zero through
seven. The corresponding 36-entry vectors are the mu=600 block of the
certificate. Each J_k is a symmetric signed permutation with

    tr(J_k)=0,  J_k^2=I,  ||J_k||_F^2=8,  E_Q(J_k)=300.

These properties, including the energy evaluated directly on every retained
root pair without using H, are checked. Distinct J_k have disjoint entry
supports, hence are Frobenius-orthogonal. In particular any larger constant
fails on J_1; the verifier explicitly distinguishes 37.51 from 37.5.

To attain equality with a positive definite metric, choose rational
0<|s|<1 and T=I+sJ_1. This is an invertible rational common map in F
coordinates. Its metric is

    M=T^T T=(1+s^2)I+2sJ_1,
    M0=2sJ_1,
    E_Q(M)=1200s^2=(75/2)||M0||_F^2.

Thus 75/2 remains sharp even for rational invertible common deformations
arbitrarily close to identity. The map on V in the original rational A8
coordinates is rational as well: the matrix representing J_1 is
(1/2) sum_{i,j} (J_1)_ij r(F_i) r(F_j)^T.

For any common map T, the metric inequality therefore gives

    ||T^T T - tr(T^T T)I/8||_F <= sqrt(2 E_Q(T^T T)/75).

This is an absolute orthogonality-defect statement using the original unit
roots. It is not an estimate after independently renormalizing T u(q).

## 5. Scope and remaining obligations

No supplier, native map, helper restoration, paid/productive invoice or κ is
changed. All five selected framework assumptions remain. This chapter covers
the selected real-symmetric case. ORBIT-PROOF.md extends it to all disjoint-frame
orbits, and HERMITIAN-PROOF.md extends the sharp constants to complex Hermitian
metrics. Independent root motions, arbitrary masked low-rank fitting matrices
and normalized correlations remain outside the claim.
No complete selected replay or formal proof-kernel check is asserted.

The selected word/root lineage retains DreamingOfClouds, Ali Romman,
Matarener and the credited native/helper/controller/geometry contributors.
Nick Petalas supplies the uniform-energy predecessor and selected-orbit
question; Brett Halligan, Aaron Wang, Josie Elliston and their predecessors
retain the earlier exact-realization/rigidity credit. Spectral theory,
rational row reduction and finite-field determinant certification are classical.

## Independent coordinate cross-check

The lead reviewer independently reconstructed the same operator in the
nonorthogonal basis B=(e_i-e_8), i=0,...,7, without importing the primary
geometry, generator, or certificate. Here B^T B=I+J and its inverse is
I-J/9. For a symmetric bilinear-form matrix Q in these coordinates, the
Frobenius metric is tr(K Q K Q), K=I-J/9. Integer roots3r have norm18, so
the direct 104-port energy matrix is H/324. With M=81 times this Frobenius
metric, the generalized eigenvalue equations are H v=4 lambda M v.

`independent.py` reconstructs all 2,860 pair terms and computes exact rational
ranks through fraction-free integer row elimination. The nullities at
4 lambda=0,150,151,152,165,182,199 are 1,6,8,7,4,6,4; their sum 36 and
rank(M)=36 certify the complete spectrum independently of the supplied
eigenvectors. The metric is positive definite because K is positive
definite. A changed quadratic coefficient destroys the claimed spectrum,
and every root-sign flip preserves its pair square. Both ordinary and
optimized modes are registered. This is independent mathematical computation
within the AI-assisted run, not independent human or proof-kernel review.
