# Fraction-free solves in the complete rational parameter optimizer

This contribution was produced by Nick Petalas. Apache-2.0.

An opt-in integer elimination kernel removes **15.49% of measured complete
solve-and-check wall time** on the declared six-parameter workload. The
median falls from 0.079004 to 0.066770 seconds across seven alternating runs
per arm. Every certificate byte agrees, including the first chosen optimal
basis, its 757 examined bases, exact point, dual and objective 24.

Claim type: scoped implementation proof, finite correctness evidence and a
local performance measurement. This improves execution of Ali Romman's
[PR5792](https://github.com/CrocSwap/integer-mult-bounds/pull/5792) parameter
tool. It does not prove a new LP theorem or improve kappa. The elementary
fraction-free algorithm and LP duality are classical. The new contribution
is their bounded implementation in this complete caller and its evidence.

## Use and reproduce

From the repository root, using CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B -W error research/rational-box-fraction-free/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -O -B -W error research/rational-box-fraction-free/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/rational-box-fraction-free
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/rational-box-fraction-free --check-source-history
```

The direct marker is `PASS_RATIONAL_BOX_FRACTION_FREE`. Each direct command
prints a generated JSON receipt bound to hashes of the package files. Replay
writes only temporary files outside the checkout. Set `IMB_RUN_DIR` to an
existing scratch directory to place all temporary files there. Another
CPython 3.12 interpreter can replace the displayed local path.

Use the unchanged input and output schemas with the new opt-in runner:

```sh
python3.12 -B research/rational-box-fraction-free/run.py problem.json > certificate.json
python3.12 -B research/rational-box-fraction-free/run.py problem.json --check certificate.json
```

The runner authenticates all three declared source inputs before importing
the original engine. It replaces only that process's `solve` binding and
restores it on return. Input parsing, incumbent validation, basis order,
feasibility tests, dual tests, JSON output and certificate checking are the
original code. No default or shared source file changes.

## Why the replacement solves the same systems

The source optimizer permits one to six parameters, at most 24 total rows,
at most 50,000 active bases, and rational numerators and denominators bounded
by 10^9. Both primal and dual solves use square matrices within this domain.
The new kernel checks that domain and requires exact `Fraction` entries.

First multiply each augmented equation by the positive least common
multiple of its own denominators. This preserves its rational solution set
and produces an integer augmented matrix. Perform ordinary row pivoting,
then use the fraction-free update

```text
next[i,j] = (pivot * current[i,j] - current[i,k] * current[k,j]) / previous_pivot
previous_pivot = 1 before the first column
```

The classical Sylvester determinant identity expresses the numerator as
`previous_pivot` times an integer minor. It applies to the augmented column
as well as coefficient columns. Row interchanges permute equations and the
corresponding minors. Thus every division is exact; the implementation also
checks its remainder explicitly. Over the rationals each update is a
nonzero scaled elimination step, preserving the solution set. A missing
pivot, or zero final diagonal, means a singular coefficient matrix. The
return is `None`, including inconsistent singular systems, as in the source.
Otherwise exact rational back substitution gives the unique solution.
Inputs are never mutated.

Therefore each square solve has the same answer. The unchanged caller takes
the same branches in the same basis enumeration and returns the same full
certificate. Its unchanged final primal-dual checker still runs. This proof
is scoped to this bounded solver interface; the finite tests corroborate it.

The complete workload maximizes
`x0-2x1+3x2-4x3+5x4-6x5`, with `-1<=xi<=2` and
`xi+x(i+1 mod 6)<=1/3`. Its exact optimum is independently visible: each
positive-price coordinate is at most 4/3 because its negative-price neighbor
is at least -1. Hence the objective is at most
`(1+3+5)*4/3+(2+4+6)=24`. Alternating 4/3 and -1 attains it.
This is a parameter-tool workload, not an authenticated supplier invoice.

## Correctness evidence

The verifier checks all 5,625 augmented two-dimensional systems whose four
matrix entries lie in `{-2,-1,0,1,2}` and whose right-hand entries lie in
`{-1,0,1}`. A separate literal determinant classifies their 1,161 singular
cases. Every nonsingular answer has zero exact residual and unchanged input.
Another 360 seeded rational systems cover every dimension one through six,
with forced singular rows in part of that domain. All 5,985 answers agree
with the source kernel. No timing result uses those differential loops.

Eight kernel controls cover shape, exact types, numerator and denominator
limits, a late row pivot and the maximum accepted rational boundary. All six
inherited regression groups run with the replacement in-process kernel,
including 100 independent geometric LP oracles, a fractional optimum,
degenerate boxes, zero objectives, invalid incumbents and forged duals.
The inherited portable subprocess test still exercises the original CLI;
a separate exported, Git-free candidate CLI test compares complete output
bytes and checks its certificate. Each of the three actual declared input
files is then changed separately and must reject before engine import.
Normal and optimized checks retain explicit exceptions throughout.

## Complete-path measurement

The opt-in benchmark is:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B -W error research/rational-box-fraction-free/benchmark.py
```

It times two fresh processes per observation: generate the complete optimum,
write its certificate, then run the separate CLI certificate check. Startup,
imports, parsing, the complete optimization, source gates on the candidate,
serialization and checking are inside the timed region. Fixture creation and
result comparison are outside it. Every output must be byte-identical and
must report objective 24 and 757 examined bases. All 14 complete pairs pass;
there are zero errors. The generated stdout receipt records the fixture,
output and source hashes, checks source stability before and after the run,
and includes every raw wall and child-CPU sample. Timing is not a CI gate.

Measured on macOS 27.0.1, arm64, CPython 3.12.15, using the interpreter above.
The host has 18 logical CPUs; the entry load averages were 2.11, 2.02, 1.49.
Another Python process was active, and the machine was unreserved. The run
order is baseline, candidate, repeated seven times. The complete wall-time
samples, in seconds, are:

| Round | Baseline | Candidate |
| ---: | ---: | ---: |
| 1 | 0.079575208 | 0.066769792 |
| 2 | 0.079004042 | 0.066722000 |
| 3 | 0.078111000 | 0.068358500 |
| 4 | 0.080634459 | 0.066205500 |
| 5 | 0.078052458 | 0.066579042 |
| 6 | 0.077945250 | 0.068450875 |
| 7 | 0.080182458 | 0.069031500 |

Baseline range is 0.077945..0.080634 seconds; candidate range is
0.066205..0.069032 seconds. Median child CPU time falls from 0.075766 to
0.063610 seconds. The wall-time ranges are disjoint. This is one bounded
workload on one host; no uniform speedup across all legal LPs is claimed.

A separate diagnostic profile of the unchanged complete in-process optimizer
records 814 square solves using 0.099 of 0.123 profiled seconds. Those times
are excluded from the benchmark. Fraction arithmetic is the measured
computation bottleneck. Feasibility arithmetic and two interpreter startups
remain, so the complete improvement is smaller than a solve-only comparison.
The observed saving fits within that work; no cached optimum is used.

## Scope, sources and review limits

Scientific base is canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. The selected
conditional kappa remains 781451/250000000, with its five framework assumptions.
The current selected-binding first example passed as metadata orientation.
No selected scientific replay, Lean, Docker, supplier admission or complete
multiplication theorem is claimed. Source-to-constraint correctness, strict
physical margins, native implementation, ownership, restoration, precision,
tape costs and outer use remain separate obligations.

The original `replay-runtime` card is refined to this independently posed
implementation question. The advance
[CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294680)
preceded the new implementation. The first passing improvement is packaged;
there is no second optimization round. The fresh overlap snapshot covered
333 open PRs and 6,046 Discussion records with complete remote pagination.
Only 98 of 8,722 main note paths were materialized in its local scan. Separate
main-tree searches covered the exact tool name, rational-box model, active
bases and fraction-free parameter optimization, including general dimension
wording. Merged-title searches and the source PR body were read. PR5792 and
its released Discussion5776 supply the predecessor, not a competing active
claim. Empty matches and sparse coverage are not novelty guarantees.

The new code is nonrecursive. The kernel stores at most six augmented rows
of seven integer entries, performs at most five elimination stages and six
back-substitution stages, and uses functions below 60 physical lines. With
input bounds, cleared entries are at most 10^72 in magnitude; determinant
bounds control intermediate minors and their products. Python allocates
integers, Fractions and JSON dynamically within these finite capacities.
This is a managed-runtime deviation from allocation-free execution.
The scoped engine-binding replacement and inherited test loader have one
authenticated target and restore their mutable bindings. Each child has a
30-second timeout; registered checks have 120 seconds. Warning-strict normal
and optimized execution, in-memory compilation and whitespace checks provide
the local diagnostics. External Python linters were unavailable. The optional
benchmark uses POSIX `resource`; Windows
benchmarking is unclaimed. Independent human and formal proof-kernel review
are unclaimed.

## Open next questions

1. Can the unchanged complete feasibility checks be accelerated while preserving
   the first optimal basis and output bytes? Start with a separate profile after
   this kernel. A second correctness and complete-path measurement is required.
2. Which authenticated supplier parameter problem benefits from this complete
   solver? Derive every row from one pinned full bill and include a positive
   margin variable. An LP optimum does not establish physical legality.

## Credit

Credit Ali Romman and PR5792 for the retained bounded optimizer, exact
certificate checker, original tests and parameter guide. Credit zxv for the inherited invoice-parser boundary helpers, and classical
LP, denominator-clearing, Sylvester and Bareiss methods. All predecessor bytes and their credit remain unchanged.
The new kernel, opt-in integration, controls and measurements were produced
by Nick Petalas.
