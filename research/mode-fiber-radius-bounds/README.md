# Mode-fiber rounding radius: 1 ≤ R ≤ 2, and R = 1 is a finite question

A scoped partial answer to the first open question of Nick Petalas's #6312
(`research/mode-preserving-rounding`, open at head `46593234`). For the PR4933
mode matrix M (112×8), let R be the least ℓ∞ radius such that every x with a
nonempty integer fiber {z ∈ ℤ^112 : Mᵀz = Mᵀx} has a point of that fiber within R.
#6312 proves R ≥ 1. This package proves:

- **Structure.** L = Mᵀℤ^112 = {x ∈ ℤ^8 : x mod 2 ∈ H8}, the Hamming construction
  of √2·E8, with index 16. The 14 row supports are the weight-four words of
  [8,4,4], with 8 rows each. MᵀM = 56·I. The row set is not closed under negation.
- **Theorem A (finite reduction).** R ≤ 1 if and only if every lattice point of L
  in the *open* zonotope Mᵀ(0,1)^112 is a 0/1 subset sum of rows. One interior
  lattice point that is not a subset sum forces R > 1. So **R = 1 is a finite
  decision problem**, and either answer has a finite exact certificate.
- **Theorem C.** **R ≤ 2.** Each support block is "one pinned coordinate, three
  free," so every block holds four disjoint row pairs equal to ±2eⱼ for each of
  its coordinates. Rounding at a vertex of the fiber polytope leaves a small
  lattice residual. A Hall-theorem block assignment then pays that residual with
  intact pairs, moving every coordinate by less than 2. `rounder.py` runs the
  construction exactly. Theorem B, a simpler basis certificate with Beck–Fiala
  rounding, gives R ≤ 6.
- **Evidence, not proof.** All 1,864 sampled interior lattice points near vertices
  and faces (face rank 0–7) are subset sums. This supports the conjecture R = 1.

[PROOF.md](PROOF.md) has the arguments and exact scope. The constructive rounder is
[rounder.py](rounder.py), the basis is in [CERTIFICATE.json](CERTIFICATE.json), the witnesses in [SEARCH.json](SEARCH.json),
and the pins in [SOURCES.json](SOURCES.json). Complete κ and the selected frontier
are unchanged. This is a property of the exact-mode contract. It does not claim
that any caller needs the contract, and supplies no physical rounder or error/tape bill.

## Reproduce

From the repository root; the standard library suffices:

```sh
python3 -I -W error -B research/mode-fiber-radius-bounds/verify.py
python3 -I -O -W error -B research/mode-fiber-radius-bounds/verify.py
python3.12 -B scripts/research_package.py --package research/mode-fiber-radius-bounds
```

Each prints `PASS_MODE_FIBER_RADIUS_BOUNDS` in about five seconds. Checked exactly:

- the structure facts, the HNF lattice identity and the rank condition Theorem A needs;
- the #6312 witness relation;
- the τ = 6 basis (|det| = 16, integral coordinates, maximum ℓ₁ norm exactly 6);
- the 14 pinned blocks and their 2eⱼ pairs;
- the Hall lemma, exhaustively over every set of at most three damaged blocks (minimum slack 3);
- 120 exact runs of the Theorem C rounder (worst error 279/140);
- every subset-sum witness.

Nine rejection controls fail closed: a flipped matrix entry (in both the
structure and block checks), a repeated basis row, a claimed τ = 5, a non-basis,
a wrong witness mask, an off-lattice target, a broken witness relation and
non-integral modes passed to the rounder. Interiority of the sampled targets came from a floating-point
LP and is not certified.

The non-certifying search scripts in `search/` need numpy and scipy:
`evidence.py SEED TRIALS` regenerates one evidence run (seeds 11–14, 320 trials
each), and `basis_search.py SEED RESTARTS` repeats the basis search.

## Open next questions

1. **Decide R = 1.** Is every lattice point of L in the open zonotope a subset
   sum? This would settle #6312's question exactly. First step: reduce the
   near-boundary cases with the signed-permutation symmetry of the rows, and try
   a face recursion, where deep points are handled by discrepancy rounding and
   points near a face reduce to the rows in that flat. Blocker: about 10¹²
   lattice points rule out brute force, and the recursion is unproved.
2. **Close the gap between 1 and 2.** Theorem C loses a full unit through the
   triangle inequality |z − y| ≤ |z − y*| + |y* − y|. An exact stress run of
   12,000 inputs reaches 1.998 with this construction, so improving the bound needs
   a different first step. First step: replace the vertex y* by a point of the
   fiber chosen near y, for example by Beck–Fiala rounding inside each block
   against the 8 mode constraints. Then reuse the pair-and-Hall repair.
   Blocker: the repair must stay within the remaining error budget.

## Credit

Dillon Amburgey (PR4933) supplies M. Nick Petalas (#6312) supplies the contract,
the radius-one witness and the question. Its predecessor credits (JoyboyBrian,
Dugongue, Ali Romman) carry over. Beck–Fiala rounding and the Hamming
construction of E8 are classical. Prepared by apoursh with substantial Anthropic
Claude (Claude Code) assistance. New work is Apache-2.0.
