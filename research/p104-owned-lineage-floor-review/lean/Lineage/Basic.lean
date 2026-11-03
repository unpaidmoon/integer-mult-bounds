import Mathlib

/-!
# Owned-lineage factorization (P104, PR6170 P_M accounting)

Abstract form of Lemma 1 of `PROOF.md`.  A lineage has moves `1..t`.  Move `l` gathers at
frame `G l` and lands at `G (l+1)` (SAME hand-offs), so the frames are antitone.  Values live
in a field `K` (the rationals in the paper), frames are subspaces of an `F`-space `V`
(`F₂⁹` in the paper) with a bilinear pairing `B` (the F₂ inner product of port labels).

* `val c w l` is the mover's port content after move `l`:
  `val 0 = 0`, `val (l+1) = c (l+1) • val l + w (l+1)`.
* `hw` is P3a: content injected at move `k` lies on ports whose label is in `G k`.
  It does not matter which register supplied it (a port, a helper or a live `X`).
* `hu` is R1: if move `l` delivers to `Y_j`, its landing lies in `p_j^⊥`.

`factor` : on every non-orthogonal pair the lineage's delivery is `α j * β i`.
`rank_le` : the F-rank of the pairing on `supp α × supp β` is at most `dim G 1 - dim G (t+1)`.
-/

open Finset

namespace Lineage

variable {K : Type*} [Field K]

/-- Content of the mover after move `l`. -/
def val {ι : Type*} (c : ℕ → K) (w : ℕ → ι → K) : ℕ → ι → K
  | 0 => fun _ => 0
  | l + 1 => fun i => c (l + 1) * val c w l i + w (l + 1) i

/-- Product of the scalars `c 1 ⋯ c l`. -/
def pr (c : ℕ → K) (l : ℕ) : K := ∏ k ∈ Icc 1 l, c k

lemma pr_succ (c : ℕ → K) (l : ℕ) : pr c (l + 1) = pr c l * c (l + 1) := by
  unfold pr
  rw [prod_Icc_succ_top (by omega)]

lemma pr_ne_zero {c : ℕ → K} (hc : ∀ k, c k ≠ 0) (l : ℕ) : pr c l ≠ 0 :=
  prod_ne_zero_iff.mpr fun k _ => hc k

/-- Closed form of the content. -/
lemma val_eq {ι : Type*} {c : ℕ → K} (hc : ∀ k, c k ≠ 0) (w : ℕ → ι → K) (l : ℕ) (i : ι) :
    val c w l i = pr c l * ∑ k ∈ Icc 1 l, w k i / pr c k := by
  induction l with
  | zero => simp [val]
  | succ l ih =>
    have h1 := pr_ne_zero hc l
    have h2 := hc (l + 1)
    show c (l + 1) * val c w l i + w (l + 1) i = _
    rw [ih, pr_succ, sum_Icc_succ_top (by omega), pr_succ]
    field_simp

variable {F : Type*} [Field F] {V : Type*} [AddCommGroup V] [Module F V] {ι : Type*}

/-- **Lemma 1 (i)**: rank one on every non-orthogonal pair. -/
theorem factor (G : ℕ → Submodule F V) (hG : Antitone G) (p : ι → V)
    (B : V →ₗ[F] V →ₗ[F] F) (c : ℕ → K) (hc : ∀ k, c k ≠ 0) (w u : ℕ → ι → K)
    (hw : ∀ k i, w k i ≠ 0 → p i ∈ G k)
    (hu : ∀ l j, u l j ≠ 0 → ∀ x ∈ G (l + 1), B (p j) x = 0) (t : ℕ) :
    ∀ i j, B (p j) (p i) ≠ 0 →
      ∑ l ∈ Icc 1 t, u l j * val c w l i =
        (∑ l ∈ Icc 1 t, u l j * pr c l) * (∑ k ∈ Icc 1 t, w k i / pr c k) := by
  intro i j hji
  rw [sum_mul]
  refine sum_congr rfl fun l hl => ?_
  by_cases hul : u l j = 0
  · simp [hul]
  rw [val_eq hc, mul_assoc]
  congr 2
  have hlt : l ≤ t := (mem_Icc.mp hl).2
  refine sum_subset (Icc_subset_Icc le_rfl hlt) fun k hk hk' => ?_
  have hkl : l + 1 ≤ k := by
    simp only [mem_Icc, not_and, not_le] at hk hk'
    exact hk' hk.1
  by_contra hne
  have hwk : w k i ≠ 0 := fun h => hne (by simp [h])
  exact hji (hu l j hul _ (hG hkl (hw k i hwk)))

/-- **Lemma 1 (ii)**, source side: `β i ≠ 0` forces `p i ∈ G 1`. -/
theorem beta_support (G : ℕ → Submodule F V) (hG : Antitone G) (p : ι → V)
    (w : ℕ → ι → K) (pc : ℕ → K) (hw : ∀ k i, w k i ≠ 0 → p i ∈ G k) (t : ℕ) (i : ι)
    (h : ∑ k ∈ Icc 1 t, w k i / pc k ≠ 0) : p i ∈ G 1 := by
  obtain ⟨k, hk, hne⟩ := exists_ne_zero_of_sum_ne_zero h
  have hwk : w k i ≠ 0 := fun h0 => hne (by simp [h0])
  exact hG (mem_Icc.mp hk).1 (hw k i hwk)

/-- **Lemma 1 (ii)**, receiver side: `α j ≠ 0` forces `G (t+1) ⊆ p_j^⊥`. -/
theorem alpha_support (G : ℕ → Submodule F V) (hG : Antitone G) (p : ι → V)
    (B : V →ₗ[F] V →ₗ[F] F) (u : ℕ → ι → K) (pc : ℕ → K)
    (hu : ∀ l j, u l j ≠ 0 → ∀ x ∈ G (l + 1), B (p j) x = 0) (t : ℕ) (j : ι)
    (h : ∑ l ∈ Icc 1 t, u l j * pc l ≠ 0) : ∀ x ∈ G (t + 1), B (p j) x = 0 := by
  obtain ⟨l, hl, hne⟩ := exists_ne_zero_of_sum_ne_zero h
  have hul : u l j ≠ 0 := fun h0 => hne (by simp [h0])
  intro x hx
  exact hu l j hul x (hG (by have := (mem_Icc.mp hl).2; omega) hx)

/-- **Lemma 1 (iii)**: the pairing between ports in `G1` and ports whose hyperplane contains
`L ≤ G1` has rank at most `dim G1 - dim L`. -/
theorem rank_le [FiniteDimensional F V] (G1 L : Submodule F V) (hL : L ≤ G1) (p : ι → V)
    (B : V →ₗ[F] V →ₗ[F] F) (R A : Type*) [Fintype R] [Fintype A] (fR : R → ι) (fA : A → ι)
    (hA : ∀ a, p (fA a) ∈ G1) (hR : ∀ r, ∀ x ∈ L, B (p (fR r)) x = 0) :
    (Matrix.of fun (r : R) (a : A) => B (p (fR r)) (p (fA a))).rank + Module.finrank F L ≤
      Module.finrank F G1 := by
  classical
  set M := Matrix.of fun (r : R) (a : A) => B (p (fR r)) (p (fA a))
  -- T : G1 → (R → F), x ↦ (B (p r) x)_r
  let T : G1 →ₗ[F] (R → F) := LinearMap.pi fun r => (B (p (fR r))).comp G1.subtype
  have hspan : LinearMap.range M.mulVecLin ≤ LinearMap.range T := by
    rw [Matrix.range_mulVecLin, Submodule.span_le]
    rintro _ ⟨a, rfl⟩
    refine ⟨⟨p (fA a), hA a⟩, ?_⟩
    ext r
    simp [T, M]
  have hker : Submodule.comap G1.subtype L ≤ LinearMap.ker T := by
    intro x hx
    simp only [LinearMap.mem_ker, T]
    ext r
    simpa using hR r x hx
  have e : Module.finrank F (Submodule.comap G1.subtype L) = Module.finrank F L :=
    (Submodule.comapSubtypeEquivOfLe hL).finrank_eq
  have h1 : M.rank ≤ Module.finrank F (LinearMap.range T) := by
    unfold Matrix.rank
    exact Submodule.finrank_mono hspan
  have h2 := LinearMap.finrank_range_add_finrank_ker T
  have h3 := Submodule.finrank_mono hker
  omega


/-- **Lemma 1 (iii), assembled**: with `α, β` the vectors of `factor`, the pairing on
`supp α × supp β` has rank at most `dim G 1 - dim G (t+1)`, the lineage's owned paid. -/
theorem lineage_cost [FiniteDimensional F V] [Fintype ι] [DecidableEq K]
    (G : ℕ → Submodule F V) (hG : Antitone G) (p : ι → V)
    (B : V →ₗ[F] V →ₗ[F] F) (c : ℕ → K) (w u : ℕ → ι → K)
    (hw : ∀ k i, w k i ≠ 0 → p i ∈ G k)
    (hu : ∀ l j, u l j ≠ 0 → ∀ x ∈ G (l + 1), B (p j) x = 0) (t : ℕ) :
    (Matrix.of fun (r : {j // ∑ l ∈ Icc 1 t, u l j * pr c l ≠ 0})
        (a : {i // ∑ k ∈ Icc 1 t, w k i / pr c k ≠ 0}) => B (p r.1) (p a.1)).rank
      + Module.finrank F (G (t + 1)) ≤ Module.finrank F (G 1) := by
  classical
  exact rank_le (G 1) (G (t + 1)) (hG (by omega)) p B _ _ Subtype.val Subtype.val
    (fun a => beta_support G hG p w (pr c) hw t a.1 a.2)
    (fun r => alpha_support G hG p B u (pr c) hu t r.1 r.2)

/-- Telescoping: the paid of a SAME lineage is `dim G 1 - dim G (t+1)` (R4). -/
theorem paid_telescope [FiniteDimensional F V] (G : ℕ → Submodule F V) (t : ℕ) :
    ∑ l ∈ Icc 1 t, ((Module.finrank F (G l) : ℤ) - Module.finrank F (G (l + 1))) =
      (Module.finrank F (G 1) : ℤ) - Module.finrank F (G (t + 1)) := by
  induction t with
  | zero => simp
  | succ t ih => rw [sum_Icc_succ_top (by omega), ih]; ring

end Lineage

#print axioms Lineage.factor
#print axioms Lineage.rank_le
#print axioms Lineage.beta_support
#print axioms Lineage.alpha_support
#print axioms Lineage.paid_telescope
#print axioms Lineage.lineage_cost
