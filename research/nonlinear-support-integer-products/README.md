# Faster complete nonlinear support replay with integer Gaussian products

This contribution was produced by Nick Petalas. Apache-2.0.

The complete finite support caller from Chris R / Clear1nsight's
[PR5210](https://github.com/CrocSwap/integer-mult-bounds/pull/5210) takes
24.54% less median wall time in the retained local measurement, from
98.860 ms to 74.598 ms. Complete RESULT/MATRICES files and the original
wrapper report remain byte-identical. This is an empirical tooling improvement
with a scoped arithmetic equivalence proof. No new kappa, predecessor theorem
audit, native supplier or multiplication theorem is claimed.

The new runner authenticates all 46 pinned source-package files, invokes the
original evidence authentication, copies the original logical inputs into
private scratch, and executes the unchanged finite checker's main function.
Its only scientific substitution is the matrix-product function. It compares
both output files against both frozen modes and checks all copied input bytes
after use. Source files and their notices remain unchanged.

## Representation and proof

For each operand A, choose e equal to the maximum binary denominator exponent
among its real and imaginary Fraction components. Write A=2^(-e) A_int, where
A_int has Gaussian-integer entries. For B=2^(-f) B_int, compute

```text
AB = 2^(-e-f) (A_int B_int)
(a+ib)(c+id) = (ac-bd) + i(ad+bc).
```

Every shift is exact because the denominators divide 2^e or 2^f. The ordinary
matrix product is a finite sum of these exact terms. Reconstructing Fraction
components with denominator 2^(e+f) returns the same canonical fractions as
the original implementation. Omitting zero terms changes no sum. Reusing the
caller's immutable zero tuple changes no value or aliasing behavior.

`products.py` accepts square matrices of dimension 1 through 16, Fraction
numerators of at most 256 bits and dyadic denominator exponents at most 64.
It validates every noncanonical-zero entry. A shared zero is skipped only after
its immutable tuple and Fraction components have been validated. Odd denominators
and larger inputs are explicitly rejected. The product is exact on this accepted
domain; an arbitrary next multiplication need not fit the same input bounds.
The unchanged finite caller's complete execution fits those bounds.

Induct on the finite caller's product calls. Source inputs are identical; each
replacement returns the same dense list of Gaussian Fraction pairs. Intervening
original operations, branches, controls and serializations receive equal values.
This proves equivalence for this authenticated complete finite caller. It does
not extend the predecessor's written all-width theorem or establish a general
Gaussian-rational product service.

The first dense normalization prototype was slower under profiling because
conversion dominated the saved Fraction arithmetic. A sparse normalization
prototype then had no measurable arithmetic improvement in five complete runs.
The accepted version skips a validated shared zero before conversion and preserves
that zero on output. Optimization stopped at its first verified improvement.

## Complete-caller measurements

Eighteen fresh processes per mode used all six execution orders three times.
There were zero failures, byte-identical complete reports and 277 products in
every adapted run. The integer runner beat the original in all 18 matched rounds
and the reference adapter in 17 of 18. Its slow outlier is retained below.

| Complete caller | Median ms | Minimum ms | Maximum ms |
| --- | ---: | ---: | ---: |
| Unchanged original wrapper | 98.860 | 97.538 | 131.133 |
| New runner, original Fraction product | 86.495 | 85.847 | 89.032 |
| New runner, integer product | 74.598 | 73.881 | 94.632 |

The overall improvement combines integer arithmetic with executing the same
finite main inside the authenticated runner rather than in another child
interpreter. The original-product reference adapter isolates the arithmetic
change: its median decreases a further 13.75% with integer products. The
24.54% headline must not be attributed to arithmetic alone.

Interpreter startup, imports, source authentication, input copying, all checks,
output comparison, serialization and scratch cleanup are inside the parent wall
timer. No result cache is used. A separate profiled reference execution assigns
0.129 of 0.207 seconds to the 277 product calls. Profiled times are excluded from
the sample. Fraction arithmetic and zero comparisons explain that hotspot;
remaining checks and startup limit the complete improvement.

Environment: CPython 3.12.15, macOS 27.0.1 arm64, 18 logical CPUs. Host load was
uncontrolled. Initial load averages were 6.09/4.17/2.73, with another Python
process using one core; final averages were 1.55/2.68/2.43. These are local
observations, not a portable speed guarantee.

The timing sample binds implementation commit 662e18c310b2fe3e7594bee9290350cab6eacaf6.
A later fix makes only temporary mutation-control copies writable when replaying
from a read-only export. The timed runner and arithmetic bytes are unchanged.

## Reproduce

From the worktree root, with this interpreter or another CPython 3.12:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/nonlinear-support-integer-products
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/nonlinear-support-integer-products/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/nonlinear-support-integer-products/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/nonlinear-support-integer-products --check-source-history
```

Expected markers are `PASS_NONLINEAR_SUPPORT_INTEGER_PRODUCTS`,
`PASS_REGISTERED_RESEARCH_PACKAGE` and `PASS_RESEARCH_COMMIT_BYTES`.
The verifier compares all 277 actual products and all 70,912 entries with the
retained product function. It also checks 146 additional product fixtures,
including capacity boundaries, ten invalid inputs, a changed source file and
an actual incorrect Gaussian multiplication sign. The retained sign control
rejects the latter. Additional fixtures are execution cases, not distinct-matrix
counts. Complete RESULT/MATRICES match both frozen modes, and the original
wrapper report agrees. Explicit exceptions preserve checks under -O.

To benchmark, choose a fresh external output path and keep temporary files there:

```sh
TMPDIR=/path/to/scratch /Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/nonlinear-support-integer-products/benchmark.py --rounds 18 --output /path/to/scratch/new-measurement.json
```

The benchmark generates its receipt from completed executions and binds all
four Python files by SHA256. The verifier emits a generated receipt bound to
package hashes. No receipt is handwritten. Default replay leaves the checkout
unchanged. CI checks exact conformance, not wall-time gains.

## Scope, attribution and limits

Scientific base is canonical main 2485805a6d47f36ea83ddde6327d453ac82d44dc,
priority revision 8, selected conditional kappa 781451/250000000. The current
selected-binding control passed. The historical card is refined to this
implementation question; selected scientific replay is outside scope.

Credit Chris R / Clear1nsight for PR5210's finite checker, portable evidence
wrapper, controls, complete output fixtures, reviewed written theorem and its
retained coded-native, released-operator and nonlinear-control predecessors.
The source package retains all prior attribution and notices. This package
does not certify that theorem's proof. Common-denominator matrix arithmetic
and sparse multiplication are classical; their bounded adapter and complete
caller integration are the new implementation contribution.

Live handoffs, active Discussions, open PR bodies, recent account work, main
README terms, merged object searches and reservations were checked before the
advance [claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294906).
The cached task helper had no usable remote snapshot and covered only 95 of
8,722 main note paths. Live queries and direct main searches supplement it.
Unpublished work and arbitrary historical diffs remain outside coverage.

Independent human and formal proof-kernel review are unclaimed. No 17-axis
native replay, uniform compiler, physical caller, precision/stock bill, selected
cold replay, Lean or Docker check was run. Larger matrices, odd denominators
and performance on another host remain outside scope.

## Open next questions

Can one larger native/caller checker use this representation with a useful
complete runtime gain? First profile a different literal caller and specify its
matrix, denominator and coefficient bounds before adapting products. This small
calibration saves milliseconds; a larger caller contract and complete measurement
are missing. No further optimization of this fixture is reserved.

## Implementation bounds

Arithmetic loops are bounded by dimension 16, with at most 4,096 nonzero term
pairs per product. Input normalization reads at most 1,024 Fraction components.
Cleared components have at most 320 bits; output common numerators have magnitude
below 2^645 before reduction. Local values and immutable zero tuples are the
only shared arithmetic state. There is no recursion, floating arithmetic or
generated scientific code.

Power of Ten rule 3 has a managed-runtime deviation: Python/Fraction allocate
within fixed dimension and bit-size bounds during this finite command. There
is no physical-tape claim. Revisit fixed buffers before a production backend.
The scientific fixture has 277 calls; subprocesses have 30-second timeouts,
registered commands 60-second timeouts. All functions are below 60 physical lines.
Rules 8/9 have a scoped dispatch deviation for loading two pinned source modules
and substituting one named product function. Targets and synchronous lifetimes
are fixed. Tests mutate only their own temporary source copies. Warning-strict
normal/optimized execution and in-memory compilation provide diagnostics;
no separate external static analyzer is claimed.

Build the Lever led to the rerunnable adapter and complete-caller benchmark.
Prove It Works led to full intermediate products, complete output comparisons
and actual source/sign mutations rather than a digest-only proxy.

## Raw complete-process wall times

Times are milliseconds. Every run completed the entire caller.

| Round | Original | Reference adapter | Integer adapter |
| --- | ---: | ---: | ---: |
| 1 | 97.957208 | 86.273416 | 73.999417 |
| 2 | 99.736500 | 86.360958 | 74.599750 |
| 3 | 98.120917 | 86.035208 | 74.374542 |
| 4 | 98.671291 | 85.846917 | 74.596083 |
| 5 | 105.044458 | 89.031625 | 74.966250 |
| 6 | 98.532666 | 86.961042 | 74.582958 |
| 7 | 98.868167 | 86.272125 | 94.631791 |
| 8 | 131.133375 | 86.792583 | 75.544000 |
| 9 | 100.199166 | 86.043750 | 75.397125 |
| 10 | 98.602959 | 87.586875 | 74.114208 |
| 11 | 99.399917 | 86.800584 | 74.520916 |
| 12 | 125.302208 | 85.972416 | 74.286583 |
| 13 | 104.901917 | 87.156875 | 73.880958 |
| 14 | 98.217625 | 87.272709 | 74.977250 |
| 15 | 98.463583 | 86.629209 | 74.477583 |
| 16 | 99.568250 | 86.309792 | 74.947125 |
| 17 | 97.538417 | 86.324250 | 74.883292 |
| 18 | 98.852792 | 88.388750 | 75.118583 |
