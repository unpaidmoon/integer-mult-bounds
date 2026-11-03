# Product preservation and replay scope

This contribution was produced by Nick Petalas. Apache-2.0.

## Exact product lemma

Let F be the retained explicit finite field, let A have shape m by k, let B
have shape k by n, and allow any of these dimensions to be zero. Every row
has its declared width and every entry is a canonical F element. The output
of `row_product(A,B,n,F)` equals the output of the pinned `decompose.mm`.
Neither routine mutates A, B or F.

The source routine extracts column j of B, applies `field_source.mv`, and
transposes the resulting column vectors. Its entry (i,j) is the field sum of
A[i,t] B[t,j], with t in increasing order. In the new routine, the accumulator
for (i,j) begins at zero. After the first s inner iterations its value is the
sum of exactly those products with 0 <= t < s. If A[i,s] is zero, skipping its
row update preserves the invariant by the field zero law. Otherwise the
multiplication table supplies A[i,s] B[s,j] and the addition table extends the
sum. Induction through k proves equality entry by entry. The column loop has
exactly n iterations, and there is one distinct output row per input row.
When m, k or n is zero, the same argument gives the declared empty or all-zero
shape. Output rows are new lists; all source rows and field tables are read only.
The zero-width branch returns exactly m distinct empty rows without visiting
any inner coefficient. The single-column branch uses the same invariant for
one scalar accumulator per output row, avoiding a one-element column loop.
The source evaluates exactly m*k*n scalar product terms and the same number
of field additions. The replacement evaluates exactly n*nnz(A) such terms
and additions. Thus it omits exactly n*(m*k-nnz(A)) zero-left-coefficient terms.
This count includes terms whose right coefficient is zero when the left one
is nonzero. It is an arithmetic count, not a count of processor instructions.

This is ordinary matrix multiplication and distributivity, not a new algebraic
identity or a claim of literature priority.

## Complete-caller consequence

The adapter authenticates every declared live source before compiling any of
its three fixed Python modules. It changes only the local module's `mm` binding.
All decomposition, factorization, orbit enumeration, map equations, determinant
checks and failure predicates retain their source bytes. No basis or decision is
cached. The source module bindings and search path are restored on every exit.

For each deterministic execution on the retained valid fixtures, replace matrix
product calls in chronological order. The lemma gives exactly the same returned
matrix without a state mutation. Consequently every later branch, extracted
block, map and exception remains the same. The source's public malformed-input
checks still run before extraction. The adapter does not offer a new contract
for malformed internal products, other fields, or arbitrary module imports.

The audit mode also compares every actual product against the original routine
before returning it. The work counter visits every left coefficient at every
actual call, checks both rectangular shapes, and sums the two exact term bills
above. No extrapolation from a sample supplies the finite work certificate.
This is preservation evidence for the new implementation,
not an independent scientific audit of PR5692. The scientific claims, domains
and receipts belong to Ali Romman and the retained predecessors.

## Bounds and engineering decisions

The new kernel has no recursion. Its loops have m, k and n iterations, and audit
of the fixed complete caller observes m,k,n <= 18, or at most 5,832 scalar
positions per product. Its additional live storage is its m by n output and
constant local references. There is no persistent arithmetic cache. The
verifier's separate differential grid has exactly 4 fields, 125 dimension
triples and 4 variants, or 2,000 products. Three fixed defective kernels and one
actual source-byte change must reject. The benchmark launches exactly ten
subprocesses serially, each with a 240-second timeout and checked exit status.
Every source scientific PASS line and complete JSON result stays required.

Power of Ten deviations apply to the following bounded Python boundaries.

- Rule 3, managed allocation. CPython allocates lists, modules, captured source
  bytes and JSON. The new matrix kernel retains at most 324 output entries for
  this caller and no input-derived cache. The source's existing exhaustive
  sets and recursion remain byte unchanged. The adapter adds three temporary
  modules, and the source loader restores prior bindings in a finally block.
  A larger caller needs its own memory and iteration limits before adoption.
- Rules 8 and 9, authenticated dynamic loading and dispatch. The source loader
  compiles exactly three fixed, hashed files because ordinary imports can read
  preexisting bytecode. Only the fixed reference, fast and differential modes
  can replace `mm`. Three explicit broken product functions are test injections
  confined by a finally block. Hash-corruption rejection and normal/optimized
  complete runs check these boundaries. Removing this dispatch requires a
  separately reviewed integration into a live caller, outside this package.
- Rule 10, available diagnostics. Registered commands use `-I -W error -B`,
  with an additional complete `-O` run. AST inspection checks new function sizes
  and syntax; no standalone linter or static type checker is installed. The
  existing source's recursion and functions are pinned dependencies, not new
  code edited to satisfy a different style policy.

Build the Lever shaped the rerunnable adapter, comparator and benchmark.
Prove It Works required comparison at every real product and the complete
unchanged caller. Benchmark checklist requires serial fresh-process pairs and
identical full output, rather than timing a small product alone.

## Limits

This is a scoped implementation-preservation proof with a finite arithmetic
work certificate. The observed wall-time medians are lower, but their ranges
overlap and this package treats wall-time improvement as inconclusive. It
supplies no new tensor classification, native operation,
physical supplier, rounded error bound, compiler, complete multiplication
algorithm or kappa. All five selected framework assumptions remain. Timing
on other hosts and integration into other consumers remain open. Independent
human and formal proof-kernel review are unclaimed.
