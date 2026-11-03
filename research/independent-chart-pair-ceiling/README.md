# Independent one-transvection chart pairs still lose

On the retained 640-input center-contact graph, every simultaneous pair of
one-transvection charts at two variable contacts strictly raises the paid
moment for every `0<theta<1`. **No higher κ, extra center reward, supplier
admission, or selected-frontier change is claimed.**

The selected record pinned at the package base remains
`κ = 781451/250000000 = 0.003125804` (PR #6030). This package does not rerun
that frontier.

## What was already known

[research/sol1337-contact-frontier](../sol1337-contact-frontier/README.md)
(PR #4867, handoff
[discussion comment 19133861](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19133861))
proved a strict loss for three families: one contact, one common transvection
on an adjacent pair, and an arbitrary subset of the 176 empty-chart contacts
retagged to one common one-transvection alternative. Its open remainder was
mixed alternatives, independently chosen paired axes, and simultaneous changes
of different original chart groups. The same handoff stops the naive lift of
all 112 Y exits from rank 8 to rank 9 (224 rank-one children against at most
64 centre rank units). This package answers the chart-pair remainder only.

## Result

Rebuilding the same graph gives 184 variable contacts, each of degree 4:

- 176 contacts on the empty chart, with 256 internal rank-0 edges;
- 8 singleton charts, each joined to the empty chart by one rank-8 edge and
  not joined to each other;
- every edge incident to a variable contact is an identity map;
- independent center reward stays 0.

There are 1,022 one-transvection charts at each contact. For any two contacts
and any ordered pair of those charts, with every other contact fixed:

| Placement | Assignments | Paid-moment lower bound on `(0,1)` |
|---|---:|---|
| No internal edge between them | disjoint sum of two single moves | `2(1+7^θ-8^θ)` |
| Rank-0 edge, charts at distance 2 | algebraic, from the 18 single classes | `1+7^θ-8^θ` |
| Rank-0 edge, same chart | 261,632 recomputed | `1+7^θ-8^θ`, and the prefix is attained |
| Rank-0 edge, the unique distance-1 partner | 261,632 recomputed | `1+7^θ-8^θ` |
| Rank-8 edge, any chart pair | 8,355,872 recomputed | `2` |

The single-contact census is repeated and matches the #4867 class counts
(188,048 moves, 18 classes), all of which majorize `{1:+1, 7:+1, 8:-1}`.
Empty-chart neighbor distances are 1,022 self-pairs, 511 distance-1 pairs
forming a perfect matching, and 521,220 distance-2 pairs. The argument is in
[PROOF.md](PROOF.md).

Any edgeless set of these contacts adds. Retagging any subset of the eight
singleton charts, with the empty-chart contacts fixed, is the case `s` of that
corollary and loses at least `s(1+7^θ-8^θ)`.

Two copies of the minimum single histogram plus either the same-chart or the
partner correction fail the prefix test. Those crude bounds are rejected on
purpose; the corresponding real assignments are enumerated. One same-chart
joint and one partner joint on a rank-0 edge, and one rank-preserving rank-8
joint, are recomputed from the incident edges and must match the correction
formula.

## What this does not cover

Three or more contacts that include an internal edge, with independently chosen
charts, are not priced. A common alternative on one original-chart group remains
the coherent-block theorem already proved in #4867; mixed labels on a connected
triple are not a corollary of these pairs. Changed maps, scalar operations,
endpoints, helper returns, routes, and a completed caller are not constructed.
The negative pair bill makes those costs unnecessary for this chart grammar.

## Reproduce

Python 3.12 or newer, standard library only. From the repository root:

```sh
python3 -B research/independent-chart-pair-ceiling/verify.py
python3 -B scripts/research_package.py --package research/independent-chart-pair-ceiling
```

Expected marker: `PASS_INDEPENDENT_CHART_PAIR_CEILING`.
The replay rebuilds the contact graph, repeats the single-contact census,
checks the empty-chart distance matching, enumerates the same-chart, partner,
and rank-8 families, and runs the rejection controls above. It does not run the
predecessor C++ flow, native amplitudes, Lean, or the selected frontier.

## Open next questions

1. Can three contacts on a connected internal path, with independently chosen
   one-transvection charts, make the joint paid moment nonpositive? Pairs and
   edgeless sets lose, but two shared edges are a different correction. The
   first step is one rank-0 path of length 2, or a multi-label reduction that
   reuses this pair certificate. A direct screen is `1022^3` triples, larger
   than this pair budget, and no such reduction is proved here.

2. Can one changed role-dependent route, other than a contact-chart retag,
   clear a positive optimistic moment while retaining every `R_X` observation,
   centre-to-Y coupling, and independent helper return? That is the routing
   half of handoff 19133861. The first step is one chronological route, a
   640-input endpoint, and the full producer/consumer histogram. No such route
   is supplied here, and the handoff already stops the naive rank-8-to-9 lift
   of all 112 Y exits.

## Credit and source boundary

Cinna Davis / 1337isnot1337 supplied the retained-center ABI and contact model.
Cao Yifan / intqwq supplied the frozen round-three native word. Dugongue
supplied the phase-exact neighborhood grammar used by PR #4867. Chris R /
Clear1nsight, with substantial OpenAI Codex assistance, proved the
coherent-contact ceiling that this pair census extends. The scalar, E8,
Clifford, helper, precision, compiler, and outer lineage retains its credit.

Prepared by unpaidmoon with substantial Cursor Grok assistance. New work is
Apache-2.0. No independent human or formal-kernel review is claimed. Exact
source commits, blobs, and SHA256 pins are in [SOURCES.json](SOURCES.json).
Frozen predecessor files are unchanged.
