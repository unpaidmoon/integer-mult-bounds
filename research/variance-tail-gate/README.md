# Sharp mean-variance screen for adaptive compiler tails

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped written proof with exact finite corroboration. The new
compiler application replaces the range-and-mean sufficient screen by the
sharp worst-case screen from the variance as well. For normalized target
log rank Z in a declared containing interval [0,1], write

```text
p=E Z, v=Var Z, 0<x<p<1, 0<v<=p(1-p), q=T(t)/P(t)>=1,
b=p+v/p.

Every law with these statistics has a strict passing tail point iff
q exp[-D(x/b || p/b)] < 1.
```

Here x is the paid tilted mean in the same coordinates and D is binary
relative entropy. The extremal law has masses 1-p/b at 0 and p/b at b.
At equality it fails, while every other law with those moments passes.
The theorem is sharp over laws on a containing interval. An exact-range
requirement can exclude the attaining law; in particular equality passes
for an actual full-range target with nonmaximal variance. Failure of the
screen does not prove that an individual histogram fails the actual gates.
[PROOF.md](PROOF.md) gives the normalization, hypotheses and proof.

The exponential majorant and its equality classification are classical.
Credit [Seneta and Weber, 1982](https://doi.org/10.1017/S144678870001884X),
Corollary 1(ii), and their credited Brook predecessor. No new probability
inequality is claimed. The contribution is its optimized compiler-gate
application, strict equality scope and the integer separation below.

## A new integer histogram separation

At t=1/2 use the abstract integer histograms

```text
W_4=32, W_64=16, W_1024=2; P_32=43.
p=1/2, v=1/8, x=3/8, b=3/4.
```

The new screen gives exactly 128/129<1. A literal passing point is
lambda=1/6, where, with a=2^(1/3),

```text
F(1/6)=(16+16a+4a^2)/43 < 26569/26875 < 128/129.
```

The older optimized range-and-mean screen is strictly greater than one;
its eighth power is 2^60/(3^3 5^5 43^8)>1. This separates the statistical
screens, rather than changing the underlying scalar criterion. The cited
scalar-to-gate equivalence supplies the three tail/ordering gates. Mirror
coverage, recurrence funding and realization of these histograms are not
established. There is no new kappa or selected-frontier change.

## Reproduce

From the repository root, with standard-library CPython 3.12:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/variance-tail-gate/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/variance-tail-gate/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/variance-tail-gate
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/variance-tail-gate --check-source-history
```

Any CPython 3.12 executable can replace the absolute local path. The direct
verifier prints a freshly generated JSON receipt binding all six package
files by SHA256, followed by `PASS_VARIANCE_TAIL_GATE no_new_kappa`.
It writes only stdout and requires no Git repository, network, predecessor
runtime input or third-party library. The universal result rests on the
written proof and cited gate implication, not this finite enumeration.

The finite checks cover:

- All 242 nonzero weight vectors in {0,1,2}^5 on the quarter grid. The 232
  nondegenerate laws give 928 transform comparisons: 64 equalities and 864
  strict inequalities. The checker independently encloses each literal
  transform and its extremal comparator with rational Taylor bounds.
- 6,496 pointwise quadratic-majorant checks, including 3,212 with z>b.
  These also test points beyond the declared unit interval, where the
  classical half-line bound remains valid.
- 120 rational stationary-parameter fixtures and 1,080 exact tariff
  decisions, with 441 passing and 639 failing two-point cases. Independent
  objective and entropy expressions agree, and 4,320 off-minimum trials
  have strictly larger objectives.
- 27 strict comparisons with the older screen and nine coincident
  maximum-variance cases; the new integer histogram, independent cube-root
  brackets, and two laws on the same strict-equality boundary.
- Twelve invalid inputs/capacity cases and four semantic mutants, covering
  a reversed critical ratio, omitted variance, untilted weights and an
  insufficient paid-mass statistical guarantee.

Scientific checks use explicit exceptions and remain active with `-O`.
All functions have fewer than 40 physical lines. Loops use fixed finite
configurations, 64 Taylor terms or 48 bisections. The exponential cache is
capped at 4,096 entries and uses 188 in this domain; rational inputs are
capped at 128 bits. Each receipt source is capped at 128 KiB. There is no
recursion, subprocess or dynamically generated code in the verifier.
Python's managed allocation is a documented Power of Ten deviation from
fixed post-initialization storage; these bounds constrain live data, and
no allocation instrumentation or real-time guarantee is claimed. The
rejection helper has four fixed local call targets. Warning-strict normal
and optimized replay and AST inspection are the local diagnostics.

## Scope and credit

The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19299691)
records the originally posed change from the independent-moment audit card
to a new analytic statistic. No predecessor result is audited, recounted
or reverified as the deliverable. Canonical base is
2485805a6d47f36ea83ddde6327d453ac82d44dc, priority revision 8.
The selected source-binding orientation passed and is metadata evidence
only. The selected conditional kappa remains .003125804.

Credit Nick Petalas [PR5254](https://github.com/CrocSwap/integer-mult-bounds/pull/5254)
for the normalized range-and-mean screen; Ali Romman
[PR5345](https://github.com/CrocSwap/integer-mult-bounds/pull/5345) for the
distinct prescribed-interior-mass screen; Dillon Amburgey
[PR4532](https://github.com/CrocSwap/integer-mult-bounds/pull/4532) for
scalar-to-gate equivalence; zxv PR4436/4483, Jacob Alan Sussman,
Ryanson Jonathan PR4459 and their retained compiler/native/outer lineage.
Their frozen files and credit are unchanged. SOURCES.json pins repository
provenance; none of those proofs is a live verifier input.

These are statistical compiler gates and an abstract histogram. Native
preparation, arbitrary-input caller correctness, owned helper restoration,
mirror/recurrence funding, movement, precision, stock and outer admission
remain open. No native replay, selected cold replay, Lean or Docker run
is part of this package. No framework assumption or complete multiplication
theorem is discharged. Independent human and formal proof-kernel review
are unclaimed. The method stopped at this first original separation.

## Open next questions

- Does a changed source-bound native profile have useful nonmaximal tilted
  variance and also satisfy every mirror and recurrence predicate? Start
  with its exact productive/paid histograms and all mirror intervals.
  Native semantics, restoration and the complete physical bill are blockers.
- Can a certified upper bound on variance suffice when exact log moments
  are costly to enclose? Start with the sign of the quadratic coefficient
  and directed bounds for one actual profile. No source-bound interval
  implementation or complete caller is supplied here.

These are follow-on questions, not additional claims of this package.
