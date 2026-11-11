# Sharp carry capacity for rectangular radix convolution

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped proof with finite corroboration. For unsigned base-B
inputs with a and b digits, the exact largest carry is

```text
min(a,b)(B-1)-1,    B>=2, a,b>=1.
```

For square inputs this improves the sufficient q(B-1) bound in
[Jose Manuel / PR3787](https://github.com/CrocSwap/integer-mult-bounds/pull/3787)
and [James Reed / PR3808](https://github.com/CrocSwap/integer-mult-bounds/pull/3808)
by one unit. Their results are cited, not audited or replayed. The new
result includes the exact carry at every position, with one input pair
attaining every maximum simultaneously. No new kappa is claimed.

## Exact envelope

Let s=min(a,b), l=max(a,b), L=a+b. Start at K_0=0, use the ordinary
convolution coefficients, and append a zero coefficient at position L-1.
For the update K_(i+1)=floor((c_i+K_i)/B), the sharp bounds are

```text
U_0 = 0,
U_k = min(k,s)(B-1)-1,    1 <= k <= l,
U_k = (L-k)(B-1),         l < k <= L.
```

Every carry satisfies K_k<=U_k. Setting every input digit to B-1 gives
equality at every position. For a=2,b=4,B=10, the envelope is
`(0,8,17,17,17,9,0)`. [PROOF.md](PROOF.md) proves the universal statement
by monotonicity and an exact evaluation of that maximal-digit recurrence.
Leading zeros and the zero-cap case B=2,s=1 are included.

A conventional binary field for this carry needs exactly
ceil(log2(s(B-1))) value bits. Relative to the old square-input range,
one value bit is saved exactly when q(B-1) is a power of two. This is a
numeric capacity consequence, without a charged physical storage saving.

## Reproduce

From the repository root with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/rectangular-convolution-carry/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/rectangular-convolution-carry/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/rectangular-convolution-carry
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/rectangular-convolution-carry --check-source-history
```

Replace the interpreter path on another machine. The direct command is
read-only, works without Git or network access, and emits
`PASS_RECTANGULAR_CONVOLUTION_CARRY` with computed counts and SHA256 hashes
of all six package files. It never imports a predecessor executable.
The registered normal and optimized commands each have a 30-second bound.
Metadata and committed-byte/history checks are separate from the proof.

The checker enumerates 79,541 complete input pairs in 86 rectangular
domains, checking 583,845 carry positions and exact positionwise maxima.
It also checks 31,744 maximal-digit profiles at 1,079,296 positions,
2,016 coefficient values against literal convolution, 4,032 binary
capacity cases, fourteen rejecting controls and three scope boundaries.
The finite input domains are explicit in `DOMAINS` in verify.py. The larger
attainment grid covers every B=2,...,32 and a,b=1,...,32. These finite
checks corroborate the proof rather than establish its all-size quantifiers.

## Scope, source pins and overlap

Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
The selected record identifies PR6030 and kappa=781451/250000000.
Binding-only baseline orientation passed; no selected scientific replay
was run. [SOURCES.json](SOURCES.json) pins the task, selected record and
two predecessor documents as historical provenance. No external file is
a live mathematical input to this standalone checker.

This originally posed question changes the uniform-transfer-audit card
to an integer-recovery side result. It does not discharge the selected
analytic_recovery assumption. The
[advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291918)
states the same scope. Entry checks included live open PRs and handoffs,
recent account work, main README formula searches and merged/all-state
searches for convolution, rectangular and maximal carries. The cached
overlap report covered 316 open PRs and 5,998 Discussion records, with
complete remote pagination. Its local search covered only 95 of 8,722
notes; direct Git searches supplemented that sparse coverage. These
checks do not establish global novelty or cover unpublished work.

Unsigned digits and zero initial carry are essential hypotheses. Signed
digits, smaller leading-digit ranges, arbitrary coefficient streams,
rounded coefficient acquisition, encoded allocation/cleanup and full
caller costs are not supplied. The final zero coefficient flushes the
carry; a bound on polynomial degree alone is not an emitted digit count.
There is no physical supplier, new kappa or complete multiplication theorem.
All five framework assumptions remain. Independent human and formal
proof-kernel review are unclaimed. Lean, Docker and predecessor or selected
cold replays were not run.

## Open next questions

The structured questions and blockers are in [TASK.json](TASK.json).

1. Can one actual encoded carry field use the smaller range without extra
   conversion or cleanup work? Start with the carry-field and local-total
   allocations in one physical-fft-word call. The backend and complete bill
   have not been changed or executed here.
2. What is the sharp envelope when the leading input digits have smaller
   declared bounds? Start with the two restricted maximal leading digits.
   That changed input domain is outside the current proof and checker.

## Credit and verifier bounds

Credit Jose Manuel / jmbarrancoml for PR3787's FFT word and carry interface,
James Reed / jwr404 for PR3808's sufficient range and recovery evidence,
and their retained radix/FFT/Karatsuba, fixed-tape and Gaussian arithmetic
lineage. Classical radix convolution, carry normalization, monotonicity
and induction remain classical; no literature-priority claim is made.
The new sharp envelope, proof and checker are produced by Nick Petalas.
Predecessor packages and credit lines are unchanged.

Power of Ten inspection covers only verify.py. Functions are below sixty
lines; control flow is nonrecursive and has no subprocess, network, file
write or generated-code path. Product digits have length at most six;
the larger recurrence grid has at most 64 coefficients. All collections
and loop domains are bounded by the explicit finite grids. Each hash
input is a regular file of at most 1 MiB. Explicit exceptions keep the
checks active under -O. Warning-strict normal and optimized execution is
the available local diagnostic; no external static analyzer is configured.
Rules 3 and 9 have managed-runtime deviations: Python allocates integers
and containers and uses runtime dispatch. The fixed domains bound live
algorithmic storage and dispatch targets; runtime allocation internals
are not instrumented. An allocation-prohibited deployment needs a native
fixed-storage implementation, which this package does not claim.
