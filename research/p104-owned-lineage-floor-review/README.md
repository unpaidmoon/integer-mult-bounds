# Owned-lineage factorization and a scoped review of PR6170's owned-layer floor

This package reviews the floor framework of DreamingOfClouds'
[PR6170](https://github.com/CrocSwap/integer-mult-bounds/pull/6170). It has two parts. The first is a scoped
independent recount: own code recomputes PR6170's owned-delivery matrix C on four frontier words. The
second is a short structural result: in PR6170's P_M accounting, a relay-free owned lineage contributes a
rank-one matrix on every non-orthogonal port pair, and its owned paid bounds the F2 rank of that term. The
consequence proved here is that **a relay-free, merge-free owned layer with exactly 8 leaves pays owned
paid >= 56, even when lineages branch and share a common descent**. Proofs are in [PROOF.md](PROOF.md).
No new word or kappa is claimed.

## Status of the PR6170 floor (read from its own files)

PR6170 is merged for archive only. Its intake record says: "Independent scientific review and
source-bound replay remain open". No later PR re-checks the floor.

- `P104-THEORY.md` sec 7 quotes a proved floor of 794.53 R0 (about 10%). The same file's CHARTORB addendum
  declares 794.53 and 813.31 invalid (the inherited cap48 row) and corrects the figure to 754.14.
- `P104-LEMMAS.md` sec 6 corrects 754.14 to 751.46 (A1 correction). Its sections 9-11 state that no floor
  above 0 rests on SPEC + paid + literals alone. Every positive floor carries the measured scope NEED = 4972
  (Z <= 20) and own/owns/ownc = 22/18/64. With the proved bound NEED >= 90 the certificate gives 0.00, and the
  floor turns positive only from NEED >= 3597, which is open.
- The LP solver, the certificate and its recheck are not in the package, and the rows "capfix, mains,
  cpres" are not written out. So the LP cannot be rebuilt from the text, and it is not re-solved here.
- The kappa law 1/kappa = 130.27 + .02364 (R0 + 380 (paid - 56)) is a fit on 11 words. A floor on R0 is
  therefore not a proved kappa ceiling.

## Result and evidence

[verify.py](verify.py) layers 1-2 run on canonical main for each word: an exact real replay, a parallel
P_M replay, and the lineage factorization.

| word | owned symbols | owned paid | rank C | NEED | Z | lineages | lineage paid | lineage rank_F2 | rank X |
|---|---|---|---|---|---|---|---|---|---|
| PR5907 | 20 | 56 | 8 | 4992 | 0 | 8 | 7 each | 7 each | 8 |
| PR6030 | 20 | 56 | 8 | 4992 | 0 | 8 | 7 each | 7 each | 8 |
| PR6144 | 26 | 56 | 10 | 4972 | 20 | 8 | 7 each | 7 each | 8 |
| PR6167 | 25 | 56 | 10 | 4972 | 20 | 8 | 7 each | 7 each | 8 |

The four words agree with PR6170's numbers (r245g is PR6144's line, with rank 10 and NEED 4972). On all
four, PUB + C = I holds exactly, R1, R3 and P3a hold with 0 violations, there are 0 STRICT edges, 0 merges
and 0 branchings, and the rank-one identity of Lemma 1 has 0 mismatches. In PR6144/PR6167 C has rank 10,
but the completion X built from the lineage terms has rank 8, which is the E8 completion.

Layer 3 derives the E8 root data exactly from the PR6030 completion. The Gram matrix is integral, the
104 roots close to 240 under reflections, and simple roots are recovered. The layer then checks the
finite facts F1-F3 for root directions. Layer 4 (`--flats`) enumerates all 440,880 one-dimensional flats
as W-orbits of the fundamental coweights and checks F1 and the span-pair ranks for every flat. All numbers
are in [RESULT.json](RESULT.json).

## Lean

[lean/Lineage/Basic.lean](lean/Lineage/Basic.lean) formalises Lemma 1 in the abstract form used by the
proof: values in any field `K`, frames as subspaces of any finite-dimensional `F`-space with any bilinear
pairing `B`, an antitone frame sequence (SAME hand-offs), P3a as the hypothesis `hw` and R1 as `hu`.
`factor` is (i) with the explicit vectors alpha_j = sum_l u_l(j) pi_l and beta_i = sum_k w_k(i)/pi_k,
`alpha_support` / `beta_support` are (ii), `rank_le` and `lineage_cost` are (iii), and `paid_telescope`
is the telescoping of SAME gaps. Because `hw` only asks where injected content lies, the formal statement
covers lineages that read X directly (Remark in PROOF.md). No `sorry`; `#print axioms` gives `propext`,
`Classical.choice`, `Quot.sound` only. Build (Lean `v4.33.0-rc1`, Mathlib pinned in `lake-manifest.json`,
the same revision as other Lean packages here):

```sh
cd research/p104-owned-lineage-floor-review/lean && lake exe cache get && lake build
```

Not formalised: Lemma 2, Theorems 3-4 and the finite facts F1-F3 (these are checked by `verify.py`), and
the identification of word events with the abstract data (checked on four words by `verify.py`).

## Relation to existing work

Corollary (completion form) identifies the relay-free owned layer with the repository's masked decoder
problem `C(P104) >= 56`: lineages are terms and lineage paid is the term cost. The floor for at most
8 terms is already known, and Theorem 3 re-derives it by a different finite input. New here:
(a) the derivation inside PR6170's P_M accounting, which connects its NEED/REL framework to the decoder
floor; and (b) Theorem 4, where terms may share cost through branching. That sharing is absent from the
plain decoder model, and it does not lower the floor at 8 leaves.

Two later packages treat the same owned-cost question in PR6170's confined REL model.
[PR6229](https://github.com/CrocSwap/integer-mult-bounds/pull/6229) (`research/p104-two-clique-relay-floor`, Nick
Petalas) proves that a block of two orthogonal four-port cliques needs 8 owned paid units, with chains,
branching, merging and re-ascents allowed, through a cumulative bound `rank_Q(C o Gamma) <= owned paid` on a
binary quotient. `research/p104-ambient-relay-floor` (AAAmirinu) extends that 8-port floor to frames that
leave the block span. Both are local 8-port statements. This package works on the whole 104-port owned
layer of real words, lineage by lineage, and does not cover merges. The two results are complementary;
PR6229's cumulative row-space invariant is the natural tool for the merge case left open here.

**Direct reads of X.** `research/fragmentation-ceiling` proves its centre bound under P-ATOM and lists
"decoders that read X directly" as an open door. In the P_M accounting this door is closed for the
relay-free, merge-free layer: by PR6170's P3a a read of X at frame g brings only x-content on ports of g,
which is what Lemma 1 already allows, so the 8-leaf floor of 56 holds for decoders that read X at any frame
(PROOF.md, Remark). Only X reads that carry owned symbols (STRICT relays) remain open.

## Reproduction

From the repository root with CPython 3.12 and NumPy:

```sh
python3.12 -B research/p104-owned-lineage-floor-review/verify.py
python3.12 -B research/p104-owned-lineage-floor-review/verify.py --flats
```

The first command runs layers 1-3 (about 40 seconds on one hosted Linux core). The second replays only
PR6030 and runs layers 3-4 (about 2 minutes). Markers: `PASS_P104_OWNED_LINEAGE_FLOOR_REVIEW` and `..._WITH_FLATS`.

## Limitations

- Not covered: merges (a mover carrying two symbols), STRICT relays, 9 or more leaves. The case of 9 or
  more terms is the open masked decoder floor.
- Nothing here controls the orthogonal entries of C, so PR6170's open premise NEED >= 3597 stays open,
  and its positive floors stay conditional.
- own/owns are not recounted: their exact definition is not given in PR6170's text.
- The finite facts are computed on the PR6030 completion. PR5907, PR6144 and PR6167 have the same port set
  and completion rank 8, so Theorem U makes the root data identical up to the diagonal gauge.
- Lemma 1 is machine-checked in Lean (see Lean); the rest is not. No independent human review is claimed.

## Open next questions

- Does Lemma 1 extend to merges and STRICT relays? Start with one merged move: its symbol carries two
  ancestor contents, and the rank-one form should split per ancestor.
- Can the orthogonal entries of C be controlled lineage by lineage (pairs with e(i) > r(j))? That is the
  gap between X and C, and the missing link to PR6170's NEED premise.

## Credit

DreamingOfClouds retains PR6170, its P_M accounting, the lemmas R1, P3a, R3, G1a, N1, N2 and N2(e), and the
REL framework used here. Ali Romman retains PR6167; PR6030, PR6144 and PR5907 and their predecessors retain
their attribution. Theorem U and the E8 completion are prior art (#1212). The masked decoder floor and its
at-most-8-term case are prior repository work. Lemmas 1-2, Theorems 3-4 and the code are new, prepared for
Matarener with Claude (Anthropic). New material is Apache-2.0.
