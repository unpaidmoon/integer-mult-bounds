# Proof of the independent chart-pair ceiling

Let `d_r` be a complete change of the paid rank histogram. For `1<=j<=9`,

    S_j(d) = sum_{r=1}^9 d_r min(r,j).

For `0<theta<1`, the forward differences `q_j = j^theta - (j-1)^theta` are
positive and strictly decreasing, with the convention `0^theta = 0`. Summation
by parts gives

    sum_r d_r r^theta
      = sum_{j=1}^8 S_j(d) (q_j - q_{j+1}) + S_9(d) q_9.

Thus `S_j(d) >= 1` for every `j<=7` and `S_j(d) >= 0` for `j=8,9` imply that
the paid moment is at least

    q_1 - q_8 = 1 + 7^theta - 8^theta.

For `x,y>0` and `0<theta<1`, `t |-> t^theta` is strictly subadditive, so
`8^theta = (7+1)^theta < 7^theta + 1^theta`. The displayed quantity is therefore
positive. If instead `S_j(d) >= 2` for every `j`, the same identity gives a
moment of at least `2 q_1 = 2`.

The predecessor single-contact screen attains `d* = {1:+1, 7:+1, 8:-1}`, whose
prefix vector is exactly this threshold: `S_j(d*) = 1` for `j<=7` and `0` for
`j>=8`. Every one of the 18 recomputed classes majorizes that vector. The
verifier repeats the 188,048 single-contact evaluations and matches the class
counts pinned from that screen.

## Contact graph used here

Rebuild the retained 640-input graph. It has 184 variable contacts, each of
degree 4, and every edge incident to a variable contact is an identity-map
constraint. Internal edges form a simple graph of 264 edges: 256 of rank 0 on
the 176 empty-chart contacts, and 8 of rank 8, each joining one of the eight
singleton charts to the empty chart. The eight singleton charts therefore have
no edge between them. There is no independent center reward. These counts are
assertions in `verify.py`, not external inputs.

A one-transvection chart means one of the 1,022 distinct images of a contact's
Lagrangian under the canonical transvection list. Two contacts that are not
joined by an internal edge have disjoint incident edges, so a simultaneous pair
of such charts has histogram equal to the sum of the two single-contact
histograms. That sum still meets the `d*` threshold, and a nonempty edgeless
set of `s` such charts has moment at least `s(1+7^theta-8^theta)`. In
particular, retagging any subset of the eight singleton charts, while leaving
every empty-chart contact fixed, is an edgeless set.

## Empty-chart neighbor geometry

Every one-transvection image of the empty-chart Lagrangian is at distance 1
from it. Among the 1,022 images, the unordered distances are 1,022 self-pairs
at distance 0, 511 pairs at distance 1, and 521,220 pairs at distance 2. The
distance-1 pairs are a perfect matching, and they are exactly the consecutive
pairs emitted by the canonical axis list. Consequently, for an ordered pair of
charts on a rank-0 edge there are three possibilities.

The original edge has rank 0. Moving exactly one end replaces that rank by 1.
The joint histogram therefore differs from the sum of the two unilateral
histograms by a correction supported on the shared edge:

- same chart: distance 0, correction `{0:+2, 1:-2}`;
- partner charts: distance 1, correction `{0:+1, 1:-1}`;
- every other ordered pair: distance 2, correction `{0:+1, 1:-1, 2:+1}`.

For distance 2 the correction has `S_1 = -1` and `S_j = 0` for `j>=2`. Adding
two `d*` thresholds leaves `S_1 >= 1`, `S_j >= 2` for `2<=j<=7`, and
`S_8,S_9 >= 0`. Every actual unilateral class is at least `d*`, so every
distance-2 assignment on a rank-0 edge meets the moment bound. This case does
not depend on which private edges the two contacts have.

The same-chart and partner corrections can destroy that crude bound. Two copies
of `d*` plus either correction fail the prefix test; the verifier rejects both
synthetic histograms. Those two families are therefore enumerated on the real
incident edges: 256 edges times 1,022 same-chart assignments, and 256 edges
times 1,022 ordered partner assignments. Every one meets the `d*` threshold.
At least one same-chart assignment attains the `d*` prefix vector, so the
constant `1+7^theta-8^theta` is sharp for adjacent pairs as well as for single
contacts.

## Rank-8 edges

Each of the eight rank-8 edges gets the full product of 1,022 charts at each
end, 8,355,872 assignments. The shared-edge correction is

    {8:+1} - {r_u} - {r_v} + {r_uv},

where `r_u` and `r_v` are the ranks after moving only one end and `r_uv` is the
rank after moving both. The verifier applies that correction to the stored
unilateral histograms and checks it against a direct incident-edge walk,
including assignments that preserve the original rank 8. Every assignment has
`S_j >= 2` for all nine prefixes, so its paid moment is at least 2 for every
`theta>0`.

## What is not proved

A connected set of three or more contacts can contain two internal edges. The
pair correction does not price that joint histogram, and the coherent-block cut
still requires one common alternative. Changed native maps, scalar operations,
endpoints, helper returns and a new route are outside this graph. No identity
above is a native phase, caller, compiler or outer-multiplication theorem, and
none of them raises the selected κ.
