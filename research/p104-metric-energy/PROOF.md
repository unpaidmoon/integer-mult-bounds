# Sharp common-metric orthogonality energy on P104

This scoped proof was produced by Nick Petalas. Apache-2.0.

## Statement and normalization

Let R be the 120 E8 root lines represented by unit vectors in R^8. Choose
one sign on each line. The quantities below are independent of these signs.
Let F and G be any two disjoint orthonormal frames contained in R, each with
eight lines, and put P = R \ (F union G). Thus P has 104 lines.

For a real symmetric 8 by 8 matrix A, write

    A0 = A - tr(A) I/8,
    E_P(A) = sum_{unordered {u,v} subset P, u perpendicular v} (u^T A v)^2,
    D_F(A0) = sum_{u in F} (u^T A0 u)^2,
    X_FG(A0) = sum_{u in F, v in G, u perpendicular v} (u^T A0 v)^2.

All norms below are Frobenius norms. The new quantitative identity is

    E_P(A) = 37 ||A0||^2 + (17/2) [D_F(A0) + D_G(A0)] + X_FG(A0).    (1)

Consequently E_P(A) >= 37 ||A0||^2 for every such P. The constant 37 is
sharp uniformly over this family. Section 4 gives an equality example and an
invertible rational common deformation attaining it arbitrarily near identity.

The claim is a scoped proof using exact finite E8 premises, with a finite
equality certificate. It is not a statement about independent motions of the
120 lines, arbitrary masked fitting matrices, or a complete supplier.

## 1. Exact finite E8 premises

The verifier constructs one integer vector r per line. Its squared norm is 8.
There are 56 vectors 2(e_i +/- e_j), i < j, with the first nonzero coordinate
positive, and 64 vectors (1,s_1,...,s_7), with s_i in {1,-1} and an even
number of minus signs. Set u=r/sqrt(8).

Two finite identities are checked directly, without a predecessor executable:

    sum_{v in R, v perpendicular u} v v^T = 9(I-u u^T)              (2)
    E_R(A) = 54 [||A||^2 - tr(A)^2/8] = 54 ||A0||^2.              (3)

For (2), every one of the 120 stars has 63 lines. In integer coordinates the
checked identity is sum s s^T = 72 I - 9 r r^T, with all 64 entries checked
for every r. This proves (2) exactly.

For (3), use the 36 independent entries a of symmetric A, with eight diagonal
entries followed by the 28 upper off-diagonal entries. For an orthogonal pair
r,s, the coefficient vector c satisfies c.a = r^T A s. The verifier sums
H = sum c c^T over all 3,780 unordered orthogonal pairs. It checks all 1,296
entries of

    H = 3456 W - 432 t t^T,
    W = diag(1 repeated 8 times, 2 repeated 28 times),
    t = (1 repeated 8 times, 0 repeated 28 times).

Since a^T W a = ||A||^2 and t.a = tr(A), division by 64 gives (3).
This coefficient identity proves (3) for all real symmetric A, not only
sampled matrices. No floating eigenvalue computation is a premise.

## 2. Removing one frame

Let L_F(A) be the energy of all orthogonal pairs of R having at least one
endpoint in F. Summing (2) over u in F gives

    sum_{u in F} sum_{v perpendicular u} (u^T A v)^2
        = 9 [||A||^2 - sum_{u in F}(u^T A u)^2].

Pairs internal to F occur twice in this sum and once in L_F. Because F is
an orthonormal basis and A is symmetric, their energy is

    sum_{unordered u,v in F} (u^T A v)^2
        = (1/2) [||A||^2 - sum_{u in F}(u^T A u)^2].

Therefore, for every frame F in R,

    L_F(A) = (17/2) [||A||^2 - sum_{u in F}(u^T A u)^2].           (4)

This argument quantifies over arbitrary frames. It does not infer a universal
frame statement from the two frames used for the equality example.

## 3. Removing two frames and the deformation consequence

Disjointness gives the exact inclusion-exclusion identity

    E_P(A) = E_R(A) - L_F(A) - L_G(A) + X_FG(A).

All energies on orthogonal pairs are unchanged by adding a scalar matrix.
Apply (3) and (4) to A0. Since 54 - 2(17/2) = 37, this is (1).
Every residual term is a square, so the lower bound follows. Equality holds
exactly when the two frame diagonals and every cross-frame orthogonal defect
of A0 vanish.

For any common real linear map T, put M=T^T T. The deformed inner product
between originally orthogonal unit roots is (Tu)^T(Tv)=u^T M v. Thus

    ||M - tr(M) I/8|| <= sqrt(E_P(M)/37).                          (5)

In particular an invertible common T preserving every such zero has
T^T T=cI with c>0. Exact qualitative rigidity has prior literature in this
repository; the contribution here is the sharp quantitative identity (1)
and its equality certificate. Equation (5) uses absolute inner products
before any separate normalization of the deformed lines. It does not price
metric changes, physical native maps or recursive work.

## 4. Sharpness and rational common deformations

In integer coordinates take F to be

    2(e_0+e_1), 2(e_0-e_1), ..., 2(e_6+e_7), 2(e_6-e_7),

and G to be the eight Sylvester rows

    g_i[j] = (-1)^{popcount(i AND j)},  0 <= i,j < 8.

Normalize all these vectors by sqrt(8). They are disjoint E8 frames. Let A
have the following nonzero entries, together with their symmetric partners:

    A[0,7]=-1, A[1,6]=-1, A[2,5]=1, A[3,4]=1.

Then tr(A)=0, A^2=I and ||A||^2=8. Direct integer evaluation checks both
zero frame diagonals and every required cross-frame zero. In this example
P has 2,860 unordered orthogonal pairs and there are 32 orthogonal F-G pairs.
Their literal energy sum is E_P(A)=296=37*8. The pair counts refer to this
explicit example; they are not asserted for every pair of deleted frames.

For any nonzero rational s with |s|<1, T_s=I+sA is invertible and

    T_s^T T_s = (1+s^2)I+2sA.

Its trace-free part is 2sA. By homogeneity it attains equality in (5), and
T_s tends to I as s tends to zero. Hence the constant cannot increase even
when restricted to positive definite common metrics from rational invertible
maps arbitrarily near the identity.

## Evidence boundary

The standard-library verifier checks the full E8 coefficient identity and
all stars, the two explicit frame deletions, all coefficients of (1) for
the example, and the literal equality sum. The written removal argument
supplies the quantifiers over every pair of disjoint frames and every real
symmetric matrix. Seven controls discriminate omitted data, changed constants,
invalid frame boundaries and a changed witness. Source hashes in its printed
receipt bind the exact proof, implementation and metadata bytes.

No human or proof-kernel review is claimed. The selected result, all five
framework assumptions, native/dirty restoration, compiler, precision/tape,
complete invoice and multiplication theorem are unchanged.
