# Skipping zero elimination rows preserves complete recurrence certificates

This contribution was produced by Nick Petalas. Apache-2.0.

The result is a scoped implementation-equivalence argument with exact finite
conformance and local performance evidence. No new M-matrix theorem or κ is
claimed. Ali Romman retains the certificate construction and checker.

## Change and invariant

In scripts/certify_coupled_recurrence.py, certify first validates A>=0 and b>=0
and builds the augmented matrix [I-A | 1 | b]. A nonpositive pivot emits the
existing noncontraction witness and returns after the unchanged checker.
Otherwise the pivot is strictly positive before the lower-row loop begins.

The only change is

```python
for i in range(k+1,n):
    if rows[i][k] == 0:
        continue
    factor = rows[i][k]/rows[k][k]
    for j in range(k,n+2): rows[i][j] -= factor*rows[k][j]
```

The equality test is exact Fraction equality. At zero, the original factor
is zero because the pivot is positive. Every omitted assignment is x<-x-0*y,
which returns the same canonical rational value. The original block performs
no validation or side effect beyond those assignments. Induction over rows
and pivots therefore gives identical augmented matrices at every pivot.

Every nonpositive-pivot decision, backsolve, weight, ratio and forcing total
is identical. The serialization budget and separate matrix-vector verifier
are unchanged, as are input parsing and CLI input hashes. The guard cannot
hide an invalid pivot because its test happens after the original pivot gate.
Invalid inputs encounter the unchanged validator before reaching elimination.
Both contracting and noncontracting alternatives retain their original scope.

This argument covers every input accepted by the original bounded interface.
It does not depend on a sparse input, an upper-triangular shape or the finite
fixtures. Dense nonzero coefficients use the original update.

## Source and conformance contract

adapter.py authenticates the current script and unchanged JSON/validation
helper by exact SHA256 before compilation. Removing exactly the two new
guard lines must reproduce the exact baseline SHA256 at canonical main
2485805a6d47f36ea83ddde6327d453ac82d44dc. It does not reconstruct an
approximation of the baseline. All certificate fields are compared, and
both original certificate checkers validate the opposite producer's result.

The registered checker covers the complete two-type grid with coefficients
0,1/2,1,3/2, plus seven sizes from one through 64. The latter include the
nilpotent half-chain, a dense positive contraction, and noncontraction at
the first and last diagonal position with zero forcing. Two additional
fixtures exercise a coupling-driven failure and the coefficient boundary.
The generated receipt reports the enumerated status counts.

Six malformed inputs, three false certificates and two mutated source-byte
inputs must reject. The repository's existing six tests additionally cover
the retained source barrier, coupled failure, reducibility, singularity,
64 types, serialization overflow and the complete portable CLI check mode.
This validates the implementation change; it is not a new audit deliverable
for the predecessor's mathematical alternatives.

## Complete-path benchmark

The workload is the existing full-size test's 64-type half-chain, with
A[i,i+1]=1/2, all other entries zero and forcing vector one. It is a valid
declared feed-forward recurrence at the interface's maximum type count.
No new sparse-only interface is introduced. This workload reaches both
backsolves, the complete matrix-vector checks, serialization and input hash.

benchmark.py times ten fresh complete CLI processes, five alternating pairs.
Both sides use the same interpreter, flags, JSON bytes and helper bytes.
Only the authenticated zero guard differs. It checks successful exit, empty
stderr, the 64-entry weights and total, and byte equality of complete stdout
before admitting each time. It reports every sample, median, range, CPU count,
load and exact source hashes. It includes CLI startup, parsing, validation,
certificate generation, internal verification and serialization. Setup and
the separate conformance suite are outside the timed region. No timing
threshold is imposed on CI or on future machines.

An untimed cProfile run of the complete baseline attributes most cost to
Fraction arithmetic in certify. It records 107776 calls to Fraction._mul
and 95616 to Fraction._sub. The zero coefficient row updates are unused
work; skipping them is the first accepted mechanism. The benchmark does
not compare configurations, omit any proof check, or time a cached result.
The generated local receipt contains the measurements; it is not hand-written.
This is a local sparse-workload result. Dense speed, all-input acceleration
and full-frontier runtime are unclaimed.

## Bounds and implementation decisions

The production change introduces no allocation, recursion, callbacks or new
authority. Existing n<=64 validation bounds its loops. All other production
code and the original contributor notice keep their bytes.

The supporting package bounds source files at 256 KiB, matrix dimension at
64, and conformance generation at 286 fixtures. Each benchmark process has
a 30-second timeout and there are exactly ten processes. The benchmark's
temporary directories are inside the caller's external output directory and
are cleaned on success or failure; existing output files are never overwritten.
The registered conformance path writes no files. Assertions are not required
for acceptance, so normal and optimized modes use the same checks.

Power-of-Ten rule 3 deviation: CPython allocates exact integers, Fractions,
lists and JSON structures dynamically. A fixed-allocation port would change
the supported runtime. The original validated dimension/coefficient bounds
remain; new fixtures and source sizes are explicitly bounded. Such a port is
deferred until a consumer requires constant allocation. No memory-speed claim
or uniform bit-complexity improvement is made.

Rule 8 deviation: the conformance loader compiles two authenticated versions
of one script and one authenticated helper. This is needed to compare the
exact old and current artifacts without a Git dependency or vendored duplicate.
Only fixed source hashes and the single literal guard are accepted; actual
source mutations reject before loading. The loader bypasses .pyc files and
restores its one temporary sys.modules entry in a finally block. Replacing
this bounded comparison seam is appropriate only if a stable production
version-selection API is introduced.

Rule 9 deviation: rejection checks invoke a bounded set of old/new certify,
verify and authentication callables. Their targets are explicit and finite.
There is no arbitrary plugin or callback input. Normal/optimized replays,
AST compilation and function-size inspection provide available diagnostics.
No static type-analyzer acceptance is claimed.
