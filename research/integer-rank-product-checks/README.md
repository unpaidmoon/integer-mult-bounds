# Integer product checks for complete rational-rank certificates

The complete rational-rank certificate produce/save/check path takes 54.94%
less wall time on the retained dense 48-by-64 rank-eight rational fixture.
This contribution was produced by Nick Petalas. Claim type: scoped exact-arithmetic
implementation proof with finite conformance and local performance evidence.
No new rank theorem, kappa, native supplier or selected-frontier change is claimed.

The shared `scripts/certify_rational_rank.py` keeps the existing input and output
formats, pivot selection, elimination, certificate serialization and exact
acceptance predicates. It changes the four multiplication checks for the pivot
minor inverse, rank factorization and complete right/left kernel bases. The
proof below covers arbitrary valid rational matrices in the existing interface.
Finite conformance is additional evidence, not an all-input exhaustive search.

## Exact replacement

For a left row x and right column y, let d and e be positive common
denominators, with X=d*x and Y=e*y integral. For every rational target z,

```text
sum(x_t*y_t) = z
if and only if
sum(X_t*Y_t) * denominator(z) = numerator(z) * d * e.
```

The new checker computes d by successive least common multiples and constructs
X exactly. It computes e and Y independently for each right column, then uses
integer dot products and the displayed cross-multiplication. Positivity makes
both implications valid. A zero inner dimension gives d=e=1 and the empty
integer sum zero, so rank zero and empty kernels retain their previous meaning.

The other checks still validate the same shapes, pivot-index sets, free-coordinate
identity blocks and rational syntax. Thus the inverse product still proves the
rank lower bound, the factorization still proves the upper bound, and the exact
kernel products and identity blocks still establish the same complete bases.
The producer and serialized result do not change. If several fields are invalid,
the first error message can change because kernel products are now batched;
all the original rejection predicates and CLI failure status remain.

To bound common-denominator growth, a row whose running least common multiple
exceeds 16384 bits declines the integer path. The corresponding product then
uses the original exact Fraction dot-product predicate. This branch changes
cost only; it neither accepts a false product nor rejects a true one. It avoids
constructing the full scaled row for a large coprime denominator product.

## Measured complete path

Each timed bundle starts a fresh certificate producer, captures its complete
JSON output, saves that output and starts a fresh `--check` process. Both
processes must exit successfully, the checker must print its exact success
marker, and every output hash must agree. The fixture is generated before timing;
profiling is a separate untimed run. Imports, input parsing, elimination, all
certificate checks, serialization, process startup, saved-file I/O and replay
are inside the timed region. There are no skipped mathematical checks.

Five alternating pairs on CPython 3.12.15, macOS 27.0.1 arm64, 18 logical CPUs:

| Complete bundle | Median | Observed range |
| --- | ---: | ---: |
| Original | 440.23 ms | 434.41 to 461.09 ms |
| Integer checks | 198.39 ms | 195.43 to 210.60 ms |

Raw samples in milliseconds, in each side's observation order:

```text
original: 434.406917, 450.502708, 461.090000, 436.349834, 440.234625
integer:  198.391583, 201.852167, 210.603875, 197.723625, 195.430375
```

All ten bundles and twenty CLI commands succeeded. All ten produced the
certificate SHA256 `48b99c3926885f307aef55c25bfed6336fe8c734834b3ce9805b24f63be81f26`.
The fixture JSON SHA256 is
`914197cf63eeab2157e26ad92720418a7924d3811bdddf7c057fb29b9c5dbbd7`.
The generated benchmark report binds the actual measured source files to SHA256.
The machine was shared; the reported end load average was about 3.09 across
18 logical CPUs. Pair order reverses on alternate pairs to spread host noise.

The untimed profile attributes 0.503 of 0.572 profiled seconds in the original
`certify` call to `verify`, including 697321 Fraction arithmetic dispatch calls.
Those instrumented times locate the bottleneck; they are not the reported
performance measurement. The measured complete-path reduction is below that
fraction of time. Parsing, elimination and process startup still limit the gain.
This is a local result for one synthetic interface fixture, not a universal
speed guarantee or a production supplier replay benchmark.

## Reproduce

From the repository root, using CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/integer-rank-product-checks/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -O -W error -B research/integer-rank-product-checks/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/integer-rank-product-checks
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/integer-rank-product-checks --check-source-history
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B -m unittest discover -s tests -p test_research_rational_rank.py -v
```

Replace the absolute interpreter with another CPython 3.12 executable as needed.
Both direct commands print `PASS_INTEGER_RANK_PRODUCTS` in a generated JSON
receipt bound to package and implementation hashes. The registered replay also
prints `PASS_REGISTERED_RESEARCH_PACKAGE`. It checks 591 complete certificate
equalities, 802 exact product/false-product cases and 24 certificate rejections.
The product cases include zero dimensions and explicit scale-limit fallbacks.
Seven relevant unit tests also pass normally and with `-O`.

For timing, provide an existing external scratch directory:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/integer-rank-product-checks/benchmark.py --scratch /absolute/external/scratch
```

This emits a generated source-bound report, two final saved certificates,
the fixture and an untimed profile into that directory. It runs exactly five
pairs. Timing is deliberately opt-in rather than a CI performance threshold.
Registered commands contain only bounded correctness checks.

## Scope, source and credit

Ali Romman's [PR5789](https://github.com/CrocSwap/integer-mult-bounds/pull/5789)
supplies the rational-rank interface, rank factorization, complete kernel
certificates and separate product checker. The byte-identical original script
is retained as `baseline.py`, including its original attribution. Its bytes
are checked against the provenance pin at canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. Classical denominator clearing,
Gaussian elimination and rank factorization retain their credit. The new
application changes implementation cost, not their mathematical content.
The parser dependency is a source-bound live input. The changed shared script
is a declared replay input; the original script's source pin is provenance.

The current `replay-runtime` card is refined to this implementation question.
The selected-binding first example passed. Existing published rank values and
predecessor scientific conclusions are premises, not the deliverable being
audited. All five framework assumptions, physical delivery, caller, precision,
stock and supplier admission obligations remain outside this change. No Lean,
Docker, complete selected replay or independent human/kernel review is claimed.

## Verification constraints

The changed shared functions are at most 35 physical lines. All their loops
inherit the validated 64-row/column bound. Certificate boundary validation
and arithmetic equalities remain enabled under `-O`. There is no recursion,
code generation, approximate arithmetic or cache of certificate decisions.
The fallback preserves the previous exact arithmetic when scaling is too large.

Power-of-Ten rule 3 has a managed-runtime deviation: Python allocates integers,
Fractions and matrices during arithmetic. The finite CLI bounds and 16384-bit
scale guard bound the new scaled representation. The parser still limits
certificate rational strings to 4096 characters and inputs to 64-by-64; no
fixed-capacity embedded implementation is claimed. Interpreter allocations
and Fraction fallback cost are not statically allocated. Warning-strict direct,
registered and unit-test commands provide the available language diagnostics;
no static type checker is configured for this script. The benchmark's subprocesses
have 120-second timeouts and fixed invocation counts; all outputs go outside
the checkout. The literal frozen baseline remains unchanged.

## Open next questions

1. Does the complete-path improvement persist on a named interface search's
   actual exported matrices? First export and source-bind one such matrix,
   then reuse the paired CLI harness. The missing input is a declared caller
   workload; the synthetic benchmark does not settle this question.
2. Can the scale threshold follow from a fixed-capacity backend's proven
   memory and arithmetic budget? Start with that backend's integer capacity.
   No such backend contract is supplied here.

The structured versions are in `TASK.json`. Apache-2.0. Independent human and
formal proof-kernel review are unclaimed.
