# Sharp common-metric orthogonality energy on P104

This contribution was produced by Nick Petalas. Apache-2.0.

A common ambient deformation of a two-frame-punctured E8 configuration obeys
an exact sum-of-squares constraint. For any real symmetric metric A, let
A0=A-tr(A)I/8 and sum the squared values u^T A v over unordered orthogonal
unit-root pairs remaining after two disjoint frames are removed. Then

    E_P(A) = 37 ||A0||_F^2
             + (17/2) sum_{u in the two frames}(u^T A0 u)^2
             + sum_{orthogonal u,v in different deleted frames}(u^T A0 v)^2.

Thus E_P(A) >= 37 ||A0||_F^2. An explicit rational symmetric involution has
norm squared 8 and energy 296, proving the uniform constant sharp. Rational
invertible common maps I+sA attain equality arbitrarily near identity.
For M=T^T T, the defect energy bounds distance from a conformal metric by
||M-tr(M)I/8||_F <= sqrt(E_P(M)/37).

Claim type: scoped proof with exact finite premises and an equality
certificate. [PROOF.md](PROOF.md) gives the quantified argument. [verify.py](verify.py)
uses integer arithmetic and the standard library. This is a quantitative
obstruction to changing the common ambient metric while keeping the E8
orthogonality constraints approximately exact. It supplies no new kappa.

## Evidence and reproduction

From the repository root:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/p104-metric-energy/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/p104-metric-energy/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/p104-metric-energy
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/p104-metric-energy --check-source-history
```

Any CPython 3.12 interpreter can replace the local absolute path. Expected
status: `PASS_P104_METRIC_ENERGY`. The checker enumerates 120 root lines,
3,780 full orthogonal pairs and all 120 stars, checks 1,296 coefficients per
quadratic identity, and evaluates all 2,860 orthogonal pairs of the explicit
sharp example. Seven controls reject changed premises or stronger constants.
The printed receipt is generated from current file hashes and computed values.
No generated files or logs are written into the checkout.

Local normal and optimized direct checks and both registered commands passed
on CPython 3.12.15, macOS 27.0.1 arm64. Each direct command took 0.13 seconds
in the initial timed run. Hosted CI is recorded separately in the PR body.

The checker has fixed dimension eight, 36 symmetric coordinates and at most
7,140 candidate root pairs. Every loop ranges over one of these fixed finite
collections. Managed Python allocation is bounded by those inventories; no
fixed-allocation claim is made. Six fixed callbacks are used only for rejecting
controls. Functions have at most 26 physical lines. Warning-strict normal and
optimized execution supply the local Python diagnostics; no external static
analyzer was available. These are implementation limits, not extra premises
of the mathematical theorem.

## Scope, predecessors and novelty

The exact E8 masked-realization questions and qualitative rigidity precede
this result. Credit Brett Halligan / [PR1212](https://github.com/CrocSwap/integer-mult-bounds/pull/1212),
Aaron Wang / PR1292, Josie Elliston / PR1389 and PR1399, and their retained
E8 decoder lineage. Their broader decoder theorems are context, not premises
replayed here. The root coordinates and elementary frame identities are
standard. No predecessor implementation is imported or copied. The new step
is the explicit quantitative energy identity, constant 37 and sharpness family.

This changes the `complex-rank-shape-decoder` card to a geometry boundary
question. It quantifies the absolute orthogonality defect forced by a common
ambient deformation. It does not bound independent port motions,
general fitting matrices, normalized correlation errors, helper topology or
productive credits. The sharp example is not identified with the selected
frame-pair orbit. The lower bound itself holds for every disjoint frame pair.
No selected supplier replay, physical implementation, full signed invoice,
formal proof-kernel check or complete multiplication theorem is supplied.
Independent human and formal proof-kernel review are unclaimed.

The selected-binding orientation command passed at base
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. The selected
conditional kappa remains 781451/250000000. Its five framework assumptions
remain. Live open PRs, active Discussions, account history, claims, main
READMEs and merged formula/object searches were checked before claiming;
these bounded and sparse searches do not establish literature priority.
The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294832)
records the original question.

## Open next questions

- Is 37 also the sharp constant for each individual disjoint-frame orbit,
  including the selected P104 orbit? First fix that orbit and evaluate the
  residual squares on trace-free symmetric matrices. This could strengthen
  a source-specific obstruction. The present uniform theorem does not identify
  the selected orbit's equality space.
- Can a useful decoder change escape common-metric rigidity through independent
  port motions while retaining legal labels and a favorable complete bill?
  First exhibit one arbitrary-input local identity with its restored outputs
  and actual consumer. Native realization and the complete invoice remain open.

See [TASK.json](TASK.json) for the structured questions and scope declaration.
