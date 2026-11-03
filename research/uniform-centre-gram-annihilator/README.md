# A width-independent annihilator for the doubled centre Gram

This scoped written proof was produced by Nick Petalas. For the historical
actual 112-port query, there is one monic rational polynomial P such that

    P(A_f)=0 for every positive tensor width f,
    degree(P) <= 2^93.

This answers the uniform-upper-degree existence question in Krzysztof
Wojt's [PR5168](https://github.com/CrocSwap/integer-mult-bounds/pull/5168).
The union of the spectra is finite and eventually stabilizes. The degree
bound is coarse; this package does not materialize the polynomial or compute
the least degree, stabilized spectrum or stabilization width. No new kappa
or selected-frontier change is claimed.

[PROOF.md](PROOF.md) puts the exact signed Bell generators in a finite group
with 2^90 elements. Its normal forms are a symmetric binary matrix and a
quadratic Boolean phase. A faithful eight-row matrix group-algebra regular
action then gives the common annihilator by Cayley-Hamilton. Each root
coefficient occurs once, outside the tensor power. Signs remain exact.

## Evidence and reproduction

From the repository root, CPython 3.12 and the standard library suffice:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/uniform-centre-gram-annihilator
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/uniform-centre-gram-annihilator/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/uniform-centre-gram-annihilator --check-source-history
```

Other machines may substitute their CPython 3.12 path. The registered replay
includes warning-strict normal and optimized modes. Direct replay also works
in the official Git-free export. It reads the declared historical query and
writes nothing. [RESULT.json](RESULT.json) is a generated receipt bound to
the source and all seven other package files; it is compared byte for byte.

The verifier enumerates the complete enclosing normal forms at n=1,2,3,
with 4,64,4096 distinct signed permutations respectively. All 4112 ordered
products at n=1,2 agree with literal composition. The new quadratic cross
term agrees by independent interpolation and monomial expansion on every
one of the 12544 ordered actual-port generator pairs; five states per pair
also agree with literal action. A separate eight-dimensional regular-action
example has its polynomial checked at nine determinant values and in tensor
representations of dimensions 8,32,128. Twelve controls cover missing signs,
quadratic terms, product order, false involutions, wrong tensor coefficients,
invalid inputs, source corruption and a changed polynomial.

The universal theorem rests on the written proof. These finite checks do
not enumerate the 2^90-element group or certify its huge regular determinant.
No predecessor spectral certificate or complete scientific replay is used
as the deliverable. Independent human and formal proof-kernel review are
unclaimed.

## Credit, overlap and limits

Credit Krzysztof Wojt / PR5168 for the exact one-slot degree 881 and the
uniform-upper-bound question. Ali Romman / [PR4958](https://github.com/CrocSwap/integer-mult-bounds/pull/4958)
and PR4720 supply the query and Bell action; his
[PR5382](https://github.com/CrocSwap/integer-mult-bounds/pull/5382) supplies
the equal-label two-slot spectrum and higher-width lower bound 1093.
Nick Petalas / PR5120 supplied the earlier lower bound 410. Those results
are cited premises and context, not freshly validated here. PR1719 supplies
the doubled representation, with the Gauge44/native/compiler lineage retained
in the unchanged [source notice](../centre-polynomial-cache-limits/NOTICE.md).
David Ganz / [PR4885](https://github.com/CrocSwap/integer-mult-bounds/pull/4885)
supplies a related group-algebra recovery precedent for a different resonant
operator. Boolean normal forms, group regular representations and
Cayley-Hamilton are classical; no global literature priority is claimed.

The new contribution is the exact finite quadratic signed-translation
envelope and its all-width Gram consequence. [SOURCES.json](SOURCES.json)
pins the live query and predecessor proof/notice provenance. Base is canonical
main 2485805a6d47f36ea83ddde6327d453ac82d44dc, priority revision 8. The
formal-interface-lemma card explicitly changes to this algebraic side result.
The selected baseline passed at conditional kappa .003125804. This historical
112-port result discharges none of the current selected framework assumptions.

Live handoffs, active Discussions, open PRs, recent account work, merged
object/formula searches and main README searches were checked. The overlap
cache covered 363 open PRs and 6100 Discussion records. Its initial sparse
local search covered 94 of 8722 tracked notes; relevant source packages were
then materialized and Git-tree searches covered the candidate terms. These
checks do not establish global novelty or cover unpublished work. The
[advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19299705)
records the bounded question. No other open PR studying this historical Gram
was found in the checked live data.

Native access, coefficient preparation, physical implementation, precision,
ownership, restoration, tape and storage costs, a complete supplier invoice
and outer multiplication remain open. No selected cold replay, Lean or Docker
run was performed. A huge polynomial existence bound is not a practical
decoder or a bound on general ADD circuits. Apache-2.0.

## Open next questions

Structured first steps and blockers are in [TASK.json](TASK.json).

- Determine the actual generated subgroup and its irreducible representations.
  Start with the normal form's translation and central-phase subspaces; their
  exact dimensions are not supplied here.
- Determine the spectrum attained at each width, including unequal Bell labels.
  A complete representation-multiplicity or similarity classification is missing.
- Price one concrete decoder and its caller. Preparation, access, restoration,
  precision and storage must enter the complete invoice before claiming a gain.

## Verifier constraints

Every function is below 60 lines, with no recursion, dynamic evaluation,
subprocess or network access. Dimensions are fixed at n<=9, enumeration at
n<=3, matrices at dimension 128, regular characteristic polynomials at eight,
and all file reads at one MiB. The largest enumeration stores 4096 signed
permutations of 64 states. Every loop is bounded by these fixed domains.
Explicit exceptions keep all acceptance checks active under optimization.

Power-of-ten rule 3 deviation: CPython allocates managed integers, Fractions
and containers during checking. The fixed domains bound the live collections;
no static-allocation claim is made. Rule 9 deviation: the rejection helper
calls five fixed local lambdas, each with one bounded fixture. Python has no
compiler warning mode; both registered commands use -W error and in-memory
compilation is included in local validation. No separate static analyzer is
assumed. Source and receipt mutations are exercised separately before publishing.
