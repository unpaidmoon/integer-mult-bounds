# Skip 113,164 redundant modular products in the complete stage-pair replay

This contribution was produced by Nick Petalas. Apache-2.0.

The complete historical h=6 stage-pair certificate needs **494,696 rather
than 607,860 modular coordinate products** in row normalization and elimination.
The new kernel skips the prefixes already proved zero by earlier pivots.
Every scientific output field and the existing cache workload agree. The
complete caller retains 64 candidate decisions, six local improvements, all
rational fallbacks and rank sum 8,684. Those mathematical results belong to
the predecessor; the new result is the implementation work reduction.

Claim type: scoped implementation-equivalence proof with an exact finite
work-count certificate. No new kappa is claimed. No frozen source is edited.
The adapter changes only the modular-rank kernel in a private process.

## Why skipping the prefix is exact

Before inspecting column j, every unprocessed row has zeros in columns
0,...,j-1. A previous pivot was cleared from every lower row. A previously
skipped column was zero in all then-unprocessed rows. These facts establish
the invariant initially and preserve it after each step.

The selected pivot row and every lower row therefore have zero prefixes.
Normalizing the full row would multiply those zeros by the pivot inverse.
Eliminating the pivot would calculate 0-c*0 on every prefix entry. Retaining
the zeros and updating only columns j,...,width-1 produces exactly the same
row, pivot selection, inverse and eventual rank. The new kernel uses the
original inverse helper and the original cache capacity of 65,536. It caches
no scientific verdict or complete certificate.

The reference bytecode observer counts executed normalization/elimination
multiplications independently of the new loop-length counters. It observes
607,860 products on 372 cache misses. The new loops execute 494,696. The
113,164 omitted products exclude unchanged input residue conversion. The
receipt also records 6,764 cache hits and all 372 live rank comparisons.

## Reproduce

From the repository root, use CPython 3.12 and its standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/stage-pair-tail-elimination/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/stage-pair-tail-elimination/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/stage-pair-tail-elimination
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/stage-pair-tail-elimination --check-source-history
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/stage-pair-tail-elimination/benchmark.py --rounds 5
```

Substitute a local CPython 3.12 executable elsewhere. The verifier prints
`PASS_STAGE_PAIR_TAIL_ELIMINATION` in a generated receipt bound to package
hashes. It writes no files. Complete callers also run directly through
`adapter.py --engine reference|tail|compare`. Comparison mode instruments the
reference and checks every live rank. Benchmark modes contain no tracing or
operation counting.

All thirteen source modules and every data file read by the complete caller
are pinned in [SOURCES.json](SOURCES.json). The loader compiles authenticated
source bytes, preventing stale bytecode from replacing them. It uses
`optimize=0` for predecessor modules in both modes, retaining their assertion
checks. No source command runs as `__main__`, so the predecessor's
artifact-writing entry point is never invoked.

## Evidence and runtime limits

Kernel controls include all 512 binary 3-by-3 matrices and all 729 ternary
2-by-3 matrices, with a separate determinant-minor rank oracle. Thirty fixed
diagonal cases cover zero width, rectangular matrices, dimensions through 64
and large rational numerators across five primes. Six invalid-input controls
reject empty, ragged, over-capacity or invalid-modulus inputs and a
noninvertible denominator. Three faulty arithmetic kernels are detected.
Complete caller comparison preserves the entire serialized mathematical
payload, source bindings and cache information.

A local locator profile puts only about 0.134 of 25.551 instrumented seconds
in modular elimination; rational subtraction dominates. This profile is not
a benchmark sample. The exact work reduction does not imply a comparable
complete wall-time gain. `benchmark.py` runs five or more alternating complete
fresh-process pairs, checks every output digest and reports all medians and
ranges without a timing threshold. Five local alternating pairs gave reference
median 8.506 s, range 8.425 to 8.646 s, and tail median 8.519 s, range 8.472 to
8.547 s. All ten complete processes succeeded with the same payload digest
and cache workload. The wall-time result is inconclusive; no complete runtime
gain is claimed. These observations are separate from the exact arithmetic
claim and from hosted CI.

## Scope, credit and engineering choices

The new adapter, kernel, conformance checker, bytecode counter and measurement
script were produced by Nick Petalas. Skipping zero prefixes in Gaussian
elimination is classical. Aaron Wang / navinor's
[PR824](https://github.com/CrocSwap/integer-mult-bounds/pull/824) supplies the
earlier performance baseline and its distinct inverse-cache and Fraction
construction changes. Douglas Colkitt supplies the stage-pair circuit, frames
and scientific caller, with the retained paired, shared-point, exclusion,
rational-frame and upstream source authors. Their bytes and credit are
unchanged. Auditing the predecessor theorem is not this contribution.

Base: canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8. Selected binding orientation passes at conditional kappa
`781451/250000000`. No supplier, selected frontier, native implementation or
framework assumption changes. The current fixture uses 36-by-36 matrices
and prime 101. The kernel's declared domain is rectangular rational/integer
matrices with at most 64 rows and columns and a prime modulus with invertible
denominators. No equivalence is claimed for malformed predecessor inputs.

New loops are bounded by 64, 1,271 kernel fixtures, three arithmetic mutants,
six invalid fixtures or five through ten benchmark pairs. Each child has a
120-second timeout. New functions fit within sixty physical lines. Managed
Python allocation is a Power of Ten deviation; new matrix storage is bounded
by 64-by-64 entries. The retained 65,536-entry cache policy is unchanged.
Authenticated compilation, thirteen import targets and one temporary opcode
callback are bounded dynamic-dispatch deviations. The import finder and tracer
are restored on exit; the adapter runs in a fresh child. Existing source
loops, allocations and long functions remain inside the frozen dependency.
Warning-strict normal and optimized execution provide available diagnostics;
no external linter is required or claimed.

No physical supplier, full multiplication theorem, Lean build, Docker run or
selected cold replay is supplied. Independent human and formal proof-kernel
review are unclaimed.

## Open next questions

Would this optimization matter in another explicitly pinned modular-rank
caller? First profile that complete caller and preserve its input and cache
contracts. This package certifies no other workload or shared integration.
[TASK.json](TASK.json) records the relevance and remaining limits.
