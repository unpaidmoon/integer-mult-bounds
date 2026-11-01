# Four stages do not attain N = 11 at K = 4 over F2

## Statement

Work in the model of [the multi-pair schedule package](../multipair-schedule-bound/README.md),
the same model executed by its `sched_search.py`. The ground field is **F2**.
There are K bank pairs. A state is a pair of K-dimensional row spaces (P, Q)
in F2^K ⊕ F2^K, modulo left block-diagonal bridges. A stage is
[[I, H], [E, I]] with HE = EH = 0, equivalently a pair of maps
ψ: Q → P and φ: P → Q with φψ = ψφ = 0, and it costs rank(E) + rank(H).
The start is (X, Y) and the goal is (Y, X).

**Theorem (this package).** For K = 4 and s = 4, no schedule reaches the goal
at cost N = 11. Theorem S already gives N ≥ 11, so every 4-stage schedule has
N ≥ 12. Parallel borrowing chains attain N = 12 at s = 3 (predecessor,
odd-stage attainment). Over F2, four stages do not beat three stages at K = 4,
and the minimum over schedules with at most four stages is 12.

The selected record is unchanged.

## Equality skeleton

Write a = dim(P ∩ Y), β = dim(P ∩ X), σ^P = K − a − β, and
d = dim(Q ∩ X), γ = dim(Q ∩ Y), σ^Q = K − d − γ.
Theorem S gives N = 2K + W with W the total waste, and 2K ≤ (s − 1) W.
For K = 4 and s = 4, N = 11 forces W = 3. The same proof, together with
P ∩ Q = 0 (which is preserved because HE = EH = 0 keeps the stage inside
GL), forces every equality schedule through the following signatures
(a, d, σ^P, σ^Q). The verifier enumerates them by a finite integer dynamic
program and keeps only states that can still reach (4, 4, 0, 0) at waste 3.
There are 18 edges:

| from | (rank H, rank E) | to |
|---|---|---|
| (0,0,0,0) | (1,1) | (0,0,1,1) |
| (0,0,0,0) | (1,2) | (0,0,1,2) |
| (0,0,0,0) | (2,1) | (0,0,2,1) |
| (0,0,1,1) | (1,2) | (1,1,1,2) |
| (0,0,1,1) | (2,1) | (1,1,2,1) |
| (0,0,1,2) | (1,1) | (1,1,1,2) |
| (0,0,1,2) | (2,1) | (2,1,1,2) |
| (0,0,2,1) | (1,1) | (1,1,2,1) |
| (0,0,2,1) | (1,2) | (1,2,2,1) |
| (1,1,1,2) | (2,1) | (3,2,1,2) |
| (1,1,2,1) | (1,2) | (2,3,2,1) |
| (1,2,2,1) | (1,1) | (2,3,2,1) |
| (1,2,2,1) | (2,1) | (3,3,1,1) |
| (2,1,1,2) | (1,1) | (3,2,1,2) |
| (2,1,1,2) | (1,2) | (3,3,1,1) |
| (2,3,2,1) | (2,1) | (4,4,0,0) |
| (3,2,1,2) | (1,2) | (4,4,0,0) |
| (3,3,1,1) | (1,1) | (4,4,0,0) |

Any geometric equality schedule has one of these signature transitions.
Ranks outside {(1,1), (1,2), (2,1)} do not appear.

## Orbit reduction

GL(X) × GL(Y) preserves X and Y, hence preserves the start and the goal.
It preserves rank and the geometric condition φψ = ψφ = 0, so it sends
schedules to schedules. The reachable states are a union of orbits.

Stage 1 from the fixed start is the set of all legal matrix pairs of the
three ranks above. Counts: 11025 of type (1,1), 66150 of type (1,2), and
66150 of type (2,1). Each set is closed under the explicit transvection
generators of GL(4,2) × GL(4,2), and each set is a single orbit. One
concrete pair per signature represents every stage-1 equality state.

Later signatures are reduced by transporting P to the standard flag of its
(a, σ^P) (pure-X summand, pure-Y summand, and a paired tilt) and minimizing
the transported Q under a computed list of elements that preserve that flag.
Every element of each K = 4 list was checked, vector by vector, to lie in
the true stabilizer. The list may omit stabilizer elements. Omission only
splits an orbit into extra representatives, which are still expanded.
It cannot identify two states that no real stabilizer element carries to
each other. The stage-2 search nevertheless returned one orbit per
reachable signature, so those orbits are genuine:

| signature | reachable states | orbits |
|---|---:|---:|
| (1,1,2,1) | 10752 | 1 |
| (1,2,2,1) | 1024 | 1 |
| (1,1,1,2) | 10752 | 1 |
| (2,1,1,2) | 1024 | 1 |

From each of those four representatives, every legal shear of the ranks
required by the skeleton was applied. None lands on a stage-3 equality
signature. Because each reachable stage-2 signature is a single orbit, no
reachable stage-2 state has such a child. The three stage-3 edges are
therefore unreachable, and the goal at cost 11 is unreachable.

## Controls

- **Engine.** An independent transcription of the predecessor's exhaustive
  search at K = 2, N ≤ 8, reproduces minimum cost 6 in exactly 3 stages and
  exactly 4 stages. That is the published frontier.
- **Positive equality.** At K = 2, s = 4, the bound is N = 6. A direct
  (no-orbit) enumeration and the orbit enumeration both find a schedule.
  Replaying either schedule reaches (Y, X) at cost 6. Flipping one bit of
  the last H makes the replay miss the goal.
- **Known negative.** At K = 3, s = 4, the bound is N = 8. Both
  enumerations find no schedule. The predecessor's unrestricted equality
  search had the same outcome. In this skeleton the obstruction is visible
  one stage earlier: the unique stage-2 orbit has no equality child.
- **Group orders.** The transvection generators produce |GL(2,2)| = 6,
  |GL(3,2)| = 168 and |GL(4,2)| = 20160.
- **Stabilizers at K ≤ 3.** For every (a, σ^P), the enumerator matches a
  brute-force count over all of GL × GL.

## What remains open

Dimension counts alone do not forbid N = 11: the integer skeleton reaches
the goal. The obstruction is linear algebra over F2. An equality schedule
over another field, or at the economically relevant even value s = 8 in the
predecessor's historical pricing, is a separate question.
