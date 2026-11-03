# A sharp error floor for shared translated Fourier routines

This contribution was produced by Nick Petalas. Apache-2.0.

Scoped written proof with exact finite corroboration. For any finite product
of cyclic groups and any nonzero order-two translation, the best shared
phase-weighted two-input Fourier convolution routine has error

    min relative coefficient error = min worst basis-pair relative output error
                                   = sqrt(2 - 8/(3 sqrt(3))).

Both forward passes use the same routine and the final pass conjugates that
routine's coefficients. Both Fourier signs use 1/N normalization, so the
desired output is (u*v)/N². The output error uses the Euclidean norm.
The optimum is independent of the group size. The explicit unit weights

    w(x) = 1/sqrt(3) - i sqrt(2/3) chi(b,x)

attain it on every basis-input pair. [PROOF.md](PROOF.md) defines both error
norms and proves the universal statement. This is a quantitative obstruction
to replacing an exact convolution boundary with this approximate shared
translated routine. It supplies no new kappa or physical construction.

## What is new and what is inherited

Hanson Sun / bbMisk's [PR1477](https://github.com/CrocSwap/integer-mult-bounds/pull/1477)
classifies the exact weighted Fourier interface, extending Ross Richardson's
[PR940](https://github.com/CrocSwap/integer-mult-bounds/pull/940). It already
rules out exact shared translated convolution. The new result quantifies the
smallest achievable error and supplies its attaining weights. The two-moment
inequality, coefficient-norm invariance and character orthogonality are
elementary tools; no literature-priority claim for those tools is made.

The original approximation question is not the open physical-routing question
in PR1477. The exact classification and its census were cited, not re-audited.
Nick Petalas's older PR4874 treats exact cancellation at arbitrary arity.
PR5946 restricts the second input with unequal forward reads and fixed
first/final charts. The present contract has two unrestricted inputs, shared
reads and phases, and measures approximation error. Its proof does not rely
on either of those packages. The separate concurrent PR1477 replay-arithmetic
work retains the predecessor's original decisions and is distinct from this
mathematical question.

This is a changed `joint-query-controller` side result. It addresses the
precision/analytic boundary of a proposed Fourier contract, rather than an
active-mode injection, helper-split search or selected paid-word change. The
selected source orientation passed at main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8, selected
conditional kappa .003125804. No selected assumption is discharged.

## Reproduction and evidence

From the repository root, using CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/shared-fourier-translation-floor/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/shared-fourier-translation-floor/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/shared-fourier-translation-floor
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/shared-fourier-translation-floor --check-source-history
```

Use another CPython 3.12 path on other machines. The direct marker is
`PASS_SHARED_FOURIER_TRANSLATION_FLOOR`. The verifier prints a generated JSON
receipt with all seven package hashes, both live source hashes and an ordered
scientific digest. It writes no receipt into the checkout. There are no
numerical tolerances or floating-point acceptance checks; the field is
Q(sqrt(2),sqrt(3),i).

The fixed finite evidence includes the algebraic field relations, all 512
basis associativity triples, the exact polynomial identity proving the
scalar maximum, 560 rational scalar grid points, and literal three-pass Fourier
circuits. Sixteen group/offset fixtures check all 772 basis-input pairs.
The minimizers cover every nonzero order-two offset in Z/2, Z/4, (Z/2)²,
Z/8, Z/2 x Z/4 and (Z/2)³.
A separate coefficient interpreter and the scalar-moment formula agree.
The finite phase catalogue checks all 1,332 assignments from
{1,-1,i,-i,(3+4i)/5,(3-4i)/5} on Z/2 and Z/4; twelve selected assignments also
receive 120 literal basis-pair checks of the Parseval normalization.

Controls reject malformed groups, zero and wrong-order translations,
nonunit weights and invalid field values. They distinguish the attaining
global phase, final conjugation and inverse Fourier sign. Separate forward
and final weights give an exact zero-error escape, verifying that the shared
contract matters. The unweighted translated routine has squared error two.
Acceptance checks remain enabled under `-O`.

The universal theorem rests on the written proof, not the finite catalogue.
Independent human and formal proof-kernel review are unclaimed. No selected
cold replay, Lean, Docker, native implementation or complete multiplier was run.

## Bounds on the checker

The checker has no recursion and no unbounded search. Functions are below
60 physical lines. Its exact field has eight rational coefficients, groups
have at most eight elements and three axes, and the largest phase product has
6^4 assignments. The root-power loop has at most seven iterations. Local
source inputs are limited to 1 MB each. Correctness checks raise explicit
exceptions and survive optimized execution.

Power-of-Ten rule 3 requires a managed-runtime deviation. Python, dataclasses,
Fraction arithmetic, hashing and JSON allocate while checking. This is confined
to the fixed finite replay above, which has no user-sized mathematical inputs
or retained process cache. The command ends after one bounded replay and writes
only to stdout. The compensating controls are the explicit domain limits,
normal and optimized complete execution and capacity-rejection control.
A fixed-storage port would be needed before using this checker in a setting
that forbids runtime allocation. Rule 9 also has a narrow test-only deviation:
the rejection helper calls one of eight closed local lambdas, never external
callbacks. Warning-strict direct execution and registered replay are the
available Python diagnostics; no repository-wide analyzer is added.

## Open next questions

1. What is the sharp shared-routine error for translations of order greater
   than two? The balanced sign reduction no longer applies. Start with Z/3
   and derive the corresponding constrained character-moment problem before
   any numerical search. This would distinguish a general translation barrier
   from the order-two theorem. The unresolved moment optimization is the blocker.
2. What is the sharp error on arbitrary unit-norm input pairs? The coefficient
   and worst basis-pair norms here do not determine that bilinear operator
   norm. Start by using the two-output formula for the exhibited minimizer,
   then establish a matching lower bound over all phases. An optimizer for
   that different norm and physical implementation costs remain open.

The structured questions are in [TASK.json](TASK.json). No further scope is
reserved, and the first proved improvement is the result packaged here.

## Credit and limits

Credit Hanson Sun / bbMisk for PR1477's interface and exact theorem, Ross
Richardson for PR940, and the retained manuscript, Fourier and analytic
contributors for the normalization and construction context. Predecessor
files and credit lines are unchanged. [SOURCES.json](SOURCES.json) pins the
predecessor contract and original resampling section. No executable source
or scientific receipt is borrowed from a predecessor.

The attaining algebraic phases are not a priced Gaussian-dyadic program.
Separate weights, other read maps, input restrictions or nonunit weights
change the hypotheses. There is no uniform relative-error claim for inputs
whose exact convolution vanishes. Native maps, restoration, movement,
precision/storage costs, the complete paid invoice, supplier admission and
all five selected framework assumptions retain their prior status.
