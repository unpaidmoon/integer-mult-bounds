# Mode-fiber rounding radius: a finite reduction and 1 ≤ R ≤ 2

Prepared for apoursh with substantial Anthropic Claude assistance. Apache-2.0.

## Setting

M is the 112×8 mode matrix of Dillon Amburgey's
[PR4933](https://github.com/CrocSwap/integer-mult-bounds/pull/4933), read from
`research/coded-native-caller/NORMALIZERS.json` (`mode_columns`), with rows
m_0, …, m_111. Nick Petalas's #6312 (`research/mode-preserving-rounding`, open
at head `46593234bfe658b63fb829f0d22b7eb216e392a2`) studies rounding x ∈ ℝ^112 to
z ∈ ℤ^112 with Mᵀz = Mᵀx, and asks in its first open question for the least
uniform radius

    R = sup { ρ(x) : the fiber F(x) = {z ∈ ℤ^112 : Mᵀz = Mᵀx} is nonempty },
    ρ(x) = min { ‖z − x‖∞ : z ∈ F(x) }.

The minimum exists because F(x) is discrete. #6312 proves R ≥ 1, using
x = (e_0+e_7+e_20+e_111)/2. This note gives a finite characterisation of R = 1
and explicit upper bounds: a basis certificate gives R ≤ 6, and the block structure of M gives R ≤ 2.

Write L = Mᵀℤ^112 ⊂ ℤ^8, V = ker Mᵀ ⊂ ℝ^112, Z = Mᵀ[0,1]^112 (a zonotope) and
S = {Mᵀz : z ∈ {0,1}^112} (subset sums of rows).

## 1. Structure of M (exact, verify.py)

* Every row has four nonzero entries, all ±1. The rows are distinct, and MᵀM = 56·I.
* The 14 row supports are exactly the 14 weight-four words of the extended
  Hamming code H8 = [8,4,4]. Each support carries 8 rows, so 8 of its 16 sign
  patterns occur. The row set is **not** closed under negation.
* L = {x ∈ ℤ^8 : x mod 2 ∈ H8}, the Hamming construction of √2·E8, with
  [ℤ^8 : L] = 16. verify.py proves this by comparing Hermite normal forms
  of the rows and of H8 ∪ 2ℤ^8.
* For every i, the other 111 rows have rank 8.

## 2. Theorem A (finite reduction)

**R ≤ 1 if and only if L ∩ int Z ⊆ S.** If some t ∈ L ∩ int Z is not a 0/1
subset sum of the rows, then every y ∈ (0,1)^112 with Mᵀy = t has ρ(y) > 1,
so R > 1. With #6312's lower bound:

    R = 1   ⇔   every lattice point of L in the open zonotope int Z is a subset sum of rows.

*Proof.*

(a) *Invariance and continuity.* F(x+n) = F(x)+n for n ∈ ℤ^112, so ρ is
ℤ^112-periodic. For v ∈ V, F(x+v) = F(x), so |ρ(x+v) − ρ(x)| ≤ ‖v‖∞.

(b) *Generic points suffice.* Fix x with F(x) ≠ ∅. The coordinate functional
v ↦ v_i is not identically zero on V. Otherwise e_i ∈ V^⊥ = col span(M), say
e_i = Ma. Then m_k·a = 0 for all k ≠ i, and since those rows have rank 8
(§1), a = 0, a contradiction. So {v ∈ V : x_i + v_i ∈ ℤ} is a countable union
of proper affine hyperplanes of V for each i. The union over i is a null set,
so there are v ∈ V with arbitrarily small ‖v‖∞ such that x+v has no integral
coordinate. By (a), R is the supremum of ρ over points with no integral coordinate.

(c) *Reduction to the open cube.* For such x, put y = x − ⌊x⌋ ∈ (0,1)^112.
Then ρ(y) = ρ(x), and t := Mᵀy ∈ L, because Mᵀx ∈ L (the fiber is nonempty)
and Mᵀ⌊x⌋ ∈ L. For y_i ∈ (0,1), an integer z_i satisfies |z_i − y_i| ≤ 1 if
and only if z_i ∈ {0,1}. Hence ρ(y) ≤ 1 ⇔ t ∈ S, and otherwise ρ(y) > 1.

(d) *Which t occur.* Mᵀ is a surjective linear map ℝ^112 → ℝ^8. The image of the
open cube is the interior of the image of the closed cube, so
{Mᵀy : y ∈ (0,1)^112} = int Z.

Combining (b)–(d): R ≤ 1 ⇔ L ∩ int Z ⊆ S. If t ∈ (L ∩ int Z) \ S, every y in
the open cube over t has ρ(y) > 1. ∎

Consequences. Deciding R = 1 is a **finite** problem, since Z is bounded. A
counterexample has a finite exact certificate: a lattice point t, a rational
y ∈ (0,1)^112 with Mᵀy = t, and infeasibility of the 0/1 system Mᵀz = t.
Conversely, R = 1 needs every one of the finitely many interior lattice points
to be a subset sum. Boundary lattice points of Z impose no condition.

## 3. Theorem B (explicit upper bound): R ≤ 6

Let B be the eight rows `[7, 35, 57, 73, 87, 90, 92, 99]` from CERTIFICATE.json.
verify.py checks |det M_B| = 16 = covol(L). Since the rows lie in L, B is a basis
of L. Each other row m_i (i ∈ N, |N| = 104) has integer coordinates w_i ∈ ℤ^8
in this basis, and max_i ‖w_i‖₁ = τ = 6. Let W be the 8×104 matrix with columns w_i.

Take y ∈ (0,1)^112 with Mᵀy = t ∈ L, as in Theorem A(b,c).

*Step 1 (Beck–Fiala rounding of y_N against W).* Keep x ∈ [0,1]^N, starting
from x = y_N, and let F be its fractional coordinates. Call row b of W
*active* if Σ_{i∈F}|W_{bi}| > τ. Since Σ_b Σ_{i∈F}|W_{bi}| ≤ τ|F|, there are
fewer than |F| active rows. So some nonzero d supported on F satisfies
W_active d = 0. Move x along d until one more coordinate is integral, and
repeat until F = ∅. Each active row value is preserved. Once a row becomes
inactive, only coordinates of F change afterwards, each by less than 1. Its
total later change is therefore less than Σ_{i∈F}|W_{bi}| ≤ τ, or zero. The
result z_N ∈ {0,1}^N has ‖W(y_N − z_N)‖∞ < τ.

*Step 2 (absorb into the basis).* Set z_B = y_B + W(y_N − z_N). Then

    Σ_{b∈B} z_b m_b = Σ_B y_b m_b + Σ_N (y_i − z_i) m_i = t − Σ_N z_i m_i ∈ L,

and B is a basis of L, so z_B ∈ ℤ^8. Hence z ∈ F(y), with |z_i − y_i| < 1 on N
and |z_b − y_b| < τ on B.

So ρ(y) < 6 for every generic y, and R ≤ 6 by Theorem A(a,b). ∎

Local search over row bases (`search/basis_search.py`, three seeds × 200 restarts)
found no basis with τ < 6. This method therefore stops at 6. Theorem C below
uses the block structure instead.

## 3′. Theorem C: R ≤ 2

*Block structure (exact, verify.py).* For each of the 14 supports s, its 8 rows
are exactly {σ_s e_{p(s)} + Σ_{k∈s∖p(s)} ε_k e_k : ε ∈ {±1}³}. So one *pinned*
coordinate p(s) has a fixed sign σ_s, and the three free coordinates take every
sign pattern. In particular, for every j ∈ s the block contains **four disjoint
row pairs** (a,b) with ±2e_j ∈ {m_a − m_b, m_a + m_b}:

- if j is free, pair rows that differ only at j, so m_a − m_b = 2(m_a)_j e_j;
- if j = p(s), pair opposite free patterns, so m_a + m_b = 2σ_s e_j.

Either sign of 2e_j is available with coefficients in {±1} on the pair.

*Hall lemma (exact, verify.py).* For every set X of at most three supports and
every nonempty J ⊆ {0,…,7}, at least |J| supports outside X meet J. The
minimum slack over all cases is 3.

*Proof of R ≤ 2.* Let y ∈ [0,1)^112 with t = Mᵀy ∈ L.

1. *Vertex.* P_t = {y′ ∈ [0,1]^112 : Mᵀy′ = t} is a nonempty polytope. Take a
   vertex y*. Its fractional coordinates F index linearly independent rows, so
   |F| ≤ 8, and |y*_i − y_i| < 1 for all i. Each block's rows lie in a
   four-dimensional coordinate subspace, so F contains at most 4 rows of any block.
2. *Round F.* Let z_F be y*_F rounded to the nearest of {0,1}. Then
   r′ = Σ_F (y*_i − z_i) m_i lies in L, because t, Σ_{i∉F} y*_i m_i and Σ_F z_i m_i
   do, and |r′_j| ≤ ½·#{i ∈ F : m_ij ≠ 0} ≤ 4.
3. *Parity.* h = r′ mod 2 ∈ H8 (§1). If h is a weight-four word, let U be one
   row outside F with support h. If h = 1⁸, let U be two rows outside F with
   complementary supports (the complement of a word is a word). If h = 0, let
   U = ∅. Step 1 guarantees each block has at least 4 rows outside F. Put
   u = Σ_U m_i, so |u_j| ≤ 1 and r′ − u = 2w with w ∈ ℤ^8 and |w_j| ≤ 2.
4. *Distinct blocks.* Call rows in F ∪ U damaged, at most 10 of them. A block with
   at most 2 damaged rows keeps at least 2 intact pairs for each of its
   coordinates. At most three blocks have three or more damaged rows. By the
   Hall lemma, the coordinates with w_j ≠ 0 have distinct undamaged-enough
   blocks s_j ∋ j.
5. *Assemble.* Set z_i = y*_i for i ∉ F ∪ U, then add 1 on U and, for each j,
   ±1 on the rows of |w_j| intact pairs of s_j representing 2·sign(w_j)·e_j.
   All touched rows are distinct. Then Mᵀz = Σ_{i∉F} y*_i m_i + Σ_F z_i m_i + u + 2w = t,
   and z ∈ ℤ^112.
6. *Error.* On F, |z_i − y_i| < 1. Elsewhere |z_i − y*_i| ≤ 1 and |y*_i − y_i| < 1,
   so |z_i − y_i| < 2.

Hence ρ(y) < 2 for every y in the open cube. By Theorem A(a,b), R ≤ 2. ∎

`rounder.py` executes these six steps literally in exact rational arithmetic and
raises if any step's claim fails. verify.py runs it on a fixed set of exact
inputs. A separate stress run on 12,000 exact random and sparse inputs found
no failure; its worst error was 839/420 ≈ 1.998, so 2 is the limit of this
construction, not evidence about R.

## 4. Evidence for R = 1 (not a proof)

`search/evidence.py` (scipy/HiGHS) samples lattice points t ∈ L near the boundary
of Z, where Theorem A's condition is hardest. It does this in two ways:

- near a vertex (face rank 0): the vertex minus a small inward lattice vector;
- near faces spanned by 1–7 random rows: rows off the face are pinned by the side
  of the supporting functional, rows on the face get fractional weights with
  denominator 2, 3, 4 or 6, and a small inward lattice vector is subtracted.

It keeps t with a positive LP interior margin and solves the 0/1 system. All
1,864 interior points found (by face rank 0–7: 401, 350, 402, 372, 175, 60, 72, 32)
are subset sums. verify.py re-checks each witness exactly, t ∈ L and Σ_{i∈z} m_i = t.
Interiority comes only from a floating-point LP and is **not** certified.
This sample supports, but does not prove, the conjecture R = 1.

## Scope

R is a property of the stated exact-mode contract for this M, inherited from
#6312. Nothing here shows that an actual caller must preserve these modes, or
supplies a physical rounder, error ledger, tape/precision bill, supplier
admission, new κ or frontier change. The five framework assumptions keep
their status. Theorems A, B and C are written proofs whose finite inputs are
checked exactly; no proof-assistant or independent human review is claimed.
Beck–Fiala's iterative rounding (1981), Hall's marriage theorem and the Hamming
construction of E8 are classical and credited as such.
