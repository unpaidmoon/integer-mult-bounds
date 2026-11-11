# Exact evaluator and complete-caller preservation

Let A be a square matrix over the integers or rationals, of dimension
0 <= n <= 5. The reference determinant enumerates every permutation p and
evaluates

```text
sum_p (-1)^(number of inversions of p) product_i A[i,p[i]].
```

The replacement returns A[0,0] for n=1 and
A[0,0]A[1,1]-A[0,1]A[1,0] for n=2. These are exactly the one and two
Leibniz terms. For every other allowed dimension it uses the same permutation
enumeration, exact products and sum, taking the sign from a table initialized
by the same inversion formula. The empty product and single empty permutation
give determinant one at n=0. Thus the evaluators agree on the entire stated
arithmetic and dimension domain, including singular and negative determinants.
No division, rounding, rank assumption or nonzero-pivot assumption enters.

The table contains sum(n!, n=0..5)=154 permutation/sign pairs. It depends only
on dimension. Matrix values are read again at every call; a changed matrix
cannot reuse an earlier determinant. A separate cycle-decomposition check
uses sign(p)=(-1)^(n-number_of_cycles) and verifies table completeness and
uniqueness. It is a conformance check, not the basis of the equality proof.

The source-bound complete caller has no determinant request outside sizes
one through five. Comparison mode evaluates both functions on every actual
request, checks exact equality, and hashes the ordered matrix/value stream.
Its 19,654 calls include every determinant requested by both the unimodular
certificate checks and the independent gcd of every minor. All remaining
functions and all control flow execute from the original authenticated source.

Consequently the changed caller computes the same unimodular conditions,
Smith identities, diagonal and divisibility conditions, independent minor gcds,
constructive unit blocks, nonunit obstructions and corrupted-certificate
decisions. It performs all original work with a cheaper exact evaluator.
This implication preserves the source caller's checks; it does not independently
prove the mathematical capacity algorithm or its physical applicability.

# Measurement contract

The benchmark launches five alternating reference/scheduled pairs, each as a
fresh CPython process. The reference arm is the original complete script.
The scheduled arm is the isolated adapter, including its source authentication
and additional imports. The timer encloses process creation, full execution,
captured output and successful termination. Timeout is thirty seconds. Every
arm must exit successfully, emit no stderr, reach the original success marker
and produce identical complete stdout. No scientific output or result is cached.

Bytecode-cache namespaces are fresh for every process. The adapter additionally
loads the two authenticated predecessor modules directly from source. Both
arms use the same interpreter, warnings and disabled cache-write settings.
There is no baseline-only profiler, tracer, extra guard or repetition inside
the timed region. Measurement summaries and source hashes are generated after
timing. Profile runs are separate and never included in the ten samples.

The diagnostic reference profile put roughly 22% of its total profiled time
inside determinant evaluation. The scheduled evaluator reduces that work;
unchanged Fraction arithmetic, matrix products and certificate checks limit
the complete gain. The measured 9.83% reduction is below that optimistic
removable share. This is a local observation, not an asymptotic or portable
speed guarantee. No performance threshold is asserted by CI.

# Implementation bounds and deviations

New loops are finite. Schedule initialization has six dimensions and 154
permutations, with at most ten inversion comparisons each. A scheduled
determinant has at most 120 terms of at most five factors. Conformance grids
have 1,248 values; source controls have eight copied files and five separately
mutated inputs. The manifest is limited to sixteen rows and each input to
one megabyte. The production caller is fixed by five input hashes.
The benchmark has exactly ten subprocesses, with thirty-second limits.
The normal and optimized registered checks each have a 120-second limit.

Functions are shorter than sixty physical lines. New control flow is iterative,
with explicit exceptions active under optimization. Temporary exports and
bytecode namespaces use context-managed cleanup. The source loader restores
the original capacity module binding on success and failure. Neither a kernel
exception nor a source mismatch is turned into scientific success.

Power of Ten deviations:

- Rule 2, inherited Smith reduction: the frozen predecessor has an unbounded
  Euclidean loop. Preserving its exact source and checks prevents changing it
  here. The caller's fixed finite input domain is unchanged, and each executed
  subprocess and registered check has a wall-clock timeout. This limits a
  stalled replay but is not a newly proved iteration bound. A separate change
  to that source needs its own bound and preservation evidence.
- Rule 3, managed allocation: CPython integers, Fractions, tuples and captured
  stdout allocate dynamically. The fixed grids, five-row matrices, 154-entry
  table and bounded source files limit live data in these scripts. No service
  loop or unbounded cache exists. Reassess storage before enlarging dimensions
  or accepting external matrices.
- Rules 8 and 9, source imports and callable replacement: the adapter uses the
  standard source loader for exactly two authenticated module paths and replaces
  one determinant function with one of three explicit engines. It bypasses
  bytecode. Comparison and corruption controls exercise the alternate targets;
  no arbitrary plugin, code generator or runtime expression is accepted.

Warning-strict normal and optimized execution, source corruption checks,
committed-byte/source-history preflight and AST inspection are the available
diagnostics. No external static analyzer or formal proof kernel is claimed.
