# Proofs: owned-lineage factorization, tree branching, eight-lineage floor

Notation follows DreamingOfClouds' [PR6170](https://github.com/CrocSwap/integer-mult-bounds/pull/6170)
`research/p104-designer-toolkit-v2/P104-LEMMAS.md` (sections 0.2, 9-11). P_M accounting: every owned MOVE
arrival becomes a fresh symbol sigma_mu with rho(sigma_mu) = the real value that moved. The move mu has a
gather frame g_mu and a landing L_mu strictly inside g_mu. u_mu(j) is the coefficient of sigma_mu in the
P_M final of Y_j, v_mu = x(rho sigma_mu), and C = sum_mu u_mu v_mu^T. Gamma_ji = p_j . p_i over F2, so the
diagonal is 1 because ports have odd weight. A pair is *non-orthogonal* when Gamma_ji = 1.

Facts used from PR6170, each recounted by `verify.py` with 0 violations on PR5907, PR6030, PR6144 and PR6167:
- R1: u_mu(j) != 0 implies L_mu inside p_j^perp.
- P3a: the x-content of the public part of any P_M value at frame g lies on ports of g.
- R3: C = delta on every non-orthogonal pair.
- R4: the gaps of the owned moves sum to owned paid.

## Definitions

The *ancestors* of a move are the symbols present in its mover's P_M value. An ancestry edge nu -> mu is
**SAME** if L_nu = g_mu and **STRICT** otherwise; a STRICT edge is a public relay. An owned layer is
**relay-free** if every edge is SAME, and **merge-free** if every move has at most one ancestor. A
**lineage** is a root-to-leaf path of the resulting forest. *Branching* means one symbol is an ancestor of
several moves.

## Lemma 1 (lineage factorization)

*Machine-checked in Lean: `lean/Lineage/Basic.lean` (`factor`, `alpha_support`, `beta_support`,
`lineage_cost`, `paid_telescope`).*

Let a lineage have moves 1..t, gathers g_l, landings L_l = g_{l+1}, and v_l = c_l v_{l-1} + w_l with
w_l in X(g_l) (P3a), v_0 = 0 and c_l != 0. Then there are alpha, beta in Q^104 with

(i) C^lineage_ji = alpha_j beta_i on every non-orthogonal pair (j, i);
(ii) beta_i != 0 implies p_i in g_1, and alpha_j != 0 implies L_t inside p_j^perp;
(iii) dim g_1 - dim L_t >= rank_F2 Gamma[supp alpha, supp beta], and the left side is the lineage's owned
paid.

*Proof.* Put e(i) = max{l : p_i in g_l} (0 if none) and r(j) = min{l : L_l inside p_j^perp}. Frames
decrease, so p_i lies in g_l iff l <= e(i), and L_l lies in p_j^perp iff l >= r(j). So w_l(i) != 0 needs
l <= e(i), and u_l(j) != 0 needs l >= r(j) by R1. For a non-orthogonal pair, e(i) >= r(j)+1 would put p_i in
g_{r(j)+1} = L_{r(j)}, inside p_j^perp, so p_i . p_j = 0; hence e(i) <= r(j). For l >= e(i) no more
coordinate i is injected, so v_l(i) = (pi_l/pi_{e(i)}) v_{e(i)}(i) with pi_l = c_1...c_l. Then

C_ji = sum_{l >= r(j)} u_l(j) v_l(i) = (sum_l u_l(j) pi_l)(v_{e(i)}(i)/pi_{e(i)}) = alpha_j beta_i.

(ii) is read off the definitions. For (iii), Gamma[supp alpha, supp beta] is part of the F2 pairing between
L_t^perp and g_1, whose rank is at most dim g_1 - dim L_t because L_t lies inside g_1. Telescoping the SAME
edges gives the lineage's paid (R4). []

## Lemma 2 (trees)

In a relay-free, merge-free owned forest (branching allowed) there is one pair (alpha^P, beta^P) per leaf P.
On every non-orthogonal pair, C_ji = sum_P alpha^P_j beta^P_i, where beta^P_i = v_kappa(i)/pi_kappa and
kappa is the deepest node on P's root path whose gather contains p_i. The path cost bound (iii) holds for
every leaf.

*Proof.* As in Lemma 1, for a node mu with u_mu(j) != 0 and a non-orthogonal pair, p_i is not in L_mu.
So the deepest node kappa with p_i in its gather lies on mu's root path at or above mu. The same kappa
serves every leaf below mu, and C^mu_ji = (u_mu(j) pi_mu) beta_i(kappa). Assign each node to one leaf
below it and sum. []

*Branching condition.* If leaves P, P' separate below a node with landing L, then beta^P_i = beta^P'_i
for every port i outside L, since the deepest gather node is shared. So supp(beta^P - beta^P') lies in L
and dim L >= dim span supp(beta^P - beta^P').

## Corollary (completion form)

X := sum over leaves of alpha^P beta^P^T agrees with C on every non-orthogonal pair. So X o Gamma = I by R3,
rank X <= #leaves, and owned paid >= sum over leaves of rank_F2 Gamma[supp alpha^P, supp beta^P], with the
tree's cost replacing the sum when leaves share a prefix (Theorem 4). Any 8-clique gives rank X >= 8, so
there are at least 8 leaves. With exactly 8 leaves, X is a rank-8 completion of the P104 pattern, hence
X = D M0 D^-1 (Theorem U, prior art #1212). Then alpha^P = A x_P and beta^P = B y_P for dual bases, where
the rows of A and B are the roots up to the diagonal gauge.

This is the repository's masked decoder problem (`C(P104) >= 56`). Lineages are terms and lineage paid is
the term cost. For at most 8 terms the floor 56 is already known; Theorem 3 re-proves it here by a
different finite input. The case of 9 or more terms is open and is not addressed.

## Finite facts (verify.py, exact integer arithmetic on the PR6030 completion)

- **F1.** The 120 root lines: the 104 P104 lines have support 49 and span F2^9. The 16 lines of the two
  frames removed from E8 have support 52 and span 16 distinct hyperplanes. Over all 440,880 one-dimensional
  flats (W-orbits of the 8 fundamental coweights, `--flats`), the support span is F2^9 except for these
  16 lines.
- **F2.** For pairs of root directions, rank_F2 Gamma[S(x), S(y)] = 7 only when both lie on removed lines
  (64 pairs); otherwise it is >= 8. Over all span pairs of all flats the ranks are 7, 8 or 9 (`--flats`).
- **F3.** For every pair of removed lines y, y' and every z = y - mu y' (mu != 0) perpendicular to a P104
  root, supp(Bz) spans F2^9. For all other pairs of root lines the minimum span is >= 8.

## Theorem 3 (eight leaves, no branching)

A relay-free, merge-free path forest with exactly 8 lineages has owned paid >= 56.

*Proof.* By the Corollary, each lineage costs at least rank_F2 Gamma[supp A x, supp B y]. Every vector lies
in some flat, and a one-dimensional flat inside it has a smaller support, so the minimum is attained on
one-dimensional flats. By F1, both spans have dimension >= 8 inside F2^9 with its nondegenerate form. Hence
the pairing rank is >= 8 - dim(span)^perp >= 7. That bound uses only the span dimensions from F1; F2 states
the same minimum directly. So 8 lineages pay >= 56. []

## Theorem 4 (eight leaves, branching allowed)

A relay-free, merge-free owned forest with exactly 8 leaves has owned paid >= 56.

*Proof.* Take a branching landing L. By the branching condition and F1, supp B(y_P - y_P') has span >= 8:
a vector whose support spans only a hyperplane must be a removed line. Otherwise its flat contains a line of
span 9, or two removed lines with different spans. So dim L >= 8. A gather has dim <= 9 and a landing is
strictly inside its gather, so branching can only occur directly below a root move F9 -> H with dim H = 8.
Two leaves on removed-line directions cannot share that step (F3: the landing would need span 9). Every
other leaf costs >= 8 along its root path (F2). A group of k leaves under one shared step therefore costs
>= 1 + 6 + 7(k - 1) = 7k, unshared leaves cost >= 7, and the total is >= 56. []

## Remark (direct reads of X are covered)

`research/fragmentation-ceiling/PROOF.md` (section 5) proves its centre bound A30-CUT under the modelling
step P-ATOM (carriers get port content only by reading the port) and lists "decoders that read X directly
(breaking P-ATOM)" among the doors outside its scope (section 6.7). In the P_M accounting used here no such
step is needed. X lives are public registers, so by P3a (proved in PR6170 from SPEC nesting) a read of any
X at frame g contributes x-content in X(g), exactly as any other public read at g. Lemma 1 only uses
w_l in X(g_l), not which register supplied w_l. So every owned lineage that reads X directly, at any frame
and time, is still a lineage of Lemma 1, and Lemma 2, Theorems 3 and 4 hold unchanged: a relay-free,
merge-free owned layer with 8 leaves pays >= 56 whoever it reads. The label table is F2^9 because every
frame is a subspace of F2^9, so this does not open the rank >= 10 table cases of the decoder floor either.
What remains of that door is the relay case: an X that has received owned content (a symbol) and is read
again is a STRICT relay, which is outside Lemma 1 (see Scope).

## Scope

Not covered: merges, STRICT relays, 9 or more leaves, and the orthogonal entries of C. NEED counts the
orthogonal entries; C and X can differ there, as in PR6144 and PR6167: X has rank 8, C has rank 10,
NEED is 4972. So nothing here proves PR6170's open premise NEED >= 3597.

Related: PR6229 (`research/p104-two-clique-relay-floor`) and `research/p104-ambient-relay-floor` prove an
8-unit floor for one 8-port two-clique block in the confined and ambient REL models, merges included. They
do not give the 104-port statement above, and this note does not give their merge case.
