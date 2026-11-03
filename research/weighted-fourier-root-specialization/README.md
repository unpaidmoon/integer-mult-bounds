# Faster complete weighted-Fourier replay

This implementation was produced by Nick Petalas. It reduces the complete
[PR1477](https://github.com/CrocSwap/integer-mult-bounds/pull/1477) scientific
caller's local median wall time by **12.22%**, using exact Gaussian quarter
turns instead of generic root multiplication. Claim type: scoped implementation
preservation proof and measured replay improvement. No new kappa is claimed.

The opt-in adapter changes one arithmetic method in private loaded modules.
Every non-Gaussian order uses the original method. All classification loops,
literal Fourier/convolution calculations, source checks, canonical receipt data
and eleven retained test groups run unchanged. Predecessor files are unchanged.
[PROOF.md](PROOF.md) gives the all-integer kernel identity and caller argument.

## Measurement

The final fixed harness uses ten alternating fresh-process pairs on macOS
27.0.1 arm64, CPython 3.12.15, with eighteen logical cores and concurrent
unrelated research processes. Each timed process includes source authentication,
module loading, the complete scientific caller and its full expected-receipt
comparison. The eleven tests and new controls run separately from the timer.

| Complete scientific caller | Median seconds | Range seconds |
|---|---:|---:|
| Original arithmetic | 0.693891438 | 0.686172875 to 0.702206500 |
| Quarter-turn specialization | 0.609113917 | 0.602982875 to 0.618809708 |

Every paired execution is faster, with savings between
0.075201126 and 0.094030834 seconds.
The timing ranges are separated. All twenty processes return success with the
same scientific stdout SHA256,
`498656a08b0dbb74d515b09c0513d41f70d587965d5acd7aa247250f3cf60c5c`.
These are local measurements, not a uniform speed guarantee or CI threshold.
Earlier five-pair development checks were excluded from this final ten-pair
measurement; the larger sample resolved scheduling noise without changing the
kernel. The untimed profile located 884,778 root multiplications in the caller.

| Pair | Original seconds | Specialized seconds |
|---|---:|---:|
| 1 | 0.686172875 | 0.607733583 |
| 2 | 0.694715542 | 0.613346416 |
| 3 | 0.694010834 | 0.618809708 |
| 4 | 0.694416084 | 0.608845416 |
| 5 | 0.697013709 | 0.602982875 |
| 6 | 0.693175875 | 0.606477625 |
| 7 | 0.692504167 | 0.607502792 |
| 8 | 0.702206500 | 0.614003042 |
| 9 | 0.693772042 | 0.609382417 |
| 10 | 0.693447042 | 0.614625916 |

`benchmark.py` generates the timing report and binds it to source and program
hashes. No hand-authored receipt is used. Reports and temporary outputs belong
outside the checkout.

## Evidence and reproduction

The new checks pass 7,225 Gaussian and 1,127 fallback kernel comparisons,
three actual kernel mutations, seven source-byte corruption controls and one
unknown-entry control. The complete scientific receipt preserves 357,184 reduced
candidates, 744 accepted layouts, 22,688 shared-routine candidates, nine accepted
shared routines, 10,662 literal basis pairs, five dense pairs, 1,136 mismatched
forward pairs and nine semantic controls. The eleven retained tests include
all 32,768 unreduced two-point cases. These are preserved workload counts,
not new mathematical coverage.

From the repository root, with the local CPython 3.12 interpreter:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/weighted-fourier-root-specialization
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/weighted-fourier-root-specialization/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/weighted-fourier-root-specialization/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/weighted-fourier-root-specialization --check-source-history
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/weighted-fourier-root-specialization/benchmark.py
```

Substitute another CPython 3.12 path on another host. The standard library is
sufficient. Expected markers are `PASS_WEIGHTED_FOURIER_LAYOUT`, eleven passing
tests, `PASS_WEIGHTED_FOURIER_ROOT_SPECIALIZATION`,
`PASS_REGISTERED_RESEARCH_PACKAGE` and `PASS_RESEARCH_COMMIT_BYTES`.
The standalone check prints a fresh receipt bound to the package and input
hashes. Registered normal and optimized commands keep all guards active.
`replay.py --baseline` and `replay.py --with-tests` expose the two practical
caller modes. Timing is opt-in and is not a registered acceptance gate.

## Scope, overlap and credit

Base is canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8. The current selected record remains the PR6030 conditional
`781451/250000000`; its five framework assumptions retain their status.
The selected binding orientation passed without a scientific supplier replay.

The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19299766)
reserves this implementation question. Live overlap covered 364 open PR bodies
and 6,107 Discussion records with complete remote pagination, plus targeted
merged searches and main-tree README searches. Local notes were sparse;
unpublished work remains a limit. No same-kernel optimization appeared in
that coverage. PR5946's restricted-input theorem and PR4874's higher-arity
classification are different mathematical results and are not extended here.

Credit Hanson Sun / bbMisk for PR1477's complete caller, independent literal
oracle, test suite, receipts and workload; Ross Richardson for PR940's
unweighted criterion; and the retained Fourier/manuscript lineage. Gaussian
quarter-turn arithmetic and substitution of equal functions are classical.
This contribution is the concrete implementation, preservation argument,
source-bound controls and complete-caller measurement. No predecessor theorem
is independently audited or re-proved as this deliverable. Apache-2.0.

Physical schedules, native implementation, rounded arithmetic, restoration,
compiler closure, stock, precision/tape and analytic recovery remain outside
this result. No selected cold replay, Lean or Docker run was performed.
Independent human and formal proof-kernel review are unclaimed.

## Open next questions

Would this specialization help an actual selected native caller? First profile
one named caller, identify material Gaussian root multiplication, then supply
its own conformance argument and complete-caller measurement. This package
supplies no selected-caller gain. The structured question is in TASK.json.

## Verifier constraints

New functions are at most 37 lines. There is no recursion, result cache,
parallel replay or generated-code execution. All arithmetic domains and process
counts are fixed. Each child process has a 120-second timeout; inputs are capped
at sixteen MiB each, seven live pins and sixteen manifest rows. The retained
caller and tests have their fixed original finite domains and are preserved
rather than rewritten.

Power of Ten rule 3 deviation: CPython allocates integer tuples and other
managed objects. The executable workload accepts no arbitrary mathematical
input, and its fixed domains bound live collections. Rule 9 deviation: a private
method replacement and the retained unittest loader use runtime dispatch;
the targets are the original and specialized functions, eleven fixed tests,
and three deliberately faulty local kernels. Source pins and semantic controls
exercise those boundaries. Warning-strict normal/optimized replay and AST
compilation supply local diagnostics; no separate Python analyzer was installed.
