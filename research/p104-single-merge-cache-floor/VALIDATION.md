# Validation and implementation bounds

The verifier passed on CPython 3.12.15, macOS 27.0.1 arm64, with output:

    PASS_SINGLE_MERGE_CACHE_FLOOR
    dimension_pairs=91 dimension_recipes=20839 reader497_recipes=50
    payload_cases=85 controls=13

The first direct warning-strict isolated replay completed in 0.27 seconds.
The normal and optimized registered commands each completed directly in 0.28
seconds. Their generated receipts were equal, including all package hashes and
the 50-recipe certificate. The registered runner passed both commands in 0.82
seconds total. These are check durations, not a performance improvement claim.

The exact commands are in README.md and VERIFY.json. Byte/source-history and
export checks follow the commit so they can authenticate the published tree;
their results are recorded in the PR body. Hosted CI remains pending at
publication. None of these checks establishes independent mathematical acceptance.

## Proof and verification boundaries

The written argument establishes the all-field, all-dimension tariff theorem.
The executable checks finite recipe coverage, rank extraction from explicit
binary flags, concave capped-sum inequalities and the relaxed scalar payload.
It does not check source geometry, native operators, actual caller placement,
physical erasure, compiler closure or the full multiplication theorem.

The package imports only the Python standard library. It runs no predecessor
verifier, source program, selected replay, Lean build or Docker task. No hosted
CI result is claimed before publication. There is no independent human or
proof-kernel acceptance.

## Code bounds

All traversals are finite. The outer dimension is at most 14, each recipe has
at most eight MOVE ranks, and the actual-instance certificate has 50 rows.
There are four public basis vectors, 81 literal inputs and five payload
mutations. The package inventory is exactly seven regular files, each limited
to 1 MiB before reading. Receipt output is optional and must lie outside the
checkout. Every failure exits by an exception; there are no retries, child
processes, network calls, dynamic code evaluation or recursive calls.

Power of Ten rule 3 has a managed-runtime deviation in verify.py. Python and
its standard library allocate during iteration, arithmetic and serialization.
The fixed dimension, rank, sample and file limits bound the application-owned
live collections; this is not a bound on the interpreter or OS memory. The
normal and optimized verifier exercise the maximum enumerated dimension.
A fixed-memory implementation would require a separate runtime and is outside
this mathematical package. No configuration or code elsewhere is changed.

Build the Lever led to the self-contained exact verifier and generated
hash-bound receipt. Prove It Works led to independent flag-rank extraction,
explicit input-loss controls and direct normal/optimized execution. The
engineering-mode playbook is Investigation, with artifact publication authorized
by the contribution assignment.
