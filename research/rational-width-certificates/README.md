# Sharp all-column certificates with rational width normalizers

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped algebraic proof with exact finite corroboration. A
complete residual may have exterior rational functions of the positive
column count, even when those functions have no fixed finite transfer
representation. For fixed physical letter tables, write

```text
E(w) = sum_j p_j(f)/q_j(f) F_j T_(j,w) B_j,     f = length(w) >= 1.
c_j = Q p_j/q_j,                              N = sum_j D_j(deg c_j+1).
```

Here Q is a common polynomial denominator with no positive-integer zeros,
D_j is the jth fixed transition dimension, and zero c_j terms are discarded.
Over characteristic zero, the complete endpoint vanishes at every positive
width if and only if it vanishes on every physical word of lengths 1,...,N.
Clearing Q and adding explicit polynomial counters gives a compact exact
closure certificate. A nonzero endpoint has a literal entry witness within
that cutoff. All input and output roles remain in the test.

The bound is sharp for each D>=1,d>=0, even with one summand. A D-cycle and
the numerator product_(k=1)^d(f-kD), divided by f, first fail at D(d+1).
The scalar family 1/f has no fixed finite transfer representation of any
dimension, so this is a strict extension of the fixed-table interface.
The all-parameter claims rest on [PROOF.md](PROOF.md).

This builds on zxv's [PR5441](https://github.com/CrocSwap/integer-mult-bounds/pull/5441),
at `11fedb46fa199283f78282187c10aea432d8b0bb`, and its explicit represented
recurrence-coefficient contract. That source and its native, phase,
compiler and physical-column lineage retain their credit. Classical
weighted automata, Newton differences, Kronecker products, polynomial
root counting and Cayley-Hamilton supply the proof ingredients. The new
result is the stated rational-width interface and sharp construction;
global literature priority is unclaimed. No predecessor executable or
scientific result is replayed or audited as the deliverable.

## Evidence and reproduction

From the repository root, with CPython 3.12:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/rational-width-certificates/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/rational-width-certificates/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/rational-width-certificates
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/rational-width-certificates --check-source-history
```

Another CPython 3.12 path may replace the installation-specific path.
The scientific command writes nothing and prints
`PASS_RATIONAL_WIDTH_CERTIFICATES` with a generated SHA256 receipt binding
every package file to the enumerated results. The registered normal and
optimized commands each have a 60-second timeout. Exact provenance is in
[SOURCES.json](SOURCES.json); it is not an executable dependency.

The standard-library checker verifies:

- Sixteen sharp cycle examples, D=1,...,4 and d=0,...,3, with actual first
  discrepancies through width sixteen.
- All 680 complete word/fixture pairs in two binary physical-column
  examples through width four. A separately written scalar path sum checks
  every entry of the two-output, three-input boundary. The zero example
  cancels two differently represented rationally normalized tables; the
  nonzero example checks the denominator-clearing factor explicitly.
- 225 exact counter values, degrees zero through eight and widths zero
  through twenty-four, including a separate binomial expansion.
- All 819 residue-matrix entries for putative reciprocal recurrences of
  orders zero through twelve. These corroborate the independent-pole
  argument; the written proof excludes every recurrence order.
- Ten controls, including six invalid-input rejections, three false
  certificate rejections and one exterior-coefficient check.

The closure producer retains actual reachable words. A separately
transcribed rank-based checker verifies every zero certificate or literal
discrepancy. Both use exact Fraction arithmetic and keep checks active
under optimized Python. Neither imports predecessor code.

## Scope and remaining obligations

The `uniform-transfer-audit` card is explicitly changed to an algebraic
interface result. It expands a sufficient certificate class relevant to
`native_all_columns` and `compiler`, without proving either selected
assumption at its actual caller. The selected source-binding baseline
passed at canonical base `2485805a6d47f36ea83ddde6327d453ac82d44dc`; it
reports selected conditional kappa .003125804. The older priority prose is
historical context, not a replacement selected record.

The theorem requires fixed tables and boundaries, characteristic zero and
no positive-width poles. It concerns exact identities, not tolerance tests.
The executable accepts rational coefficients and uses a sufficient
nonnegative-coefficient pole guard; it is not a general root solver or a
certificate parser for untrusted files. Its test fixtures preserve every
declared role, but no physical dirty-return implementation is supplied.

No actual selected caller, native/tape implementation, normalization cost,
ownership or erasure procedure, precision/storage bound, paid invoice or
complete multiplication theorem is claimed. All five selected framework
assumptions remain. No selected cold replay, Lean or Docker run is needed
or performed. Independent human and formal proof-kernel review are unclaimed.

## Open next questions

1. Does one actual provider or consumer require a rational function of its
   column multiplicity? Pin its complete residual and exact denominator
   first. This would connect the certificate to a real admission question;
   physical realization and its full paid bill remain blockers.
2. Can a small pole-free common denominator lower the source-specific
   cutoff? First reduce each p_j/q_j and compute a polynomial least common
   multiple. This can reduce certificate size; it does not minimize all
   equivalent transfer representations or prove physical savings.

No follow-on investigation is reserved.

## Verifier limits

Only verify.py is executable. It has no recursion, subprocess, network,
dynamic imports or generated code. Functions are below sixty physical
lines. Its checked interface permits at most four terms, four original
states per term, four letters, three boundary roles per side, polynomial
input degree at most sixteen and at most sixty-four lifted states. The
fixed fixtures use at most sixteen lifted states. Literal path enumeration
has width at most six by an explicit guard and width four in the replay;
counter and residue loops have the fixed bounds listed above. Receipt
reads are limited to ten files of at most one MiB each.

Power of Ten rules 3 and 9 require managed-runtime deviations. Python
Fraction, tuple, iterator and JSON operations allocate and use runtime
dispatch. The bounded fixed fixtures and explicit capacities constrain
live state and call targets; there is no steady service loop. The
prototype does not offer arbitrary external inputs. Warning-strict normal
and optimized runs, syntax inspection and function-size checks are the
available diagnostics. No external static analyzer is claimed.
