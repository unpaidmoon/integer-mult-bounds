# Division-free dyadic dual-pair exchange

One arbitrary common-chart spare role gives a coefficient-preserving
alternative to Euclidean dual-pair preparation. For the nonunit pair
a=(3,5), b=(2,-1), the emitted basis program falls from twenty gates and
scalar allowance 134 to seven gates and allowance 64, on the same three
roles. This is a scoped constructive proof and compiler improvement,
produced by Nick Petalas. No new kappa is claimed.

Given ab=1, the compiler realizes

```text
S = [[I-ba,b],[a,0]],    S^2 = I,
(a,0) S = e_spare^T,    S e_spare = (b,0)^T.
```

It uses three off-diagonal block shears and one sign SCALE. Every ADD
coefficient is a signed input coefficient. There is no Euclidean quotient,
odd division, INIT, CLEAR or change of chart. Three block shears are
necessary for this particular exchange, even with free invertible
block-diagonal operations. This restricted block count does not establish
optimality among arbitrary scalar circuits.

For A_a and A_b equal to the summed retained ADD tariffs of the row and
column, the cheaper displayed factorization has exact scalar allowance
`2 + min(2 A_a + A_b, A_a + 2 A_b)`. Its gate count is either
`2 nnz(a)+nnz(b)+1` or `nnz(a)+2 nnz(b)+1`; minimizing the tariff can
differ from minimizing the gate count.

Applying S, a D-linear G on the spare, and S again gives
`x -> x+b(G-I)ax`, `z -> z`, for arbitrary incoming z. This complete
consumer has scalar allowance twice the exchange bill, plus the separate
cost of G. During the basis exchange alone, the spare contains ax and is
not restored. Availability of a physical spare is an explicit hypothesis.

[PROOF.md](PROOF.md) gives the complete algebra, block-count obstruction,
prefix growth envelope, coefficient tariff and dirty-spare calculation.
[compiler.py](compiler.py) emits either factorization and selects the
cheaper of these two by default. [verify.py](verify.py) uses a separate
dense Fraction interpreter, full dirty-input columns and an independently
written tariff calculation. [RESULT.json](RESULT.json) is generated and
bound to all package implementation/documentation files and live sources.

## Reproduction

Use CPython 3.12 and the standard library, from the repository root:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/division-free-dual-exchange/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -O -B research/division-free-dual-exchange/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/division-free-dual-exchange
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/division-free-dual-exchange --check-source-history
```

Any CPython 3.12 path can replace the interpreter shown. Expected scientific
marker: `PASS_DIVISION_FREE_DUAL_EXCHANGE`. Expected registered marker:
`PASS_REGISTERED_RESEARCH_PACKAGE`. `verify.py --write` explicitly
regenerates RESULT.json; default replay is read-only. The source comparator
is called only on the one named padded pair, to measure its emitted
program. No predecessor scientific suite is run.

The finite replay passes 116 integer dual pairs with both vectors in
[-3,3]^2 for both factorizations, 64 dyadic pairs through dimension eight,
three valid compiler-boundary cases, nine complete two-coordinate-field
consumers and nineteen rejecting controls. Every
scalar prefix is checked against its proved magnitude envelope. Both
direct warning-strict normal/optimized commands completed in under one
second locally on CPython 3.12. These durations describe the bounded
checks; no execution-speed comparison is claimed.

## Scope, provenance and credit

Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
The selected record at that base has conditional kappa .003125804 and five
retained framework assumptions. The binding-only first example passed.
This changes the `p104-side-correction` card to an enabling scalar-boundary
construction; it does not meet that card's complete supplier acceptance gate.
The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294890)
is the canonical investigation. The first emitted-program improvement is
packaged without a larger construction search.

Ali Romman supplies [PR5611](https://github.com/CrocSwap/integer-mult-bounds/pull/5611)'s
dual-pair specification and complete Euclidean compiler, and
[PR5602](https://github.com/CrocSwap/integer-mult-bounds/pull/5602)'s
helper handoff and scalar tariff, following
[PR5599](https://github.com/CrocSwap/integer-mult-bounds/pull/5599).
All retained P104, native, controller and compiler contributors keep their
credit. Nick Petalas's
[PR5115](https://github.com/CrocSwap/integer-mult-bounds/pull/5115)
is earlier source-only borrowing with no spare and a different shear
contract. The two-role conditioning question in PR6016 is not extended
here. Elementary stabilized completion and block-shear identities are
classical; the new claim is this explicit coefficient-preserving compiler
application and its stated bill, not historical priority for the algebra.
Apache-2.0. Independent human and formal proof-kernel review are unclaimed.

Live handoffs, active Discussions, open PRs, recent account contributions,
main README formulas/objects and merged searches were checked before the
claim. The cached overlap report has sparse local-note coverage. Those
bounded checks do not cover unpublished work or prove global novelty.

This package constructs no physical P104 handoff, productive target split,
native supplier, rounded implementation or favorable complete invoice.
Chart access, spare allocation/lifetimes, G's cost and legality,
precision/storage, compiler closure and outer funding remain obligations.
The source caller's coefficient-magnitude cap remains applicable to an
installation. Selected scientific replay, Lean and a complete multiplication
theorem are outside this result.

## Open next questions

1. Is there a current helper boundary with an available arbitrary spare at
   every chart needed by this exchange and its return? This determines
   whether the compiler can help an actual supplier. First identify one
   exact word, cut, dual pair and spare lifetime, then charge every required
   transport and target debit. Physical availability and the complete
   signed invoice are the blockers.
2. Can a physically legal use of G improve the complete consumer bill after
   chart changes and precision are charged? First price one exact G and its
   full S/G/S macro. The algebraic one-call count alone is insufficient;
   no such source/consumer match is supplied here.

## Executable bounds

Build the Lever led to the retained compiler and executable evidence.
Prove It Works led to full matrix checks, including every arbitrary spare
column. Power of Ten inspection found no recursion in the new code and
kept functions below sixty physical lines. Compiler inputs have at most
sixteen coordinates, 64 numerator bits and 32 fractional bits. Its output
has at most 49 scalar operations. Every loop in the finite verifier has an
explicit fixed dimension or enumeration bound. Checks use exceptions,
so optimized Python preserves them.

Managed Python allocation is a rule 3 deviation bounded by these offline
input, file and enumeration limits; no steady service is provided. Loading
one authenticated predecessor module for the single comparison is a
restricted rule 8/9 deviation with one fixed target. No source-level
dynamic generation or network call occurs. Warning-strict normal and
optimized execution provide diagnostics. No shared lint configuration,
predecessor source, pinned evidence or selected record is changed.
