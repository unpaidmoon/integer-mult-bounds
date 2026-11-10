# Every unequal T1 mask pair has a monotone chain

**Exhaustive finite census, with an explicit word for every pair. No new κ.**
In the unsigned six-source characteristic-6 floor model, all 2280 endpoint
pairs whose masks differ are realized by a floor word that keeps the
multiset `(6,6,6,7,7,7)` at every index `s = 4,...,18`. The equal-mask
pairs are the 120 pure slides of PR #7042 and are not rebuilt as the new
claim. The selected conditional κ remains `781451/250000000`.

The argument and the orbit table are in [PROOF.md](PROOF.md).

## Scope and evidence

Original card: `connector-alphabet-change`. The card asks whether one new
connector operation has a favorable budget. Scope status: **changed**. The
alphabet stays the unsigned dirty connector. The assigned question is open
question 1 of PR #7042: which unequal endpoint masks are joined by a
monotone chain of this multiset.

The predecessor already showed that every equal-mask pair works and that
one unequal pair works. The missing statement was the boundary of that
transport. This package lists every unequal pair, splits them into the ten
orbits of the symmetric group on the six sources, finds one 14-step path
in each orbit, and checks the transported word on all 2280 pairs.

Evidence class: **exhaustive finite census**. The domain is the finite set
of triples `(M_4, D, M_18)` with `M_4 ≠ M_18`. The enumeration is every
3-subset pair and every final letter. Each word is checked against the
diagonal multiset at all fifteen indices. A failed search is not used; every
orbit returned a witness. This is not a proof about shapes other than
`(6,6,6,7,7,7)`, and it is not unrestricted nonexistence or existence
outside this model.

`current-priorities.md` on this base still prints the older decimal from
#5599. The verifier reads `certificates/selected-result.json` and does not
edit it.

## Reproduce

Python 3.12, standard library only, from the repository root:

```sh
python3 -B research/c6-t1-unequal-mask-chains/verify.py
python3 -O -B research/c6-t1-unequal-mask-chains/verify.py
python3 -B scripts/research_package.py --package research/c6-t1-unequal-mask-chains
```

The marker is

```text
PASS_C6_T1_UNEQUAL_MASK_CHAINS pairs=2280 orbits=10 witnesses=10 checked=2280 controls=7
```

The controls recheck the two endpoint domains (20 splits at `s = 18`, 120
splits at `s = 4`), the recorded moving word, a swapped-letter failure, the
ten orbit sizes, and the selected κ string. Checks raise `SystemExit`, so
`-O` does not strip them.

Not run: a proof assistant, a SAT solver, a supplier or native replay, and
`scripts/research_selected_baseline.py`. The selected record is provenance
and the κ guard only.

## Open next questions

- For one separation-3 family other than type T1, which unequal endpoint
  masks are joined by a monotone chain of that family's multiset? *Why:*
  T1 is the only family with no coordinate 12, and its transport is now
  complete. A family that uses a 12 has a different legal step. *First
  step:* fix that family's multiset, list its legal exchange, and search
  one symmetry class of unequal masks. *Blocked by:* the step rule in this
  package exchanges a 6 with a 7 only. It does not apply to a coordinate
  12.

## Credit

The depth-two interface is Nick Petalas's (PR #4231, PR #4248, PR #6107),
with the Ross Richardson PR #934/PR #943 lineage. JosieElliston's PR #6141
records the c=6 solver verdict. PR #6955 classifies the empty centre.
PR #7029 isolates type T1 as the family with no frozen 12. PR #7042, head
`807149a85d185b8272aa1fda43ba6d8d7c541cfe`, constructs the 120 equal-mask
words, one moving word, and the two endpoint lemmas used here. Those lemmas
are rechecked on the same finite domains and are not a new classification.
The upstream finding that records the open question is discussion comment
19514157.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Independent
human review and a proof-assistant proof are unclaimed. Apache-2.0.
