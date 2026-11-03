# Remove 7,982,993 product terms from the complete raw-pencil replay

This opt-in adapter replaces the column-materializing matrix product in Ali
Romman's [PR5692](https://github.com/CrocSwap/integer-mult-bounds/pull/5692)
complete decomposition caller with a direct row update. It removes repeated
column vectors, generator sums and products whose left coefficient is zero.
The change is isolated in this package. All predecessor files remain byte exact.

Claim types: **finite arithmetic-work certificate** and a **scoped preservation proof**.
The complete caller's scalar product terms fall from
19,651,114 to 11,668,121, removing exactly
7,982,993 terms and the same number of field additions.
Wall-time improvement remains inconclusive. [PROOF.md](PROOF.md) gives the
matrix-product lemma, exact term formulas and complete-caller consequence.
No new classification, physical supplier or kappa is claimed.

## Evidence

The preservation check compares all 2,779,301 actual matrix products with the source routine.
It retains the complete five-domain raw-pencil census, literal row/column map
equations, polynomial divisor oracle, larger constructed examples, cases with
no invertible slice and all original failure controls. These scientific checks and
claims are the predecessor's work. Their execution here checks preservation of
the new implementation rather than independently reviewing that mathematics.

An additional 2,000 product comparisons cover all dimension triples in
{0,1,2,3,4} over F2, F3, F4 and F9, including zero shapes, zero coefficients,
input preservation and distinct output row ownership. Three deliberately broken
products and an actual changed source file must reject. Explicit exception
checks stay active under `-O`.

For an m by k matrix A and k by n matrix B, the original routine evaluates
m*k*n scalar product terms and additions. The new routine evaluates n*nnz(A).
The certificate visits every actual A and checks the rectangular shapes before
summing those bills. This counts field arithmetic; processor instructions and
paid recursive calls have separate bills.

## Timing evidence

The final five alternating fresh-process pairs measured an observed median
22.613577 seconds versus 20.655674 seconds.
Reference range is 21.130680 to 23.452057 seconds;
new range is 20.180521 to 22.918939 seconds.
The ranges overlap and their variation exceeds the median difference, so this
package makes **no reliable wall-time improvement claim**. An earlier
unspecialized version was also inconclusive. Zero failures occurred and every
complete scientific output byte agrees in all ten final runs.

| Pair | Reference seconds | New seconds |
|---|---:|---:|
| 1 | 22.613577 | 20.402866 |
| 2 | 23.452057 | 22.918939 |
| 3 | 22.294591 | 20.846005 |
| 4 | 22.693414 | 20.655674 |
| 5 | 21.130680 | 20.180521 |

Environment: 3.12.15, macOS-27.0.1-arm64-arm-64bit, 18 logical CPUs.
Other work ran on the shared host; observed load averages during measurement
were about 3 to 4.5. Both sides use the same interpreter, flags, complete
fixtures and fresh source modules. No arithmetic cache is warmed across runs.
The source profile attributes 6.423 of 36.578 instrumented seconds to the
2,779,301 matrix products. Row reduction remains the largest retained component.
The profile locates work; its timings are not used as a speed ratio.

## Reproduce

From the repository root, using CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/raw-pencil-row-products/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/raw-pencil-row-products/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/raw-pencil-row-products
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/raw-pencil-row-products --check-source-history
```

Another CPython 3.12 interpreter can replace the absolute path. Expected markers
are `PASS_RAW_PENCIL_DECOMPOSITION`, `PASS_RAW_PENCIL_ROW_PRODUCTS`,
`PASS_REGISTERED_RESEARCH_PACKAGE` and `PASS_RESEARCH_COMMIT_BYTES`.
The direct verifier prints a newly computed package-hash receipt and writes no
persistent files. Its source mutation control uses a temporary directory.

For the complete before/after measurement:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/raw-pencil-row-products/benchmark.py
```

It runs five alternating fresh-process pairs, checks exit codes, every scientific
output byte, the final expected JSON and empty stderr, and emits its raw samples
and package hashes. Timing includes interpreter startup, source authentication,
module loading and every source scientific check. The benchmark itself is opt-in;
registered checks establish preservation without imposing a timing threshold.

## Scope and limitations

This supplies an exact arithmetic reduction toward the external package's
faster-extraction question on one fixed complete caller. It does not settle
that wall-time question. It does not change the initially suggested BIT construction
model or supply a new construction. The source-binding orientation passed on
base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8; selected
conditional kappa is `781451/250000000`. The five framework assumptions remain.
Native realization, physical ownership, restoration, routing, precision, storage
and the complete recursive invoice remain outside this engineering contribution.
Independent human and formal proof-kernel review are unclaimed. Lean, Docker,
other pencil callers and the selected scientific cold replay were not run.

The product lemma applies to valid rectangular matrices over the retained field.
The measured caller uses dimensions at most 18. Other workloads need separate
measurements. There is no persistent arithmetic cache or cross-invocation reuse.
[SOURCES.json](SOURCES.json) pins six live predecessor files; all are declared in
[VERIFY.json](VERIFY.json). Changed bytes reject before source execution.

## Open next questions

- Does a quiescent host confirm a wall-time gain? Run the same complete five-pair
  benchmark and retain all samples and output hashes. The present shared-host
  ranges overlap.
- Can this kernel benefit the separate raw-pencil special-linear transporter?
  First profile one complete phase and name its input/output boundary before
  installing the adapter. No such benchmark or coverage argument is supplied.

[TASK.json](TASK.json) records first steps and blockers. Optimization stopped
at the first exact arithmetic improvement. Neither follow-on is attempted here.

## Credit

This contribution was produced by Nick Petalas.

Credit Ali Romman / PR5692 for raw-pencil decomposition, the field
source, proof, complete caller and explicit faster-extraction question; the
retained PR5664/5637 finite-field lineage; PR5250, apoursh / PR5672 and PR5683/5689
for the preceding pencil interfaces; and David Ganz's tensor-atlas lineage.
Kronecker decomposition, primary module theory, Wong sequences, Berlekamp
factorization and direct matrix multiplication are classical. Their credit and
all predecessor notices remain unchanged. Apache-2.0.
